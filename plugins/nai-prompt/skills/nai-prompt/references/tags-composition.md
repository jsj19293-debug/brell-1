# 구도·포즈·배경 태그 (단부루)

표기 규칙은 tags-character.md와 같다.
출처: https://danbooru.donmai.us/wiki_pages/tag_group:image_composition (항목 구성을 검색 결과로 확인했다)

## 프레이밍 (가까운 것 → 먼 것)
portrait ✔, close-up ✔, upper body ✔, cowboy shot ✔(허벅지 중간부터 위), lower body, full body ✔, wide shot, very wide shot, head out of frame, feet out of frame

**복장 중심 선택 기준**
- 전신 의상, 신발까지 보여야 함 → full body
- 상의·허리 디테일 → cowboy shot
- 얼굴·머리 장식·목 장식 → upper body, portrait

## 각도
from above ✔, from below ✔, from side ✔, from behind ✔, profile, straight-on, dutch angle ✔

## 원근
foreshortening ✔, fisheye ✔, perspective, depth of field, vanishing point, pov
- bokeh ✔는 배경 흐림 효과라서 배경 없는 기본값에서는 쓰지 않는다.

## 시선
looking at viewer ✔, looking away ⚠, looking to the side, looking back, looking up, looking down, looking afar, eye contact

## 자세
- 서기·앉기: standing ✔, sitting ✔, wariza ✔, seiza ✔, crossed legs ✔, knees up ✔, squatting, kneeling
- 눕기: lying, on back, on side
- 기울기: leaning forward ✔, leaning back, contrapposto ✔, head tilt ✔
- 팔: arms behind back ✔, arms up, arms crossed
- 움직임: walking, running, jumping

## 손동작
- 신호: peace sign(V4.5에서 v에서 바뀜), double v, thumbs up, pointing, pointing at viewer, waving, salute, shushing
- 손 위치: hand on own hip ✔, hands on own hips, hands up ✔, own hands together ✔, hand on own chest, hand on own cheek, hand in own hair, hands in pockets, outstretched hand, reaching towards viewer
- 태그로 부족하면 문장으로 쓴다: `her right hand holds the brim of her hat against the wind`

## 다중 캐릭터 상호작용 (NAI 문법)
각 캐릭터 칸에 `source#동작`, `target#동작`, `mutual#동작`을 쓴다. 예) A: `source#hug`, B: `target#hug` / 둘 다: `mutual#holding hands`

## 배경
**기본값(요청 없을 때)**: `simple background, white background`

단색 대안(요청 시): grey background, black background, gradient background ✔, two-tone background, abstract background ✔, pattern background
- transparent background는 단부루 태그지만 NAI 출력이 실제로 투명해지지 않는다.

장면(요청 시에만):
- 실내외: outdoors, indoors, scenery
- 실외: cityscape, street, alley, rooftop ✔, beach, ocean, forest, field, flower field, garden, castle, ruins, shrine, church
- 실내: classroom, bedroom, cafe ✔, library, kitchen, bathroom, office
- 하늘·시간: sky, cloud, blue sky, night, night sky, starry sky, sunset, day
- 날씨·빛: rain, snow, cherry blossoms, falling petals, light rays, sunlight, backlighting

배경을 넣을 때는 문장으로 위치 관계를 준다: `She stands on wet cobblestones in front of a closed bakery, lit by a single street lamp to her right.`
- `background dataset`은 인물 없는 배경 사진용이므로 캐릭터 그림에는 쓰지 않는다(공식 블로그).
