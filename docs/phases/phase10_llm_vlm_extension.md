# Phase 10. LLM/VLM Extension

## 1. Phase 목표

Phase 10의 목표는 MissionBot-ROS2에 자연어 기반 Mission Understanding 계층을 추가하는 것이다.

사용자가 한국어 자연어로 로봇에게 명령하면, LLM이 명령을 해석하여 ROS2 실행 모듈이 처리할 수 있는 구조화된 Mission command로 변환한다.

이번 Phase에서는 LLM을 로봇의 직접 제어기로 사용하지 않는다.

```text
LLM
→ 자연어 해석

ROS2 / Navigation2 / MoveIt2
→ 실제 실행
```

Phase 10의 최종 구현 범위:

```text
OpenAI API 연결
LLM Mission Parser
Pydantic Structured Outputs
다중 명령 테스트
Semantic Validator
ROS2 Mission Parser Node
```

이번 Phase에서 제외한 범위:

```text
실제 VLM 이미지 입력
Object detection 및 grounding
Navigation2 goal 직접 전달
MoveIt2 task 직접 실행
복합 task planner
LangGraph Agent
VLA
```

---

## 2. 시작 전 상태

Phase 9까지 MissionBot-ROS2에서는 다음 흐름을 확인했다.

```text
ROS2 기본 구조
→ Gazebo TurtleBot3
→ RViz2 / TF2
→ SLAM
→ Navigation2
→ rosbag2
→ Failure Analysis
→ Control Basics
→ MoveIt2 Basics
```

Phase 10에서는 기존 실행 모듈을 대체하지 않고, 그 앞에 자연어 명령 해석 계층을 추가했다.

```text
Natural Language
→ Mission Understanding
→ Robot Execution Modules
```

---

## 3. 최종 시스템 구조

```text
사용자 자연어 명령
        ↓
/missionbot/user_command
        ↓
mission_parser_node
        ↓
OpenAI LLM Mission Parser
        ↓
Pydantic Structured Outputs
        ↓
Semantic Validator
        ↓
Execution Allowed 판단
        ↓
/missionbot/mission_command
```

역할 분리:

```text
LLM Mission Parser
→ 자연어 의미 해석
→ entity와 intent 추출
→ MissionCommand 생성

Structured Outputs
→ 필드와 타입 고정

Semantic Validator
→ 필드 간 의미 규칙 검사
→ 실행 안전 조건 검사

Mission Parser Node
→ ROS2 topic 입출력
→ 검증 실패 및 unknown 명령 발행 차단
```

---

## 4. 개발 환경

```text
OS:
Ubuntu 22.04 LTS

ROS2:
Humble Hawksbill

Python:
3.10

Project:
~/projects/missionbot-ros2

Package:
mission_parser

Build Type:
ament_python

LLM API:
OpenAI Responses API

Final Parser Model:
gpt-4o-mini

Structured Output:
Pydantic BaseModel
```

---

## 5. 패키지 구조

```text
src/mission_parser/
├── package.xml
├── setup.py
├── setup.cfg
├── resource/
│   └── mission_parser
└── mission_parser/
    ├── __init__.py
    ├── openai_connection_test.py
    ├── llm_mission_parser.py
    ├── semantic_validator.py
    ├── semantic_validator_test.py
    └── mission_parser_node.py
```

파일 역할:

```text
openai_connection_test.py
→ OpenAI API 연결 확인

llm_mission_parser.py
→ 자연어를 MissionCommand로 변환
→ 다중 명령 통합 테스트

semantic_validator.py
→ MissionCommand 의미 및 안전 규칙 검사
→ 실행 허용 여부 판단

semantic_validator_test.py
→ Validator 독립 테스트

mission_parser_node.py
→ ROS2 자연어 입력과 Mission command 출력 연결
```

---

## 6. OpenAI API 연결 준비

초기 설치 명령:

```bash
sudo apt update
sudo apt install -y python3-pip

python3 -m pip install --user openai python-dotenv
```

설치 확인:

```bash
python3 -m pip --version
python3 -m pip show openai
python3 -m pip show python-dotenv
```

API key는 Python 코드에 직접 작성하지 않고 프로젝트 루트의 `.env`에서 관리했다.

```text
~/projects/missionbot-ros2/.env
```

형식:

```text
OPENAI_API_KEY=API_KEY_VALUE
```

