# MissionBot-ROS2 Phase 7 인수인계 문서

> 목적: 이 문서는 MissionBot-ROS2 프로젝트의 Phase 7. Failure Analysis 완료 상태를 정리하고, 다른 채팅창에서 Phase 8. Control basics를 바로 이어가기 위한 인수인계 문서다.
> 이 문서와 아래의 이어가기 프롬프트만 있으면 Phase 7 완료 상태를 복원하고 Phase 8을 시작할 수 있다.

---

## 1. 프로젝트 정체성

MissionBot-ROS2는 UNICON Lab 준비를 위한 ROS2 기반 모바일 매니퓰레이션 준비 프로젝트다.

이 프로젝트는 처음부터 복잡한 모바일 매니퓰레이션을 완성하는 것이 아니라, ROS2와 Gazebo 기반 이동로봇 시스템을 먼저 이해하고 이후 RViz2 / TF2, SLAM, Navigation2, 센서 로그 분석, 제어 기초, MoveIt2 로봇팔 조작 기초, LLM/VLM 기반 미션 이해까지 단계적으로 연결하는 프로젝트다.

현재 핵심 흐름은 다음이다.

```text
ROS2 기본 구조 이해
→ Gazebo + TurtleBot3 이동로봇 실행
→ RViz2 / TF2로 센서와 좌표계 확인
→ SLAM Toolbox로 지도 생성
→ Navigation2로 목표 지점 이동
→ rosbag2로 센서와 주행 로그 저장
→ 실패 원인 분류
→ 제어 기초 정리
→ MoveIt2와 로봇팔 기초
→ LLM/VLM Mission Understanding
```

---

## 2. 현재 Phase 상태

## Phase 0. Project setup

상태: 완료

완료한 것:

```text
[x] GitHub repository 생성
[x] README.md 작성
[x] .gitignore 작성
[x] docs/00_project_overview.md 작성
[x] notes/experiment_log.md 작성
[x] notes/troubleshooting.md 작성
[x] 기본 폴더 구조 생성
```

---

## Phase 0.5. Environment setup

상태: 기능 검증 완료

완료한 것:

```text
[x] VMware Workstation 17 기반 Ubuntu 22.04 VM 구성
[x] ROS2 Humble 활성화 확인
[x] Gazebo Classic 설치 확인
[x] TurtleBot3 Gazebo 패키지 확인
[x] Tailscale 기반 원격 네트워크 연결 확인
[x] NoMachine 기반 MacBook → Ubuntu VM GUI 접속 확인
[x] VS Code Remote SSH 연결 가능
[x] Gazebo에서 TurtleBot3 Burger spawn 확인
[x] teleop_keyboard로 TurtleBot3 이동 확인
[x] /cmd_vel publisher/subscriber 연결 확인
[x] /odom 출력 확인
[x] /scan 약 5Hz 출력 확인
[x] TurtleBot3 본체가 Gazebo 화면에서 실제로 보이는 것 확인
```

---

## Phase 1. ROS2 basics

상태: 완료

완료 의미:

```text
ROS2의 기본 실행 흐름을 한 번 경험했다.

패키지 생성
→ 노드 작성
→ setup.py 등록
→ colcon build
→ source install/setup.bash
→ ros2 run 실행
→ topic 확인
→ service 호출
→ launch 실행
→ rqt_graph 확인
```

완료한 주요 항목:

```text
[x] missionbot_basic Python ROS2 패키지 생성
[x] pose_subscriber.py 작성
[x] velocity_publisher.py 작성
[x] turtlesim_pubsub.launch.py 작성
[x] publisher / subscriber / service / launch 실습
[x] rqt_graph 연결 확인
[x] Package not found 오류 해결
```

---

## Phase 2. Gazebo + TurtleBot3

상태: 완료

완료 의미:

```text
turtlesim이 아닌 Gazebo TurtleBot3 환경에서 실제 이동로봇 시뮬레이션의 기본 구조를 확인했다.

Gazebo launch
→ TurtleBot3 spawn
→ /cmd_vel 명령
→ teleop 이동
→ /odom 위치 변화 확인
→ /scan LiDAR 데이터 확인
→ rqt_graph 연결 확인
```

