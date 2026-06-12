# Troubleshooting

이 문서는 MissionBot-ROS2 프로젝트를 진행하면서 발생한 오류와 해결 과정을 기록하는 문서입니다.

오류를 해결한 뒤에는 반드시 원인, 해결 방법, 배운 점을 함께 기록합니다.

---

## 기록 규칙

각 오류는 아래 형식으로 기록합니다.

- TS-{번호}_{오류요약}

예시:

- TS-0001_ros2_package_build_error
- TS-0002_turtlebot3_model_not_found
- TS-0003_gazebo_launch_failed

---

## TS-0001_example_error

### 1. 발생 날짜

- Date:

### 2. 발생 단계

- Phase:
- 작업 내용:

### 3. 오류 상황

오류 메시지:

    여기에 오류 메시지를 붙여넣기

### 4. 사용 환경

- OS:
- ROS2 version:
- Gazebo version:
- Python version:
- TurtleBot3 model:
- 기타:

### 5. 원인 추정

-

### 6. 해결 방법

사용한 명령어:

    여기에 해결에 사용한 명령어 작성

### 7. 해결 결과

-

### 8. 배운 점

-

### 9. 다시 발생하지 않도록 주의할 점

-


---

## TS-0003_missionbot_basic_package_not_found

### 1. 발생 날짜

- Date: 2026-05-25

### 2. 발생 단계

- Phase: Phase 1. ROS2 basics
- 작업 내용: missionbot_basic launch 파일 실행

### 3. 오류 상황

오류 메시지:

    Package 'missionbot_basic' not found: "package 'missionbot_basic' not found, searching: ['/home/user/turtlebot3_ws/install/turtlebot3_simulations', '/home/user/turtlebot3_ws/install/turtlebot3_manipulation_gazebo', '/home/user/turtlebot3_ws/install/turtlebot3_gazebo', '/home/user/turtlebot3_ws/install/turtlebot3_fake_node', '/opt/ros/humble']"

실행한 명령어:

    ros2 launch missionbot_basic turtlesim_pubsub.launch.py

### 4. 사용 환경

- OS: Ubuntu 22.04 LTS
- ROS2 version: Humble Hawksbill
- Gazebo version: Gazebo Classic 11.10.2
- Python version:
- TurtleBot3 model: burger
- Project path: ~/projects/missionbot-ros2

### 5. 원인 추정

현재 터미널에 MissionBot workspace의 `install/setup.bash`가 source되지 않았다.

에러 메시지의 searching 경로에는 다음만 포함되어 있었다.

- /home/user/turtlebot3_ws/install/...
- /opt/ros/humble

하지만 missionbot_basic 패키지는 다음 workspace에 있다.

- /home/user/projects/missionbot-ros2/install

따라서 ROS2가 현재 터미널 환경에서 missionbot_basic 패키지를 찾지 못했다.

### 6. 해결 방법

사용한 명령어:

    cd ~/projects/missionbot-ros2
    source install/setup.bash
    ros2 pkg list | grep missionbot_basic
    ros2 launch missionbot_basic turtlesim_pubsub.launch.py

### 7. 해결 결과

- `ros2 pkg list | grep missionbot_basic` 명령에서 missionbot_basic 패키지가 확인되었다.
- `ros2 launch missionbot_basic turtlesim_pubsub.launch.py` 명령이 정상 실행되었다.
- turtlesim_node, pose_subscriber, velocity_publisher가 launch 파일로 함께 실행되었다.

### 8. 배운 점

ROS2 기본 환경과 내가 만든 workspace 환경은 다르다.

`.bashrc`에서 자동으로 적용되는 것은 주로 다음 환경이다.

- /opt/ros/humble/setup.bash
- ~/turtlebot3_ws/install/setup.bash

하지만 MissionBot 프로젝트에서 직접 만든 패키지를 실행하려면 다음 설정을 현재 터미널에 추가로 적용해야 한다.

- ~/projects/missionbot-ros2/install/setup.bash

즉, colcon build 후에는 다음 명령을 실행해야 한다.

    source install/setup.bash

### 9. 다시 발생하지 않도록 주의할 점