API key 값은 Git, 로그, 문서에 기록하지 않는다.

`.gitignore`:

```gitignore
.env
.env.*
*.pem
*.key
```

---

## 7. `.env` 로딩 방식

ROS2 Python 패키지는 빌드 후 `install/`에 설치된다.

`__file__`을 기준으로 `.env`를 찾으면 다음과 같은 설치 경로를 가리킬 수 있었다.

```text
install/mission_parser/lib/.env
```

이번 프로젝트에서는 MissionBot 프로젝트 루트에서 실행한다는 규칙을 사용했다.

```python
project_root = Path.cwd()
env_path = project_root / ".env"
load_dotenv(dotenv_path=env_path)
```

실행 기준:

```bash
cd ~/projects/missionbot-ros2
source install/setup.bash
ros2 run mission_parser mission_parser_node
```

---

## 8. OpenAI API 연결 테스트

실행:

```bash
cd ~/projects/missionbot-ros2

colcon build --packages-select mission_parser
source install/setup.bash

ros2 run mission_parser openai_connection_test
```

확인 결과:

```text
LLM 응답:
MissionBot-ROS2 Phase 10 연결이 성공적으로 테스트되었습니다.
```

이를 통해 다음을 확인했다.

```text
ROS2 Python package 실행
.env API key 로드
OpenAI client 생성
Responses API 요청
LLM output_text 출력
```

---

## 9. MissionCommand schema

최종 Pydantic schema의 핵심 구조:

```python
class MissionCommand(BaseModel):
    intent: Literal[
        "move_to",
        "inspect_object",
        "stop",
        "unknown",
    ]

    target: str | None
    object: str | None
    constraints: list[str]

    requires_navigation: bool
    requires_vision: bool
    requires_manipulation: bool
```

JSON 예시:

```json
{
  "intent": "move_to",
  "target": "desk",
  "object": null,
  "constraints": [
    "front"
  ],
  "requires_navigation": true,
  "requires_vision": false,
  "requires_manipulation": false
}
```

---

## 10. 필드 정의

### intent

사용자 명령의 핵심 목적을 표현한다.

```text
move_to
→ 특정 장소 또는 landmark로 이동

inspect_object
→ 물체 찾기 또는 확인

stop
→ 현재 동작 정지

unknown
→ 현재 MissionBot 지원 범위 밖
```

### target

이동 목적지 또는 spatial landmark다.

예:

```text
desk
shelf
door
charging_station
```

방향 자체는 target으로 사용하지 않는다.

잘못된 예:

```text
left
front
front_of_desk
```

### object

사용자가 찾거나 확인하려는 물체다.

예:

```text
cup
red_cup
bottle
```

이동 목적지로 사용된 책상이나 선반은 object에 넣지 않는다.

### constraints

사용자가 명시한 공간 관계 또는 추가 행동 조건이다.

```text
front
behind
left
right
near
stop_after_arrival
```

### requires_navigation

이동로봇의 이동이 필요한지 나타낸다.

### requires_vision

카메라 또는 물체 인식이 필요한지 나타낸다.

### requires_manipulation

로봇팔 조작이 필요한지 나타낸다.

이번 Phase의 지원 intent에는 실제 manipulation intent가 없으므로 테스트 결과에서는 `false`로 사용했다.

---

## 11. 영어 정규화 기준

사용자 자연어가 한국어여도 Mission command 내부 문자열은 영어로 통일했다.

```text
책상 → desk
선반 → shelf
컵 → cup
빨간 컵 → red_cup
앞 → front
뒤 → behind
왼쪽 → left
오른쪽 → right
```

문자열 형식:

```text
lowercase_snake_case
```

예:

```text
red_cup
stop_after_arrival
charging_station
```

이 기준을 적용하면 이후 Python과 ROS2 모듈에서 문자열 비교가 단순해진다.

```python
if command["target"] == "desk":
    ...
```

---

## 12. 최소 LLM Mission Parser

초기 흐름:

```text
사용자 자연어
→ OpenAI Responses API
→ JSON 문자열
→ json.loads()
```

초기 구현에서는 모델의 응답에 Markdown code block이 포함될 가능성을 고려해 별도 문자열 정리 함수도 사용했다.

하지만 prompt로만 JSON 출력을 요청하면 다음 문제가 남는다.