완료한 주요 항목:

```text
[x] TurtleBot3 Gazebo empty_world 실행
[x] TurtleBot3 Burger spawn 확인
[x] /cmd_vel topic 확인
[x] /odom topic 확인
[x] /scan topic 확인
[x] teleop_keyboard로 TurtleBot3 이동 확인
[x] gzclient crash 원인 분리 및 GUI 재연결 확인
```

---

## Phase 3. RViz2 + TF2

상태: 완료

완료 의미:

```text
Gazebo에서 생성되는 TurtleBot3의 topic과 TF 정보를 RViz2에서 시각화했다.

Gazebo TurtleBot3
→ /cmd_vel
→ /odom
→ /scan
→ /tf, /tf_static
→ RViz2
```

완료한 주요 항목:

```text
[x] RViz2 실행
[x] Fixed Frame을 odom으로 설정
[x] TF display 추가
[x] RobotModel display 추가
[x] LaserScan display 추가
[x] view_frames로 TF tree 생성
[x] odom → base_footprint → base_link → base_scan 연결 확인
[x] tf2_echo로 transform 확인
[x] teleop 이동 중 TF 변화 확인
```

---

## Phase 4. SLAM

상태: 완료

완료 의미:

```text
TurtleBot3의 /scan, /odom, /tf 정보를 SLAM Toolbox에 연결해 실제 /map 지도를 생성했다.

RViz2에서 지도 생성 과정을 시각적으로 확인했고, teleop 이동으로 지도 확장을 확인했다.

마지막으로 생성된 지도를 .pgm / .yaml 파일로 저장했다.
```

완료한 주요 항목:

```text
[x] TurtleBot3 Gazebo World 실행
[x] SLAM Toolbox online async 모드 실행
[x] use_sim_time:=True 적용
[x] /map topic 생성 확인
[x] RViz2에서 SLAM 지도 시각화 확인
[x] teleop으로 지도 확장 확인
[x] map_saver_cli로 지도 저장
[x] tb3_world_slam_map_01.pgm 생성 확인
[x] tb3_world_slam_map_01.yaml 생성 확인
```

저장된 지도 파일:

```text
maps/phase04_slam/tb3_world_slam_map_01.pgm
maps/phase04_slam/tb3_world_slam_map_01.yaml
```

---

## Phase 5. Navigation2

상태: 완료

완료 의미:

```text
Phase 4에서 생성한 지도를 Navigation2에 연결했고, TurtleBot3가 저장된 map 위에서 현재 위치를 추정한 뒤 RViz2에서 지정한 목표 지점까지 이동하는 것을 확인했다.

이를 통해 MissionBot-ROS2는 수동 조작 중심의 이동로봇 확인 단계를 넘어, 저장된 map 기반 자율 주행 흐름을 처음으로 검증했다.
```

완료한 주요 항목:

```text
[x] Phase 4 map 파일 확인
[x] TurtleBot3 Gazebo World 실행
[x] Navigation2 실행
[x] use_sim_time:=True 적용
[x] /map topic 생성 확인
[x] /amcl node 실행 확인
[x] /map_server node 실행 확인
[x] /planner_server node 실행 확인
[x] /controller_server node 실행 확인
[x] /bt_navigator node 실행 확인
[x] RViz2 Fixed Frame을 map으로 설정
[x] 2D Pose Estimate로 AMCL 초기 위치 지정
[x] /amcl_pose topic 출력 확인
[x] map → odom transform 생성 확인
[x] 2D Nav Goal로 목표 지점 지정
[x] TurtleBot3 목표 이동 확인
[x] /plan topic 생성 확인
[x] /cmd_vel topic 발행 확인
[x] 주요 Nav2 lifecycle node active [3] 확인
```

---

## Phase 6. rosbag2 Logging

상태: 완료

완료 의미:

```text
Navigation2 주행 중 발생하는 핵심 ROS2 topic을 rosbag2로 기록하고, 저장된 bag 파일을 다시 재생하여 RViz2에서 확인하는 전체 흐름을 검증했다.

이를 통해 MissionBot-ROS2는 주행 결과를 실시간으로 보는 수준을 넘어, 재현 가능한 로그 데이터로 남길 수 있게 되었다.
```

