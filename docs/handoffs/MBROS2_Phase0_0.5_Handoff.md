# MissionBot-ROS2 Phase 0 / 0.5 인수인계 문서

> 목적: 이 문서는 다른 채팅창에서 MissionBot-ROS2 프로젝트를 바로 이어가기 위한 현재 상태 요약 문서다.  
> 이 문서와 아래의 이어가기 프롬프트만 있으면 Phase 1 시작 전 상태를 복원할 수 있도록 작성했다.

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

## 2. Phase 상태

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

기본 폴더 구조:

```text
missionbot-ros2/
├── README.md
├── .gitignore
├── docs/
│   └── 00_project_overview.md
├── notes/
│   ├── experiment_log.md
│   └── troubleshooting.md
├── configs/
├── maps/
├── results/
├── rosbags/
└── src/
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

아직 문서화로 마무리할 것:

```text
[ ] docs/01_environment_strategy.md 작성
[ ] notes/experiment_log.md에 Phase 0 / 0.5 성공 기록 추가
[ ] notes/troubleshooting.md에 주요 오류와 해결 과정 정리
[ ] git commit
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
VS Code Remote SSH

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

Main ROS2 Workspace:
~/turtlebot3_ws

MissionBot Project Location:
~/projects/missionbot-ros2
```

---

## 4. 매 작업 시작 시 기본 루틴

Ubuntu VM에서 ROS2/Gazebo 작업을 시작할 때는 보통 다음 순서로 확인한다.

```bash
source ~/.bashrc
echo $ROS_DISTRO
echo $TURTLEBOT3_MODEL
which ros2
which gazebo
ros2 pkg list | grep turtlebot3_gazebo
echo $DISPLAY
```

정상 기대값:

```text
humble
burger
/opt/ros/humble/bin/ros2
/usr/bin/gazebo
turtlebot3_gazebo
:0 또는 GUI 표시 가능한 DISPLAY 값
```

---

## 5. 현재 .bashrc 기준

중복 출력 문제는 해결했다.

최소한 아래 내용이 들어가 있어야 한다.

```bash
# ROS2 Humble 기본 환경
source /opt/ros/humble/setup.bash

# TurtleBot3 workspace가 빌드된 경우에만 적용
if [ -f "$HOME/turtlebot3_ws/install/setup.bash" ]; then
  source "$HOME/turtlebot3_ws/install/setup.bash"
fi

# TurtleBot3 기본 모델
export TURTLEBOT3_MODEL=burger

# Gazebo가 TurtleBot3 모델과 mesh 파일을 찾도록 경로 추가
if [ -d "$HOME/turtlebot3_ws/install/turtlebot3_gazebo/share/turtlebot3_gazebo/models" ]; then
  export GAZEBO_MODEL_PATH="$GAZEBO_MODEL_PATH:$HOME/turtlebot3_ws/install/turtlebot3_gazebo/share/turtlebot3_gazebo/models"
fi

if [ -d "$HOME/turtlebot3_ws/src/turtlebot3_simulations/turtlebot3_gazebo/models" ]; then
  export GAZEBO_MODEL_PATH="$GAZEBO_MODEL_PATH:$HOME/turtlebot3_ws/src/turtlebot3_simulations/turtlebot3_gazebo/models"
fi
```

---

## 6. 확인된 ROS2 / Gazebo 결과

## 6.1 TurtleBot3 Gazebo 실행

실행 명령:

```bash
source ~/.bashrc
export TURTLEBOT3_MODEL=burger
ros2 launch turtlebot3_gazebo empty_world.launch.py
```

확인 결과:

```text
TurtleBot3 Burger spawn 성공
Gazebo 화면에서 바퀴 두 개 달린 로봇 본체 확인
teleop_keyboard로 로봇 이동 확인
LiDAR ray 때문에 로봇이 잘 안 보일 수 있으나 확대하면 본체 확인 가능
```

---

## 6.2 teleop 실행

새 터미널:

```bash
source ~/.bashrc
ros2 run turtlebot3_teleop teleop_keyboard
```

조작:

```text
w: 앞으로
x: 뒤로
a: 왼쪽 회전
d: 오른쪽 회전
s: 정지
```

---

## 6.3 topic 확인

실행 명령:

```bash
source ~/.bashrc
ros2 topic list
```

확인된 주요 토픽:

```text
/clock
/cmd_vel
/imu
/joint_states
/odom
/parameter_events
/performance_metrics
/robot_description
/rosout
/scan
/tf
/tf_static
```

---

## 6.4 /odom 확인

실행 명령:

```bash
ros2 topic echo /odom --once
```

확인 결과:

```text
frame_id: odom
child_frame_id: base_footprint
pose.position.x / y 값 출력 확인
```

의미:

```text
Gazebo 안에서 TurtleBot3의 위치 변화가 ROS2 /odom 토픽으로 publish되고 있음
```

---

## 6.5 /scan 확인

실행 명령:

```bash
ros2 topic hz /scan
```

확인 결과:

```text
average rate: 약 4.95Hz ~ 4.97Hz
```

의미:

```text
LiDAR scan 데이터가 약 5Hz로 지속 publish되고 있음
```

---

## 6.6 /cmd_vel 연결 확인

실행 명령:

```bash
ros2 topic info /cmd_vel -v
```

확인 결과:

```text
Type: geometry_msgs/msg/Twist

Publisher count: 1
Node name: teleop_keyboard