```text
필드 누락 가능성
타입 불일치 가능성
허용되지 않은 intent 가능성
JSON 밖 설명 추가 가능성
```

이를 해결하기 위해 Structured Outputs를 적용했다.

---

## 13. Structured Outputs 적용

Structured Outputs 적용 흐름:

```text
Pydantic MissionCommand
→ OpenAI Responses API parse
→ schema를 따르는 MissionCommand 객체
```

핵심 호출 구조:

```python
response = client.responses.parse(
    model="gpt-4o-mini",
    input=[
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": user_command,
        },
    ],
    text_format=MissionCommand,
)
```

결과:

```python
mission_command = response.output_parsed
```

Pydantic 객체를 dictionary로 변환:

```python
command_dictionary = mission_command.model_dump()
```

Structured Outputs 적용 후 수동 JSON 정리와 `json.loads()` 처리를 제거했다.

---

## 14. Prompt 의미 규칙

Prompt에는 다음 역할을 정의했다.

```text
사용자의 자연어 명령을 Mission command로 변환한다.
로봇을 직접 실행하지 않는다.
Navigation2, MoveIt2, VLM 실행 코드를 생성하지 않는다.
사용자 명령에 없는 조건을 임의로 추가하지 않는다.
```

출력 기준:

```text
문자열은 영어로 작성
lowercase_snake_case 사용
한국어 장소, 물체, 방향을 영어 표준 표현으로 정규화
```

공간 관계 기준:

```text
front, behind, left, right, near는 공간 관계
공간 관계는 constraints에 저장
방향 자체를 target으로 사용하지 않음
```

예:

```text
책상 앞으로 이동해줘
```

변환:

```text
target = desk
constraints = ["front"]
```

다음처럼 변환하지 않는다.

```text
target = front_of_desk
object = desk
```

---

## 15. 모델 선택

OpenAI 연결 테스트 초기에는 `gpt-4.1-mini`를 사용했다.

최종 Mission Parser에서는 `gpt-4o-mini`를 사용했다.

이번 parser의 역할은 다음과 같은 제한된 구조화 작업이다.

```text
짧은 자연어 명령 분류
entity 추출
필드별 boolean 판단
영어 표준 표현 변환
```

따라서 최종 테스트에서는 `gpt-4o-mini`를 사용해 기능을 검증했다.

---

## 16. 테스트 명령

테스트 세트:

```text
1. 책상 앞으로 이동해줘
2. 빨간 컵을 찾아줘
3. 선반 앞까지 가서 멈춰
4. 왼쪽에 있는 컵을 확인해줘
5. 멈춰
6. 커피를 만들어줘
```

예상 intent:

```text
1. move_to
2. inspect_object
3. move_to
4. inspect_object
5. stop
6. unknown
```

---

## 17. Exact-match 테스트

LLM 실제 결과와 미리 정의한 예상 결과를 dictionary 단위로 비교했다.

`constraints`는 순서가 달라도 의미가 같을 수 있으므로 비교 전에 정렬했다.

```python
normalized["constraints"] = sorted(
    normalized["constraints"]
)
```

Exact-match는 한 명령의 모든 필드가 일치해야 PASS가 된다.

초기 결과:

```text
PASS: 4
FAIL: 2
Exact-match pass rate: 66.7%
```

실패 내용:

```text
"선반 앞까지"에서 front 누락
"왼쪽에 있는 컵"에서 left를 target으로 사용
```

Prompt의 공간 관계 규칙과 예시를 강화한 뒤:

```text
PASS: 5
FAIL: 1
Exact-match pass rate: 83.3%
```

남은 불일치:

```text
커피를 만들어줘
expected object = null
actual object = coffee
```

이 결과는 명백한 의미 오류가 아니라 `unknown` 명령에서 추출한 entity를 보존할 것인지에 대한 정책 차이였다.

최종 정책:

```text
unknown에서도 추출 가능한 entity는 보존 가능
모든 실행 flag는 false
실제 실행은 차단
```

예상값을 정책에 맞게 조정한 최종 결과:

```text
Exact-match PASS: 6
Exact-match FAIL: 0
Exact-match pass rate: 100.0%
```

---

## 18. Structured Outputs의 한계

Structured Outputs 적용 후 모든 결과가 schema와 자료형을 따랐다.

그러나 다음과 같은 의미 문제는 여전히 발생할 수 있었다.