완료한 주요 항목:

```text
[x] 기존 Gazebo / RViz2 / Navigation2 노드 정리
[x] ros2 bag 명령어 인식 확인
[x] 기록 대상 topic 선정
[x] /scan, /odom, /tf, /tf_static, /cmd_vel, /amcl_pose, /plan topic 확인
[x] ros2 bag record로 Navigation2 주행 topic 기록
[x] ros2 bag info로 기록 결과 확인
[x] metadata.yaml로 bag 파일 구조 확인
[x] ros2 bag play로 playback 확인
[x] --topics 옵션으로 일부 topic 선택 재생 확인
[x] --rate 옵션으로 playback 속도 조절 확인
[x] RViz2에서 rosbag playback 시각화 확인
[x] use_sim_time=true와 --clock 옵션 필요성 확인
```

기록된 정상 bag:

```text
rosbags/phase06_logging/p06_nav2_goal_01
```

정상 bag topic count:

```text
/scan       793
/odom       4664
/tf_static  1
/cmd_vel    840
/tf         8557
/plan       41
/amcl_pose  39
```

---

## Phase 7. Failure Analysis

상태: 완료

완료 의미:

```text
Phase 6에서 기록한 정상 Navigation2 주행 bag을 baseline으로 삼고, 실패 상황을 rosbag2로 기록한 뒤 ROS2 topic 증거를 기준으로 실패 유형을 분류했다.

이를 통해 MissionBot-ROS2는 단순히 Navigation2 주행 성공 여부를 확인하는 수준에서 나아가, 실패 상황을 재현 가능한 로그 데이터로 남기고 원인을 분류하는 기본 Failure Analysis 흐름을 갖추게 되었다.
```

완료한 주요 항목:

```text
[x] Phase 6 정상 주행 bag baseline 확인
[x] 정상 bag topic count 확인
[x] Failure Type 후보 정의
[x] topic별 판단 기준 정리
[x] Failure Analysis Decision Table 작성
[x] Baseline Bag Inspection Commands 정리
[x] failure_case_template.md 작성
[x] Failure Analysis Workflow 작성
[x] 첫 실패 사례 계획 수립
[x] P07-FAIL-0001_unreachable_goal_test 실패 bag 기록
[x] ros2 bag info로 실패 bag 정보 확인
[x] P07-FAIL-0001_unreachable_goal_test.md 작성
[x] /cmd_vel 기반 control_oscillation 보조 증거 확인
[x] notes/experiment_log.md에 실패 실험 인덱싱
[x] README.md Result 섹션에 Phase 7 Summary 추가
[x] notes/phase_summaries/phase07_failure_analysis_summary.md 작성
```

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

Simulator:
Gazebo Classic 11.10.2

Robot:
TurtleBot3 Burger

Visualization:
RViz2

SLAM:
slam_toolbox

Navigation:
Navigation2

Logging:
rosbag2

Failure Analysis:
rosbag2 기반 topic 증거 분석

Main TurtleBot3 Workspace:
~/turtlebot3_ws

