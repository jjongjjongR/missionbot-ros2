# MissionBot-ROS2 Phase 10 인수인계 문서

> 목적: 이 문서는 MissionBot-ROS2 프로젝트의 Phase 10. LLM/VLM Extension 완료 상태를 정리하고, 다른 채팅창에서 현재 상태를 정확히 복원해 다음 확장 작업을 이어가기 위한 인수인계 문서다.
> 이 문서와 `MBROS2_Phase10_prompt.md`만 있으면 Phase 10 완료 상태, 구현 구조, 테스트 결과, 주요 판단과 다음 시작 지점을 복원할 수 있다.

---

## 1. 프로젝트 정체성

MissionBot-ROS2는 UNICON Lab 준비를 위한 ROS2 기반 모바일 매니퓰레이션 준비 프로젝트다.

처음부터 완전한 모바일 매니퓰레이터나 대형 VLA 시스템을 구현하는 프로젝트가 아니다.

ROS2와 Gazebo 기반 이동로봇 시스템부터 시작해 센서, 좌표계, 지도 작성, 자율주행, 로그 분석, 실패 분석, 제어, 로봇팔 조작, 자연어 기반 미션 이해를 단계적으로 직접 구현하고 이해하는 프로젝트다.

현재까지의 핵심 흐름은 다음과 같다.

```text
ROS2 기본 구조
→ Gazebo + TurtleBot3
→ RViz2 + TF2
→ SLAM Toolbox
→ Navigation2
→ rosbag2 logging
→ Failure Analysis
→ Control Basics
→ MoveIt2 Basics
→ LLM Mission Understanding
```

Phase 10 완료 의미:

```text
사람의 자연어 명령
→ LLM 기반 의미 해석
→ 구조화된 Mission command
→ 의미 및 실행 안전성 검증
→ 검증된 명령만 ROS2 topic으로 전달
```

---

## 2. 현재 Phase 상태

```text
[x] Phase 0. Project setup
[x] Phase 0.5. Environment setup
[x] Phase 1. ROS2 basics
[x] Phase 2. Gazebo + TurtleBot3
[x] Phase 3. RViz2 + TF2
[x] Phase 4. SLAM
[x] Phase 5. Navigation2
[x] Phase 6. rosbag2 logging
[x] Phase 7. Failure Analysis
[x] Phase 8. Control basics
[x] Phase 9. MoveIt2 Basics
[x] Phase 10. LLM/VLM Extension
```

Phase 10의 실제 구현 범위는 LLM Mission Parser까지다.

Phase 이름에는 LLM/VLM Extension이 포함되어 있지만, 이번 Phase에서는 실제 VLM 이미지 입력이나 객체 grounding을 구현하지 않았다.

---

## 3. 최종 확정 환경

```text
Development Client:
MacBook

Remote Network:
Tailscale

Remote GUI:
NoMachine

Code Editing:
Antigravity IDE
VS Code Remote SSH 가능

Host:
Windows Desktop

Virtualization:
VMware Workstation 17

Guest OS:
Ubuntu 22.04 LTS

ROS2:
Humble Hawksbill

Python:
3.10

Simulator:
Gazebo Classic 11.10.2

Mobile Robot:
TurtleBot3 Burger

Visualization:
RViz2

SLAM:
slam_toolbox

Navigation:
Navigation2

Logging:
rosbag2

Manipulation:
MoveIt2
Panda demo robot arm
ros2_control

LLM API:
OpenAI Responses API

Final Mission Parser Model:
gpt-4o-mini

Structured Output:
Pydantic BaseModel

MissionBot Project:
~/projects/missionbot-ros2

TurtleBot3 Workspace:
~/turtlebot3_ws
```

---

## 4. 프로젝트 구조 원칙

이 프로젝트는 별도의 `missionbot_ws/src` 구조를 사용하지 않는다.

ROS2 패키지는 프로젝트 루트 바로 아래의 `src/`에 작성한다.

```text
~/projects/missionbot-ros2/src/
```

주의:

```text
missionbot_ws/src를 새로 만들지 않는다.
기존 Phase 구조를 임의로 바꾸지 않는다.
폴더 이름과 문서 위치를 새로 정의하지 않는다.
```

Phase 10에서 추가한 ROS2 패키지:

```text
src/mission_parser/
```

---

## 5. Phase 10 최종 패키지 구조

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

각 파일 역할:

```text
openai_connection_test.py
→ .env에서 API key 로드
→ OpenAI Responses API 연결 확인

llm_mission_parser.py
→ 자연어 명령을 MissionCommand로 변환
→ Structured Outputs 적용
→ 6개 명령 자동 테스트
→ Exact-match 및 Validator 통합 테스트

semantic_validator.py
→ MissionCommand 필드 간 의미 규칙 검사
→ errors와 warnings 생성
→ 실행 허용 여부 판단

semantic_validator_test.py
→ 정상 및 비정상 MissionCommand 독립 테스트

mission_parser_node.py
→ 자연어 ROS2 topic 구독
→ LLM Parser와 Validator 실행
→ 검증된 MissionCommand JSON topic 발행
```

---

## 6. API key 관리

OpenAI API key는 프로젝트 루트의 `.env`에서 관리한다.

```text
~/projects/missionbot-ros2/.env
```

파일 형식:

```text
OPENAI_API_KEY=본인_API_KEY
```

실제 API key 값은 다음 위치에 절대 포함하지 않는다.

```text
Python 코드
Git repository
README
experiment_log
troubleshooting
handoff
prompt
터미널 출력 캡처
```

`.gitignore` 기준:

```gitignore
.env
.env.*
*.pem
*.key
```

현재 코드는 프로젝트 루트에서 실행한다는 전제로 다음 방식으로 `.env`를 찾는다.

```python
project_root = Path.cwd()
env_path = project_root / ".env"
```

따라서 실행 전 위치를 맞춘다.

```bash
cd ~/projects/missionbot-ros2
source install/setup.bash
```

---

## 7. Phase 10 세부 단계 완료 상태

```text
[x] 10-1. OpenAI API 연결
[x] 10-2. 최소 LLM Mission Parser 구현
[x] 10-3. Structured Outputs 적용
[x] 10-4. 다중 자연어 명령 테스트
[x] 10-4. Semantic Validator 구현
[x] 10-5. ROS2 Mission Parser Node 구현
[x] 10-6. 문서화
```

---

## 8. OpenAI API 연결 결과

ROS2 실행 파일:

```text
openai_connection_test
```

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

초기 연결 테스트에서는 `gpt-4.1-mini`를 사용했다.

최종 Mission Parser는 제한된 명령 분류와 구조화 작업에 맞춰 `gpt-4o-mini`를 사용했다.

---

## 9. MissionCommand 최종 schema

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

대표 JSON:

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

## 10. MissionCommand 필드 의미

### intent

```text
move_to
→ 장소 또는 landmark 이동

inspect_object
→ 물체 찾기 또는 확인

stop
→ 즉시 정지

unknown
→ 현재 MissionBot 지원 범위 밖
```

### target

이동 목적지나 landmark를 표현한다.

```text
desk
shelf
door
charging_station
```

다음 값은 target으로 사용하지 않는다.

```text
left
right
front
behind
front_of_desk
```

### object

사용자가 찾거나 확인하려는 물체다.

```text
cup
red_cup
bottle
```

이동 landmark로 사용된 책상이나 선반은 object로 저장하지 않는다.

### constraints

사용자가 명시한 공간 관계나 추가 조건이다.

```text
front
behind
left
right
near
stop_after_arrival
```

### requires_navigation

이동로봇 이동 기능 필요 여부다.

### requires_vision

카메라나 물체 인식 기능 필요 여부다.

### requires_manipulation

로봇팔 조작 기능 필요 여부다.

Phase 10의 지원 intent에는 실제 manipulation 명령이 포함되지 않았기 때문에 현재 테스트에서는 `false`로 사용했다.

---

## 11. 문자열 정규화 정책

사용자 입력은 한국어 또는 영어로 받을 수 있다.

MissionCommand 내부의 문자열 값은 영어 `lowercase_snake_case`로 정규화한다.

```text
책상 → desk
선반 → shelf
컵 → cup
빨간 컵 → red_cup
앞 → front
왼쪽 → left
도착 후 정지 → stop_after_arrival
```

이 규칙을 사용한 이유:

```text
한국어와 영어 표현 혼합 방지
띄어쓰기 차이 방지
대소문자 차이 방지
ROS2 실행 모듈에서 단순 문자열 비교 가능
```

---

## 12. Structured Outputs 적용

초기 구현은 다음 방식이었다.

```text
LLM 자유 문자열
→ JSON code block 제거
→ json.loads()
→ Python dictionary
```

이 방식에는 다음 문제가 있었다.

