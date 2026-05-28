# MissionBot-ROS2 Phase 1 인수인계 문서

> 목적: 이 문서는 MissionBot-ROS2 프로젝트의 Phase 1. ROS2 basics 완료 상태를 정리하고, 다른 채팅창에서 Phase 2. Gazebo + TurtleBot3를 바로 이어가기 위한 인수인계 문서다.  
> 이 문서와 아래의 이어가기 프롬프트만 있으면 Phase 1 완료 상태를 복원하고 Phase 2를 시작할 수 있다.

---

## 1. 프로젝트 정체성

MissionBot-ROS2는 UNICON Lab 준비를 위한 ROS2 기반 모바일 매니퓰레이션 준비 프로젝트다.

이 프로젝트는 처음부터 복잡한 모바일 매니퓰레이션을 완성하는 것이 아니라, ROS2와 Gazebo 기반 이동로봇 시스템을 먼저 이해하고 이후 SLAM, Navigation2, 센서 로그 분석, 제어 기초, MoveIt2 로봇팔 조작 기초, LLM/VLM 기반 미션 이해까지 단계적으로 연결하는 프로젝트다.

현재 핵심 목표는 다음이다.

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

완료한 것:

```text
[x] missionbot_basic Python ROS2 패키지 생성
[x] turtlesim 실행
[x] /turtle1/pose topic 확인
[x] pose_subscriber.py 작성
[x] setup.py entry_points에 pose_subscriber 등록
[x] colcon build
[x] source install/setup.bash 적용
[x] ros2 run으로 pose_subscriber 실행
[x] rqt_graph로 /turtlesim → /turtle1/pose → /pose_subscriber 연결 확인
[x] velocity_publisher.py 작성
[x] setup.py entry_points에 velocity_publisher 등록
[x] /turtle1/cmd_vel topic으로 Twist 메시지 publish
[x] turtlesim 거북이 이동 확인
[x] /clear service 호출
[x] /spawn service 호출
[x] turtlesim_pubsub.launch.py 작성
[x] package.xml에 geometry_msgs, launch, launch_ros 의존성 추가
[x] setup.py data_files에 launch 파일 설치 설정 추가
[x] ros2 launch로 turtlesim_node, pose_subscriber, velocity_publisher 동시 실행
[x] Package not found 오류 해결
```

Phase 1 완료 판정:

```text
Phase 1은 ROS2 기본 구조 학습 기준으로 완료로 본다.
publisher, subscriber, service, launch, build, source, rqt_graph까지 한 바퀴 실습했다.
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
│   ├── concepts/
│   ├── templates/
│   └── handoffs/
│
├── src/
│   └── missionbot_basic/
│
├── configs/
├── maps/
├── rosbags/
├── results/
└── notes/
    ├── experiment_log.md
    ├── troubleshooting.md
    ├── daily_logs/
    ├── phase_summaries/
    └── handoff_notes/
```

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

---

## 6. Phase 1에서 만든 ROS2 패키지

패키지 이름:

```text
missionbot_basic
```

패키지 위치:

```text
~/projects/missionbot-ros2/src/missionbot_basic
```

패키지 역할:

```text
ROS2 기본 노드 실습
publisher/subscriber 구조 이해
service 호출 방식 이해
launch 파일 작성 방식 이해
```

---

## 7. Phase 1에서 작성한 주요 파일

## 7.1 pose_subscriber.py

위치:

```text
src/missionbot_basic/missionbot_basic/pose_subscriber.py
```

역할:

```text
/turtle1/pose topic을 구독한다.
turtlesim/msg/Pose 메시지를 받는다.
수신한 x, y, theta 값을 로그로 출력한다.
```

핵심 구조:

```text
rclpy 초기화
Node 상속
create_subscription()
pose_callback()
rclpy.spin()
```

확인한 연결:

```text
/turtlesim
→ /turtle1/pose
→ /pose_subscriber
```

---

## 7.2 velocity_publisher.py

위치:

```text
src/missionbot_basic/missionbot_basic/velocity_publisher.py
```

역할:

```text
/turtle1/cmd_vel topic으로 geometry_msgs/msg/Twist 메시지를 publish한다.
0.5초마다 linear.x와 angular.z 속도 명령을 발행한다.
turtlesim 거북이를 실제로 움직인다.
```