MissionBot Project Location:
~/projects/missionbot-ros2
```

---

## 4. 현재 프로젝트 폴더 기준

README 기준으로 MissionBot-ROS2 프로젝트는 루트 바로 아래 `src/`를 ROS2 패키지 작성 위치로 사용한다.

주의:

```text
missionbot_ws/src 구조를 만들지 않는다.
```

현재 기준 구조:

```text
missionbot-ros2/
├── README.md
├── docs/
│   ├── phases/
│   │   ├── phase05_navigation2.md
│   │   ├── phase06_rosbag2_logging.md
│   │   └── phase07_failure_analysis.md
│   ├── concepts/
│   ├── templates/
│   └── handoffs/
│       ├── MBROS2_Phase7_Handoff.md
│       └── MBROS2_Phase7_prompt.md
│
├── src/
│   └── missionbot_basic/
│
├── configs/
├── maps/
│   └── phase04_slam/
│       ├── tb3_world_slam_map_01.pgm
│       └── tb3_world_slam_map_01.yaml
│
├── rosbags/
│   ├── phase06_logging/
│   │   └── p06_nav2_goal_01/
│   │       ├── metadata.yaml
│   │       └── p06_nav2_goal_01_0.db3
│   └── failure_cases/
│       └── P07-FAIL-0001_unreachable_goal_test/
│           ├── metadata.yaml
│           └── P07-FAIL-0001_unreachable_goal_test_0.db3
│
├── results/
│   └── failure_cases/
│       ├── failure_case_template.md
│       └── P07-FAIL-0001_unreachable_goal_test.md
│
└── notes/
    ├── experiment_log.md
    ├── troubleshooting.md
    ├── daily_logs/
    ├── phase_summaries/
    │   ├── phase05_navigation2_summary.md
    │   ├── phase06_rosbag2_logging_summary.md
    │   └── phase07_failure_analysis_summary.md
    └── handoff_notes/
```

현재 프로젝트 루트에서 확인된 기본 폴더:

```text
build
configs
docs
install
log
maps
notes
README.md
results
rosbags
src
```

`build`, `install`, `log`는 Phase 1에서 `colcon build`를 수행했기 때문에 생성된 ROS2 빌드 산출물이다.

---

## 5. 현재 .bashrc 기준

새 터미널을 열면 `.bashrc`가 자동 실행되고, 아래 환경이 적용된다.

```text
ROS2 Humble
TurtleBot3 workspace
TURTLEBOT3_MODEL=burger
GAZEBO_MODEL_PATH
```

새 터미널을 열면 다음 문구가 자동으로 출력된다.

```text
ROS2 humble is activated!
```

이 문구는 사용자가 의도적으로 유지하는 환경 적용 확인 메시지다.

주의:

```text
source ~/.bashrc를 매번 다시 실행할 필요는 없다.
```

다만, MissionBot 프로젝트에서 직접 만든 패키지를 실행하려면 별도로 아래 명령이 필요하다.

```bash
cd ~/projects/missionbot-ros2
source install/setup.bash
```

이 둘의 역할은 다르다.

```text
source ~/.bashrc
→ ROS2 Humble, TurtleBot3 workspace, Gazebo model path 등 기본 환경 적용

source install/setup.bash
→ MissionBot 프로젝트에서 colcon build로 만든 패키지를 현재 터미널이 인식
```

TurtleBot3 Gazebo, RViz2, SLAM Toolbox, Navigation2, rosbag2 같은 외부 ROS2 패키지를 실행할 때는 `.bashrc`로 기본 ROS2/TurtleBot3 환경이 잡혀 있으면 충분한 경우가 많다.

---

## 6. Phase 7 Baseline Bag

Phase 7에서 정상 기준으로 사용한 bag은 다음이다.

```text
rosbags/phase06_logging/p06_nav2_goal_01
```

정상 bag 정보:

```text
Files:             p06_nav2_goal_01_0.db3
Bag size:          8.8 MiB
Storage id:        sqlite3
Duration:          164.287617550s
Messages:          14935
```

정상 bag topic count:

```text
/scan       793
/odom       4664
/tf_static  1
/cmd_vel    840
/tf         8557
/plan       41
/amcl_pose  39
```

정상 bag 의미:

```text
Navigation2가 저장된 map 위에서 목표 지점 이동을 수행하는 동안 기록된 정상 주행 데이터다.

Failure Analysis에서는 이 bag을 기준 데이터로 삼아 실패 bag과 비교했다.
```

---

## 7. Phase 7 Failure Type 후보

Phase 7에서 정의한 실패 유형 후보는 다음과 같다.

```text
goal_unreachable
path_planning_failure
localization_failure
obstacle_blocked
control_oscillation
sensor_missing
timeout
unknown
```

주요 판단 기준:

```text
/plan 없음
→ path_planning_failure 가능성

/plan 있음 + /cmd_vel 있음 + 목표 도달 실패
→ goal_unreachable 가능성

/cmd_vel 있음 + /odom 변화 거의 없음 + /scan 근접 장애물
→ obstacle_blocked 가능성

