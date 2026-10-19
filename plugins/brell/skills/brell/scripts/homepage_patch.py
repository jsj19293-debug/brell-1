#!/usr/bin/env python3
"""비밀만남 홈페이지(index.html 한 파일) 업데이트 패치.

사용: python3 homepage_patch.py 원본.html spec.json 결과.html

홈페이지 구조 (2026-10 기준):
  - const SITE_CONFIG={...};   profiles(프사·비밀사진 3장), regions(지역·장소·소속 회원), music, map ...
  - const pages={"phone": "...", "meeting": "..."};   iframe에 넣는 HTML 두 장. meeting 안에 const people=[...];
  - const I18N={"한국어 문장": [영어, 일본어, 중국어], ...};   한국어 덩어리를 통째로 키로 찾아 바꾼다.

spec.json (필요한 키만 쓴다)
{
  "profiles_add":  [ {SITE_CONFIG.profiles 항목}, ... ],          # 끝에 추가
  "profiles_update": { "M05": {"바꿀 키": 값}, ... },
  "people_add":    [ {pages.meeting people 항목}, ... ],          # 끝에 추가
  "people_update": { "M05": {"바꿀 키": 값}, ... },
  "buildings_add": [ {"region": "station", "after": "hospital", "building": {...}} ],
  "building_members": [ {"building": "officetel", "add": ["M19"], "remove": []} ],
  "text_replace":  [ {"where": "meeting|phone|outer", "old": "18명", "new": "20명", "count": 1, "check": true} ],
                   # check:false = 주석처럼 화면에 안 나오는 글자(번역 누락 검사에서 뺌)
  "i18n_add":      { "한국어": ["English", "日本語", "中文"], ... }
}

규칙
  - 원본 서식(들여쓰기·한 줄 secrets·\\u003c 이스케이프)을 그대로 지킨다. 원본을 다시 써 봐서 글자 하나라도 다르면 멈춘다.
  - 끝나면 새로 생긴 한국어 덩어리 중 I18N에 없는 것을 전부 출력한다(번역 누락 = 0개여야 완료).
"""
import json, re, sys

HRE = re.compile(r"[^'\"`<>\n{}]*[가-힣][^'\"`<>\n{}]*")  # 홈페이지 trSource와 같은 규칙


def dump_cfg(o, ind=0, key=None, inline=False):
    sp = '  ' * ind
    if inline:
        return json.dumps(o, ensure_ascii=False, separators=(', ', ': '))
    if isinstance(o, dict):
        if not o:
            return '{}'
        return '{\n' + ',\n'.join(f'{sp}  {json.dumps(k, ensure_ascii=False)}: {dump_cfg(v, ind + 1, k)}' for k, v in o.items()) + '\n' + sp + '}'
    if isinstance(o, list):
        if not o:
            return '[]'
        il = key == 'secrets'
        return '[\n' + ',\n'.join(f'{sp}  {dump_cfg(v, ind + 1, None, il)}' for v in o) + '\n' + sp + ']'
    return json.dumps(o, ensure_ascii=False)


def dump_pages(o):
    return json.dumps(o, ensure_ascii=False, separators=(', ', ': ')).replace('<', '\\u003c')


def dump_compact(o):
    return json.dumps(o, ensure_ascii=False, separators=(',', ':'))


def die(msg):
    sys.exit('중단: ' + msg)


def replace_once(text, old, new, count, label):
    n = text.count(old)
    if n != count:
        die(f'[{label}] "{old[:40]}" 가 {n}번 나옴 (기대 {count}번)')
    return text.replace(old, new)


