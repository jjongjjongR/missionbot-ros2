# MissionBot-ROS2 Phase 2 인수인계 문서

> 목적: 이 문서는 MissionBot-ROS2 프로젝트의 Phase 2. Gazebo + TurtleBot3 완료 상태를 정리하고, 다른 채팅창에서 Phase 3. RViz2 + TF2를 바로 이어가기 위한 인수인계 문서다.
> 이 문서와 아래의 이어가기 프롬프트만 있으면 Phase 2 완료 상태를 복원하고 Phase 3를 시작할 수 있다.

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

Phase 1 완료 의미:

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

## Phase 2. Gazebo + TurtleBot3

상태: 완료

완료한 것:

```text
[x] 기존 turtlesim 관련 노드가 남아 있지 않은 것 확인
[x] ROS2 Humble 환경 확인
[x] TURTLEBOT3_MODEL=burger 확인
[x] ros2 실행 경로 확인
[x] gazebo 실행 경로 확인
[x] turtlebot3_gazebo 패키지 인식 확인
[x] turtlebot3_teleop 패키지 인식 확인
[x] MissionBot 프로젝트 루트 확인
[x] Gazebo TurtleBot3 empty_world 실행
[x] TurtleBot3 Burger spawn 확인
[x] gzclient crash 발생 확인
[x] gzserver와 ROS2 topic은 살아 있는 것 확인
[x] gzclient --verbose로 Gazebo GUI 재연결
[x] /cmd_vel topic 확인
[x] /odom topic 확인
[x] /scan topic 확인
[x] teleop_keyboard 실행
[x] 키보드 입력으로 TurtleBot3 이동 확인
[x] /cmd_vel publisher/subscriber 연결 확인
[x] /cmd_vel 실제 Twist 메시지 값 확인
[x] /odom 메시지 출력 확인
[x] TurtleBot3 이동 전후 /odom position 값 변화 확인
[x] /scan LaserScan 메시지 출력 확인
[x] rqt_graph로 /teleop_keyboard → /cmd_vel → Gazebo/TurtleBot3 연결 확인
[x] 실행 후 노드와 토픽 정리 흐름 확인
```

Phase 2 완료 판정:

```text
Phase 2는 Gazebo + TurtleBot3 기본 구조 학습 기준으로 완료로 본다.
TurtleBot3 Burger를 Gazebo empty_world에 spawn했고, /cmd_vel, /odom, /scan을 중심으로 이동로봇 시뮬레이션의 기본 topic 구조를 확인했다.
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

현재 프로젝트 루트에서 확인된 폴더:

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

Phase 2에서 TurtleBot3 Gazebo만 실행할 때는 `.bashrc`로 TurtleBot3 환경이 잡혀 있으면 충분했다.

---

## 6. Phase 2 시작 전 환경 확인 결과

Phase 2 시작 전 아래 명령어로 환경을 확인했다.

```bash
ros2 node list
echo $ROS_DISTRO
echo $TURTLEBOT3_MODEL
which ros2
which gazebo
ros2 pkg list | grep turtlebot3_gazebo
ros2 pkg list | grep turtlebot3_teleop
cd ~/projects/missionbot-ros2
pwd
ls
```

확인된 결과:

```text
ros2 node list
→ 기존 노드 없음

echo $ROS_DISTRO
→ humble

echo $TURTLEBOT3_MODEL
→ burger

which ros2
→ /opt/ros/humble/bin/ros2

which gazebo
→ /usr/bin/gazebo

ros2 pkg list | grep turtlebot3_gazebo
→ turtlebot3_gazebo

ros2 pkg list | grep turtlebot3_teleop
→ turtlebot3_teleop

