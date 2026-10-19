# NAI V4.5 Full 공식 문법 요약

조사일: 2026-10-19. 이 환경에서는 docs.novelai.net을 직접 열지 못해 공식 페이지의 검색 결과 발췌로 확인했다. 정확한 문자열(프리셋 내용 등)은 실제 페이지에서 다시 확인한다.

> 참고: 현재 NovelAI 최신 모델은 V5다. 공식 문서 일부는 V5 기준으로 바뀌었으므로 이 스킬은 **V4.5 규칙**을 따른다.

## 1. 강조·약화
출처: https://docs.novelai.net/en/image/strengthening-weakening/

- `{태그}`는 1.05배, `[태그]`는 1/1.05배다. 겹치면 곱해진다(`{{태그}}` = 1.1025배). 괄호의 짝을 맞춘다.
- **숫자 가중치(V4 이상)**: `1.5::rain, night ::`처럼 쓴다. 단독 `::`가 구간을 닫는다.
  - 0~1 사이 값은 약화다.
  - `::`는 열려 있는 괄호도 닫는다.
  - 공식 예: `1girl, 1.5::rain, night ::, 0.5::coat ::, black shoes`
- **음수 가중치(V4.5 이상)**: `-1::hat ::`으로 모자를 지우는 경우가 많고, 안 되면 `-3`까지 쓴다. `-1::monochrome ::`처럼 반대 개념으로 밀 수도 있다.
  - 특정 요소 제거에는 음수 가중치가, 긴 제외 목록에는 Undesired Content가 낫다.
- **범위**: V4.5 발표문은 숫자 가중치가 10 이상에서도 비교적 안정적이라고 했다(https://novelai.net/updates?id=v4-numeric-emphasis). 이 스킬의 -3~3은 그 안의 보수적인 범위다.
  - 커뮤니티에서는 1.1~1.5를 많이 쓰고, 높은 값은 그림이 깨진다는 경고도 있다(커뮤니티 팁).
- 태그가 숫자로 끝나면 `::` 앞에 공백을 둔다(커뮤니티 팁, arca.live/b/aiart/144911662).
- A1111식 `(tag:1.2)` 문법은 NAI에서 쓰지 않는다.

## 2. 자연어
출처: https://docs.novelai.net/en/image/models/

- V4부터 자연어를 이해한다. 태그와 문장을 섞어 쓸 수 있다.
- **토큰 상한**: Base Prompt와 모든 Character Prompt를 합쳐 약 512 T5 토큰이다.
- T5 토크나이저는 대부분의 유니코드(일본어, 이모지 등)를 지원하지 않으므로 **영어로만** 쓴다.
- 문장과 태그의 배치 순서에 대한 공식 권장은 찾지 못했다. 커뮤니티 의견은 "태그로 정확한 개념을, 자연어로 요소 간 관계(손 위치, 빛 방향, 겹침)를"이다(arca.live/b/aiart/181003788, 의견).

## 3. 다중 캐릭터
출처: https://docs.novelai.net/en/image/multiplecharacters/

- Base Prompt에는 장면 전체와 **인원 태그**(`2girls`, `1boy, 1girl`)를 넣는다.
- 캐릭터마다 Character Prompt 칸이 있고 `girl`/`boy`/`other`로 시작한다.
- 위치는 기본 AI's Choice이고, Custom으로 바꾸면 **5×5 그리드**에서 지정한다. 위치는 자연어로도 함께 적는다.
- V4는 최대 6명을 지원한다. V4.5도 같다고 추정되지만 확인하지 못했다.
- 상호작용 태그는 `source#동작`(하는 쪽), `target#동작`(받는 쪽), `mutual#동작`(서로)이다. 각 캐릭터 칸에 넣는다.

## 4. 텍스트
출처: https://docs.novelai.net/en/image/textrendering/

- `text, english text` 태그를 넣고, Base Prompt **맨 끝**에 `Text: 문구`를 쓴다. 그 뒤의 내용은 전부 그림에 글자로 나올 수 있다.
- 영어만 되고 약 118~120자 이내다. 여러 문구는 빈 줄로 나눈다.

## 5. Add Quality Tags 토글
출처: https://docs.novelai.net/en/image/qualitytags/

- 기본으로 켜져 있다. 위치는 프롬프트 칸 하단이다.
- V4.5 Full에서 켜면 프롬프트 끝에 `, location, very aesthetic, masterpiece, no text`가 붙는다.
- **이 스킬은 퀄리티 태그를 쓰지 않으므로 토글을 끄도록 안내한다.** 끄면 `location`, `no text`도 붙지 않는다는 점을 함께 알린다.

## 6. Undesired Content 프리셋
출처: https://docs.novelai.net/en/image/undesiredcontent/

- V4.5 Full 프리셋은 Heavy, Light, Human Focus, Furry Focus, None이다.
- Heavy·Light에는 `worst quality`, `bad quality`, `sketch`, `flat colors` 같은 퀄리티·그림체 항목이 들어 있다(발췌 확인, 전체 문자열은 확인 못 함).
- 이 스킬은 **None을 권장**하고, 구체적인 제외 요소만 직접 쓴다.

## 7. 태그 순서
출처: https://docs.novelai.net/en/image/tags/

- 공식 권장 순서: 인원(`1girl`) → 캐릭터 → 작품 → 나머지는 자유. 이 스킬은 캐릭터·작품 태그를 쓰지 않으므로 인원 → 외형 → 복장 → 포즈 → 구도 → 배경 순으로 쓴다.
- "앞쪽 태그가 더 강하다"는 공식 문서상 V3 이하 설명이다. 4.5에서도 순서에 민감하다는 커뮤니티 의견이 있다(arca.live/b/aiart/138308689, 의견). 중요한 것을 앞에 둔다.

## 8. 배경
- 공식 문서에서 배경 관련 권장은 찾지 못했다.
- `simple background, white background`는 단부루 표준 태그다.
- 공식 문서 예 `-1::simple background ::, location`은 하얀 배경에서 캐릭터를 끌어내는 용도다. **배경 없음을 원할 때는 쓰지 않는다.**

## 9. Full과 Curated
- Full은 더 넓은 데이터로 학습해 Curated가 못 그리는 개념도 그린다. Curated는 정제된 데이터로 학습했다.
- 기본 퀄리티 태그가 서로 다르다. 이 스킬은 **Full** 기준이다.