def main(src_path, spec_path, out_path):
    src = open(src_path, encoding='utf-8').read()
    spec = json.load(open(spec_path, encoding='utf-8'))
    L = src.split('\n')

    # ── SITE_CONFIG ──
    cs = next((i for i, l in enumerate(L) if l.startswith('const SITE_CONFIG=')), None)
    if cs is None:
        die('SITE_CONFIG 줄을 못 찾음')
    ce = next(i for i in range(cs, len(L)) if L[i] == '};')
    cfg_txt = '\n'.join(L[cs:ce + 1])[len('const SITE_CONFIG='):-1]
    cfg = json.loads(cfg_txt)
    if dump_cfg(cfg) != cfg_txt:
        die('SITE_CONFIG 서식이 예상과 다름 (스크립트 갱신 필요)')

    codes = [p['code'] for p in cfg['profiles']]
    for p in spec.get('profiles_add', []):
        if p['code'] in codes:
            die(f'profiles에 {p["code"]} 이미 있음')
        cfg['profiles'].append(p)
    for code, patch in spec.get('profiles_update', {}).items():
        t = next((p for p in cfg['profiles'] if p['code'] == code), None)
        if not t:
            die(f'profiles에 {code} 없음')
        t.update(patch)

    all_b = {b['id']: (r, b) for r in cfg.get('regions', []) for b in r['buildings']}
    for item in spec.get('buildings_add', []):
        r = next((r for r in cfg['regions'] if r['id'] == item['region']), None)
        if not r:
            die(f'region {item["region"]} 없음')
        if item['building']['id'] in all_b:
            die(f'building {item["building"]["id"]} 이미 있음')
        ids = [b['id'] for b in r['buildings']]
        pos = ids.index(item['after']) + 1 if item.get('after') in ids else len(ids)
        r['buildings'].insert(pos, item['building'])
        all_b[item['building']['id']] = (r, item['building'])
    for item in spec.get('building_members', []):
        if item['building'] not in all_b:
            die(f'building {item["building"]} 없음')
        b = all_b[item['building']][1]
        b['members'] = [m for m in b['members'] if m not in item.get('remove', [])] + [m for m in item.get('add', []) if m not in b['members']]

    new_cfg_txt = dump_cfg(cfg)
    L[cs:ce + 1] = ('const SITE_CONFIG=' + new_cfg_txt + ';').split('\n')

    # ── pages ──
    ip = next(i for i, l in enumerate(L) if l.startswith('const pages='))
    pbody = L[ip][len('const pages='):].rstrip(';')
    pages = json.loads(pbody)
    if dump_pages(pages) != pbody:
        die('pages 서식이 예상과 다름')
    mt = pages['meeting']
    m = re.search(r'const people=(\[.*?\]);\n', mt, re.S)
    if not m:
        die('meeting 안 people 배열 없음')
    people = json.loads(m.group(1))
    if dump_compact(people) != m.group(1):
        die('people 서식이 예상과 다름')
    pcodes = [p['code'] for p in people]
    for p in spec.get('people_add', []):
        if p['code'] in pcodes:
            die(f'people에 {p["code"]} 이미 있음')
        people.append(p)
    for code, patch in spec.get('people_update', {}).items():
        t = next((p for p in people if p['code'] == code), None)
        if not t:
            die(f'people에 {code} 없음')
        t.update(patch)
    pages['meeting'] = mt[:m.start(1)] + dump_compact(people) + mt[m.end(1):]

    # ── 글자 바꾸기 ──
    for r in spec.get('text_replace', []):
        where, cnt = r.get('where', 'meeting'), r.get('count', 1)
        if where in ('meeting', 'phone'):
            pages[where] = replace_once(pages[where], r['old'], r['new'], cnt, where)
        elif where == 'outer':
            joined = '\n'.join(L)
            L = replace_once(joined, r['old'], r['new'], cnt, 'outer').split('\n')
            ip = next(i for i, l in enumerate(L) if l.startswith('const pages='))
        else:
            die(f'where={where} 는 지원 안 함 (config는 profiles_update 등으로)')
    L[ip] = 'const pages=' + dump_pages(pages) + ';'

    # ── I18N ──
    ii = next(i for i, l in enumerate(L) if l.startswith('const I18N='))
    ibody = L[ii][len('const I18N='):].rstrip(';')
    I18N = json.loads(ibody)
    if dump_compact(I18N) != ibody:
        die('I18N 서식이 예상과 다름')
    for k, v in spec.get('i18n_add', {}).items():
        if not (isinstance(v, list) and len(v) == 3):
            die(f'i18n "{k}" 는 [영어, 일본어, 중국어] 3개여야 함')
        I18N[k.strip()] = v
    L[ii] = 'const I18N=' + dump_compact(I18N) + ';'

    out = '\n'.join(L)
    open(out_path, 'w', encoding='utf-8').write(out)

    # ── 번역 누락 검사: 이번에 추가·수정한 값 전부 ──
    touched = []
    touched += spec.get('profiles_add', []) + list(spec.get('profiles_update', {}).values())
    touched += spec.get('people_add', []) + list(spec.get('people_update', {}).values())
    touched += [b['building'] for b in spec.get('buildings_add', [])]
    touched += [r['new'] for r in spec.get('text_replace', []) if r.get('where') in ('meeting', 'phone') and r.get('check', True)]
    segs = set()
    for t in touched:
        segs |= {s.strip() for s in HRE.findall(json.dumps(t, ensure_ascii=False) if not isinstance(t, str) else t)}
    missing = sorted(s for s in segs if s and not s.startswith(('//', 'http')) and s not in I18N)
    print(f'완료: {out_path}  profiles {len(cfg["profiles"])}명 · people {len(people)}명 · I18N {len(I18N)}개')
    if missing:
        print(f'번역 누락 {len(missing)}개 (i18n_add에 넣고 다시 실행):')
        for s in missing:
            print('  -', s)
        sys.exit(2)
    print('번역 누락 0개')


if __name__ == '__main__':
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:])
