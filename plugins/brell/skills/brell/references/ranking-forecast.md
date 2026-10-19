# 바베챗 신작랭킹 마감 예측

바베챗 작품이 7일 신작랭킹(주간)을 끝낼 때 누적 프로챗이 얼마쯤 될지, 순위가 어디쯤일지 추정한다. 제작자 작품과 같은 기간 신작들의 실제 통계로 교차검증한다.

## 쓰는 곳
- 랭킹: `https://babechat.ai/dashboard?tab=new_ranking&gender=male&type=realtime|daily|weekly`
- 통계: `https://statistics.babechat.ai/character/{id}` (전체 통계 `/overview`)
- 통계 API (statistics.babechat.ai 탭에서 `fetch`, 읽기 전용 GET만 쓴다)
  - 검색: `https://babe-api.fastwrtn.com/babechat/search?search={이름}&sort=popular&limit=5&offset=0&isSafetyEnabled=false` → `id`, `publishedAt`(UTC), `chatCount`
  - 기록: `https://babe-api.fastwrtn.com/character?characterId={id}&period=month|day` → `data[0].datas[]` = 약 30분 간격 `{chatCount, likeCount, isTopNew, createdAt(UTC)}`, 누적값
- 시간은 모두 KST로 바꿔 보고한다(UTC+9).

## 숫자 읽는 법 (중요)
- 랭킹 목록 한 줄은 `[대화량] [지표] [순위] N [제목]` 순서다. 앞 숫자가 그 작품 대화량, 뒤 숫자가 랭킹 지표(프로챗)다. 숫자는 제목 **앞에** 붙은 것이 그 작품 것이다.
- **실시간 지표는 누적이 아니다.** 최근 약 1~1.5시간 사용량이다(2026-10-17 확인: 실시간 ÷ 최근 1시간 대화 증가 ≈ 100~150). 제작자가 실시간 숫자를 누적으로 말하면 바로잡는다.
- **일간**: 직전 24시간 프로챗. **주간**: 출시부터의 누적 프로챗(7일까지). 둘 다 **매일 낮 12시(KST) 기준**으로 갱신되고, 갱신이 몇 분 늦을 수 있다.
- 대화량 1당 프로챗(이하 PC비율)은 작품마다 65~105, 평균 약 85였다(2026-10-17, 일간·주간 지표 ÷ 같은 구간 대화량 증가).

## 절차
1. **기준 잡기**: 제작자 작품을 검색해 `publishedAt`과 기록을 받는다. 지금 출시 후 몇 시간째인지, 누적 대화량, 최근 1시간·2시간 증가량을 적는다.
2. **비교군 고르기**: 신작랭킹 `weekly`·`daily`·`realtime` 상위 30위 안에서 출시 2~7일 된 작품 8~12개를 고른다. 장르가 비슷한 작품을 우선한다.
3. **비교군 곡선**: 각 작품의 출시 후 14h·24h·48h·72h·96h·120h·144h·168h 시점 대화량을 뽑는다(아래 스니펫). 제작자 작품의 현재 경과 시간을 기준점으로 삼아 `7일 대화량 ÷ 기준점 대화량` 배수를 구한다. 아직 7일이 안 된 작품은 "이상"으로 표시한다.
4. **PC비율 보정**: 비교군마다 `주간 지표 ÷ 그날 12시 시점 누적 대화량`, `일간 지표 ÷ 전날 12시~그날 12시 대화량 증가`를 구한다. 제작자 작품이 이미 일간·주간에 올라와 있으면 그 작품 자체 비율을 쓴다. 없으면 `실시간 ÷ 최근 1시간 증가`를 비교군과 견줘 비슷한 작품들의 PC비율을 빌려 쓴다.
5. **예측**: 7일 대화량 = 현재 대화량 × 배수(보수·중간·낙관 = 비교군 하위·중앙·상위). 7일 누적 프로챗 = 7일 대화량 × PC비율. 범위로 낸다.
6. **순위 감각**: 최신 `weekly` 목록의 1·2·5·7·10위 지표와 견준다. 최근 1시간 속도가 제작자 작품보다 빠른 더 늦게 나온 신작이 있으면 위협 요인으로 따로 적는다.

## 스니펫 (statistics.babechat.ai 탭)
```js
const at=(d,t)=>{let v=null;for(const x of d){if(new Date(x.createdAt).getTime()<=t)v=x.chatCount;}return v;};
const names=[/* 작품 제목들 */];
const S=n=>fetch('https://babe-api.fastwrtn.com/babechat/search?search='+encodeURIComponent(n)+'&sort=popular&limit=5&offset=0&isSafetyEnabled=false').then(r=>r.json()).then(s=>s.data.find(x=>x.name===n)||s.data[0]);
const out=await Promise.all(names.map(async n=>{const c=await S(n);const j=await fetch('https://babe-api.fastwrtn.com/character?characterId='+c.id+'&period=month').then(r=>r.json());const d=j.data[0].datas,p=new Date(c.publishedAt).getTime();return [n.slice(0,10),c.publishedAt,[14,24,48,72,96,120,144,168].map(h=>at(d,p+h*36e5)).join('/'),'now:'+d[d.length-1].chatCount].join(' ');}));
out.join('\n')
```
- 순서대로 하나씩 `await`하면 도구가 시간 초과로 끊긴다. `Promise.all`로 한 번에 받는다.
- 랭킹 목록은 dashboard 탭에서 `document.body.innerText`를 줄로 나눠, `숫자줄 다음이 'N'`인 곳을 순위로 잡고 그 앞 두 줄(대화량·지표)과 뒤 한 줄(제목)을 묶는다.

## 참고 기준치 (2026-10-17 측정, 오래되면 다시 잰다)
| 작품 | 14h 대화량 | 7일(또는 측정 시점) | 배수 |
|---|---|---|---|
| 동창회에서 남의 여친 따먹기 | 1.5만 | 10.4만 | 7.0 |
| RE:이건 NTL 해달라는거잖아 | 2.2만 | 14.7만 | 6.6 |
| 기사단에서 살아남기 | 2.0만 | 13.9만+ (4.8일) | 7+ |
| E.G.O 제로 아카데미 | 1.0만 | 10.4만 | 10.1 |
| 그 찐따의 누나 | 2.0만 | 9.7만 | 4.8 |
| XX팬스요? 제가요? | 1.4만 | 6.6만 | 4.7 |
| 한량과 서릿발 규수, 신소율 | 3.9만 | 9.4만 | 2.4 |
| 그 닌자마을의 풍습 | 3.1만 | 8.7만 | 2.8 |
- 첫날 몰린 작품(14h 대화량이 큰 작품)일수록 배수가 낮다.
- 그때 주간 신작 1위 1,274만, 2위 1,027만, 7위 726만, 10위 637만.

## 기다리지 않기
- 낮 12시 갱신을 기다리려고 오래 멈추지 않는다. 지금 있는 숫자로 먼저 예측을 보고하고, "12시 갱신 뒤 다시 보면 범위가 좁아진다"고 덧붙인다.

## 보고 형식
- 첫 줄: 예상 7일 누적 프로챗(중간값)과 범위.
- 실시간 숫자를 누적으로 오해했으면 바로잡는 한 단락.
- 비교군 표(14h·7일·배수), PC비율과 근거, 시나리오별(보수·중간·낙관) 대화량과 프로챗, 주간 순위 감각, 위협 신작.
- 추정치임을 밝히고, 각 숫자의 출처(통계 페이지·랭킹 탭·측정 시각)를 적는다.
