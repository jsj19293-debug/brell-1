#!/usr/bin/env python3
"""패치한 홈페이지를 4개 언어(ko/en/ja/zh)로 띄워 확인한다.

사용: python3 homepage_check.py 결과.html 코드1 [코드2 ...]
  예) python3 homepage_check.py out.html M19 M20

확인하는 것
  - 언어별로 페이지 오류(JS 예외)가 없는지
  - 가입 회원 수(#factMembers)
  - 지정한 회원 이름이 그 언어 이름으로 보이는지(I18N에서 찾아 대조)
  - 지정한 회원의 프로필 창이 열리는지, 창 안에 한글이 남았는지(ko 제외)
Playwright(Chromium)가 필요하다. 클라우드 작업공간에는 깔려 있다.
"""
import asyncio, json, re, sys, pathlib
from playwright.async_api import async_playwright

LANGS = ['ko', 'en', 'ja', 'zh']
IDX = {'en': 0, 'ja': 1, 'zh': 2}


def load(path):
    L = open(path, encoding='utf-8').read().split('\n')
    I18N = json.loads(next(l for l in L if l.startswith('const I18N='))[len('const I18N='):].rstrip(';'))
    pages = json.loads(next(l for l in L if l.startswith('const pages='))[len('const pages='):].rstrip(';'))
    people = json.loads(re.search(r'const people=(\[.*?\]);\n', pages['meeting'], re.S).group(1))
    return I18N, {p['code']: p for p in people}


async def main(path, codes):
    I18N, people = load(path)
    url = pathlib.Path(path).resolve().as_uri()
    bad = 0
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        for lang in LANGS:
            pg = await b.new_page(viewport={'width': 1300, 'height': 900})
            errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)))
            await pg.goto(f'{url}?lang={lang}#meeting')
            await pg.wait_for_timeout(2500)
            fr = next((f for f in pg.frames if f != pg.main_frame), pg.main_frame)
            await fr.evaluate("()=>{const g=document.querySelector('#gateEnter'); if(g) g.click();}")
            await pg.wait_for_timeout(500)
            fm = await fr.evaluate("()=>{const e=document.querySelector('#factMembers');return e?e.innerText:null}")
            line = [f'[{lang}] 오류 {len(errs)}개 · 회원 수 {fm}']
            for c in codes:
                p = people.get(c)
                if not p:
                    line.append(f'{c}: people에 없음'); bad += 1; continue
                name = p['name'] if lang == 'ko' else (I18N.get(p['name']) or [p['name']] * 3)[IDX[lang]]
                opened = await fr.evaluate("""(n)=>{const el=[...document.querySelectorAll('button,a,article,li,div')].reverse().find(e=>e.innerText&&e.innerText.includes(n)&&e.offsetParent);if(!el)return null;el.scrollIntoView();el.click();return true}""", name)
                await pg.wait_for_timeout(700)
                dlg = await fr.evaluate("()=>{const d=document.querySelector('#profileDialog');return d&&d.open?d.innerText:''}")
                left = len(re.findall(r'[가-힣]', dlg)) if lang != 'ko' else 0
                ok = bool(opened) and name in dlg and left == 0
                bad += 0 if ok else 1
                line.append(f'{c} {name}: {"OK" if ok else "확인 필요"}' + (f' (창 안 한글 {left}자)' if left else '') + ('' if opened else ' (카드 못 찾음)'))
                await fr.evaluate("()=>{const d=document.querySelector('#profileDialog');if(d&&d.open)d.close()}")
            if errs:
                bad += 1
                line.append('오류: ' + errs[0][:120])
            print(' | '.join(line))
            await pg.close()
        await b.close()
    print('결과:', '전부 통과' if bad == 0 else f'확인 필요 {bad}건')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    asyncio.run(main(sys.argv[1], sys.argv[2:]))