```text
JSON 밖 설명 생성 가능
필드 누락 가능
타입 불일치 가능
지원하지 않는 intent 생성 가능
```

최종 구현에서는 Pydantic `MissionCommand`와 OpenAI Structured Outputs를 사용했다.

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

---

## 13. Pydantic Field 설명 추가

Structured Outputs를 적용했지만 초기 결과는 다음과 같이 의미적으로 잘못되었다.

입력:

```text
책상 앞으로 이동해줘
```

초기 결과:

```json
{
  "intent": "move_to",
  "target": "front_of_desk",
  "object": "desk",
  "constraints": [
    "stop_after_arrival"
  ],
  "requires_navigation": true,
  "requires_vision": false,
  "requires_manipulation": false
}
```

문제:

```text
공간 관계와 landmark가 target에 결합됨
이동 landmark가 object에도 중복 저장됨
사용자가 말하지 않은 stop_after_arrival이 추가됨
사용자가 말한 front가 올바르게 분리되지 않음
```

이를 보완하기 위해 Pydantic 필드에 `Field(description=...)`을 추가했다.

핵심 기준:

```text
target
→ 이동 목적지 또는 landmark
→ 공간 관계를 포함하지 않음

object
→ 사용자가 찾거나 확인하려는 물체
→ 이동 landmark는 포함하지 않음

constraints
→ 사용자가 명시한 공간 관계와 행동 조건만 저장
→ 말하지 않은 조건을 임의로 생성하지 않음
```

---

## 14. Prompt 의미 규칙 보완

Prompt에 다음 규칙을 명시했다.

```text
front, behind, left, right, near는 공간 관계다.
공간 관계는 target이 아니라 constraints에 저장한다.
방향 표현만으로 target을 생성하지 않는다.
사용자가 명시한 공간 관계는 생략하지 않는다.
사용자가 말하지 않은 constraint를 추가하지 않는다.
```

한국어 표현 예:

```text
"X 앞까지"
→ target = X
→ constraints에 front 추가

"왼쪽에 있는 X"
→ object = X
→ target = null
→ constraints에 left 추가
```

특히 실패했던 문장을 few-shot 예시로 추가했다.

```text
선반 앞까지 가서 멈춰
왼쪽에 있는 컵을 확인해줘
```

---

## 15. 다중 명령 테스트

최종 테스트 세트:

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

초기 Exact-match 결과:

```text
PASS: 4
FAIL: 2
TOTAL: 6
Exact-match pass rate: 66.7%
```

초기 실패:

```text
"선반 앞까지"에서 front 누락
"왼쪽에 있는 컵"에서 left를 target으로 사용
```

Prompt 보완 후:

```text
PASS: 5
FAIL: 1
TOTAL: 6
Exact-match pass rate: 83.3%
```

남은 불일치:

```text
커피를 만들어줘

actual:
object = coffee

initial expected:
object = null
```

---

## 16. Unknown entity 보존 정책

`"커피를 만들어줘"` 결과의 `object="coffee"`는 반드시 잘못된 값이라고 보기 어려웠다.

최종 정책:

```text
unknown이어도 명령에서 추출 가능한 entity는 보존할 수 있다.
모든 실행 flag는 false여야 한다.
unknown 명령은 실행 계층으로 전달하지 않는다.
```

최종 expected:

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

중요한 기준:

```text
유효한 MissionCommand
≠
실행 가능한 MissionCommand
```

---

## 17. Semantic Validator 구현 이유

Structured Outputs는 다음을 보장한다.

```text
필드 존재
필드 타입
intent enum
constraints 배열
boolean 형식
```

하지만 다음 의미 규칙은 자동으로 보장하지 않는다.

```text
move_to에 target이 존재하는가
방향이 target에 잘못 들어갔는가
inspect_object에 object가 존재하는가
unknown인데 실행 flag가 true인가
stop인데 새로운 실행 모듈을 요청하는가
```

Prompt 규칙만 계속 늘리면 특정 테스트 문장에 과적합할 수 있기 때문에 Python 기반 Semantic Validator를 구현했다.

---

## 18. Semantic Validator 반환 구조

```python
class SemanticValidationResult(BaseModel):
    is_valid: bool
    errors: list[str]
    warnings: list[str]
```

Validator는 LLM 결과를 자동으로 고치지 않는다.

```text
MissionCommand 입력
→ 의미 규칙 검사
→ errors와 warnings 반환
→ 실행 가능 여부 판단
```

