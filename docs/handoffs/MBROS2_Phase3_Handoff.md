# MissionBot-ROS2 Phase 3 인수인계 문서

> 목적: 이 문서는 MissionBot-ROS2 프로젝트의 Phase 3. RViz2 + TF2 완료 상태를 정리하고, 다른 채팅창에서 Phase 4. SLAM을 바로 이어가기 위한 인수인계 문서다.
> 이 문서와 아래의 이어가기 프롬프트만 있으면 Phase 3 완료 상태를 복원하고 Phase 4를 시작할 수 있다.

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

Phase 2 완료 의미:

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

## Phase 3. RViz2 + TF2

상태: 완료

완료한 것:

```text
[x] RViz2 실행 전 환경 확인
[x] ROS2 Humble 확인
[x] TURTLEBOT3_MODEL=burger 확인
[x] ros2 실행 경로 확인
[x] gazebo 실행 경로 확인
[x] rviz2 실행 경로 확인
[x] turtlebot3_gazebo 패키지 인식 확인
[x] turtlebot3_teleop 패키지 인식 확인
[x] MissionBot 프로젝트 루트 확인
[x] Gazebo TurtleBot3 empty_world 실행
[x] TurtleBot3 Burger spawn 확인
[x] gzclient crash 발생 확인
[x] gzserver와 ROS2 topic은 살아 있는 것 확인
[x] /cmd_vel topic 확인
[x] /odom topic 확인
[x] /scan topic 확인
[x] /tf topic 확인
[x] /tf_static topic 확인
[x] /tf, /tf_static 메시지 타입 확인
[x] RViz2 실행
[x] Fixed Frame을 odom으로 설정
[x] TF display 추가
[x] TF 좌표축 확인
[x] RobotModel display 추가
[x] TurtleBot3 Burger 모델 표시 확인
[x] LaserScan display 추가
[x] LaserScan Topic을 /scan으로 설정
[x] /scan ranges가 empty_world에서 inf 위주로 나오는 것 확인
[x] view_frames로 TF tree 생성
[x] frames.pdf 확인
[x] odom → base_footprint → base_link → base_scan 연결 확인
[x] tf2_echo로 odom → base_footprint transform 확인
[x] tf2_echo로 base_link → base_scan transform 확인
[x] teleop 이동 중 odom → base_footprint transform 변화 확인
[x] RViz2에서 RobotModel / TF 좌표계 움직임 확인
```

Phase 3 완료 의미:

```text
Gazebo에서 생성되는 TurtleBot3의 topic과 TF 정보를 RViz2에서 시각화했다.

Gazebo TurtleBot3
→ /cmd_vel
→ /odom
→ /scan
→ /tf, /tf_static
→ RViz2

위 흐름을 확인했고, 다음 Phase인 SLAM에서 /scan과 TF가 왜 중요한지 이해할 준비가 되었다.
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

TurtleBot3 Gazebo, RViz2, SLAM Toolbox 같은 외부 ROS2 패키지를 실행할 때는 `.bashrc`로 기본 ROS2/TurtleBot3 환경이 잡혀 있으면 충분한 경우가 많다.

---

## 6. Phase 3 시작 전 환경 확인 결과

Phase 3 시작 전 아래 명령어로 환경을 확인했다.

```bash
ros2 node list
echo $ROS_DISTRO
echo $TURTLEBOT3_MODEL
which ros2
which gazebo
which rviz2
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

which rviz2
→ /opt/ros/humble/bin/rviz2

ros2 pkg list | grep turtlebot3_gazebo
→ turtlebot3_gazebo

ros2 pkg list | grep turtlebot3_teleop
→ turtlebot3_teleop

pwd
→ /home/user/projects/missionbot-ros2
```

이 결과를 기준으로 Phase 3 RViz2 + TF2 실행 준비가 완료된 것으로 판단했다.

---

## 7. Phase 3에서 실행한 주요 명령어

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
[turtlebot3_diff_drive]: Subscribed to [/cmd_vel]
[turtlebot3_diff_drive]: Advertise odometry on [/odom]
[turtlebot3_diff_drive]: Publishing odom transforms between [odom] and [base_footprint]
```

이 로그를 통해 TurtleBot3 Burger가 Gazebo 서버 안에 정상 생성되었고, odom 관련 TF 발행까지 시작된 것을 확인했다.

---

## 7.2 주요 topic 확인

