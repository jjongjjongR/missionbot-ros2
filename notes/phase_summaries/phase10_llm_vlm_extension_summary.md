# Phase 10. LLM/VLM Extension Summary

## 1. Phase 개요

Phase 10에서는 사용자의 한국어 자연어 명령을 OpenAI API 기반 LLM으로 해석하고, MissionBot의 실행 계층이 사용할 수 있는 구조화된 Mission command로 변환하는 기능을 구현했다.

이번 Phase의 실제 구현 범위는 다음과 같다.

```text
LLM Mission Parser
Structured Outputs
Semantic Validator
ROS2 Mission Parser Node
```

Phase 이름에는 LLM/VLM Extension이 포함되어 있지만 이번 Phase에서는 실제 VLM 기반 영상 해석이나 객체 선택 기능까지 구현하지 않았다.

전체 처리 흐름:

```text
사용자 자연어 명령
→ OpenAI LLM Mission Parser
→ Pydantic Structured Outputs
→ Semantic Validator
→ 실행 허용 여부 판단
→ 검증된 ROS2 Mission command 발행
```

---

## 2. 완료한 주요 작업

```text
[x] mission_parser ament_python 패키지 생성
[x] OpenAI Python SDK 설치
[x] python-dotenv 설치
[x] 프로젝트 루트의 .env에서 OPENAI_API_KEY 로드
[x] .env와 비밀키 파일을 .gitignore에 등록
[x] OpenAI Responses API 연결 테스트
[x] 한국어 자연어 명령을 JSON으로 변환
[x] JSON 내부 문자열을 영어로 정규화
[x] lowercase_snake_case 출력 규칙 적용
[x] gpt-4o-mini 기반 Mission Parser 구성
[x] Pydantic MissionCommand schema 정의
[x] Structured Outputs 적용
[x] intent 허용값 제한
[x] target, object, constraints 의미 분리
[x] navigation, vision, manipulation 필요 여부 분리
[x] 공간 관계 prompt 규칙 추가
[x] 6개 자연어 명령 테스트 구성
[x] Exact-match 자동 비교 구현
[x] Semantic Validator 구현
[x] Validator 독립 테스트 구현
[x] unknown 명령 실행 차단 정책 구현
[x] ROS2 mission_parser_node 구현
[x] /missionbot/user_command 구독
[x] /missionbot/mission_command 발행
[x] Validation 실패 명령 발행 차단
[x] 지원 범위 밖 명령 발행 차단
```

---

## 3. MissionCommand 구조

최종 Mission command 구조:

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

필드 의미:

```text
intent
→ 사용자의 핵심 의도

target
→ 이동 목적지 또는 spatial landmark

object
→ 사용자가 찾거나 확인하려는 물체

constraints
→ front, left, right와 같은 공간 관계 또는 추가 조건

requires_navigation
→ 이동로봇 Navigation 기능 필요 여부

requires_vision
→ 카메라 또는 물체 인식 기능 필요 여부

requires_manipulation
→ 로봇팔 조작 기능 필요 여부
```

지원한 intent:

```text
move_to
inspect_object
stop
unknown
```

---

## 4. LLM 출력 정규화 기준

사용자 명령은 한국어 또는 영어로 입력할 수 있지만, Mission command 내부 문자열은 영어 표준값으로 변환했다.

예:

```text
책상 → desk
선반 → shelf
빨간 컵 → red_cup
앞 → front
왼쪽 → left
```

문자열 표현은 가능한 한 `lowercase_snake_case`로 통일했다.

```text
red_cup
stop_after_arrival
```

이 규칙을 사용한 이유는 이후 ROS2 실행 모듈이 문자열을 비교하거나 routing할 때 한국어 표현, 띄어쓰기, 대문자 차이가 섞이지 않도록 하기 위해서다.

---

## 5. Structured Outputs

초기 구현에서는 모델에게 JSON만 출력하도록 prompt를 작성한 뒤 다음 과정을 수행했다.

```text
LLM 문자열 응답
→ Markdown code block 제거
→ json.loads()
→ Python dictionary
```

이 방식은 모델이 JSON 밖의 설명을 추가하거나 필드를 누락할 가능성이 있었다.