자동 수정하지 않은 이유:

```text
원본 LLM 출력 보존
오류 원인 확인 가능
잘못된 보정으로 사용자 의도 변경 방지
실행 전 명시적 차단
```

---

## 19. Validator 주요 규칙

### 공통

```text
필수 필드 존재 여부
lowercase_snake_case 형식
지원하지 않는 constraint
constraint 중복
방향 표현의 target 사용
front_of_desk 같은 결합 target
```

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
모든 requires_* 값은 false
```

### unknown

```text
모든 requires_* 값은 false
추출된 entity는 보존 가능
실제 실행은 차단
```

---

## 20. Validator 독립 테스트

실행:

```bash
cd ~/projects/missionbot-ros2
source install/setup.bash

ros2 run mission_parser semantic_validator_test
```

테스트 항목:

```text
정상 move_to
target이 없는 move_to
direction을 target으로 사용한 inspect_object
navigation이 true인 stop
entity를 보존한 안전한 unknown
manipulation이 true인 위험한 unknown
```

결과:

```text
최종 Semantic Validator 테스트 결과
PASS: 6
FAIL: 0
TOTAL: 6
```

대표 탐지 오류:

```text
[MOVE_TO_TARGET_REQUIRED]
[TARGET_SPATIAL_RELATION_INVALID]
[STOP_NAVIGATION_MUST_BE_FALSE]
[UNKNOWN_MANIPULATION_MUST_BE_FALSE]
```

---

## 21. Validation과 Execution Allowed 분리

두 개념을 분리했다.

```text
Semantic Validation
→ MissionCommand 필드가 프로젝트 의미 규칙에 맞는가

Execution Allowed
→ 실제 실행 계층으로 전달할 수 있는가
```

실행 허용 규칙:

```python
if not validation_is_valid:
    return False

if command["intent"] == "unknown":
    return False

return True
```

예:

```text
커피를 만들어줘
→ intent = unknown
→ Semantic Validation = True
→ Execution Allowed = False
```

---

## 22. LLM과 Validator 통합 테스트

실행:

```bash
cd ~/projects/missionbot-ros2
source install/setup.bash

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

`Execution Allowed`가 5/6인 것은 의도한 결과다.

```text
커피를 만들어줘
→ 지원 범위 밖의 unknown
→ topic 및 실행 전달 차단
```

---

## 23. ROS2 Mission Parser Node

Node:

```text
mission_parser_node
```

입력 topic:

```text
/missionbot/user_command
```

message type:

```text
std_msgs/msg/String
```

출력 topic:

```text
/missionbot/mission_command
```

message type:

```text
std_msgs/msg/String
```

처리 흐름:

```text
/missionbot/user_command
→ mission_parser_node
→ OpenAI LLM Mission Parser
→ Pydantic MissionCommand
→ Semantic Validator
→ Execution Allowed
→ /missionbot/mission_command
```

---

## 24. ROS2 Node 실행 방법

터미널 1:

```bash
cd ~/projects/missionbot-ros2
source install/setup.bash

ros2 run mission_parser mission_parser_node
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

## 25. 정상 명령 ROS2 결과

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

출력:

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

## 26. Unknown 명령 ROS2 차단 결과

입력:

```text
커피를 만들어줘
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

확인 결과:

```text
/missionbot/mission_command에 새로운 메시지가 발행되지 않음
```

---

## 27. package.xml 및 setup.py

`package.xml` 주요 의존성:

```xml
<depend>rclpy</depend>
<depend>std_msgs</depend>
```

최종 ROS2 실행 파일:

```text
mission_parser openai_connection_test
mission_parser llm_mission_parser
mission_parser semantic_validator_test
mission_parser mission_parser_node
```

확인 명령:

```bash
ros2 pkg executables mission_parser
```

---

## 28. Phase 10 핵심 트러블슈팅

### 28.1 Structured Outputs 이후 의미 필드 불일치

증상:

```text
target = front_of_desk
object = desk
constraints = ["stop_after_arrival"]
```

원인:

```text
Schema는 타입을 제한하지만
target, object, constraints의 의미 차이를 충분히 설명하지 못함
```

해결:

```text
Pydantic Field description 추가
Prompt 필드 의미 규칙 추가
정상 및 비정상 예시 추가
```

### 28.2 Prompt만으로 의미 일관성 확보의 한계

증상:

```text
front 조건 누락
left를 target으로 배치
unknown entity 정책 불일치
```

판단:

```text
실패할 때마다 prompt와 예시를 계속 추가하면
특정 테스트 문장에 과적합할 수 있음
```

해결:

```text
자연어 의미 해석
→ Prompt

필드와 타입 고정
→ Structured Outputs

프로젝트 의미 규칙과 안전 검사
→ Python Semantic Validator
```

### 28.3 Unknown entity 정책

증상:

```text
커피를 만들어줘
→ object = coffee
```

최종 판단:

```text
모델 오류가 아니라 정책 미정 문제
unknown에서도 entity 보존 가능
모든 실행 flag는 false
실제 실행 및 topic 발행은 차단
```

---

## 29. Phase 10 기록 파일

```text
README.md
notes/experiment_log.md
notes/troubleshooting.md
notes/phase_summaries/phase10_llm_vlm_extension_summary.md
docs/phases/phase10_llm_vlm_extension.md
docs/handoffs/MBROS2_Phase10_Handoff.md
docs/prompt/MBROS2_Phase10_prompt.md
```

Experiment log:

```text
P10-EXP-0001_openai_api_connection_test
P10-EXP-0002_llm_mission_parser_minimal
P10-EXP-0003_structured_outputs_multi_command_test
P10-EXP-0004_semantic_validator_test
P10-EXP-0005_llm_parser_validator_integration
P10-EXP-0006_ros2_mission_parser_node
```

Troubleshooting 핵심 항목:

```text
TS-0003_structured_output_semantic_field_mismatch
TS-0004_prompt_only_semantic_consistency_limit
```

---

## 30. 코드 작성 규칙

사용자는 코드를 직접 Antigravity에서 타이핑하며 학습한다.

코드를 제공할 때는 변경 내용을 생략하지 말고 직접 입력할 수 있도록 제공한다.

새 코드와 수정 코드는 다음 형식의 한국어 주석을 사용한다.

```python
# 2026-06-12 신규 : 이 코드가 새로 추가된 이유와 역할을 설명함.
```

```python
# 2026-06-12 수정 : 기존 코드에서 무엇을 변경했고 왜 변경했는지 설명함.
```

함수와 주요 처리 단계에는 세부 주석을 작성한다.

예:

```python
# 2026-06-12 신규 : 프로젝트 루트의 .env 파일에서 OpenAI API key를 읽어오는 함수를 정의함.
def load_api_key() -> str | None:
```

코드를 한 번에 과도하게 확장하지 않는다.

```text
개념 설명
→ 작은 코드 작성
→ 사용자가 직접 실행
→ 결과 확인
→ 다음 단계
```

---

## 31. 프로젝트 진행 원칙

반드시 지킬 것:

```text
기존 Phase와 폴더 구조를 임의로 변경하지 않는다.
missionbot_ws/src를 만들지 않는다.
src/ 아래에 ROS2 패키지를 둔다.
사용자가 직접 코드를 타이핑한다.
개념을 설명한 뒤 프로젝트에 적용한다.
결과를 확인하기 전에 다음 구현으로 넘어가지 않는다.
앞서 나가서 대형 Agent나 VLA를 구현하지 않는다.
```

사용자가 요청하지 않은 다음 기능을 임의로 추가하지 않는다.

---

## 32. Phase 10에서 구현하지 않은 것

```text
실제 VLM 이미지 입력
YOLO object detection
Vision-language grounding
카메라 기반 object selector
Navigation2 goal 자동 전송
landmark를 map coordinate로 변환
MoveIt2 자동 실행
manipulation intent
복합 task planning
Mission Router
LangGraph Agent
VLA policy
실제 모바일 매니퓰레이션 전체 통합
```

---

## 33. 현재 기술적 한계

### 제한된 intent

```text
move_to
inspect_object
stop
unknown
```

### 제한된 테스트 세트

```text
6개 자연어 명령
```

### 실제 landmark 미연결

```text
target = desk
→ 실제 map 좌표로 변환되지 않음
```

### 실제 영상 미연결

```text
object = red_cup
→ 실제 카메라 영상의 물체와 연결되지 않음
```

### 실행 모듈 미연결

```text
requires_navigation = true
→ Navigation2 goal을 자동 전송하지 않음

requires_manipulation = true
→ MoveIt2 계획이나 trajectory를 자동 실행하지 않음
```

---

## 34. 다음 확장 후보