```bash
ros2 topic list | grep -E "cmd_vel|odom|scan|tf"
```

확인 결과:

```text
/cmd_vel
/odom
/scan
/tf
/tf_static
```

의미:

```text
/cmd_vel
→ TurtleBot3 속도 명령 topic

/odom
→ TurtleBot3 위치, 자세, 속도 추정 topic

/scan
→ TurtleBot3 LiDAR LaserScan topic

/tf
→ 계속 변하는 좌표계 관계 topic

/tf_static
→ 고정된 좌표계 관계 topic
```

---

## 7.3 /tf, /tf_static 확인

```bash
ros2 topic info /tf
ros2 topic info /tf_static
```

확인 결과:

```text
/tf
Type: tf2_msgs/msg/TFMessage
Publisher count: 2
Subscription count: 0

/tf_static
Type: tf2_msgs/msg/TFMessage
Publisher count: 1
Subscription count: 0
```

해석:

```text
/tf
→ 동적으로 변하는 좌표계 관계를 발행한다.
→ 예: odom → base_footprint

/tf_static
→ 정적으로 고정된 좌표계 관계를 발행한다.
→ 예: base_link → base_scan
```

`Subscription count: 0`은 RViz2를 켜기 전이라 구독자가 없다는 뜻으로 판단했다.
RViz2에서 TF display를 추가하면 RViz2가 `/tf`, `/tf_static`을 구독할 수 있다.

---

## 7.4 RViz2 실행

```bash
rviz2
```

RViz2에서 설정한 것:

```text
Global Options
→ Fixed Frame: odom
```

`Fixed Frame`을 `odom`으로 설정한 이유:

```text
현재 Phase에서는 SLAM을 하지 않았기 때문에 map frame이 없다.
Gazebo TurtleBot3는 odom 기준으로 로봇 위치와 TF를 발행한다.
따라서 RViz2의 기준 좌표계는 odom으로 설정하는 것이 적절하다.
```

---

## 7.5 TF display 추가

RViz2 설정:

```text
Add
→ By display type
→ TF
→ OK
```

확인한 frame:

```text
odom
base_footprint
base_link
base_scan
imu_link
wheel_left_link
wheel_right_link
caster_back_link
```

의미:

```text
TurtleBot3의 이동 기준 좌표계, 본체 좌표계, 센서 좌표계, 바퀴 좌표계가 RViz2에서 확인되었다.
```

---

## 7.6 RobotModel display 추가

RViz2 설정:

```text
Add
→ By display type
→ RobotModel
→ OK
```

설정값:

```text
Description Source: Topic
Description Topic: /robot_description
```

확인한 것:

```text
TurtleBot3 Burger 본체 모델이 RViz2에 표시되었다.
TF 좌표계 위에 로봇 모델이 정상적으로 연결되었다.
```

의미:

```text
TF는 로봇의 좌표계 뼈대이고, RobotModel은 그 좌표계 구조에 로봇 외형을 입히는 역할을 한다.
```

---

## 7.7 LaserScan display 추가

RViz2 설정:

```text
Add
→ By display type
→ LaserScan
→ OK

Topic: /scan
Style: Points
```

확인한 것:

```text
LaserScan display 추가 성공
Topic /scan 설정 성공
Style을 Points로 설정
에러 없음
```

다만 empty_world에서는 주변 장애물이나 벽이 거의 없기 때문에 RViz2에서 LiDAR 점이 잘 보이지 않았다.

확인 명령:

```bash
ros2 topic echo /scan --once --field ranges | head -n 20
```

확인 결과:

```text
inf 위주로 출력됨
```

판단:

```text
/scan이 죽은 것이 아니다.
empty_world에서 LiDAR가 감지할 물체가 거의 없기 때문에 ranges 값이 inf 위주로 나온 것이다.
따라서 RViz2에 찍힐 실제 점도 거의 없을 수 있다.
```

---

## 7.8 TF tree 확인

실행 명령:

```bash
ros2 run tf2_tools view_frames
```

생성 파일:

```text
frames.pdf
```

확인한 구조:

```text
odom
→ base_footprint
→ base_link
→ base_scan
```

추가로 확인한 링크:

```text
base_link
→ imu_link

base_link
→ wheel_left_link

base_link
→ wheel_right_link

base_link
→ caster_back_link
```

의미:

```text
TurtleBot3의 이동 기준 좌표계, 본체 좌표계, LiDAR 좌표계, 바퀴 좌표계가 하나의 TF tree로 연결되어 있음을 확인했다.
```

---

## 7.9 특정 transform 직접 조회

실행 명령 1:

```bash
ros2 run tf2_ros tf2_echo odom base_footprint
```

확인한 것:

```text
odom 기준 base_footprint의 Translation과 Rotation 출력
```

의미:

```text
로봇이 odom 기준에서 어디에 있는지 확인하는 transform이다.
로봇이 움직이면 이 값은 변한다.
```

실행 명령 2:

```bash
ros2 run tf2_ros tf2_echo base_link base_scan
```

확인한 것:

```text
base_link 기준 base_scan의 Translation과 Rotation 출력
```

의미:

```text
LiDAR가 로봇 본체 기준 어디에 붙어 있는지 확인하는 transform이다.
LiDAR는 로봇 본체에 고정되어 있으므로 이 값은 거의 고정된다.
```

---

## 7.10 teleop 이동 중 TF 변화 확인

터미널 구성:

```text
터미널 1
→ ros2 launch turtlebot3_gazebo empty_world.launch.py

터미널 2
→ rviz2

터미널 3
→ ros2 run tf2_ros tf2_echo odom base_footprint

터미널 4
→ ros2 run turtlebot3_teleop teleop_keyboard
```

teleop 실행 명령:

```bash
ros2 run turtlebot3_teleop teleop_keyboard
```

조작:

```text
w: 전진
x: 후진
a: 왼쪽 회전
d: 오른쪽 회전
s: 정지
```

확인한 것:

```text
teleop 입력으로 TurtleBot3 이동 명령을 발행했다.
odom → base_footprint transform의 Translation 또는 Rotation 값이 변했다.
RViz2에서도 로봇 모델과 TF 좌표계 움직임을 확인했다.
```

의미:

```text
teleop_keyboard
→ /cmd_vel
→ turtlebot3_diff_drive
→ /odom
→ /tf
→ RViz2 시각화

위 흐름이 정상적으로 연결되어 있음을 확인했다.
```

---

## 8. Phase 3에서 배운 핵심 개념

## 8.1 RViz2

```text
RViz2는 시뮬레이터가 아니라 ROS2 데이터 시각화 도구다.
Gazebo가 가상 세계를 실행한다면, RViz2는 ROS2 topic, TF, 로봇 모델, 센서 데이터를 시각적으로 보여준다.
```

---

## 8.2 Fixed Frame

```text
RViz2가 모든 데이터를 그릴 기준 좌표계다.
현재는 SLAM을 하지 않았기 때문에 map frame이 없고, odom을 Fixed Frame으로 사용했다.
```

---

## 8.3 TF2

```text
TF2는 ROS2에서 좌표계 사이의 관계를 관리하는 시스템이다.
로봇 본체, LiDAR, IMU, 바퀴 같은 요소들이 각각 어떤 위치 관계를 갖는지 표현한다.
```

---

## 8.4 /tf

```text
계속 변하는 좌표계 관계를 담는 topic이다.
예: odom → base_footprint
```

---

## 8.5 /tf_static

```text
고정된 좌표계 관계를 담는 topic이다.
예: base_link → base_scan
```

---

## 8.6 RobotModel

```text
RViz2에서 로봇의 URDF 기반 외형을 보여주는 Display다.
TF 좌표계 구조 위에 로봇 모델을 연결해 보여준다.
```

---

## 8.7 LaserScan

```text
2D LiDAR 거리 센서 데이터다.
TurtleBot3에서는 /scan topic으로 발행된다.
empty_world에서는 감지할 물체가 거의 없어 ranges 값이 inf 위주로 나올 수 있다.
```

---

## 8.8 TF tree

```text
좌표계 사이의 부모-자식 관계를 나무 구조처럼 나타낸 것이다.
Phase 3에서는 view_frames로 frames.pdf를 생성해 TF tree를 확인했다.
```

---

## 8.9 tf2_echo

```text
두 좌표계 사이의 transform을 숫자로 직접 확인하는 도구다.
Phase 3에서는 odom → base_footprint, base_link → base_scan 관계를 확인했다.
```

---

## 9. Phase 2와 Phase 3의 연결

Phase 2에서 확인한 것:

```text
/cmd_vel
→ 로봇 이동 명령

/odom
→ 로봇 위치 추정

/scan
→ LiDAR 거리 센서
```