핵심 구조:

```text
rclpy 초기화
Node 상속
create_publisher()
create_timer()
Twist 메시지 생성
publish()
```

확인한 연결:

```text
/velocity_publisher
→ /turtle1/cmd_vel
→ /turtlesim
```

---

## 7.3 turtlesim_pubsub.launch.py

위치:

```text
src/missionbot_basic/launch/turtlesim_pubsub.launch.py
```

역할:

```text
turtlesim_node, pose_subscriber, velocity_publisher를 한 번에 실행한다.
```

실행 명령:

```bash
ros2 launch missionbot_basic turtlesim_pubsub.launch.py
```

실행되는 노드:

```text
/turtlesim
/pose_subscriber
/velocity_publisher
```

---

## 7.4 setup.py

위치:

```text
src/missionbot_basic/setup.py
```

수정한 내용:

```text
pose_subscriber entry point 등록
velocity_publisher entry point 등록
launch 파일 설치를 위한 data_files 설정 추가
```

등록된 실행 명령:

```text
ros2 run missionbot_basic pose_subscriber
ros2 run missionbot_basic velocity_publisher
```

---

## 7.5 package.xml

위치:

```text
src/missionbot_basic/package.xml
```

포함된 주요 의존성:

```text
rclpy
turtlesim
geometry_msgs
launch
launch_ros
```

의미:

```text
rclpy: Python ROS2 노드 작성
turtlesim: turtlesim 메시지와 실습 환경
geometry_msgs: Twist 메시지 사용
launch, launch_ros: launch 파일 실행
```

---

## 8. Phase 1 최종 실행 확인 명령

프로젝트 루트로 이동:

```bash
cd ~/projects/missionbot-ros2
```

빌드:

```bash
colcon build --packages-select missionbot_basic
```

현재 터미널에 MissionBot workspace 적용:

```bash
source install/setup.bash
```

등록된 실행 파일 확인:

```bash
ros2 pkg executables missionbot_basic
```

정상 기대값:

```text
missionbot_basic pose_subscriber
missionbot_basic velocity_publisher
```

launch 실행:

```bash
ros2 launch missionbot_basic turtlesim_pubsub.launch.py
```

node 확인:

```bash
ros2 node list
```

정상 기대값:

```text
/pose_subscriber
/turtlesim
/velocity_publisher
```

topic 확인:

```bash
ros2 topic info /turtle1/pose
ros2 topic info /turtle1/cmd_vel
```

정상 기대값:

```text
/turtle1/pose
Publisher count: 1
Subscription count: 1

/turtle1/cmd_vel
Publisher count: 1
Subscription count: 1
```

시각화:

```bash
rqt_graph
```

확인할 구조:

```text
/velocity_publisher
→ /turtle1/cmd_vel
→ /turtlesim
→ /turtle1/pose
→ /pose_subscriber
```

---

## 9. Phase 1에서 확인한 service

사용한 service:

```text
/clear
/spawn
```

확인 명령:

```bash
ros2 service list
ros2 service type /clear
ros2 service call /clear std_srvs/srv/Empty
ros2 service type /spawn
ros2 interface show turtlesim/srv/Spawn
ros2 service call /spawn turtlesim/srv/Spawn "{x: 2.0, y: 2.0, theta: 0.0, name: 'mission_turtle'}"
```

배운 점:

```text
topic은 계속 흐르는 데이터다.
service는 필요할 때 한 번 요청하고 응답받는 구조다.
service interface에서 --- 위는 request, 아래는 response다.
```

---

## 10. Phase 1에서 발생한 주요 오류

## 10.1 Package 'missionbot_basic' not found

발생 상황:

```bash
ros2 launch missionbot_basic turtlesim_pubsub.launch.py
```

오류 메시지:

```text
Package 'missionbot_basic' not found
```

원인:

```text
현재 터미널에 MissionBot workspace의 install/setup.bash가 source되지 않았다.
```

에러 메시지에서 ROS2가 검색한 경로:

```text
/home/user/turtlebot3_ws/install/...
/opt/ros/humble
```

하지만 `missionbot_basic`은 아래 workspace에 있다.

```text
/home/user/projects/missionbot-ros2/install
```

해결:

```bash
cd ~/projects/missionbot-ros2
source install/setup.bash
ros2 pkg list | grep missionbot_basic
ros2 launch missionbot_basic turtlesim_pubsub.launch.py
```

해결 결과:

```text
missionbot_basic 패키지 인식 성공
launch 실행 성공
turtlesim_node, pose_subscriber, velocity_publisher 동시 실행 성공
```

상세 기록 위치:

```text
notes/troubleshooting.md
TS-0003_missionbot_basic_package_not_found
```

---

## 11. Phase 1 기록 파일

Phase 1 관련 정리 파일:

```text
notes/experiment_log.md
notes/troubleshooting.md
notes/phase_summaries/phase01_ros2_basics_summary.md
docs/phases/phase01_ros2_basics.md
docs/handoffs/MBROS2_Phase1_Handoff.md
```

README 업데이트 내용:

```text
Phase map에서 Phase 1 체크 완료
Result 섹션에 Phase 1 Summary 추가
```

---

## 12. Phase 1 완료 판정

Phase 1은 다음 기준을 만족했으므로 완료로 판단한다.

```text
[x] missionbot_basic 패키지 생성
[x] pose_subscriber 작성 및 실행
[x] velocity_publisher 작성 및 실행
[x] /turtle1/pose topic 연결 확인
[x] /turtle1/cmd_vel topic 연결 확인
[x] service 호출 확인
[x] launch 파일 작성 및 실행
[x] rqt_graph 연결 확인
[x] troubleshooting 기록
[x] experiment_log 기록
[x] phase summary 작성
[x] handoff 문서 작성
```

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

---

## 13. Phase 2 시작 목표

다음 Phase:

```text
Phase 2. Gazebo + TurtleBot3
```

Phase 2의 핵심 목표:

```text
turtlesim이 아니라 Gazebo 환경의 TurtleBot3 Burger를 대상으로 ROS2 topic 구조를 확인한다.
```

첫 번째로 할 일:

```text
Gazebo TurtleBot3 empty_world 실행
```

이후 확인할 것:

```text
/cmd_vel topic 확인
teleop_keyboard 실행
/cmd_vel publisher/subscriber 연결 확인
/odom topic echo 확인
/scan topic hz 확인
rqt_graph로 TurtleBot3 graph 확인
```

---

## 14. Phase 2 시작 전 확인 명령

새 터미널에서 확인:

```bash
echo $ROS_DISTRO
echo $TURTLEBOT3_MODEL
which ros2
which gazebo
ros2 pkg list | grep turtlebot3_gazebo
```

정상 기대값:

```text
humble
burger
/opt/ros/humble/bin/ros2
/usr/bin/gazebo
turtlebot3_gazebo
```

MissionBot workspace 확인이 필요하면:

```bash
cd ~/projects/missionbot-ros2
source install/setup.bash
ros2 pkg list | grep missionbot_basic
```

---

## 15. Phase 2에서 주의할 점

```text
Gazebo + TurtleBot3는 turtlesim보다 topic과 node가 훨씬 많다.
Phase 2에서는 처음부터 SLAM, Nav2, MoveIt2로 앞서가지 않는다.
우선 /cmd_vel, /odom, /scan 세 개만 집중해서 확인한다.
```

Phase 1과 Phase 2의 연결:

```text
/turtle1/cmd_vel
→ /cmd_vel

/turtle1/pose
→ /odom

turtlesim_node
→ Gazebo TurtleBot3 plugin

rqt_graph 확인
→ TurtleBot3 node-topic graph 확인

launch 파일
→ Gazebo, TurtleBot3, RViz2 실행 관리 구조
```

---

## 16. 다음 채팅 시작 지점

다음 채팅에서는 아래 상태에서 시작하면 된다.

```text
현재 MissionBot-ROS2는 Phase 1. ROS2 basics를 완료했다.

완료한 것:
- missionbot_basic 패키지 생성
- pose_subscriber 작성
- velocity_publisher 작성
- service 호출 실습
- launch 파일 작성
- rqt_graph 확인
- experiment_log, troubleshooting, phase summary, docs/phases, handoff 정리

다음 목표:
- Phase 2. Gazebo + TurtleBot3 시작
- 첫 단계는 Gazebo TurtleBot3 empty_world 실행과 /cmd_vel, /odom, /scan topic 확인
```

---