다음 구현 후보는 README에 이미 예정된 다음 모듈이다.

```text
src/vision_object_selector/
```

가능한 역할:

```text
MissionCommand의 object
+ constraints
+ 카메라 이미지 또는 탐지 결과
→ 실제 장면의 대상 객체 선택
```

예:

```text
object = red_cup
constraints = ["left"]
+ 카메라 장면
→ 왼쪽의 빨간 컵 선택
```

그러나 다음 채팅에서 바로 구현하지 않는다.

먼저 다음을 확정해야 한다.

```text
1. 다음 작업을 별도 Phase로 추가할지
2. Phase 10 후속 extension으로 진행할지
3. YOLO 기반 object selector로 시작할지
4. VLM 기반 object selector로 시작할지
5. 실제 카메라 대신 정적 이미지 테스트부터 시작할지
6. 입력과 출력 schema를 어떻게 정의할지
```

Phase 번호나 Phase map은 사용자의 확인 없이 추가하거나 변경하지 않는다.

---

## 35. 다음 채팅 시작 지점

다음 채팅에서는 아래 상태에서 시작한다.

```text
현재 MissionBot-ROS2는 Phase 10. LLM/VLM Extension을 완료했다.

완료한 것:
- mission_parser ament_python 패키지 생성
- OpenAI Responses API 연결
- 프로젝트 루트의 .env에서 API key 로드
- gpt-4o-mini 기반 LLM Mission Parser 구현
- 한국어 명령을 영어 MissionCommand로 정규화
- Pydantic MissionCommand schema 정의
- Structured Outputs 적용
- Field description을 통한 필드 의미 보완
- 공간 관계 prompt 규칙 추가
- 6개 자연어 명령 자동 테스트
- Exact-match 6/6
- Semantic Validator 구현
- Validator 독립 테스트 6/6
- Semantic Validation 6/6
- Execution Allowed 5/6
- unknown 명령 실행 차단
- mission_parser_node 구현
- /missionbot/user_command 구독
- /missionbot/mission_command 발행
- unknown 명령 topic 발행 차단
- README Result 작성
- experiment_log 작성
- troubleshooting 작성
- phase summary 작성
- Phase 10 extension 문서 작성
- Phase 10 handoff와 prompt 작성
```

주요 결과물:

```text
src/mission_parser/mission_parser/openai_connection_test.py
src/mission_parser/mission_parser/llm_mission_parser.py
src/mission_parser/mission_parser/semantic_validator.py
src/mission_parser/mission_parser/semantic_validator_test.py
src/mission_parser/mission_parser/mission_parser_node.py
docs/phases/phase10_llm_vlm_extension.md
notes/phase_summaries/phase10_llm_vlm_extension_summary.md
notes/experiment_log.md
notes/troubleshooting.md
docs/handoffs/MBROS2_Phase10_Handoff.md
docs/prompt/MBROS2_Phase10_prompt.md
```

다음 시작 작업:

```text
Phase 10 완료 상태와 문서 반영 여부 확인
→ 다음 확장 범위 결정
→ 사용자의 확인 후에만 다음 구현 시작
```

다음 확장 후보:

```text
vision_object_selector 설계
```

처음부터 VLA, LangGraph, 실제 로봇 자동 실행으로 넘어가지 않는다.

---

## 36. Phase 10 완료 판정

```text
[x] OpenAI API 연결
[x] API key 보안 관리
[x] 최소 LLM Mission Parser 구현
[x] 영어 표준 MissionCommand 출력
[x] Structured Outputs 적용
[x] Pydantic Field 의미 설명
[x] 공간 관계 prompt 보완
[x] 다중 명령 테스트
[x] Exact-match 6/6
[x] Semantic Validator 구현
[x] Validator 독립 테스트 6/6
[x] LLM + Validator 통합 검증
[x] unknown 실행 차단
[x] ROS2 Mission Parser Node 구현
[x] 자연어 topic 구독
[x] 검증된 JSON topic 발행
[x] 지원 범위 밖 명령 발행 차단
[x] Phase 10 문서화
```

최종 완료 의미:

```text
MissionBot-ROS2는 사용자의 한국어 자연어 명령을
OpenAI 기반 LLM으로 해석하고,
정해진 schema의 MissionCommand로 변환한 뒤,
Python Semantic Validator로 의미와 실행 안전성을 검사하고,
검증되고 지원되는 명령만 ROS2 topic으로 전달할 수 있게 되었다.
```