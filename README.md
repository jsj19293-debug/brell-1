# brell-1 플러그인 저장소

## brell (v0.6.0)

BRELL 캐릭터챗 작업 스킬입니다. v0.6.0에서 `/NAI`(NovelAI V4.5 Full 이미지 프롬프트)를 합쳤습니다.

### `/NAI`
명령어를 쳤을 때만 작동합니다. 예) `/NAI 엘린 캐릭터, 비 오는 항구에서 일하는 장면, 복장 3벌`

- 오리지널 캐릭터 디자인만 합니다. 기존 캐릭터 오마쥬·코스프레는 거절합니다.
- 자연어는 영어로, 색·소재·길이·위치·구조를 구체적으로 씁니다.
- 상황에 맞는 복장을 여러 벌 설계하고, 가중치는 -3 ~ 3 범위로 씁니다.
- 작가 태그, 퀄리티 태그, 그림체 태그는 거절합니다.
- 배경은 기본으로 넣지 않고(`simple background, white background`), 요청하면 추가합니다.
- 참조처: NAI 공식 문서, 단부루 위키, 아카라이브 AI그림 채널, 핀터레스트. 아카라이브와 핀터레스트는 브라우저(Claude in Chrome 등)가 연결되어 있으면 로그인된 상태로 봅니다.
- 파일: `plugins/brell/skills/brell/references/nai/`, 검사기 `plugins/brell/skills/brell/scripts/nai_check_prompt.py`

### 설치
claude.ai에 올린 brell(My Uploads)을 이 버전으로 바꾸거나, Claude Code에서:
```
/plugin marketplace add jsj19293-debug/brell-1
/plugin install brell@brell-1
```
두 경로로 동시에 설치하면 brell이 두 개가 되므로 하나만 씁니다.
