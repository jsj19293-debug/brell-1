# 에덴

## 주소·로그인
- `https://www.eden-chat.com/my-works` (`edenchat.ai`는 열리지 않는다)
- 바로 가면 `/login`으로 넘어간다. '에덴에 어서오세요' → 'Google로 시작하기' 후 `/my-works`로 돌아온다. 누른 뒤 탭 번호가 바뀔 수 있으니 탭 목록을 다시 조회한다.

## 편집화면 진입
- 에덴 탭에서 `fetch('/api/user/works')`로 id·title을 읽어 id를 찾는다 → `/edit-work/{id}`.

## 탭 구성
- 기본설정 · 작품 소개 · 상세 설정(메인) · 캐릭터 설정 · 미디어 에셋 · 프리셋 · 시작 상황 · 추천 페르소나 · 로어북.

## 언어 판본
- 상단 '언어 판본 선택'에 한국어(원문)·English·日本語·中文（繁體）. 주소로는 `?language=en|ja|zh-TW`. 판본마다 메인·로어북·작품소개 등이 따로 저장되고 '번역 저장'으로 저장한다. '자동 번역' 버튼은 누르지 않는다. 번역·최신화 절차는 `../translate.md`.

## 읽기 (같은 탭에서 fetch, 읽기만)
- 작품 `GET /api/works/{id}`, 캐릭터 `GET /api/works/{id}/characters`.
- 필드: `scenario_settings`(메인), `description`(작품소개), `lorebook[]`(key는 쉼표로 이은 문자열·title·value·triggerMode·turnRange·offKeywords·offTurnRange), `start_scenarios[]`(title·detailedSettings·subPrompt), 캐릭터 `character_details`, `visibility`, `status`, `updated_at`.

## 넣기
- 메인·작품소개: react-hook-form 객체(입력칸 fiber 위쪽 props에서 `setValue`·`getValues`를 가진 것)로 `setValue('scenario_settings'|'description', 새값, {shouldDirty:true, shouldTouch:true})`. 넣기 전에 `getValues()` 값이 서버 값과 같은지 먼저 확인한다.
- 로어북: '로어북' 탭에서 입력칸 fiber를 올라가며 `setLorebook`을 가진 memoizedState를 찾는다. 상태 형태 `{id,title,keywords[],content,keywordInput,triggerMode,offKeywords[],offKeywordInput,turnRange,offTurnRange}`. `setEditingLorebook({})` 후 `setLorebook(새배열)`. 넣은 뒤 다시 찾아 읽어 확인한다.
- 시작 상황: 왼쪽 목록에서 시작 설정 이름을 눌러 바꾸고, '상세 설정' textarea에 네이티브 setter + input 이벤트로 넣는다. 다른 시작 설정을 눌렀다 돌아와 값이 남았는지 확인한다.
- 구조가 바뀌어 못 찾으면 화면 입력으로 대체하되 항목이 많으면 방법을 상의한다.

## 저장 (주의)
- **편집기가 변경 후 잠시 뒤 서버에 자동 임시저장한다**(2026-10 확인. 화면 위 "변경사항이 임시 저장됨 · 시각"). 이때 서버의 `status`가 `draft`, `visibility`가 `private`로 바뀌어 **공개·링크 공개작이 비공개가 된다.** 브라우저 네트워크 기록에는 잡히지 않을 수 있다.
- 그래서 에덴은 값을 넣는 순간 서버에 들어간다고 보고, 넣기 전에 제작자에게 "임시저장되면 비공개로 바뀐다"고 알리고 동의를 받는다. 다른 사이트보다 에덴을 마지막에 한다.
- 넣은 뒤 `GET /api/works/{id}`의 `updated_at`·`visibility`·`status`를 읽어 보고한다. 공개 상태를 되돌리는 '작품 게시'는 제작자가 누른다.

## 누르지 않는 것
- 임시저장 버튼, 작품 게시. 작품 카드 '수정' 옆 휴지통(삭제).