pwd
→ /home/user/projects/missionbot-ros2
```

이 결과를 기준으로 Phase 2 Gazebo TurtleBot3 실행 준비가 완료된 것으로 판단했다.

---

## 7. Phase 2에서 실행한 주요 명령어

## 7.1 TurtleBot3 empty_world 실행

```bash
ros2 launch turtlebot3_gazebo empty_world.launch.py
```

의미:

```text
turtlebot3_gazebo 패키지 안의 empty_world.launch.py를 실행한다.
Gazebo 빈 월드에 TurtleBot3 Burger를 spawn한다.
```

확인한 주요 로그:

```text
Spawn status: SpawnEntity: Successfully spawned entity [burger]
```

이 로그를 통해 TurtleBot3 Burger가 Gazebo 서버 안에 정상 생성된 것을 확인했다.

---

## 7.2 Gazebo GUI 재연결

처음 launch 실행 중 `gzclient`가 crash 되었다.

오류 메시지:

```text
gzclient: Assertion `px != 0' failed.
[ERROR] [gzclient-2]: process has died
```

하지만 Gazebo 서버와 TurtleBot3 topic은 살아 있었다.

확인 명령:

```bash
ros2 topic list | grep -E "cmd_vel|odom|scan"
```

확인 결과:

```text
/cmd_vel
/odom
/scan
```

이후 새 터미널에서 아래 명령어로 GUI를 다시 연결했다.

```bash
gzclient --verbose
```

확인한 주요 로그:

```text
Connected to gazebo master @ http://127.0.0.1:11345
```

판단:

```text
문제는 TurtleBot3 spawn 실패가 아니라 Gazebo GUI 클라이언트인 gzclient 쪽 문제였다.
gzserver는 살아 있었고, ROS2 topic도 정상적으로 생성되어 있었다.
```

---

## 7.3 TurtleBot3 teleop 실행

```bash
ros2 run turtlebot3_teleop teleop_keyboard
```

역할:

```text
키보드 입력을 읽고 geometry_msgs/msg/Twist 메시지로 바꿔 /cmd_vel topic으로 publish한다.
```

확인한 흐름:

```text
키보드 입력
→ teleop_keyboard
→ /cmd_vel
→ turtlebot3_diff_drive
→ TurtleBot3 이동
```

확인한 조작:

```text
w: 앞으로 이동
x: 뒤로 이동
a: 왼쪽 회전
d: 오른쪽 회전
s: 정지
```

---

## 7.4 /cmd_vel 확인

확인 명령:

```bash
ros2 topic info /cmd_vel
ros2 topic echo /cmd_vel
```

확인한 내용:

```text
/cmd_vel은 geometry_msgs/msg/Twist 타입이다.
teleop_keyboard가 /cmd_vel을 publish한다.
Gazebo TurtleBot3 쪽 diff drive plugin이 /cmd_vel을 subscribe한다.
w, a, d, s 키 입력에 따라 linear.x와 angular.z 값이 변했다.
```

핵심 의미:

```text
/cmd_vel은 이동로봇의 속도 명령 topic이다.
linear.x는 전진/후진 속도, angular.z는 회전 속도를 의미한다.
```

---

## 7.5 /odom 확인

확인 명령:

```bash
ros2 topic info /odom
ros2 topic echo /odom --once
```

확인한 내용:

```text
/odom은 nav_msgs/msg/Odometry 타입이다.
TurtleBot3 이동 전후로 pose.pose.position.x 또는 pose.pose.position.y 값이 변했다.
```

중요하게 본 항목:

```text
header.frame_id: odom
child_frame_id: base_footprint
pose.pose.position.x
pose.pose.position.y
```

핵심 의미:

```text
/odom은 로봇의 위치, 자세, 속도 추정 정보를 담는 topic이다.
Phase 1의 /turtle1/pose가 turtlesim 위치 정보였다면, Phase 2의 /odom은 실제 이동로봇 구조에 가까운 위치 추정 topic이다.
```

---

## 7.6 /scan 확인

확인 명령:

```bash
ros2 topic info /scan
ros2 topic echo /scan --once
```

확인한 내용:

```text
/scan은 sensor_msgs/msg/LaserScan 타입이다.
LaserScan 메시지가 정상 출력되는 것을 확인했다.
```

중요하게 본 항목:

```text
angle_min
angle_max
angle_increment
range_min
range_max
ranges
```

핵심 의미:

```text
/scan은 TurtleBot3의 LiDAR 센서 데이터 topic이다.
ranges는 각 방향에 대한 거리 배열이다.
inf 값은 해당 방향에 측정 가능한 장애물이 없거나 너무 멀다는 뜻으로 볼 수 있다.
```

---

## 7.7 rqt_graph 확인

실행 명령:

```bash
rqt_graph
```

확인한 연결:

```text
/teleop_keyboard
→ /cmd_vel
→ Gazebo/TurtleBot3 관련 node
```

의미:

```text
단순히 topic 이름만 확인한 것이 아니라, 실제 publisher와 subscriber 연결 구조를 시각적으로 확인했다.
```

---

## 8. Phase 2에서 배운 핵심 개념

## 8.1 Gazebo는 gzserver와 gzclient로 나뉜다

```text
gzserver
→ 실제 시뮬레이션 서버
→ 물리 계산, 센서, 로봇 plugin, topic 발행 담당

gzclient
→ 사람이 보는 Gazebo GUI
→ 창, 카메라, 모델 시각화 담당
```

이번 Phase에서 `gzclient`가 죽어도 `gzserver`는 살아 있었고, TurtleBot3 topic도 정상적으로 존재했다.

---

## 8.2 /cmd_vel

```text
/cmd_vel
→ 로봇에게 속도 명령을 보내는 topic
→ geometry_msgs/msg/Twist 타입
```

주요 필드:

```text
linear.x
→ 전진/후진 속도

angular.z
→ 회전 속도
```

---

## 8.3 /odom

```text
/odom
→ 로봇 위치, 자세, 속도 추정 정보를 담는 topic
→ nav_msgs/msg/Odometry 타입
```

주요 필드:

```text
header.frame_id: odom
child_frame_id: base_footprint
pose.pose.position.x
pose.pose.position.y
```

---

## 8.4 /scan

```text
/scan
→ TurtleBot3 LiDAR 거리 센서 데이터 topic
→ sensor_msgs/msg/LaserScan 타입
```

주요 필드:

```text
angle_min
angle_max
angle_increment
range_min
range_max
ranges
```

---

## 8.5 rqt_graph

```text
rqt_graph
→ 현재 실행 중인 ROS2 node와 topic 연결 구조를 시각적으로 보여주는 도구
```

이번 Phase에서는 `/teleop_keyboard → /cmd_vel → Gazebo/TurtleBot3` 연결을 확인했다.

---

## 9. Phase 1과 Phase 2의 연결

Phase 1에서 배운 turtlesim 구조:

```text
/velocity_publisher
→ /turtle1/cmd_vel
→ /turtlesim
→ /turtle1/pose
→ /pose_subscriber
```

Phase 2에서 확인한 TurtleBot3 구조:

```text
/teleop_keyboard
→ /cmd_vel
→ TurtleBot3 diff drive
→ /odom

TurtleBot3 LiDAR
→ /scan
```

연결 의미:

```text
/turtle1/cmd_vel
→ /cmd_vel

/turtle1/pose
→ /odom

turtlesim_node
→ Gazebo TurtleBot3 plugin

rqt_graph 확인
→ TurtleBot3 node-topic graph 확인
```

즉, Phase 1에서 배운 publisher, subscriber, topic, launch 개념이 Phase 2에서 Gazebo TurtleBot3 구조로 확장되었다.

---

## 10. Phase 2에서 발생한 주요 이슈

## 10.1 gzclient crash

발생 상황:

```bash
ros2 launch turtlebot3_gazebo empty_world.launch.py
```

오류 메시지:

```text
gzclient: /usr/include/boost/smart_ptr/shared_ptr.hpp:728:
Assertion `px != 0' failed.
[ERROR] [gzclient-2]: process has died
```

동시에 확인된 정상 로그:

```text
Spawn status: SpawnEntity: Successfully spawned entity [burger]
[turtlebot3_diff_drive]: Subscribed to [/cmd_vel]
[turtlebot3_diff_drive]: Advertise odometry on [/odom]
[turtlebot3_diff_drive]: Publishing odom transforms between [odom] and [base_footprint]
```

원인 판단:

```text
TurtleBot3 spawn 실패가 아니라 Gazebo GUI 클라이언트인 gzclient 문제로 판단했다.
gzserver와 ROS2 topic은 정상적으로 살아 있었다.
```

확인 명령:

```bash
ros2 topic list | grep -E "cmd_vel|odom|scan"
```

확인 결과:

```text
/cmd_vel
/odom
/scan
```

해결 방법:

```bash
gzclient --verbose
```

해결 결과:

```text
Gazebo master에 다시 연결되었고, Gazebo GUI를 다시 확인할 수 있었다.
```

추가 참고:

```text
같은 문제가 반복되면 VMware + NoMachine + Gazebo GUI 렌더링 문제일 가능성이 있다.
필요할 경우 다음 우회 명령을 검토할 수 있다.

QT_X11_NO_MITSHM=1 LIBGL_ALWAYS_SOFTWARE=1 gzclient --verbose
```

---

## 11. Phase 2 기록 상태

이번 Phase에서 수행한 대부분의 작업은 실험이라기보다 다음에 해당한다.

```text
환경 확인
Gazebo 실행 확인
topic 구조 확인
메시지 타입 확인
기본 이동 확인
```

따라서 `notes/experiment_log.md`에는 무리하게 기록하지 않는다.

기록 기준:

```text
experiment_log.md
→ 특정 목표를 가진 주행 실험, 조건 비교, rosbag 저장, 실패 재현, 결과 분석 등을 기록

docs/phases/
→ Phase에서 배운 개념과 진행 내용을 정리

notes/troubleshooting.md
→ 반복 가능성이 있는 오류와 해결 과정을 정리
```

Phase 2에서 문서화할 수 있는 파일:

```text
docs/phases/phase02_gazebo_turtlebot3.md
docs/handoffs/MBROS2_Phase2_Handoff.md
```

troubleshooting 후보:

```text
notes/troubleshooting.md
→ TS-0003_gzclient_camera_assertion_failed
```

단, 사용자가 실제로 파일에 기록하기 전까지는 기록 완료로 단정하지 않는다.

---

## 12. Phase 2 완료 판정

Phase 2는 다음 기준을 만족했으므로 완료로 판단한다.

```text
[x] ROS2 Humble 환경 확인
[x] TurtleBot3 Burger 모델 환경 확인
[x] turtlebot3_gazebo 패키지 인식 확인
[x] turtlebot3_teleop 패키지 인식 확인
[x] Gazebo empty_world 실행
[x] TurtleBot3 Burger spawn 확인
[x] /cmd_vel topic 확인
[x] /odom topic 확인
[x] /scan topic 확인
[x] teleop_keyboard로 TurtleBot3 이동 확인
[x] /cmd_vel Twist 메시지 확인
[x] /odom Odometry 메시지 확인
[x] TurtleBot3 이동 전후 /odom 값 변화 확인
[x] /scan LaserScan 메시지 확인
[x] rqt_graph로 node-topic 연결 확인
[x] gzclient crash 원인 분리 및 GUI 재연결 확인
```

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

---

## 13. 다음 Phase 시작 목표

다음 Phase:

```text
Phase 3. RViz2 + TF2
```

Phase 3의 핵심 목표:

```text
Gazebo에서 실행 중인 TurtleBot3를 RViz2에서 시각화하고, TF2를 통해 로봇 좌표계 구조를 확인한다.
```

첫 번째로 할 일:

```text
RViz2 실행 전 현재 환경과 TurtleBot3 Gazebo 상태를 확인한다.
```

이후 확인할 것:

```text
RViz2 실행
Fixed Frame 설정
RobotModel 표시
LaserScan 표시
/tf topic 확인
/tf_static topic 확인
odom → base_footprint → base_link → base_scan 좌표계 연결 확인
TF tree 확인
```

---

## 14. Phase 3 시작 전 확인 명령

새 터미널에서 확인:

```bash
echo $ROS_DISTRO
echo $TURTLEBOT3_MODEL
which ros2
which gazebo
which rviz2
ros2 pkg list | grep turtlebot3_gazebo
```

정상 기대값:

```text
humble
burger
/opt/ros/humble/bin/ros2
/usr/bin/gazebo
/opt/ros/humble/bin/rviz2
turtlebot3_gazebo
```

Gazebo TurtleBot3 실행:

```bash
ros2 launch turtlebot3_gazebo empty_world.launch.py
```

필요 시 GUI 재연결:

```bash
gzclient --verbose
```

주요 topic 확인:

```bash
ros2 topic list | grep -E "cmd_vel|odom|scan|tf"
```

정상 기대값:

```text
/cmd_vel
/odom
/scan
/tf
/tf_static
```

---

## 15. Phase 3에서 주의할 점

```text
Phase 3에서는 SLAM, Nav2, MoveIt2로 앞서가지 않는다.
우선 RViz2와 TF2만 집중한다.
```

Phase 2와 Phase 3의 연결:

```text
Phase 2
→ Gazebo에서 TurtleBot3가 움직이고 /cmd_vel, /odom, /scan이 나오는지 확인