- missionbot_basic 같은 직접 만든 패키지가 안 보이면 먼저 `ros2 pkg list | grep missionbot_basic`으로 확인한다.
- 패키지가 안 나오면 프로젝트 루트에서 `source install/setup.bash`를 실행한다.
- 그래도 안 나오면 `colcon build --packages-select missionbot_basic` 후 다시 source한다.
- `source ~/.bashrc`와 `source install/setup.bash`의 역할을 구분한다.

---

---

## TS-0003_gzclient_camera_assertion_failed

### 1. 발생 날짜

- Date: 2026-06-01

### 2. 발생 단계

- Phase: Phase 2. Gazebo + TurtleBot3 / Phase 3. RViz2 + TF2
- 작업 내용: TurtleBot3 Gazebo empty_world 실행

### 3. 오류 상황

TurtleBot3 Gazebo launch 실행 중 `gzclient` 프로세스가 종료되었다.

실행 명령:

```bash
ros2 launch turtlebot3_gazebo empty_world.launch.py
```

오류 메시지:

```text
[gzclient-2] libcurl: (6) Could not resolve host: fuel.ignitionrobotics.org
[gzclient-2] gzclient: /usr/include/boost/smart_ptr/shared_ptr.hpp:728:
typename boost::detail::sp_member_access<T>::type boost::shared_ptr<T>::operator->() const
[with T = gazebo::rendering::Camera;
typename boost::detail::sp_member_access<T>::type = gazebo::rendering::Camera*]:
Assertion `px != 0' failed.
[ERROR] [gzclient-2]: process has died
cmd 'gzclient --gui-client-plugin=libgazebo_ros_eol_gui.so'
```

동시에 확인된 정상 로그:

```text
Spawn status: SpawnEntity: Successfully spawned entity [burger]
[turtlebot3_diff_drive]: Subscribed to [/cmd_vel]
[turtlebot3_diff_drive]: Advertise odometry on [/odom]
[turtlebot3_diff_drive]: Publishing odom transforms between [odom] and [base_footprint]
```

### 4. 사용 환경

- OS: Ubuntu 22.04 LTS
- ROS2 version: Humble Hawksbill
- Gazebo version: Gazebo Classic 11.10.2
- TurtleBot3 model: burger
- Virtualization: VMware Workstation 17
- Remote GUI: NoMachine
- Development Client: MacBook

### 5. 원인 추정

이 오류는 TurtleBot3 spawn 실패가 아니라 Gazebo GUI 클라이언트인 `gzclient` 문제로 판단했다.

근거:

```text
1. TurtleBot3 Burger spawn은 성공했다.
2. gzserver는 계속 살아 있었다.
3. /cmd_vel, /odom, /scan, /tf, /tf_static topic이 정상적으로 생성되었다.
4. robot_state_publisher도 정상적으로 실행되었다.
5. odom → base_footprint transform도 발행되었다.
```

따라서 문제는 다음 쪽에 가깝다.

```text
Gazebo Classic GUI client
VMware 그래픽 렌더링
NoMachine GUI 환경
Gazebo GUI plugin
카메라 렌더링 관련 assertion
```

### 6. 확인 방법

Gazebo GUI가 죽어도 바로 실패로 판단하지 않고, 새 터미널에서 아래 topic을 확인한다.

```bash
ros2 topic list | grep -E "cmd_vel|odom|scan|tf"
```

정상 기준:

```text
/cmd_vel
/odom
/scan
/tf
/tf_static
```

위 topic이 살아 있다면 Gazebo 시뮬레이션 서버와 TurtleBot3 ROS2 데이터는 정상으로 판단한다.

### 7. 해결 또는 우회 방법

현재 프로젝트에서는 근본 해결보다는 우회 진행 방식을 사용한다.

우회 기준:

```text
1. TurtleBot3 spawn 성공 여부를 먼저 본다.
2. /cmd_vel, /odom, /scan, /tf, /tf_static topic 존재 여부를 확인한다.
3. topic이 살아 있으면 Gazebo GUI가 죽어도 Phase 진행 가능으로 판단한다.
4. Phase 3부터는 RViz2 중심으로 로봇 모델, TF, LaserScan을 확인한다.
```

필요 시 Gazebo GUI 재연결:

```bash
gzclient --verbose
```

추가 우회 후보:

```bash
QT_X11_NO_MITSHM=1 LIBGL_ALWAYS_SOFTWARE=1 gzclient --verbose
```

단, 현재까지는 RViz2 중심 진행으로 충분했다.

### 8. 해결 결과

Phase 3에서는 `gzclient` crash가 발생했지만 다음을 확인했다.

```text
[x] TurtleBot3 Burger spawn 성공
[x] /cmd_vel 생성
[x] /odom 생성
[x] /scan 생성
[x] /tf 생성
[x] /tf_static 생성
[x] RViz2 실행 성공
[x] TF display 성공
[x] RobotModel display 성공
[x] LaserScan display 연결 성공
[x] TF tree 확인 성공
[x] teleop 이동 중 transform 변화 확인 성공
```

따라서 `gzclient` crash는 Phase 진행을 막는 치명적 오류가 아니라, GUI 렌더링 관련 반복 이슈로 분리했다.

### 9. 배운 점

```text
Gazebo는 gzserver와 gzclient로 나뉜다.