/amcl_pose 없음 또는 위치 추정 불안정
→ localization_failure 가능성

/scan, /odom, /tf 등 핵심 topic 누락
→ sensor_missing 가능성

linear.x는 작고 angular.z가 반복적으로 큼
→ control_oscillation 증상 가능성

Duration이 길지만 목표 도달 증거 없음
→ timeout 또는 goal_unreachable 가능성
```

---

## 8. Phase 7 첫 실패 사례

첫 실패 사례 ID:

```text
P07-FAIL-0001_unreachable_goal_test
```

실패 상황:

```text
RViz2에서 장애물 내부 또는 장애물과 가까운 위치를 2D Nav Goal로 지정했다.

TurtleBot3는 목표 근처까지 이동했지만 최종 목표에는 도달하지 못했다.

목표 근처에서 path가 바뀌는 현상이 보였고, TurtleBot3가 제자리에서 회전하는 동작을 반복했다.
```

실패 bag 위치:

```text
rosbags/failure_cases/P07-FAIL-0001_unreachable_goal_test
```

실패 분석 문서:

```text
results/failure_cases/P07-FAIL-0001_unreachable_goal_test.md
```

실패 bag 정보:

```text
Files:             P07-FAIL-0001_unreachable_goal_test_0.db3
Bag size:          5.2 MiB
Storage id:        sqlite3
Duration:          92.231500380s
Messages:          9038
```

기록된 topic count:

```text
/cmd_vel     1034
/plan        51
/amcl_pose   58
/scan        447
/odom        2628
/tf_static   1
/tf          4819
```

판단:

```text
/plan이 51개 기록되었으므로 path_planning_failure로 보기는 어렵다.

/cmd_vel이 1034개 기록되었으므로 controller가 속도 명령을 발행한 것은 확인된다.

/scan, /odom, /tf, /tf_static, /amcl_pose가 모두 기록되었으므로 sensor_missing 또는 명확한 localization_failure 가능성은 낮다.

목표 근처까지 이동했지만 최종 도달하지 못했으므로 goal_unreachable로 판단했다.
```

최종 판정:

```text
Failure Type: goal_unreachable
Root Cause: 장애물 내부 또는 도달하기 어려운 위치를 2D Nav Goal로 지정하여, Navigation2가 목표 근처까지 접근했지만 최종 목표에 도달하지 못했다.
Secondary Symptom: control_oscillation
Confidence: high
```

---

## 9. /cmd_vel Oscillation Evidence

실패 bag의 뒤쪽 구간에서 `/cmd_vel`을 선택 재생해 목표 근처의 속도 명령 패턴을 확인했다.

사용한 명령:

```bash
cd ~/projects/missionbot-ros2

ros2 bag play rosbags/failure_cases/P07-FAIL-0001_unreachable_goal_test \
  --topics /cmd_vel \
  --start-offset 62 \
  --rate 0.5 \
  --clock
```

`ros2 topic echo /cmd_vel` 출력에서 확인한 패턴:

```text
linear.x는 대부분 0.0 또는 매우 작은 값
angular.z는 큰 양수와 음수 값이 반복
```

대표 관찰 값:

```text
linear.x: 0.0
angular.z: -0.9979487179487179

linear.x: 0.0
angular.z: -0.9487179487179487

linear.x: 0.0
angular.z: 1.0000000000000004

linear.x: 0.0
angular.z: 0.8974358974358978
```

해석:

```text
전진 속도 명령은 거의 없고 회전 속도 명령이 반복적으로 발행되었다.

따라서 TurtleBot3가 목표 근처에서 전진해 목표에 수렴하기보다 회전 동작을 반복한 것으로 볼 수 있다.
```

판단:

```text
이번 실패 사례의 주 Failure Type은 goal_unreachable이다.

control_oscillation은 주 실패 원인이 아니라, goal_unreachable 상황에서 관찰된 보조 증상으로 기록한다.
```

---

## 10. Phase 7 주요 명령어

## 10.1 정상 bag 확인

```bash
cd ~/projects/missionbot-ros2