Subscription count: 1
Node name: turtlebot3_diff_drive
```

의미:

```text
teleop_keyboard가 /cmd_vel을 publish하고,
Gazebo의 turtlebot3_diff_drive plugin이 /cmd_vel을 subscribe하고 있음.
따라서 키보드 입력 → /cmd_vel → Gazebo 로봇 이동 구조가 정상 동작함.
```

---

## 7. 해결한 주요 문제

## 7.1 NoMachine 흰 화면 / connection reset 문제

증상:

```text
MacBook NoMachine에서 Ubuntu VM 접속 시 흰 화면 또는 connection reset 발생
```

확인한 것:

```bash
nc -vz 100.95.184.79 4000
```

결과:

```text
Connection to 100.95.184.79 port 4000 succeeded
```

의미:

```text
MacBook에서 Ubuntu VM의 NoMachine 4000번 포트까지 도달 가능.
4000번 포트 문제는 아님.
```

NoMachine 서비스 확인:

```bash
sudo /usr/NX/bin/nxserver --status
```

재시작:

```bash
sudo /usr/NX/bin/nxserver --restart
```

재시작 후 확인된 상태:

```text
nxserver: Enabled
nxnode: Enabled
nxd: Enabled
```

결과:

```text
NoMachine GUI 접속 정상화
```

---

## 7.2 Gazebo에서 TurtleBot3 외형이 안 보이는 문제

증상:

```text
Gazebo에서 로봇이 움직이지만 본체가 잘 안 보임
파란 부채꼴 형태의 LiDAR ray만 크게 보임
```

확인한 것:

```bash
find ~/turtlebot3_ws -name burger_base.stl
find ~/turtlebot3_ws -name lds.stl
find ~/turtlebot3_ws -name left_tire.stl
```

mesh 파일은 실제로 존재했다.

해결:

```bash
export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:$HOME/turtlebot3_ws/install/turtlebot3_gazebo/share/turtlebot3_gazebo/models
export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:$HOME/turtlebot3_ws/src/turtlebot3_simulations/turtlebot3_gazebo/models
```

결과:

```text
Gazebo가 TurtleBot3 mesh/model 경로를 찾을 수 있게 됨.
확대 후 바퀴 두 개 달린 TurtleBot3 Burger 본체 확인.
```

주의:

```text
LiDAR ray가 크게 보이므로 처음에는 로봇 본체가 안 보이는 것처럼 느껴질 수 있다.
Gazebo에서 확대하거나 시점을 바꿔야 본체가 잘 보인다.
```

---

## 7.3 gzclient crash 문제

증상:

```text
gzclient: gazebo::rendering::Camera Assertion `px != 0' failed.
gzclient process died
```

판단:

```text
gzserver, spawn_entity, /cmd_vel, /odom, /scan은 정상.
문제는 Gazebo GUI 클라이언트 gzclient 또는 GUI plugin 충돌에 가까움.
```

우회 방법:

```bash
gzclient --verbose
```

또는 필요 시:

```bash
QT_X11_NO_MITSHM=1 LIBGL_ALWAYS_SOFTWARE=1 gzclient --verbose
```

현재는 NoMachine 및 Gazebo 화면이 정상적으로 뜨고 TurtleBot3 이동까지 확인했다.

---

## 8. Phase 0.5 완료 판정

기능 기준으로는 Phase 0.5 완료로 본다.

완료 기준:

```text
[x] MacBook에서 NoMachine으로 Ubuntu VM GUI 접속
[x] VS Code Remote SSH 연결 가능
[x] ROS2 Humble 활성화
[x] Gazebo Classic 실행
[x] TurtleBot3 Gazebo 패키지 인식
[x] TurtleBot3 Burger spawn
[x] teleop 이동
[x] /cmd_vel 연결 확인
[x] /odom 확인
[x] /scan 확인
[x] Gazebo에서 실제 TurtleBot3 본체 확인
```

남은 마감 작업:

```text
[ ] RViz2 실행 확인
[ ] rosbag2 record/info 짧은 테스트
[ ] docs/01_environment_strategy.md 작성
[ ] notes/experiment_log.md 업데이트
[ ] notes/troubleshooting.md 업데이트
[ ] git commit
```

---

## 9. Phase 1 진입 전 마지막 체크

Phase 1로 넘어가기 직전 아래만 확인하면 된다.

```bash
source ~/.bashrc
echo $ROS_DISTRO
echo $TURTLEBOT3_MODEL
which ros2
which gazebo
ros2 pkg list | grep turtlebot3_gazebo
```

그리고 가능하면 RViz2 실행:

```bash
rviz2
```

rosbag2 확인:

```bash
mkdir -p ~/test_rosbags
cd ~/test_rosbags
ros2 bag record /cmd_vel /odom /scan -o test_tb3_basic
```

5초 후 Ctrl + C:

```bash
ros2 bag info test_tb3_basic
```

---

## 10. 다음 단계

다음은 Phase 1로 넘어간다.

Phase 1의 시작 목표:

```text
ROS2 workspace 확인 또는 생성
missionbot_basic 패키지 생성
turtlesim 실행
/turtle1/pose topic 확인
Python으로 pose_subscriber 노드 직접 작성
setup.py entry_points 등록
colcon build
source 적용
ros2 run으로 실행
rqt_graph로 연결 확인
```

첫 번째로 할 일은 너무 앞서가지 말고 아래 중 하나다.

```text
1. MissionBot-ROS2 프로젝트 안에 ROS2 workspace를 어디에 둘지 확인
2. missionbot_ws/src 구조 생성
3. missionbot_basic Python 패키지 생성
4. turtlesim /turtle1/pose 구독 실습
```

추천 시작점:

```text
Phase 1-1: ROS2 workspace 구조 확인 및 missionbot_basic 패키지 생성
```

---