이를 개선하기 위해 Pydantic `MissionCommand` 모델과 OpenAI Structured Outputs를 적용했다.

```text
Pydantic MissionCommand
→ Responses API parse
→ schema를 따르는 MissionCommand 객체
```

Structured Outputs 적용 후 다음 항목을 구조적으로 제한할 수 있었다.

```text
필드 존재 여부
필드 타입
intent enum
constraints 배열
requires_* boolean
```

---

## 6. 다중 자연어 명령 테스트

다음 6개 명령을 테스트했다.

```text
1. 책상 앞으로 이동해줘
2. 빨간 컵을 찾아줘
3. 선반 앞까지 가서 멈춰
4. 왼쪽에 있는 컵을 확인해줘
5. 멈춰
6. 커피를 만들어줘
```

초기 결과에서는 다음 문제가 발견되었다.

```text
"선반 앞까지"의 front 조건 누락
"왼쪽"을 constraints가 아닌 target으로 배치
unknown 명령의 object 보존 여부가 예상 정책과 불일치
```

공간 관계 규칙을 prompt에 추가했다.

```text
front, behind, left, right, near는 공간 관계다.
공간 관계 자체를 target으로 사용하지 않는다.
공간 관계는 constraints 배열에 넣는다.
```

`unknown` 명령 정책은 다음처럼 확정했다.

```text
추출 가능한 target, object, constraints는 보존할 수 있다.
모든 실행 flag는 false여야 한다.
unknown 명령은 실제 실행 계층으로 전달하지 않는다.
```

최종 테스트 결과:

```text
Exact-match PASS: 6
Exact-match FAIL: 0
TOTAL: 6
Exact-match pass rate: 100.0%
```

---

## 7. Semantic Validator

Structured Outputs는 출력 구조와 자료형을 제한하지만, 필드 사이의 의미적 일관성까지 자동으로 보장하지는 않는다.

따라서 Python 기반 Semantic Validator를 별도로 구현했다.

주요 검사 규칙:

```text
move_to
→ target 필수
→ object는 null
→ requires_navigation은 true

inspect_object
→ object 필수
→ requires_vision은 true
→ requires_manipulation은 false

stop
→ target과 object는 null
→ constraints는 빈 배열
→ 모든 실행 flag는 false

unknown
→ 모든 실행 flag는 false
→ 추출된 entity는 보존 가능
→ 실제 실행은 차단
```

공통 검사:

```text
필수 필드 누락
lowercase_snake_case 형식
방향 표현의 target 사용
지원하지 않는 constraint
constraint 중복
stop_after_arrival 사용 위치
```

Validator는 잘못된 명령을 자동으로 수정하지 않고 다음 결과를 반환한다.

```text
is_valid
errors
warnings
```

독립 테스트 결과:

```text
PASS: 6
FAIL: 0
TOTAL: 6
```

---

## 8. Validation과 실행 허용의 차이

이번 Phase에서는 다음 두 개념을 분리했다.

```text
Semantic Validation
→ Mission command 내부 값이 의미 규칙에 맞는가

Execution Allowed
→ 실제 MissionBot 실행 계층으로 전달할 수 있는가
```

예:

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

판정:

```text
Semantic Validation: True
Execution Allowed: False
```

`unknown` 명령은 내부 구조가 안전하고 일관적일 수 있지만, MissionBot이 지원하는 명령이 아니므로 실행하지 않는다.

최종 통합 테스트:

```text
Exact-match PASS: 6/6
Semantic Validation PASS: 6/6
Execution Allowed: 5/6
```

---

## 9. ROS2 Mission Parser Node

자연어 명령 입출력을 ROS2 topic으로 연결하기 위해 `mission_parser_node`를 구현했다.

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

전체 흐름:

```text
/missionbot/user_command
→ mission_parser_node
→ OpenAI LLM Mission Parser
→ Structured MissionCommand
→ Semantic Validator
→ Execution Allowed 확인
→ /missionbot/mission_command
```

정상 명령:

```text
책상 앞으로 이동해줘
```

결과:

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

지원 범위 밖 명령:

```text
커피를 만들어줘
```