ros2 bag info rosbags/phase06_logging/p06_nav2_goal_01
```

## 10.2 실패 bag 기록

```bash
cd ~/projects/missionbot-ros2

ros2 bag record \
  /scan \
  /odom \
  /tf \
  /tf_static \
  /cmd_vel \
  /amcl_pose \
  /plan \
  -o rosbags/failure_cases/P07-FAIL-0001_unreachable_goal_test
```

## 10.3 실패 bag 정보 확인

```bash
ros2 bag info rosbags/failure_cases/P07-FAIL-0001_unreachable_goal_test
```

## 10.4 실패 bag 뒤쪽 /cmd_vel 확인

```bash
ros2 bag play rosbags/failure_cases/P07-FAIL-0001_unreachable_goal_test \
  --topics /cmd_vel \
  --start-offset 62 \
  --rate 0.5 \
  --clock
```

다른 터미널:

```bash
ros2 topic echo /cmd_vel
```

## 10.5 Phase 7 문서 확인 명령

```bash
grep -n "P07-FAIL-0001_unreachable_goal_test" notes/experiment_log.md
grep -n "Failure Type: goal_unreachable" notes/experiment_log.md
grep -n "Secondary Symptom: control_oscillation" notes/experiment_log.md

grep -n "cmd_vel Evidence Result" results/failure_cases/P07-FAIL-0001_unreachable_goal_test.md
grep -n "Confidence: high" results/failure_cases/P07-FAIL-0001_unreachable_goal_test.md
```

---

## 11. Phase 7에서 배운 핵심 개념

## 11.1 Failure Analysis

```text
Failure Analysis는 rosbag과 topic 기록을 기반으로 로봇이 왜 실패했는지 분류하는 과정이다.
```

MissionBot에서의 의미:

```text
Navigation2 주행 실패를 감으로 판단하지 않고, /plan, /cmd_vel, /odom, /amcl_pose, /scan, /tf 같은 topic 증거를 기준으로 분류한다.
```

---

## 11.2 Baseline Bag

```text
Baseline bag은 정상 주행 기준 데이터다.
```

이번 Phase에서는 Phase 6에서 기록한 정상 Navigation2 주행 bag을 baseline으로 사용했다.

```text
rosbags/phase06_logging/p06_nav2_goal_01
```

---

## 11.3 Failure Case

```text
Failure case는 실패 상황 하나를 기록하고 분석하는 단위다.
```

이번 Phase에서는 첫 실패 사례로 다음 케이스를 기록했다.

```text
P07-FAIL-0001_unreachable_goal_test
```

---

## 11.4 goal_unreachable

```text
goal_unreachable은 목표 지점에 최종적으로 도달하지 못한 실패 유형이다.
```

이번 케이스에서는 `/plan`과 `/cmd_vel`이 존재하고 로봇이 목표 근처까지 이동했지만, 장애물 내부 또는 도달하기 어려운 위치가 목표로 지정되어 최종 도달에 실패했다.

---

## 11.5 control_oscillation

```text
control_oscillation은 로봇이 목표 근처에서 안정적으로 수렴하지 못하고 회전 또는 흔들림을 반복하는 증상이다.
```

이번 케이스에서는 `linear.x`는 거의 0이고 `angular.z`가 반복적으로 크게 나타났기 때문에 control_oscillation을 보조 증상으로 기록했다.

---

## 11.6 topic evidence

```text
topic evidence는 실패 유형을 판단하는 데 사용하는 ROS2 topic 기반 증거다.
```

이번 Phase에서 사용한 주요 topic evidence:

```text
/plan
→ 경로 생성 여부

/cmd_vel
→ 이동 명령 발행 여부

/odom
→ 로봇 이동 상태

/amcl_pose
→ map 위 위치 추정

/scan
→ 주변 장애물 또는 센서 입력

/tf, /tf_static
→ 좌표계 관계
```

---

## 12. Phase 7에서 발생한 주요 현상

## 12.1 /cmd_vel echo가 처음에 아무것도 나오지 않던 현상

상황:

```text
ros2 topic echo /cmd_vel
ros2 topic hz /cmd_vel
```

위 명령을 실행했지만 아무 반응이 없었다.

판단:

```text
/cmd_vel 데이터가 없는 것이 아니라, bag play 타이밍 문제였다.