gzserver
→ 실제 시뮬레이션 서버
→ 물리 계산, 센서, robot plugin, ROS2 topic 발행 담당

gzclient
→ 사람이 보는 Gazebo GUI
→ 창, 카메라, 모델 렌더링 담당
```

`gzclient`가 죽어도 `gzserver`가 살아 있으면 ROS2 topic은 정상적으로 발행될 수 있다.

### 10. 다시 발생하지 않도록 주의할 점

```text
1. gzclient crash만 보고 TurtleBot3 실행 실패로 판단하지 않는다.
2. 반드시 /cmd_vel, /odom, /scan, /tf, /tf_static topic을 확인한다.
3. RViz2 단계에서는 Gazebo GUI보다 ROS2 topic과 TF 상태를 우선한다.
4. VMware + NoMachine + Gazebo GUI 환경에서는 GUI crash가 반복될 수 있음을 전제로 진행한다.
5. 실제 시각화가 필요하면 RViz2를 우선 사용한다.
```

---

## TS-0003_structured_output_semantic_field_mismatch

### 1. 발생 날짜

* Date: 2026-06-12

### 2. 발생 단계

* Phase: Phase 10. LLM/VLM Extension
* 작업 내용: OpenAI Structured Outputs 기반 LLM Mission Parser 구현

### 3. 오류 상황

Pydantic `MissionCommand` schema와 OpenAI Structured Outputs를 적용한 뒤 다음 명령을 테스트했다.

```text
책상 앞으로 이동해줘
```

LLM은 schema의 모든 필드와 자료형을 지켰지만 다음과 같이 의미적으로 잘못된 결과를 반환했다.

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

예상한 결과는 다음과 같았다.

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

발견된 문제:

```text
target
front_of_desk
→ 목적지와 공간 관계가 하나의 문자열로 합쳐짐

object
desk
→ 이동 landmark가 물체 필드에도 중복 저장됨

constraints
stop_after_arrival
→ 사용자가 명시하지 않은 조건이 임의로 추가됨

constraints
front 누락
→ 사용자가 명시한 공간 관계가 보존되지 않음
```

### 4. 사용 환경

* OS: Ubuntu 22.04 LTS
* ROS2 version: Humble Hawksbill
* Python version: 3.10
* Package: `mission_parser`
* API: OpenAI Responses API
* Initial parser model: `gpt-4.1-mini`
* Final parser model: `gpt-4o-mini`
* Output schema: Pydantic `MissionCommand`

### 5. 원인 추정

Structured Outputs는 다음 항목을 제한할 수 있었다.

```text
필드 존재 여부
필드 자료형
intent 허용값
constraints 배열 형식
requires_* boolean 형식
```

하지만 schema만으로는 다음과 같은 필드의 의미를 충분히 제한하지 못했다.

```text
target과 object의 역할 차이
공간 관계를 target에 포함할지 constraints에 저장할지
사용자에게 없는 조건을 추가해도 되는지
```

기존 Pydantic 필드는 자료형만 정의되어 있었고, 각 필드가 MissionBot에서 어떤 의미를 가지는지에 대한 설명이 부족했다.

기존 형태:

```python
target: str | None
object: str | None
constraints: list[str]
```

이 구조는 문자열과 배열이라는 자료형은 제한하지만, `front_of_desk`나 `stop_after_arrival`이 의미적으로 올바른지는 판단하지 못했다.

### 6. 해결 방법

#### 6.1 Pydantic Field 설명 추가

`BaseModel`만 사용하던 코드를 수정해 `Field`를 추가했다.

```python
from pydantic import BaseModel, Field
```

각 필드에 MissionBot에서 사용하는 의미를 설명했다.

```python
target: str | None = Field(
    description=(
        "A navigation destination or spatial landmark. "
        "Use a simple canonical noun such as desk or shelf. "
        "Do not include spatial relations such as front_of_desk."
    )
)

