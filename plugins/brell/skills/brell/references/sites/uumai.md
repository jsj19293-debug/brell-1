# 우마이

## 주소·로그인
- `https://uumm.ai`
- 공지 팝업 '닫기' → 오른쪽 위 사람 아이콘 → 'Google로 계속하기'. `/login`으로 직접 가면 홈으로 돌아오므로 반드시 아이콘으로 연다. 로그인돼 있으면 `/create`로 바로 가도 스튜디오가 열린다.

## 편집화면 진입
- `/create`(왼쪽 '스튜디오') → '작품' 탭 카드 → 주황색 '편집'. 주소가 `/create/editor`라 직접 가지 않는다.
- 카드 '편집' 버튼은 innerText가 '편집'인 버튼 목록에서 카드 글자(제목·수정일)를 대조해 고른다.
- 들어간 뒤 왼쪽 위 작품명과 최종 수정일로 확인한다. 작품 상세 창이 떠 있으면 X로 닫는다.
- 같은 제목이 둘이면('공개' 발행본과 '초안') 따로 말이 없을 때 '공개'·발행일이 있는 쪽으로 들어가고 초안이 있다고 보고한다.

## 탭 구성
- 왼쪽 메뉴: 기본 정보(작품명·짧은 소개·상세 작품소개) · 상세 정보(메인) · 인트로 · 이미지 · 로어북 · JSX 컴포넌트 · 스킬 · BGM · 마무리 설정. 쓰는 메뉴는 기본 정보 · 상세 정보 · 인트로 · 이미지 · 로어북 · 마무리 설정이고, JSX 컴포넌트 · 스킬 · BGM은 쓰지 않는다.
- 상세 정보의 에디터 이름은 '상세 프롬프트'이며 화면에 50,000자 상한과 토큰 추정치가 표시된다. 작업 기준은 규격표(우마이 메인 15,000자)를 따른다.
- 로어북 '이름'은 AI 프롬프트에 반영되지 않고 설정(본문)만 전달된다(출처: 우마이 가이드 「07 - 로어북」 https://docs.channel.io/uumm_ai/ko/articles/07---%EB%A1%9C%EC%96%B4%EB%B6%81-875d13fe).
- 메뉴 버튼은 `innerText`로 찾아 누른다. 메뉴를 옮겨도 편집 내용은 유지된다.

## 읽기
- 에디터는 CodeMirror 6. `.cm-content`에는 React fiber가 없고 `cmTile`이 붙어 있다. 전문은 `el.cmTile.view.state.doc.toString()`(없으면 `cmTile` 안에서 `state.doc`을 가진 객체)으로 읽는다. 화면에 보이는 innerText는 일부만 나온다.
- 기본 정보의 에디터 2개: [0] 짧은 소개, [1] 상세 작품소개(HTML).
- 긴 글은 `localStorage`에 넣고 새 탭을 `/robots.txt`로 열어 `<pre>`에 넣어 읽은 뒤 지운다.

## 넣기
- 메인·인트로·작품소개: `.cm-editor`에서 부모로 올라가 fiber가 있는 첫 요소를 찾고, 그 fiber 위쪽 props 중 `value`(문자열)와 `onChange`를 가진 것에 `onChange(새문자열)`. 반영 후 `value === 새문자열` 확인, 메뉴를 옮겼다 돌아와 다시 확인.
- 인트로 메뉴(구 '시작 설정')는 에디터 2개(인트로 내용, 인트로 프롬프트). 인트로 탭은 '설정 추가'의 형제 버튼이며 누른 뒤 1초쯤 기다린다. 제목은 placeholder '인트로의 제목'인 input.
- 로어북(zustand): '로어북 테스트' 버튼의 fiber를 올라가 `lorebooks`를 가진 상태를 찾으면 읽기용 목록이 나온다.
  - 수정 함수는 항목을 한 번 펼쳐(목록 줄 클릭) 이름 입력칸 fiber에서 `updateLorebook`·`deleteLorebook`·`setEditingLorebook`·`addKeyword`·`removeKeyword`를 얻어 `window`에 보관한다. 항목 펼침은 위쪽 ^ 로 접는다(접어도 수정 유지).
  - `updateLorebook(id, patch)`: `formData.lorebooks`를 고친다. 넣은 뒤 1초쯤 기다려 위 목록을 다시 읽어 확인한다.
  - `importLorebooks(items)`: 끝에 추가(`{name, keywords[], content, activateOnIntro}`). `notKeywords`를 비우므로 제외 키워드는 추가 후 `updateLorebook`으로.
  - `reorderLorebooks(전체배열)`: `order`를 1부터 다시 매겨 넘긴다. 반영 안 될 때가 있어 다시 읽어 확인하고, 안 됐으면 `updateLorebook`/`deleteLorebook`으로 한다.
  - 항목 필드: `id, order, name, keywords[], content, activateOnIntro, isConstant, andKeywords[], notKeywords[], scanTurns, folderId …`
- JS 도구는 최상위 `return`을 쓰면 뒤 코드가 돌지 않고 undefined가 나온다. 분기는 if/else 식으로 쓴다.

## 로어북 테스트 (무료, 검수용)
- 테스트 창의 textarea 2개(직전 AI 응답, 보낼 메시지)에 네이티브 setter + input 이벤트로 값을 넣고 '테스트'. 항목별 발동 여부와 걸린 키가 나온다.

## 누르지 않는 것
- '편집' 바로 왼쪽 '삭제'. 오른쪽 위 저장·발행(제작자가 누른다).