실패 bag은 92초 길이이고, /cmd_vel을 처음부터 느리게 재생하면 관심 구간까지 도달하는 데 시간이 오래 걸릴 수 있다.
```

해결:

```bash
ros2 bag play rosbags/failure_cases/P07-FAIL-0001_unreachable_goal_test \
  --topics /cmd_vel \
  --start-offset 62 \
  --rate 0.5 \
  --clock
```

결과:

```text
bag 뒤쪽 구간부터 재생하자 /cmd_vel 메시지가 정상적으로 출력되었다.
```

주의:

```text
이 내용은 시스템 오류라기보다 rosbag playback 분석 시 중요한 사용 팁이다.
```

---

## 13. Phase 7 기록 파일

Phase 7 관련 정리 파일:

```text
README.md
notes/experiment_log.md
docs/phases/phase07_failure_analysis.md
notes/phase_summaries/phase07_failure_analysis_summary.md
results/failure_cases/failure_case_template.md
results/failure_cases/P07-FAIL-0001_unreachable_goal_test.md
docs/handoffs/MBROS2_Phase7_Handoff.md
docs/handoffs/MBROS2_Phase7_prompt.md
```

experiment_log 업데이트 내용:

```text
P07-FAIL-0001_unreachable_goal_test
```

troubleshooting 정리 여부:

```text
정식 troubleshooting 항목은 필수로 추가하지 않는다.

이번 Phase에서 발생한 /cmd_vel echo 타이밍 문제는 오류 해결이라기보다 rosbag playback 분석 팁에 가깝다.
따라서 docs/phases/phase07_failure_analysis.md 또는 failure report의 분석 과정에 기록하는 것으로 충분하다.
```

---

## 14. Phase 7 완료 판정

Phase 7은 다음 기준을 만족했으므로 완료로 판단한다.

```text
[x] 정상 baseline bag 확인
[x] 실패 유형 후보 정의
[x] topic 기반 판단 기준 정리
[x] Failure Analysis Decision Table 작성
[x] failure_case_template.md 작성
[x] Failure Analysis Workflow 작성
[x] 첫 실패 bag 기록
[x] 실패 bag과 정상 bag 비교
[x] 실패 유형 최종 판정
[x] /cmd_vel 기반 보조 증거 확인
[x] failure report 작성
[x] experiment_log 인덱싱
[x] README Result 섹션 업데이트
[x] phase summary 작성
[x] handoff 문서 작성
```

완료 의미:

```text
MissionBot-ROS2는 이제 단순히 Navigation2 주행을 성공시키는 것에서 나아가, 실패 상황을 rosbag2로 기록하고 topic 증거를 기반으로 실패 원인을 분류할 수 있게 되었다.

이번 Phase를 통해 정상 주행과 실패 주행을 비교하는 기본 분석 흐름을 만들었고, 이후 제어 기초나 더 복잡한 실패 분석으로 확장할 준비가 되었다.
```

---

## 15. Phase 8 시작 목표

다음 Phase:

```text
Phase 8. Control basics
```

Phase 8의 핵심 목표:

```text
TurtleBot3의 /cmd_vel 속도 명령과 /odom 반응을 기준으로 이동로봇 제어의 기초를 이해한다.
```

Phase 8에서 중요하게 연결될 개념:

```text
control
→ 로봇을 원하는 방향과 속도로 움직이게 만드는 과정

/cmd_vel
→ 로봇에게 보내는 속도 명령

linear.x
→ 전진/후진 속도 명령

angular.z
→ 회전 속도 명령

/odom
→ 로봇이 실제로 어떻게 움직였는지 추정한 결과

open-loop control
→ 피드백 없이 정해진 속도 명령을 일정 시간 보내는 방식