object: str | None = Field(
    description=(
        "An object that the user explicitly wants to inspect or manipulate. "
        "Use null when a place or landmark is only a navigation destination."
    )
)

constraints: list[str] = Field(
    description=(
        "Only explicitly stated spatial or behavioral constraints. "
        "Examples: front, left, right, stop_after_arrival. "
        "Never infer constraints that the user did not state."
    )
)
```

#### 6.2 Prompt 필드 의미 규칙 강화

System prompt에 다음 규칙을 추가했다.

```text
target은 이동 목적지 또는 장소 landmark만 나타낸다.
target에는 방향이나 공간 관계를 합치지 않는다.

"책상 앞"은
target = desk
constraints = ["front"]
로 분리한다.

front_of_desk와 같은 결합 표현을 target으로 사용하지 않는다.

object는 사용자가 찾기, 확인하기, 집기 대상으로 명시한 물체만 나타낸다.

이동 목적지로 사용된 책상과 선반은 object에 넣지 않는다.

constraints에는 사용자가 명시한 조건만 넣는다.

사용자가 정지나 도착 후 정지를 말하지 않았다면
stop_after_arrival을 추가하지 않는다.
```

#### 6.3 올바른 출력과 잘못된 출력 예시 추가

Prompt에 다음과 같은 예시를 추가했다.

```text
입력:
책상 앞으로 이동해줘

올바른 출력:
target = desk
object = null
constraints = ["front"]

잘못된 출력:
target = front_of_desk
object = desk
constraints = ["stop_after_arrival"]
```

### 7. 해결 결과

수정 후 동일한 명령을 다시 실행했다.

```text
책상 앞으로 이동해줘
```

최종 결과:

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

다음 의미 분리가 정상적으로 이루어졌다.

```text
desk
→ 이동 목적지이므로 target

front
→ 공간 관계이므로 constraints

object
→ 찾거나 조작할 물체가 아니므로 null

stop_after_arrival
→ 사용자가 말하지 않았으므로 생성하지 않음
```

### 8. 배운 점

* Structured Outputs가 적용되었다고 해서 출력 의미까지 자동으로 올바른 것은 아니다.
* JSON schema는 필드와 자료형을 제한하지만, 필드 사이의 의미적 역할은 별도로 정의해야 한다.
* Pydantic `Field(description=...)`은 단순한 코드 설명이 아니라 모델이 각 필드의 의미를 이해하는 데 사용할 수 있다.
* `target`, `object`, `constraints`처럼 의미가 겹칠 수 있는 필드는 명시적인 규칙과 예시가 필요하다.
* 사용자가 말하지 않은 값을 생성하지 않는 규칙을 별도로 작성해야 한다.

### 9. 다시 발생하지 않도록 주의할 점

새로운 MissionCommand 필드를 추가할 때는 자료형만 정의하지 않는다.

```python
field_name: type
```

대신 다음을 함께 정의한다.

```text
필드가 의미하는 것
필드에 들어가면 안 되는 값
다른 필드와의 차이
정상 예시
잘못된 예시
```

Structured Outputs 결과를 확인할 때는 schema 통과 여부와 의미 정확성을 분리해서 평가한다.

```text
Schema Validation
→ 필드와 자료형이 맞는가