```text
공간 관계 누락
공간 관계를 잘못된 필드에 저장
target과 object 역할 혼동
사용자에게 없는 constraint 추가
```

즉, 다음 두 항목은 다르다.

```text
Schema Validation
→ JSON 구조와 타입이 올바른가

Semantic Validation
→ 필드 값과 필드 사이 관계가 올바른가
```

이를 해결하기 위해 Semantic Validator를 구현했다.

---

## 19. Semantic Validator 구조

파일:

```text
src/mission_parser/mission_parser/semantic_validator.py
```

결과 구조:

```python
class SemanticValidationResult(BaseModel):
    is_valid: bool
    errors: list[str]
    warnings: list[str]
```

Validator는 잘못된 값을 자동 수정하지 않는다.

```text
Mission command 입력
→ 규칙 검사
→ errors / warnings 반환
→ is_valid 결정
```

자동 수정을 하지 않은 이유:

```text
LLM 원본 출력과 오류 원인을 유지
잘못된 자동 보정으로 인한 의도 변경 방지
실행 계층에 전달하기 전 명확하게 차단
```

---

## 20. Validator 공통 규칙

필수 필드:

```text
intent
target
object
constraints
requires_navigation
requires_vision
requires_manipulation
```

문자열 형식:

```text
lowercase_snake_case
```

허용한 공간 관계:

```text
front
behind
left
right
near
```

허용한 constraint:

```text
front
behind
left
right
near
stop_after_arrival
```

검사 항목:

```text
필수 필드 누락
target 문자열 형식
object 문자열 형식
constraint 문자열 형식
constraint 중복
지원하지 않는 constraint
방향 표현을 target으로 사용
front_of_desk 형태의 결합 target
```

---

## 21. Intent별 Validator 규칙

### move_to

```text
target 필수
object는 null
requires_navigation은 true
requires_manipulation은 false
```

### inspect_object

```text
object 필수
requires_vision은 true
requires_manipulation은 false
```

### stop

```text
target은 null
object는 null
constraints는 빈 배열
requires_navigation은 false
requires_vision은 false
requires_manipulation은 false
```

### unknown

```text
requires_navigation은 false
requires_vision은 false
requires_manipulation은 false
추출한 target, object, constraints는 보존 가능
```

`unknown`에 추출 정보가 남아 있고 모든 실행 flag가 `false`라면 경고를 반환한다.

```text
[UNKNOWN_ENTITY_PRESERVED]
```

---

## 22. Semantic Validator 독립 테스트

테스트한 6개 항목:

```text
정상 move_to
target이 없는 잘못된 move_to
direction이 target으로 들어간 inspect_object
navigation flag가 true인 잘못된 stop
object가 보존된 안전한 unknown
manipulation flag가 true인 잘못된 unknown
```

실행:

```bash
ros2 run mission_parser semantic_validator_test
```

결과:

```text
PASS: 6
FAIL: 0
TOTAL: 6
```

탐지된 대표 오류:

```text
[MOVE_TO_TARGET_REQUIRED]
[TARGET_SPATIAL_RELATION_INVALID]
[STOP_NAVIGATION_MUST_BE_FALSE]
[UNKNOWN_MANIPULATION_MUST_BE_FALSE]
```

---

## 23. 실행 허용 정책

Semantic Validation과 실제 실행 허용 여부를 분리했다.

```python
def is_execution_allowed(
    command: dict[str, Any],
    validation_is_valid: bool,
) -> bool:
    if not validation_is_valid:
        return False

    if command["intent"] == "unknown":
        return False

    return True
```

의미:

```text
Validation 실패
→ 실행 불가

unknown
→ 구조가 유효해도 실행 불가

유효한 move_to, inspect_object, stop
→ 다음 실행 계층으로 전달 가능
```

---

## 24. LLM과 Validator 통합 테스트

실행:

```bash
ros2 run mission_parser llm_mission_parser
```

최종 결과:

```text
Exact-match PASS: 6
Exact-match FAIL: 0
TOTAL: 6
Exact-match pass rate: 100.0%
Semantic Validation PASS: 6/6
Execution Allowed: 5/6
```

`Execution Allowed`가 5/6인 이유:

```text
커피를 만들어줘
→ intent = unknown
→ Semantic Validation = True
→ Execution Allowed = False
```