처리 결과:

```text
intent = unknown
Semantic Validation = True
Execution Allowed = False
topic 발행 차단
```

---

## 10. 주요 실행 명령

빌드:

```bash
cd ~/projects/missionbot-ros2

colcon build --packages-select mission_parser
source install/setup.bash
```

OpenAI 연결 테스트:

```bash
ros2 run mission_parser openai_connection_test
```

LLM Mission Parser 통합 테스트:

```bash
ros2 run mission_parser llm_mission_parser
```

Semantic Validator 독립 테스트:

```bash
ros2 run mission_parser semantic_validator_test
```

ROS2 Mission Parser Node:

```bash
ros2 run mission_parser mission_parser_node
```

자연어 명령 발행:

```bash
ros2 topic pub --once \
/missionbot/user_command \
std_msgs/msg/String \
"{data: '책상 앞으로 이동해줘'}"
```

Mission command 확인:

```bash
ros2 topic echo /missionbot/mission_command
```

---

## 11. 발생한 주요 문제

### Python pip 미설치

```text
/usr/bin/python3: No module named pip
```

해결:

```bash
sudo apt install -y python3-pip
```

### ROS2 package 미인식

```text
Package 'mission_parser' not found
```

해결:

```text
ament_python 구조 확인
setup.py entry point 등록
colcon build
source install/setup.bash
```

### `.env` 경로 오류

잘못 탐색한 경로:

```text
install/mission_parser/lib/.env
```

실제 경로:

```text
~/projects/missionbot-ros2/.env
```

해결:

```python
project_root = Path.cwd()
env_path = project_root / ".env"
```

### Structured Outputs 이후 의미 오류

```text
front 조건 누락
left를 target으로 사용
unknown object 정책 불일치
```

해결:

```text
prompt 공간 관계 규칙 보완
unknown entity 보존 정책 확정
Python Semantic Validator 추가
```

---

## 12. 주요 결과 파일

```text
src/mission_parser/package.xml
src/mission_parser/setup.py
src/mission_parser/setup.cfg
src/mission_parser/resource/mission_parser
src/mission_parser/mission_parser/__init__.py
src/mission_parser/mission_parser/openai_connection_test.py
src/mission_parser/mission_parser/llm_mission_parser.py
src/mission_parser/mission_parser/semantic_validator.py
src/mission_parser/mission_parser/semantic_validator_test.py
src/mission_parser/mission_parser/mission_parser_node.py
```

수정 또는 기록 파일:

```text
.env
.gitignore
README.md
notes/experiment_log.md
notes/troubleshooting.md
notes/phase_summaries/phase10_llm_vlm_extension_summary.md
docs/phases/phase10_llm_vlm_extension.md
```

---

## 13. Phase 10에서 배운 핵심

```text
LLM은 로봇을 직접 제어하는 실행 계층이 아니다.
LLM은 자연어 명령을 구조화하는 상위 해석 계층이다.
```

```text
Structured Outputs는 schema와 타입을 안정화한다.
Semantic Validator는 필드 간 의미와 실행 안전성을 검사한다.
```

```text
유효한 Mission command와 실행 가능한 Mission command는 다를 수 있다.
```

```text
ROS2 Node는 검증되고 지원되는 명령만 다음 topic으로 전달해야 한다.
```

---

## 14. 이번 Phase에서 제외한 범위

```text
VLM 기반 실제 이미지 해석
Object detection
Object grounding
Navigation2 goal 자동 생성
MoveIt2 manipulation 자동 실행
Mission Router
복합 task planning
LangGraph Agent
VLA policy
실제 모바일 매니퓰레이션 통합
```

---

## 15. Phase 10 완료 의미

Phase 10을 통해 MissionBot-ROS2는 다음 흐름을 처음으로 구현했다.

```text
사람의 자연어 명령
→ LLM 기반 의미 해석
→ 구조화된 Mission command
→ Python 기반 의미 검증
→ 실행 허용 여부 판단
→ ROS2 topic 전달
```

이로써 ROS2의 기존 이동·인식·조작 모듈 앞에 연결할 수 있는 상위 Mission Understanding 계층의 기초가 마련되었다.