Phase 3에서 확인한 것:

```text
/tf
→ 움직이는 좌표계 관계

/tf_static
→ 고정 좌표계 관계

RViz2
→ /odom, /scan, /tf, /robot_description을 시각화
```

연결 의미:

```text
Phase 2에서는 데이터가 topic으로 흐르는지 확인했다.
Phase 3에서는 그 topic 데이터가 어떤 좌표계 기준으로 해석되고, RViz2에서 어떻게 보이는지 확인했다.
```

---

## 10. Phase 3에서 발생한 주요 이슈

## 10.1 gzclient crash

발생 상황:

```bash
ros2 launch turtlebot3_gazebo empty_world.launch.py
```

오류 메시지:

```text
[gzclient-2] libcurl: (6) Could not resolve host: fuel.ignitionrobotics.org
[gzclient-2] gzclient: /usr/include/boost/smart_ptr/shared_ptr.hpp:728:
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

원인 판단:

```text
TurtleBot3 spawn 실패가 아니라 Gazebo GUI 클라이언트인 gzclient 문제로 판단했다.
gzserver와 ROS2 topic은 정상적으로 살아 있었다.
```

확인 명령:

```bash
ros2 topic list | grep -E "cmd_vel|odom|scan|tf"
```

확인 결과:

```text
/cmd_vel
/odom
/scan
/tf
/tf_static
```

대응:

```text
Gazebo GUI에 의존하지 않고 RViz2 중심으로 진행했다.
Phase 3에서는 Gazebo GUI가 아니라 RViz2에서 TF, RobotModel, LaserScan을 확인했다.
```

필요 시 우회 명령:

```bash
gzclient --verbose
```

또는:

```bash
QT_X11_NO_MITSHM=1 LIBGL_ALWAYS_SOFTWARE=1 gzclient --verbose
```

단, 현재까지는 RViz2 중심 진행으로 충분했다.

---

## 10.2 LaserScan 점이 보이지 않음

상황:

```text
LaserScan display 추가 성공
Topic: /scan 설정 성공
Style: Points 설정 성공
에러 없음
하지만 RViz2 화면에서 LiDAR 점이 잘 보이지 않음
```

확인 명령:

```bash
ros2 topic echo /scan --once --field ranges | head -n 20
```

결과:

```text
inf 위주로 출력됨
```

판단:

```text
/scan이 죽은 것이 아니다.
empty_world에서 LiDAR가 감지할 벽이나 장애물이 거의 없기 때문에 ranges가 inf 위주로 나온다.
따라서 RViz2에 표시될 점도 거의 없을 수 있다.
```

---

## 11. Phase 3 기록 파일

Phase 3 관련 정리 파일:

```text
docs/phases/phase03_rviz2_tf2.md
notes/phase_summaries/phase03_rviz2_tf2_summary.md
docs/handoffs/MBROS2_Phase3_Handoff.md
docs/handoffs/MBROS2_Phase3_prompt.md
```

README 업데이트 내용:

```text
Phase map에서 Phase 3 체크 완료
Result 섹션에 Phase 3 Summary 추가
```

troubleshooting 업데이트 내용:

```text
TS-0003_gzclient_camera_assertion_failed
```

experiment_log 업데이트 후보:

```text
P03-EXP-0001_rviz2_tf2_visualization_check
```

---

## 12. Phase 3 완료 판정

Phase 3는 다음 기준을 만족했으므로 완료로 판단한다.

```text
[x] RViz2 실행 성공
[x] Fixed Frame = odom 설정
[x] TF display 표시 성공
[x] RobotModel 표시 성공
[x] LaserScan display 연결 성공
[x] /scan topic 정상 확인
[x] empty_world라 ranges가 inf 위주인 것 확인
[x] view_frames로 TF tree 확인
[x] tf2_echo로 transform 직접 조회
[x] teleop 이동 중 odom → base_footprint transform 변화 확인
[x] gzclient crash를 Gazebo GUI 문제로 분리하고 RViz2 중심으로 진행
```

완료 의미:

```text
TurtleBot3의 센서 데이터와 로봇 모델이 어떤 좌표계 기준으로 해석되는지 RViz2와 TF2를 통해 확인했다.

