#!/usr/bin/env python3
"""NAI 4.5 프롬프트 검사기.

검사 항목: 금지 태그(퀄리티·작가·그림체·메타·IP), 가중치 범위(-3~3),
`::` 닫힘, 영어 외 문자, 대략적인 길이.

사용법:
  python3 check_prompt.py prompt.txt
  echo "1girl, solo, ..." | python3 check_prompt.py
  python3 check_prompt.py --bg-allowed prompt.txt   # 배경 요청이 있을 때
종료 코드: 0 = 통과(경고만 있을 수 있음), 1 = 오류 있음.
"""
import re
import sys

WEIGHT_MIN, WEIGHT_MAX = -3.0, 3.0

BANNED_EXACT = {
    # 퀄리티·미학
    "masterpiece", "best quality", "high quality", "amazing quality", "great quality",
    "good quality", "normal quality", "low quality", "worst quality", "bad quality",
    "very aesthetic", "aesthetic", "top aesthetic", "displeasing", "very displeasing",
    "absurdres", "highres", "lowres", "incredibly absurdres", "ultra detailed",
    "extremely detailed", "8k", "4k", "hd", "newest", "recent",
    # 메타
    "official art", "game cg", "cover", "magazine cover", "commentary", "translated",
    "signature", "watermark", "artist name", "dated", "logo", "web address",
    "traditional media", "faux traditional media",
    # 그림체·매체·채색
    "sketch", "lineart", "flat color", "anime coloring", "cel shading", "realistic",
    "photorealistic", "semi-realistic", "painterly", "impressionism", "art nouveau",
    "ukiyo-e", "oekaki", "pixel art", "3d", "chibi", "super deformed",
    "monochrome", "greyscale", "sepia", "partially colored", "limited palette",
    "spot color", "high contrast", "muted color", "retro artstyle",
    "chromatic aberration", "film grain", "jpeg artifacts", "scan artifacts",
    # IP·오마쥬
    "cosplay", "parody", "style parody", "crossover", "homage",
    # 미성년자
    "loli", "shota", "child", "kid", "toddler",
}

BANNED_PATTERNS = [
    (r"^artist:", "작가 태그"),
    (r"^(by|art by|drawn by)\s", "작가 지정"),
    (r"in the style of", "그림체 지정"),
    (r"\b(anime|manga|cartoon|watercolor|realistic|painterly)\s+style\b", "그림체 지정"),
    (r"\((medium|style)\)$", "매체·시대 그림체 태그"),
    (r"^year \d{4}$", "연도 태그"),
    (r"^score_\d", "점수 태그"),
    (r"^rating:", "등급 태그"),
    (r"\(cosplay\)$", "코스프레 태그"),
    (r"inspired by", "오마쥬 표현"),
]

BACKGROUND_HINTS = [
    "outdoors", "indoors", "scenery", "cityscape", "street", "forest", "beach",
    "classroom", "bedroom", "sky", "night sky", "sunset", "bokeh", "blurry background",
]

WEIGHT_RE = re.compile(r"(-?\d+(?:\.\d+)?)::")


def split_tags(text):
    body = text.split("Text:")[0]  # Text: 뒤는 그림 속 글자이므로 검사하지 않는다
    body = re.sub(r"-?\d+(?:\.\d+)?::|::", ",", body)
    body = re.sub(r"[{}\[\]]", "", body)
    parts = re.split(r"[,\n|]", body)
    return [p.strip().lower() for p in parts if p.strip()]


def check(text, bg_allowed=False):
    errors, warnings = [], []

    # 영어 외 문자 (Text: 뒤 제외)
    body = text.split("Text:")[0]
    non_ascii = sorted({c for c in body if ord(c) > 127})
    if non_ascii:
        errors.append(f"영어 외 문자: {' '.join(non_ascii)} (T5는 거의 인식 못 함)")

    # 가중치 범위
    for m in WEIGHT_RE.finditer(body):
        val = float(m.group(1))
        if not WEIGHT_MIN <= val <= WEIGHT_MAX:
            errors.append(f"가중치 {val}가 -3~3 범위를 벗어남")

    # :: 닫힘: 여는 것(숫자::)과 닫는 것(단독 ::)의 수를 비교
    opens = len(WEIGHT_RE.findall(body))
    total = body.count("::")
    closes = total - opens
    if closes < opens:
        errors.append(f"닫히지 않은 가중치 구간 {opens - closes}개 (뒤의 태그 전부에 걸림)")

    # 괄호 짝
    for o, c in ("{}", "[]"):
        if body.count(o) != body.count(c):
            errors.append(f"괄호 짝이 맞지 않음: {o}{c}")

    # 금지 태그
    for tag in split_tags(text):
        if tag in BANNED_EXACT:
            errors.append(f"금지 태그: '{tag}'")
            continue
        for pat, why in BANNED_PATTERNS:
            if re.search(pat, tag):
                errors.append(f"금지 태그({why}): '{tag}'")
                break

    # 배경
    tags = split_tags(text)
    if not bg_allowed:
        found = [t for t in tags if t in BACKGROUND_HINTS]
        if found:
            warnings.append(f"배경 태그가 있음: {', '.join(found)} (요청이 없었다면 빼기)")
        if not any("simple background" in t or "white background" in t for t in tags):
            warnings.append("배경 기본값 'simple background, white background'가 없음")
    if re.search(r"-\d+(?:\.\d+)?::\s*simple background", body):
        warnings.append("simple background에 음수 가중치: 배경이 생기는 방향")

    # 길이 (T5 512 토큰 대략치)
    words = len(re.findall(r"[A-Za-z]+", body))
    if words > 350:
        warnings.append(f"영어 단어 {words}개: 512 토큰 상한에 가까울 수 있음")

    # 추상어만 있는 문장
    abstract = {"elegant", "mysterious", "beautiful", "cute", "cool", "stylish",
                "gorgeous", "fancy", "unique", "dramatic", "intricate", "detailed"}
    for sent in re.split(r"(?<=[.!?])\s+|\n|,", body):
        words_in = re.findall(r"[a-z]+", sent.lower())
        if len(words_in) >= 5 and sent.strip().endswith("."):
            if any(w in abstract for w in words_in) and not re.search(
                r"\b(black|white|grey|gray|red|blue|green|gold|silver|brown|pink|purple|"
                r"navy|ivory|leather|wool|silk|satin|lace|metal|left|right|sleeve|collar|"
                r"hem|waist|shoulder|knee|thigh|ankle|button|strap|pleat)\b", sent.lower()):
                warnings.append(f"추상적인 문장: \"{sent.strip()[:60]}...\"")

    return errors, warnings


def main():
    args = sys.argv[1:]
    bg_allowed = "--bg-allowed" in args
    files = [a for a in args if not a.startswith("--")]
    text = open(files[0], encoding="utf-8").read() if files else sys.stdin.read()
    errors, warnings = check(text, bg_allowed)
    for e in errors:
        print(f"[오류] {e}")
    for w in warnings:
        print(f"[경고] {w}")
    if not errors and not warnings:
        print("[통과] 문제 없음")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
