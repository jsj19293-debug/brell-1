# brell-1 플러그인 저장소

## nai-prompt

NovelAI Diffusion V4.5 Full 이미지 프롬프트를 만드는 Claude Code 스킬입니다.

- 오리지널 캐릭터 디자인만 합니다. 기존 캐릭터 오마쥬·코스프레는 거절합니다.
- 자연어는 영어로, 색·소재·길이·위치·구조를 구체적으로 씁니다.
- 상황에 맞는 복장을 여러 벌 설계하고, 가중치는 -3 ~ 3 범위로 씁니다.
- 작가 태그, 퀄리티 태그, 그림체 태그는 거절합니다.
- 배경은 기본으로 넣지 않고(`simple background, white background`), 요청하면 추가합니다.
- 참조처: NAI 공식 문서, 단부루 위키, 아카라이브 AI그림 채널, 핀터레스트. 아카라이브와 핀터레스트는 브라우저(Claude in Chrome 등)가 연결되어 있으면 로그인된 상태로 봅니다.

### 설치

```
/plugin marketplace add jsj19293-debug/brell-1
/plugin install nai-prompt@brell-1
```

### 사용 예

- "엘린 캐릭터 NAI 프롬프트 짜줘. 비 오는 항구에서 일하는 장면, 복장 3벌"
- "이 캐릭터 연회복 디자인해줘, 소매 디테일 강조"
- "두 캐릭터가 손잡고 걷는 구도로, 배경은 밤거리"

### 검사기

```
python3 plugins/nai-prompt/skills/nai-prompt/scripts/check_prompt.py prompt.txt
```

금지 태그, 가중치 범위, `::` 닫힘, 영어 외 문자, 배경 기본값, 추상적인 문장을 검사합니다.