Phase 3
→ RViz2에서 TurtleBot3 모델, LaserScan, TF 좌표계를 시각적으로 확인
```

중요한 연결:

```text
/odom
→ 로봇 위치 변화 정보

/scan
→ LiDAR 거리 센서 정보

/tf, /tf_static
→ odom, base_footprint, base_link, base_scan 같은 좌표계 관계 정보
```

---

## 16. 다음 채팅 시작 지점

다음 채팅에서는 아래 상태에서 시작하면 된다.

```text
현재 MissionBot-ROS2는 Phase 2. Gazebo + TurtleBot3를 완료했다.

완료한 것:
- ROS2 Humble, TurtleBot3 Burger 환경 확인
- turtlebot3_gazebo, turtlebot3_teleop 패키지 확인
- Gazebo TurtleBot3 empty_world 실행
- TurtleBot3 Burger spawn 확인
- gzclient crash 발생 후 gzclient --verbose로 GUI 재연결
- /cmd_vel topic 확인
- teleop_keyboard로 TurtleBot3 이동 확인
- /cmd_vel Twist 메시지 확인
- /odom Odometry 메시지 확인
- TurtleBot3 이동 전후 /odom 값 변화 확인
- /scan LaserScan 메시지 확인
- rqt_graph로 /teleop_keyboard → /cmd_vel → Gazebo/TurtleBot3 연결 확인

다음 목표:
- Phase 3. RViz2 + TF2 시작
- 첫 단계는 RViz2 실행 전 환경 확인과 TurtleBot3 Gazebo 재실행 준비
```

추천 시작점:

```text
Phase 3-1. RViz2 / TF2 시작 전 환경 확인
```

첫 단계에서 할 일:

```text
1. 기존 Gazebo/TurtleBot3 관련 노드가 남아 있지 않은지 확인
2. ROS2 Humble 환경 확인
3. TURTLEBOT3_MODEL=burger 확인
4. rviz2 실행 파일 인식 확인
5. turtlebot3_gazebo 패키지 인식 확인
6. Gazebo TurtleBot3 empty_world 재실행 준비
7. /tf, /tf_static을 다음 단계에서 확인할 준비
```
