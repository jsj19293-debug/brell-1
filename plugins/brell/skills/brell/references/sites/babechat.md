# 바베챗

## 주소·로그인
- `https://babechat.ai`
- 처음엔 '베리 혜택' 같은 홍보 팝업 → 아래 '닫기'. 그 뒤 '어떤 콘텐츠를 추천할까요?' 취향 선택 팝업은 고르지 말고 아래 '로그인 / 회원가입' → 'Google 계정으로 시작하기'. 로그인 뒤 홍보 팝업이 한 번 더 뜨면 '닫기'.

## 편집화면 진입
- 오른쪽 위 **프로필 사진**(맨 오른쪽 원형) → '캐릭터 관리'(`/character/my`) → 제목 줄 점 3개 → '수정'. 주소 `/character/edit/{id}`.
- **프로필 사진 바로 왼쪽 '19' 토글은 성인작 표시 설정이다. 누르지 않는다.** 잘못 눌렀으면 바로 다시 눌러 `[role=switch]`의 `aria-checked`가 true인지 확인하고 보고한다.
- '수정'을 누르면 "임시 저장된 데이터가 있어요. 이어서 수정할까요?" 창이 뜰 수 있다. '처음부터 수정'(서버 버전)과 '이어서 수정'(임시 저장본) 중 고르지 말고 제작자에게 묻는다.

## 탭 구성
- 프로필 · 캐릭터 설정(메인) · 캐릭터 에셋 · 시작 상황 · 로어북 · 기타 설정 및 등록.
- 시작 상황은 위쪽에 시작 설정 이름 버튼이 여러 개 있다. 버튼 안 `span` 글자로 찾아 `closest('button')`을 누른다(버튼 innerText에 배지 글자가 섞일 수 있음).
- 로어북 항목은 줄 오른쪽 끝 펼침 화살표로 연다(왼쪽에 수정·삭제).
- 로어북은 동시 적용 기본 5개라 중요한 항목을 위에 둔다.

## 데이터 (react-hook-form)
- 편집 화면 전체가 하나의 react-hook-form이다. '불러오기' 버튼 fiber를 올라가 props에서 `setValue`·`getValues`를 가진 객체를 찾는다.
- 필드: `description`(소개, 500), `characterDetails`(메인, 7,000), `initialTitle`·`initialAction`(상황, 1,000)·`initialMessage`(첫 대사, 500)·`playGuide`(500)·`replySuggestions[]`(기본 시작 설정), `startingScenarios[]`(나머지 시작 설정, 같은 키), `keywordBooks[]`(로어북 `{id,title,content,keywords[],order}`).

## 읽기
- 위 폼에서 `getValues()`로 읽는다. 긴 글은 `localStorage`에 넣고 새 탭을 `/robots.txt`로 열어 `<pre>`에 넣어 읽은 뒤 지운다.

## 넣기
- 소개·메인·시작 상황 칸: 해당 탭에서 textarea/input을 값으로 찾아 네이티브 setter + input 이벤트. 넣은 뒤 `getValues()`로 반영 확인.
- 로어북: **`setValue('keywordBooks', 새배열, {shouldDirty:true, shouldTouch:true})`만 쓴다.** useFieldArray의 내부 fields 상태를 직접 dispatch하면 화면 목록과 폼 값이 어긋난다. 삭제도 배열에서 빼고 `order`를 0부터 다시 매겨 넣는다. 넣은 뒤 화면 목록(droppable 자식) 제목과 개수를 확인한다.

## 누르지 않는 것
- '수정' 바로 아래 '삭제'. 로어북 줄 왼쪽의 삭제. 성인작 토글. 저장·등록 버튼(제작자가 누른다).
