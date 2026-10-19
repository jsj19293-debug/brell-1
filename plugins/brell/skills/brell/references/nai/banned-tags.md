# 거절 태그 목록

이 스킬은 아래 태그를 프롬프트에 넣지 않는다. 사용자가 요청하면 거절하고 대안을 제안한다. 기준은 단부루 태그 분류다(1=작가, 3=작품, 4=캐릭터, 5=메타). 일반 태그 중에서는 그림체를 바꾸는 태그(tag_group:image_composition의 styles·techniques 항목, tag_group:artistic_license, tag_group:visual_aesthetic)가 해당한다.

## 1. 퀄리티·미학 태그
masterpiece, best quality, high quality, amazing quality, great quality, good quality, normal quality, low quality, worst quality, bad quality, very aesthetic, aesthetic, top aesthetic, displeasing, very displeasing, absurdres, highres, lowres, incredibly absurdres, score_9 등 score_ 계열, rating:general 등 rating: 계열, ultra detailed, extremely detailed, 8k, 4k, hd, perfect, beautiful detailed

## 2. 작가 태그
- 작가 이름 전부
- `artist:` 접두사(NAI 작가 문법)
- `by ~`, `in the style of ~`, `drawn by ~`, `art by ~`

## 3. 연도·시대 그림체 태그
year 2024 등 year 계열, newest, recent, mid, early, old, 1980s (style), 1990s (style), 2000s (style), retro artstyle

## 4. 메타 태그
official art, game cg, cover, magazine cover, commentary, translated, signature, watermark, artist name, dated, logo, web address, traditional media, faux traditional media

## 5. 그림체·매체·채색 태그
- 그림체: sketch, lineart, flat color, anime coloring, cel shading, realistic, photorealistic, semi-realistic, painterly, impressionism, art nouveau, ukiyo-e, oekaki, pixel art, 3d, chibi, super deformed
- 매체: watercolor (medium), oil painting (medium), acrylic paint (medium), colored pencil (medium), marker (medium), ink (medium), pastel (medium)
- 색 처리: monochrome, greyscale, sepia, partially colored, limited palette, spot color, high contrast, muted color
- 카메라 효과(그림체 계열): chromatic aberration, film grain, jpeg artifacts, scan artifacts

**주의**: 옷 색을 말하는 태그는 허용한다. `monochrome`(그림 전체 흑백)은 금지지만 `black and white dress`, `white dress`는 허용한다. `limited palette`도 금지지만, 색 수를 줄이고 싶으면 옷 색을 2~3개로 직접 지정한다.

## 6. 기존 작품·캐릭터 관련(오마쥬 금지)
- 작품명 태그(단부루 분류 3): 게임·애니·만화·버튜버 그룹명 등
- 캐릭터명 태그(분류 4): 보통 `이름 (작품)` 형태다
- cosplay, `~ (cosplay)`, parody, style parody, crossover, homage, inspired by
- 특정 작품에 묶인 의상 태그: `~ (작품) uniform`, plugsuit 같은 고유 의상명, `캐릭터 (의상명)` 형태
- **판별 규칙**: 괄호 안에 작품명이 들어가거나 작품·캐릭터를 가리키는 태그는 전부 거절한다. 일반 의상 태그(serafuku, maid, kimono, armor)는 허용한다.

## 거절할 때의 대안
| 사용자 요청 | 대안 |
|---|---|
| "고퀄로", "masterpiece 넣어줘" | 퀄리티 태그 대신 구체적인 디테일 묘사를 늘린다(소재 질감, 봉제선, 장식 구조) |
| "OO 작가 그림체로" | 그림체 대신 캐릭터·의상 디자인 요소를 구체화한다. 그림체는 사용자가 NAI에서 직접 정하는 영역이라고 안내한다 |
| "수채화 느낌", "실사풍" | 거절한다. 원하는 분위기를 조명·소재 묘사로 바꾸자고 제안한다(예: soft light from the left, sheer fabric) |
| "OO 캐릭터 코스프레" | 거절한다. 분위기·색 계열만 가져와 오리지널 디자인으로 바꾼 시안을 낸다 |