Semantic Validation
→ 각 값이 올바른 필드에 들어갔는가
```

---

## TS-0004_prompt_only_semantic_consistency_limit

### 1. 발생 날짜

* Date: 2026-06-12

### 2. 발생 단계

* Phase: Phase 10. LLM/VLM Extension
* 작업 내용: 다중 자연어 명령 테스트 및 Semantic Validation 설계

### 3. 오류 상황

Structured Outputs와 Pydantic `Field` 설명을 적용한 뒤 6개의 자연어 명령을 테스트했다.

```text
1. 책상 앞으로 이동해줘
2. 빨간 컵을 찾아줘
3. 선반 앞까지 가서 멈춰
4. 왼쪽에 있는 컵을 확인해줘
5. 멈춰
6. 커피를 만들어줘
```

첫 번째 다중 명령 테스트 결과:

```text
PASS: 4
FAIL: 2
TOTAL: 6
Exact-match pass rate: 66.7%
```

첫 번째 실패:

```text
입력:
선반 앞까지 가서 멈춰
```

실제 결과:

```json
{
  "intent": "move_to",
  "target": "shelf",
  "object": null,
  "constraints": [
    "stop_after_arrival"
  ],
  "requires_navigation": true,
  "requires_vision": false,
  "requires_manipulation": false
}
```

예상 결과:

```json
{
  "intent": "move_to",
  "target": "shelf",
  "object": null,
  "constraints": [
    "front",
    "stop_after_arrival"
  ],
  "requires_navigation": true,
  "requires_vision": false,
  "requires_manipulation": false
}
```

문제:

```text
"앞까지"에 포함된 front 공간 관계가 누락됨
```

두 번째 실패:

```text
입력:
왼쪽에 있는 컵을 확인해줘
```

실제 결과:

```json
{
  "intent": "inspect_object",
  "target": "left",
  "object": "cup",
  "constraints": [],
  "requires_navigation": false,
  "requires_vision": true,
  "requires_manipulation": false
}
```

예상 결과:

```json
{
  "intent": "inspect_object",
  "target": null,
  "object": "cup",
  "constraints": [
    "left"
  ],
  "requires_navigation": false,
  "requires_vision": true,
  "requires_manipulation": false
}
```

문제:

```text
left를 공간 관계가 아니라 target으로 사용함
```

공간 관계 prompt를 추가한 뒤 두 오류는 해결되었지만, 다음 테스트가 새롭게 불일치했다.

```text
입력:
커피를 만들어줘
```

실제 결과:

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

기존 예상 결과:

```json
{
  "intent": "unknown",
  "target": null,
  "object": null,
  "constraints": [],
  "requires_navigation": false,
  "requires_vision": false,
  "requires_manipulation": false
}
```

두 번째 테스트 결과:

```text
PASS: 5
FAIL: 1
TOTAL: 6
Exact-match pass rate: 83.3%
```

### 4. 사용 환경

* OS: Ubuntu 22.04 LTS
* ROS2 version: Humble Hawksbill
* Python version: 3.10
* Package: `mission_parser`
* Model: `gpt-4o-mini`
* Output: Pydantic Structured Outputs
* Test count: 6

### 5. 원인 추정

공간 관계 오류는 prompt에 규칙을 추가해 개선할 수 있었다.

하지만 다음 방식만 계속 반복하면 문제가 생길 수 있다고 판단했다.

```text
테스트 실패
→ prompt 규칙 추가
→ 예시 추가
→ 다시 테스트
→ 다른 표현에서 실패
→ prompt 규칙 추가
```

Prompt만 계속 늘리면 다음 문제가 발생할 수 있다.

```text
특정 테스트 문장에 과도하게 맞춰짐
prompt가 길어지고 복잡해짐
새로운 표현에서 다시 다른 오류 발생 가능
실행 안전 규칙이 확률적인 LLM 출력에 의존함
```

또한 `"object": "coffee"`는 반드시 잘못된 결과라고 보기 어려웠다.

```text
intent
→ 현재 MissionBot에서 지원하지 않으므로 unknown

object
→ 사용자가 언급한 대상인 coffee를 추출

실행 flag
→ 모두 false
```

따라서 이는 모델 오류라기보다 `unknown` 명령에서 추출된 정보를 보존할 것인지에 대한 정책이 정의되지 않은 문제였다.

### 6. 해결 방법

#### 6.1 공간 관계 prompt 규칙 보완

Prompt에 공간 관계 전용 규칙을 추가했다.

```text
front, behind, left, right, near는 장소나 물체가 아니라 공간 관계다.

공간 관계는 target에 넣지 않고 constraints에 넣는다.

"X 앞까지"는
target = X
constraints에 front 추가

"왼쪽에 있는 X"는
target = null
object = X
constraints에 left 추가

