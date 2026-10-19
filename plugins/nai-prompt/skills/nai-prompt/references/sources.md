# 출처별 조사 방법과 검증 상태

## 조사 방법

| 출처 | 용도 | 접속 |
|---|---|---|
| NAI 공식 문서 docs.novelai.net, blog.novelai.net | 문법·모델 동작의 최종 기준 | WebSearch/WebFetch. 열리지 않으면 검색 결과 발췌를 쓰고, 발췌라고 밝힌다 |
| 단부루 위키 danbooru.donmai.us/wiki_pages/tag_group:* | 태그 철자·의미·분류(작가·작품·캐릭터·메타) | WebFetch. 막히면 github.com/DominikDoom/a1111-sd-webui-tagcomplete 의 tags/danbooru.csv(태그, 분류, 게시물 수, 별칭)로 확인한다 |
| 아카라이브 AI그림 채널 arca.live/b/aiart | 실사용 팁, 4.5에서 먹히는 표현 | **사용자 브라우저(로그인됨)** 가 연결되어 있으면 브라우저로 연다. 없으면 WebSearch 검색 결과만 쓴다 |
| 핀터레스트 pinterest.com | 의상 실루엣·소재·구조 레퍼런스 | **사용자 브라우저(로그인됨)** 로만 제대로 볼 수 있다. 없으면 이 출처는 "확인 못 함"으로 둔다 |

**브라우저 도구 이름**: `mcp__claude-in-chrome__*`(Claude in Chrome), `mcp__Claude_Browser__*` 또는 `mcp__remote-devices__Claude_Browser__*`(내장 브라우저). 쓰기 전에 해당 브라우저 스킬을 읽는다. 사용자 비밀번호는 묻지 않는다.

**아카라이브 검색어 예**: "NAI 4.5 자연어", "노벨AI 4.5 가중치 음수", "4.5 의상 색 번짐", "4.5f 캐릭터 프롬프트", "흰배경 고정"
**핀터레스트 검색어 예**: references/outfit-design.md 7항 참조

## 표시 규칙
- 공식 문서: 링크만 붙인다.
- 커뮤니티: "커뮤니티 팁" 또는 "의견"이라고 표시한다.
- 근거 없는 판단: "출처 없음(판단)"
- 열어 보지 못한 출처: "확인 못 함"

## 이 스킬 작성 시 확인 상태 (2026-10-19)
- 클라우드 환경이라 docs.novelai.net, danbooru.donmai.us, arca.live, pinterest.com 페이지를 직접 열지 못했다. 공식 문서·아카라이브는 **검색 결과 발췌**로 확인했다. 단부루는 GitHub의 danbooru.csv 사본 앞부분(고빈도 태그)으로 확인했다.
- 핀터레스트는 보지 못했다. 패션 용어는 봉제 용어 사전(sewguide.com, moodfabrics.com)과 일반 지식으로 채웠다.
- 다시 확인할 것: UC 프리셋 전체 문자열, V4.5 최대 인원(6명 추정), ⚠ 표시 태그, ±10 이상 가중치 동작.

## 주요 출처 링크
- https://docs.novelai.net/en/image/strengthening-weakening/
- https://docs.novelai.net/en/image/models/
- https://docs.novelai.net/en/image/multiplecharacters/
- https://docs.novelai.net/en/image/textrendering/
- https://docs.novelai.net/en/image/qualitytags/
- https://docs.novelai.net/en/image/undesiredcontent/
- https://docs.novelai.net/en/image/tags/
- https://novelai.net/updates?id=v4-numeric-emphasis
- https://blog.novelai.net/novelai-diffusion-v4-5-full-release-678318c86205
- https://danbooru.donmai.us/wiki_pages/tag_group:image_composition
- https://raw.githubusercontent.com/DominikDoom/a1111-sd-webui-tagcomplete/main/tags/danbooru.csv
- arca.live/b/aiart/144911662 (가중치·태그 정보글)
- arca.live/b/aiart/159947900 (4.5 Full Q&A, 의상 태그 순서·색 번짐·배경)
- arca.live/b/aiart/181003788 (태그와 자연어 역할 분담)
- arca.live/b/aiart/138308689 (태그 순서 민감도)
- arca.live/b/aiart/135938936 (텍스트·태그 이름 변경)
