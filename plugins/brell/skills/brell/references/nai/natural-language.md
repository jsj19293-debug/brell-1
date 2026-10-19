# 구체적 자연어 작성법

NAI 4.5는 자연어를 이해하지만, 정확한 개념은 태그가 더 안정적이다. 그래서 **태그로 무엇이 있는지를, 문장으로 어떻게 생겼고 어디에 붙어 있는지를** 쓴다(커뮤니티 의견, arca.live/b/aiart/181003788).

## 문장에 꼭 들어갈 정보 (하나 이상)
- **색**: 정확한 색 이름. 예) charcoal grey, deep burgundy, pale mint, brass, ivory
- **소재**: wool, leather, linen, satin, velvet, knit, denim, sheer chiffon, brushed metal
- **길이·크기**: ends at mid-thigh, cropped just above the navel, ankle-length, oversized
- **핏**: fitted, loose, tailored at the waist, flared from the hips
- **위치**: on the left shoulder, along the hem, at the center of the chest, wrapped twice around the waist
- **구조**: double-breasted, high stand collar, three box pleats at the back, laced up the sides
- **상태**: sleeves rolled to the elbows, top button undone, slightly wrinkled, wet at the hem

## 금지: 추상어만 있는 문장
elegant, mysterious, beautiful, cute, cool, stylish, gorgeous, fancy, unique, dramatic, aesthetic, detailed, intricate만으로 된 문장은 쓰지 않는다. 이런 단어를 쓰려면 같은 문장에 구체 정보를 붙인다.

## 나쁜 예 → 좋은 예

| 나쁜 예 | 좋은 예 |
|---|---|
| She wears an elegant mysterious outfit. | She wears a fitted charcoal wool coat that ends at mid-thigh, with a high stand collar and a single row of brass buttons. |
| A cool fantasy armor. | Brushed steel pauldrons cover only the right shoulder, held by two brown leather straps that cross over the chest. |
| Cute accessories in her hair. | Two small pearl hairpins hold her bangs back above the left eyebrow. |
| A stylish modern hanbok. | A short ivory jeogori with a deep navy collar band, worn over a pleated ankle-length chima in dusty rose. |
| Her pose is dynamic. | She steps forward on her left foot, her right hand pulling the coat's lapel aside. |
| Detailed sleeves. | Each sleeve widens from the elbow into a bell shape and ends in a band of black lace. |

## 문장 쓰는 규칙
1. **한 문장에 한 부위.** 여러 옷을 한 문장에 몰지 않는다. 색이 섞이는 원인이 된다.
2. **주어를 분명히.** `She`, `The coat`, `The left sleeve`처럼 무엇에 대한 문장인지 앞에 둔다.
3. **태그와 겹치게.** 문장으로 묘사한 옷은 태그로도 넣는다. 예) 태그 `black coat, high collar` + 문장으로 구조 설명
4. **1~3문장이면 충분하다.** 문장이 많으면 토큰을 빨리 쓰고 핵심이 흐려진다.
5. **관계를 쓴다.** 겹침(worn over, tucked into), 고정(pinned with, held by), 손 위치(her left hand rests on the sword hilt)처럼 태그로 표현하기 어려운 것을 문장으로 쓴다.
6. **그림체 묘사는 쓰지 않는다.** "painted in soft watercolor", "anime style", "realistic rendering" 같은 표현은 금지 태그와 같은 이유로 거절한다.
7. **가중치는 문장 단위로 건다.** `1.3::문장 ::`처럼 문장 전체를 감싼다.