방향 표현만으로 target을 생성하지 않는다.
```

실패한 두 문장을 few-shot 예시로 추가했다.

#### 6.2 Unknown entity 보존 정책 확정

`unknown` 명령의 정책을 다음처럼 확정했다.

```text
unknown이어도 명령에서 추출 가능한 target, object, constraints는 보존할 수 있다.

단, 다음 실행 flag는 모두 false여야 한다.

requires_navigation = false
requires_vision = false
requires_manipulation = false

unknown 명령은 실제 실행 계층으로 전달하지 않는다.
```

따라서 `"커피를 만들어줘"`의 예상값을 다음처럼 수정했다.

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

#### 6.3 Python Semantic Validator 구현

Prompt만으로 실행 안전성을 보장하지 않고, Python 코드에서 Mission command를 다시 검사하도록 `semantic_validator.py`를 구현했다.

주요 검사 규칙:

```text
move_to
→ target 필수
→ object는 null
→ requires_navigation은 true

inspect_object
→ object 필수
→ requires_vision은 true

stop
→ target과 object는 null
→ constraints는 빈 배열
→ 모든 실행 flag는 false

unknown
→ 모든 실행 flag는 false
→ entity 보존 가능
→ 실제 실행은 차단
```

공통 검사:

```text
공간 관계가 target에 들어갔는지 검사
front_of_desk 형태의 결합 target 검사
지원하지 않는 constraint 검사
중복 constraint 검사
lowercase_snake_case 형식 검사
```

#### 6.4 Validation과 Execution Allowed 분리

두 개념을 별도로 정의했다.

```text
Semantic Validation
→ Mission command 내부 필드가 의미 규칙에 맞는가

Execution Allowed
→ 실제 실행 계층으로 전달할 수 있는가
```

실행 허용 함수:

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

### 7. 해결 결과

Semantic Validator 독립 테스트 결과:

```text
PASS: 6
FAIL: 0
TOTAL: 6
```

LLM Mission Parser와 Validator 통합 테스트 결과:

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

ROS2 Node에서도 동일한 정책을 적용했다.

```text
정상 명령
→ Validation 통과
→ mission_command topic 발행

unknown 명령
→ Validation 통과 가능
→ Execution Allowed = False
→ topic 발행 차단

Validation 실패 명령
→ 오류 출력
→ topic 발행 차단
```

### 8. 배운 점

* Prompt 개선은 의미 해석 정확도를 높이는 데 필요하지만, 실행 안전 규칙까지 prompt에만 의존하면 안 된다.
* Structured Outputs는 schema를 보장하고, Semantic Validator는 필드 사이의 의미적 일관성을 검사한다.
* 테스트 예상값도 절대적인 정답이 아니라 프로젝트 정책에 따라 검토해야 한다.
* `"object": "coffee"`처럼 모델 출력이 예상과 다르더라도, 먼저 모델 오류인지 정책 미정인지 구분해야 한다.
* LLM 출력은 다음 세 단계로 나누어 처리하는 것이 안정적이다.

```text
LLM Mission Parser
→ 자연어 의미 해석

Structured Outputs
→ 필드와 자료형 고정

Semantic Validator
→ 프로젝트 규칙과 실행 안전성 검사
```

* 의미적으로 유효한 명령과 실제 실행 가능한 명령은 서로 다를 수 있다.

### 9. 다시 발생하지 않도록 주의할 점

LLM 테스트가 실패했을 때 바로 prompt 예시를 추가하지 않는다.

다음 순서로 판단한다.

```text
1. Schema 또는 자료형 오류인가
2. 필드 의미 배치 오류인가
3. 사용자 표현 해석 오류인가
4. 예상 결과의 정책이 아직 정해지지 않은 것인가
5. 실행 안전 규칙을 Python 코드로 검사해야 하는가
```

Prompt에는 자연어의 의미를 해석하는 규칙을 둔다.

```text
한국어 표현 정규화
target, object, constraints 분리
공간 관계 해석
```

Python Validator에는 반드시 지켜야 하는 규칙을 둔다.

```text
필수 필드 관계
intent별 실행 flag
지원하지 않는 constraint
unknown 실행 차단
```

특정 테스트 문장 6개에만 맞도록 prompt를 계속 확장하지 않고, 새로운 표현을 포함한 별도 평가 세트로 일반화 성능을 확인해야 한다.