이는 실패가 아니라 의도한 실행 차단 결과다.

---

## 25. ROS2 Mission Parser Node

파일:

```text
src/mission_parser/mission_parser/mission_parser_node.py
```

Node 이름:

```text
mission_parser_node
```

구독 topic:

```text
/missionbot/user_command
```

발행 topic:

```text
/missionbot/mission_command
```

message type:

```text
std_msgs/msg/String
```

callback 처리 흐름:

```text
String message 수신
→ 빈 명령 확인
→ LLM Mission Parser 호출
→ MissionCommand model_dump
→ Semantic Validation
→ warning 출력
→ Validation 실패 차단
→ Execution Allowed 확인
→ unknown 차단
→ JSON String message 발행
```

---

## 26. package.xml 변경

자연어 명령과 JSON 결과를 String topic으로 전달하기 위해 다음 의존성을 추가했다.

```xml
<depend>std_msgs</depend>
```

기존 ROS2 Python Node 의존성:

```xml
<depend>rclpy</depend>
```

---

## 27. setup.py 실행 파일

최종 `console_scripts`:

```python
entry_points={
    "console_scripts": [
        "openai_connection_test = "
        "mission_parser.openai_connection_test:main",

        "llm_mission_parser = "
        "mission_parser.llm_mission_parser:main",

        "semantic_validator_test = "
        "mission_parser.semantic_validator_test:main",

        "mission_parser_node = "
        "mission_parser.mission_parser_node:main",
    ],
},
```

확인:

```bash
ros2 pkg executables mission_parser
```

결과:

```text
mission_parser llm_mission_parser
mission_parser mission_parser_node
mission_parser openai_connection_test
mission_parser semantic_validator_test
```

---

## 28. ROS2 Node 실행

터미널 1:

```bash
cd ~/projects/missionbot-ros2
source install/setup.bash

ros2 run mission_parser mission_parser_node
```

시작 로그:

```text
Mission Parser Node가 시작되었습니다.
명령 수신 topic: /missionbot/user_command
결과 발행 topic: /missionbot/mission_command
```

터미널 2:

```bash
cd ~/projects/missionbot-ros2
source install/setup.bash

ros2 topic echo /missionbot/mission_command
```

터미널 3:

```bash
cd ~/projects/missionbot-ros2
source install/setup.bash

ros2 topic pub --once \
/missionbot/user_command \
std_msgs/msg/String \
"{data: '책상 앞으로 이동해줘'}"
```

---

## 29. 정상 명령 topic 결과

입력:

```text
책상 앞으로 이동해줘
```

Node 로그:

```text
사용자 명령 수신: 책상 앞으로 이동해줘
검증된 Mission command 발행:
{"intent": "move_to", "target": "desk", ...}
```

출력 topic:

```text
/missionbot/mission_command
```

출력 JSON:

```json
{
  "intent": "move_to",
  "target": "desk",
  "object": null,
  "constraints": [
    "front"
  ],
  "requires_navigation": true,
  "requires_vision": false,
  "requires_manipulation": false
}
```

---

## 30. Unknown 명령 차단 결과

입력:

```text
커피를 만들어줘
```

LLM 결과:

```json
{
  "intent": "unknown",
  "target": null,
  "object": "coffee",
  "constraints": [],
  "requires_navigation": false,
  "requires_vision": false,
  "requires_manipulation": false
}
```

Node 로그:

```text
[UNKNOWN_ENTITY_PRESERVED]
unknown 명령에 추출된 정보가 남아 있지만
모든 실행 flag가 false이므로 실행은 차단됩니다.

Mission command는 의미적으로 유효하지만
MissionBot의 실행 지원 범위 밖이므로
발행하지 않았습니다.
```

`/missionbot/mission_command`에는 새로운 메시지가 발행되지 않았다.

---

## 31. Phase 10 발생 이슈

### 31.1 Python pip 미설치

오류:

```text
/usr/bin/python3: No module named pip
```

해결:

```bash
sudo apt install -y python3-pip
```

### 31.2 mission_parser package 미인식

오류:

```text
Package 'mission_parser' not found
```

해결 흐름:

```text
ament_python 구조 확인
setup.py console_scripts 확인
colcon build
source install/setup.bash
```

### 31.3 `.env` 탐색 경로 오류

잘못된 경로:

```text
install/mission_parser/lib/.env
```