feedback
→ 실제 로봇 상태를 보고 명령을 조정하는 방식
```

단, Phase 8 시작 시 처음부터 PID, MPC, 강화학습 제어로 앞서가지 않는다.

첫 단계에서는 `/cmd_vel`과 `/odom`의 관계를 복습하고, 단순한 속도 명령이 로봇 움직임에 어떤 결과를 만드는지 확인한다.

---

## 16. Phase 8 시작 전 확인할 것

Phase 8 시작 전 확인할 기본 항목:

```bash
cd ~/projects/missionbot-ros2
pwd

echo $ROS_DISTRO
echo $TURTLEBOT3_MODEL

which ros2
which gazebo
which rviz2

ros2 pkg list | grep turtlebot3_gazebo
ros2 pkg list | grep turtlebot3_teleop
```

정상 기대값:

```text
/home/user/projects/missionbot-ros2
humble
burger
/opt/ros/humble/bin/ros2
/usr/bin/gazebo
/opt/ros/humble/bin/rviz2
turtlebot3_gazebo
turtlebot3_teleop
```

---

## 17. Phase 8에서 주의할 점

```text
Phase 8에서는 MoveIt2, LLM/VLM, Manipulation으로 앞서가지 않는다.

우선 TurtleBot3 이동로봇의 /cmd_vel 명령과 /odom 반응을 기준으로 제어의 기초를 이해한다.
```

처음부터 복잡한 제어 알고리즘을 구현하지 않는다.

Phase 8의 첫 목표는 다음과 같다.

```text
1. 기존 Gazebo / RViz2 / Nav2 관련 노드 정리
2. ROS2 / TurtleBot3 환경 확인
3. TurtleBot3 Gazebo World 실행
4. /cmd_vel과 /odom topic 확인
5. /cmd_vel의 linear.x, angular.z 의미 복습
6. /odom으로 실제 이동 반응 확인
7. 단순 open-loop control 실습 준비
```

---

## 18. 다음 채팅 시작 지점

다음 채팅에서는 아래 상태에서 시작하면 된다.

```text
현재 MissionBot-ROS2는 Phase 7. Failure Analysis를 완료했다.

완료한 것:
- Phase 6 정상 Navigation2 주행 bag을 baseline으로 정의
- 실패 유형 후보 정의
- topic별 판단 기준 정리
- failure_case_template.md 작성
- Failure Analysis Workflow 작성
- 첫 실패 사례 P07-FAIL-0001_unreachable_goal_test 계획 및 기록
- 실패 bag을 ros2 bag info로 확인
- /plan, /cmd_vel, /odom, /amcl_pose, /scan, /tf 기반으로 실패 유형 판단
- 최종 Failure Type을 goal_unreachable로 판정
- Secondary Symptom으로 control_oscillation 기록
- /cmd_vel 뒤쪽 구간을 --start-offset으로 재생해 angular.z 반복 증거 확인
- failure report 작성
- experiment_log 인덱싱
- README Result 섹션 업데이트
- phase summary 작성

주요 결과물:
- docs/phases/phase07_failure_analysis.md
- notes/phase_summaries/phase07_failure_analysis_summary.md
- results/failure_cases/failure_case_template.md
- results/failure_cases/P07-FAIL-0001_unreachable_goal_test.md
- rosbags/failure_cases/P07-FAIL-0001_unreachable_goal_test
- notes/experiment_log.md의 P07-FAIL-0001_unreachable_goal_test

다음 목표:
- Phase 8. Control basics 시작
- 첫 단계는 /cmd_vel과 /odom 관계를 기준으로 이동로봇 제어 기초를 이해하는 것
```

추천 시작점:

```text
Phase 8-1. Control basics 시작 전 환경 확인과 /cmd_vel - /odom 관계 복습
```

첫 단계에서 할 일:

```text
1. 기존 Gazebo / RViz2 / Nav2 관련 노드가 남아 있지 않은지 확인
2. ROS2 Humble 환경 확인
3. TURTLEBOT3_MODEL=burger 확인
4. TurtleBot3 Gazebo 패키지 확인
5. MissionBot 프로젝트 위치 확인
6. TurtleBot3 Gazebo World 실행
7. /cmd_vel topic 확인
8. /odom topic 확인
9. linear.x와 angular.z 의미 복습
10. /cmd_vel 명령과 /odom 반응의 관계를 설명
```