이제 다음 Phase인 SLAM에서 /scan과 TF가 왜 중요한지 이해할 준비가 되었다.
```

---

## 13. Phase 4 시작 목표

다음 Phase:

```text
Phase 4. SLAM
```

Phase 4의 핵심 목표:

```text
SLAM Toolbox를 사용해 TurtleBot3가 이동하면서 /scan과 TF를 기반으로 지도를 생성한다.
```

Phase 4에서 중요하게 연결될 개념:

```text
/scan
→ 지도 생성을 위한 LiDAR 입력

/tf
→ 로봇 위치와 센서 좌표계 관계

odom
→ 로봇 이동 추정 기준

map
→ SLAM을 통해 새로 생성될 지도 기준 좌표계
```

---

## 14. Phase 4 시작 전 확인 명령

새 터미널에서 확인:

```bash
ros2 node list
echo $ROS_DISTRO
echo $TURTLEBOT3_MODEL
which ros2
which gazebo
which rviz2
ros2 pkg list | grep slam_toolbox
ros2 pkg list | grep turtlebot3_gazebo
ros2 pkg list | grep turtlebot3_teleop
cd ~/projects/missionbot-ros2
pwd
ls
```

정상 기대값:

```text
기존 노드 없음
humble
burger
/opt/ros/humble/bin/ros2
/usr/bin/gazebo
/opt/ros/humble/bin/rviz2
slam_toolbox
turtlebot3_gazebo
turtlebot3_teleop
/home/user/projects/missionbot-ros2
```

만약 `slam_toolbox`가 나오지 않으면 설치 여부를 확인해야 한다.

---

## 15. Phase 4에서 주의할 점

```text
Phase 4에서는 Navigation2로 앞서가지 않는다.
우선 SLAM Toolbox로 지도 생성 흐름만 집중한다.
```

Phase 3와 Phase 4의 연결:

```text
Phase 3
→ RViz2에서 /scan, /tf, /tf_static, RobotModel을 확인

Phase 4
→ SLAM Toolbox가 /scan과 TF를 사용해 map을 생성
```

중요한 연결:

```text
/scan
→ LiDAR 거리 센서 데이터
→ SLAM의 주요 입력

/tf
→ odom, base_footprint, base_link, base_scan 관계
→ SLAM이 센서 데이터를 로봇 위치와 연결해 해석하는 데 필요

map
→ SLAM이 새롭게 만들어낼 지도 기준 좌표계
```

---

## 16. 다음 채팅 시작 지점

다음 채팅에서는 아래 상태에서 시작하면 된다.

```text
현재 MissionBot-ROS2는 Phase 3. RViz2 + TF2를 완료했다.

완료한 것:
- ROS2 Humble, TurtleBot3 Burger 환경 확인
- turtlebot3_gazebo, turtlebot3_teleop, rviz2 확인
- Gazebo TurtleBot3 empty_world 실행
- TurtleBot3 Burger spawn 확인
- gzclient crash 발생 후, gzserver와 ROS2 topic은 정상임을 확인
- /cmd_vel, /odom, /scan 확인
- /tf, /tf_static 확인
- RViz2 실행
- Fixed Frame을 odom으로 설정
- TF display 확인
- RobotModel display 확인
- LaserScan display를 /scan에 연결
- empty_world에서 /scan ranges가 inf 위주로 나오는 것 확인
- view_frames로 frames.pdf 생성
- TF tree에서 odom → base_footprint → base_link → base_scan 구조 확인
- tf2_echo로 odom → base_footprint, base_link → base_scan 확인
- teleop 이동 중 odom → base_footprint transform 변화 확인

다음 목표:
- Phase 4. SLAM 시작
- 첫 단계는 SLAM Toolbox 설치/인식 확인과 SLAM 실행 전 환경 점검
```

추천 시작점:

```text
Phase 4-1. SLAM Toolbox 시작 전 환경 확인
```

첫 단계에서 할 일:

```text
1. 기존 Gazebo/RViz2 관련 노드가 남아 있지 않은지 확인
2. ROS2 Humble 환경 확인
3. TURTLEBOT3_MODEL=burger 확인
4. rviz2 실행 파일 인식 확인
5. slam_toolbox 패키지 인식 확인
6. turtlebot3_gazebo 패키지 인식 확인
7. turtlebot3_teleop 패키지 인식 확인
8. Phase 4에서 사용할 /scan, /tf, /tf_static, map 개념을 가볍게 연결
9. SLAM 실행 전 Gazebo TurtleBot3 재실행 준비
```