해결:

```python
project_root = Path.cwd()
env_path = project_root / ".env"
```

### 31.4 공간 관계 의미 오류

문제:

```text
front 누락
left를 target으로 사용
```

해결:

```text
공간 관계 prompt 규칙 보완
few-shot 예시 추가
Semantic Validator 구현
```

### 31.5 Unknown entity 정책

문제:

```text
커피를 만들어줘
→ object = coffee
```

판단:

```text
unknown이어도 추출한 entity는 보존 가능
모든 실행 flag를 false로 유지
실제 실행은 차단
```

---

## 32. 보안 기준

```text
API key를 코드에 직접 작성하지 않는다.
API key를 출력하지 않는다.
.env를 Git에 commit하지 않는다.
문서에 실제 API key를 기록하지 않는다.
```

확인:

```bash
git status
```

`.env`가 Git 변경 목록에 나타나지 않아야 한다.

---

## 33. Phase 10에서 배운 핵심 개념

### LLM Mission Parser

```text
자연어 명령을 로봇 실행 모듈이 이해할 수 있는
구조화된 Mission command로 바꾸는 모듈
```

### Structured Outputs

```text
LLM 출력의 필드와 자료형을 schema로 고정
```

### Semantic Validation

```text
schema를 통과한 필드들이 MissionBot 의미 규칙에도 맞는지 검사
```

### Execution Policy

```text
유효한 명령인지와 실행 가능한 명령인지 분리
```

### ROS2 Interface

```text
자연어와 검증된 Mission command를 topic으로 연결
```

---

## 34. Phase 10의 한계

현재 Mission Parser는 제한된 intent와 prompt 규칙을 사용한다.

```text
지원 intent:
move_to
inspect_object
stop
unknown
```

아직 실제 지도 landmark와 연결하지 않았다.

```text
target = desk
→ 실제 map coordinate로 변환되지 않음
```

아직 영상 속 물체와 연결하지 않았다.

```text
object = red_cup
→ 실제 카메라 이미지의 물체 선택으로 연결되지 않음
```

아직 실제 로봇 명령으로 연결하지 않았다.

```text
requires_navigation = true
→ Navigation2 goal 자동 전송 안 함

requires_manipulation = true
→ MoveIt2 trajectory 자동 실행 안 함
```

테스트 세트도 6개 명령으로 제한되어 있다.

---

## 35. 추후 확장 방향

Mission Router:

```text
MissionCommand
→ intent와 requires_* 확인
→ 적절한 실행 모듈로 전달
```

Navigation target resolver:

```text
target = desk
→ landmark database
→ map coordinate
→ Navigation2 goal
```

VLM 또는 Object Selector:

```text
카메라 이미지
+ object = red_cup
+ constraints = left
→ 실제 장면의 대상 물체 선택
```

Manipulation task interface:

```text
검증된 manipulation command
→ MoveIt2 planning request
```

단, 이 항목들은 Phase 10 구현 범위에 포함하지 않는다.

---

## 36. Phase 10 완료 판정

```text
[x] mission_parser 패키지 생성
[x] OpenAI API 연결
[x] .env 기반 API key 관리
[x] 최소 LLM Mission Parser 구현
[x] 영어 표준 Mission command 출력
[x] Structured Outputs 적용
[x] Pydantic MissionCommand schema 정의
[x] 다중 자연어 명령 테스트
[x] 공간 관계 의미 규칙 보완
[x] unknown entity 정책 확정
[x] Semantic Validator 구현
[x] Validator 독립 테스트 6/6
[x] LLM 통합 Exact-match 6/6
[x] Semantic Validation 6/6
[x] unknown 명령 실행 차단
[x] mission_parser_node 구현
[x] /missionbot/user_command 구독
[x] /missionbot/mission_command 발행
[x] 지원 범위 밖 명령 topic 발행 차단
[x] README Result 작성
[x] experiment_log 작성
[x] troubleshooting 작성
[x] phase summary 작성
[x] Phase 10 문서 작성
```

완료 의미:

```text
MissionBot-ROS2는 한국어 자연어 명령을 LLM으로 해석하고,
구조화된 Mission command로 변환한 뒤,
Python 기반 의미 검증과 실행 허용 판단을 거쳐,
검증된 명령만 ROS2 topic으로 전달할 수 있게 되었다.
```