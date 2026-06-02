# MissionBot-ROS2 Phase 4 인수인계 문서

> 목적: 이 문서는 MissionBot-ROS2 프로젝트의 Phase 4. SLAM 완료 상태를 정리하고, 다른 채팅창에서 Phase 5. Navigation2를 바로 이어가기 위한 인수인계 문서다.
> 이 문서와 아래의 이어가기 프롬프트만 있으면 Phase 4 완료 상태를 복원하고 Phase 5를 시작할 수 있다.

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

## Phase 4. SLAM

상태: 완료

완료한 것:

```text
[x] SLAM Toolbox 시작 전 환경 확인
[x] ROS2 Humble 확인
[x] TURTLEBOT3_MODEL=burger 확인
[x] ros2 실행 경로 확인
[x] gazebo 실행 경로 확인
[x] rviz2 실행 경로 확인
[x] slam_toolbox 패키지 인식 확인
[x] turtlebot3_gazebo 패키지 인식 확인
[x] turtlebot3_teleop 패키지 인식 확인
[x] MissionBot 프로젝트 루트 확인
[x] TurtleBot3 Gazebo World 실행
[x] /cmd_vel topic 확인
[x] /odom topic 확인
[x] /scan topic 확인
[x] /tf topic 확인
[x] /tf_static topic 확인
[x] turtlebot3_world에서 /scan ranges에 실제 거리값이 나오는 것 확인
[x] SLAM Toolbox online async 모드 실행
[x] use_sim_time:=True 적용
[x] /slam_toolbox node 확인
[x] /map topic 생성 확인
[x] /map_metadata topic 생성 확인
[x] /slam_toolbox/scan_visualization topic 확인
[x] /map type이 nav_msgs/msg/OccupancyGrid인 것 확인
[x] RViz2 실행
[x] RViz2 Fixed Frame을 map으로 설정
[x] Map display 추가
[x] Map Topic을 /map으로 설정
[x] TF display 추가
[x] RobotModel display 추가
[x] LaserScan display 추가
[x] RViz2에서 SLAM 지도 시각화 확인
[x] teleop_keyboard로 TurtleBot3 이동
[x] TurtleBot3 이동에 따라 지도 확장 확인
[x] map_saver_cli로 지도 저장
[x] tb3_world_slam_map_01.pgm 생성 확인
[x] tb3_world_slam_map_01.yaml 생성 확인
[x] yaml 파일의 image, mode, resolution, origin, threshold 값 확인
[x] pgm 파일이 Netpbm PGM 이미지 파일로 인식되는 것 확인
[x] PGM 출력 시 깨진 문자처럼 보이는 내용이 이미지 픽셀 데이터임을 확인
```

Phase 4 완료 의미:

```text
Phase 3에서는 RViz2와 TF2를 통해 센서와 좌표계가 정상적으로 연결되는지 확인했다.

Phase 4에서는 그 센서 데이터와 좌표계 정보를 SLAM Toolbox에 연결해 실제 /map topic을 생성했고, RViz2에서 지도가 확장되는 것을 확인했다.

마지막으로 map_saver_cli를 사용해 생성된 지도를 .pgm / .yaml 파일로 저장했다.

이제 Phase 5 Navigation2에서 이 지도를 기반으로 목표 지점 이동을 실습할 준비가 되었다.
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
│   └── phase04_slam/
│       ├── tb3_world_slam_map_01.pgm
│       └── tb3_world_slam_map_01.yaml
│
├── rosbags/
├── results/
└── notes/
    ├── experiment_log.md
    ├── troubleshooting.md
    ├── daily_logs/
    ├── phase_summaries/
    │   └── phase04_slam_summary.md
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

TurtleBot3 Gazebo, RViz2, SLAM Toolbox, Navigation2 같은 외부 ROS2 패키지를 실행할 때는 `.bashrc`로 기본 ROS2/TurtleBot3 환경이 잡혀 있으면 충분한 경우가 많다.

---

## 6. Phase 4 시작 전 환경 확인 결과

Phase 4 시작 전 아래 명령어로 환경을 확인했다.

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

ros2 pkg list | grep slam_toolbox
→ slam_toolbox

ros2 pkg list | grep turtlebot3_gazebo
→ turtlebot3_gazebo

ros2 pkg list | grep turtlebot3_teleop
→ turtlebot3_teleop

pwd
→ /home/user/projects/missionbot-ros2
```

이 결과를 기준으로 Phase 4 SLAM 실행 준비가 완료된 것으로 판단했다.

---

## 7. Phase 4에서 실행한 주요 명령어

## 7.1 TurtleBot3 World 실행

```bash
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

의미:

```text
turtlebot3_gazebo 패키지 안의 turtlebot3_world.launch.py를 실행한다.
벽과 구조물이 있는 Gazebo World에 TurtleBot3 Burger를 spawn한다.
SLAM은 주변 구조물을 LiDAR로 관측해야 하므로 empty_world보다 turtlebot3_world가 적합하다.
```

확인한 주요 topic:

```text
/cmd_vel
/odom
/scan
/tf
/tf_static
```

---

## 7.2 /scan 확인

```bash
ros2 topic echo /scan --once --field ranges | head -n 20
```

의미:

```text
TurtleBot3 LiDAR가 주변 벽이나 구조물을 실제로 감지하는지 확인한다.
empty_world에서는 inf 위주로 나올 수 있지만, turtlebot3_world에서는 숫자 거리값이 섞여 나올 수 있다.
숫자 거리값이 나온다는 것은 SLAM이 지도를 만들 입력을 받을 수 있다는 뜻이다.
```

---

## 7.3 SLAM Toolbox 실행

```bash
ros2 launch slam_toolbox online_async_launch.py use_sim_time:=True
```

의미:

```text
slam_toolbox 패키지의 online_async_launch.py를 실행한다.
TurtleBot3가 움직이는 동안 실시간으로 지도를 생성한다.
use_sim_time:=True 옵션으로 Gazebo의 /clock 시뮬레이션 시간을 사용한다.
```

Gazebo 환경에서는 실제 컴퓨터 시간이 아니라 시뮬레이션 시간이 `/clock`으로 흐르기 때문에 `use_sim_time:=True` 설정이 중요하다.

---

## 7.4 SLAM Toolbox 실행 확인

```bash
ros2 node list
```

확인된 주요 node:

```text
/gazebo
/robot_state_publisher
/slam_toolbox
/transform_listener_impl_62b98f4d38e0
/turtlebot3_diff_drive
/turtlebot3_imu
/turtlebot3_joint_state
/turtlebot3_laserscan
```

topic 확인:

```bash
ros2 topic list | grep -E "map|scan|tf|odom"
```

확인된 topic:

```text
/map
/map_metadata
/odom
/scan
/slam_toolbox/scan_visualization
/tf
/tf_static
```

/map topic 정보 확인:

```bash
ros2 topic info /map
```

확인 결과:

```text
Type: nav_msgs/msg/OccupancyGrid
Publisher count: 1
Subscription count: 1
```

이를 통해 SLAM Toolbox가 `/map` topic을 정상적으로 생성하고 있음을 확인했다.

---

## 7.5 RViz2 실행 및 SLAM 지도 시각화

```bash
rviz2
```

RViz2 설정:

```text
Global Options
→ Fixed Frame: map
```

추가한 Display:

```text
Map
→ Topic: /map

TF
→ map, odom, base_footprint, base_link, base_scan 확인

RobotModel
→ Description Source: Topic
→ Description Topic: /robot_description

LaserScan
→ Topic: /scan
→ Style: Points
```

확인한 것:

```text
[x] RViz2 Global Status: Ok
[x] Fixed Frame = map
[x] Map display Topic = /map
[x] TF 표시
[x] RobotModel 표시
[x] LaserScan 표시
[x] SLAM 지도 영역 표시
```

---

## 7.6 teleop으로 지도 확장

```bash
ros2 run turtlebot3_teleop teleop_keyboard
```

조작 키:

```text
w: 전진
x: 후진
a: 왼쪽 회전
d: 오른쪽 회전
s: 정지
```

지도 확장 시 주의한 점:

```text
전진은 짧게
회전은 천천히
급회전 금지
벽과 구조물을 충분히 관측
중간중간 멈추며 RViz2에서 지도 확인
```

확인한 것:

```text
[x] TurtleBot3 이동에 따라 LaserScan 데이터가 변함
[x] RViz2에서 지도 영역이 넓어짐
[x] 검은색 벽/장애물 영역과 흰색 자유 공간이 확장됨
[x] RobotModel이 map 위에서 이동함
```

---

## 7.7 지도 저장

지도 저장 전 로봇을 정지했다.

```text
teleop_keyboard 터미널에서 s 입력
```

지도 저장 폴더 생성:

```bash
cd ~/projects/missionbot-ros2
mkdir -p maps/phase04_slam
```

지도 저장 도구 확인:

```bash
ros2 pkg list | grep nav2_map_server
```

지도 저장 명령어:

```bash
ros2 run nav2_map_server map_saver_cli -f maps/phase04_slam/tb3_world_slam_map_01
```

저장 결과 확인:

```bash
ls -lh maps/phase04_slam
```

저장된 파일:

```text
tb3_world_slam_map_01.pgm
tb3_world_slam_map_01.yaml
```

파일 크기:

```text
tb3_world_slam_map_01.pgm   12K
tb3_world_slam_map_01.yaml  139
```

---

## 7.8 저장된 지도 파일 확인

yaml 파일 확인:

```bash
cat maps/phase04_slam/tb3_world_slam_map_01.yaml
```

확인된 내용:

```yaml
image: tb3_world_slam_map_01.pgm
mode: trinary
resolution: 0.05
origin: [-2.94, -2.57, 0]
negate: 0
occupied_thresh: 0.65
free_thresh: 0.25
```

pgm 파일 타입 확인:

```bash
file maps/phase04_slam/tb3_world_slam_map_01.pgm
```

확인 결과:

```text
Netpbm image data, size = 112 x 103, rawbits, greymap
```

pgm 헤더 확인:

```bash
head -n 5 maps/phase04_slam/tb3_world_slam_map_01.pgm
```

확인된 주요 헤더:

```text
P5
112 103
255
```

판단:

```text
P5는 바이너리 PGM 이미지 형식이다.
112 103은 가로 112픽셀, 세로 103픽셀을 의미한다.
255는 픽셀 밝기 최댓값을 의미한다.
헤더 이후 깨진 문자처럼 보이는 출력은 이미지 픽셀 데이터이므로 정상이다.
```

---

## 8. Phase 4에서 배운 핵심 개념

## 8.1 SLAM

```text
SLAM은 로봇이 움직이면서 자기 위치를 추정하고 동시에 주변 지도를 만드는 과정이다.
```

이번 Phase에서는 SLAM Toolbox를 사용해 TurtleBot3의 LiDAR `/scan`과 TF 정보를 기반으로 `/map`을 생성했다.

---

## 8.2 /scan

```text
/scan은 TurtleBot3의 2D LiDAR 거리 센서 데이터다.
SLAM의 주요 입력으로 사용된다.
```

---

## 8.3 /odom

```text
/odom은 로봇의 위치, 자세, 속도 추정 정보를 담는 topic이다.
SLAM은 odom 정보를 참고하지만, odom은 시간이 지나면 오차가 누적될 수 있다.
```

---

## 8.4 /tf, /tf_static

```text
/tf는 계속 변하는 좌표계 관계를 담는다.
예: odom → base_footprint

/tf_static은 고정된 좌표계 관계를 담는다.
예: base_link → base_scan
```

SLAM은 `/scan`이 어느 위치와 방향에서 측정된 데이터인지 알아야 하므로 TF 정보가 필요하다.

---

## 8.5 map frame

SLAM 이전 TF 구조:

```text
odom
→ base_footprint
→ base_link
→ base_scan
```

SLAM 이후 TF 구조:

```text
map
→ odom
→ base_footprint
→ base_link
→ base_scan
```

`map` frame은 SLAM으로 생성되는 지도 기준 좌표계다.

---

## 8.6 /map

```text
/map은 SLAM 결과로 생성되는 지도 topic이다.
```

메시지 타입:

```text
nav_msgs/msg/OccupancyGrid
```

OccupancyGrid는 공간을 격자로 나누고 각 칸이 장애물인지, 빈 공간인지, 아직 모르는 공간인지 표현한다.

---

## 8.7 use_sim_time

Gazebo는 시뮬레이션 시간을 `/clock` topic으로 발행한다.

따라서 Gazebo 환경에서 SLAM Toolbox를 실행할 때는 다음 옵션을 사용했다.

```bash
use_sim_time:=True
```

이 설정은 SLAM Toolbox가 Gazebo의 시간 기준에 맞춰 `/scan`, `/tf`, `/odom` 데이터를 해석하게 한다.

---

## 8.8 PGM / YAML 지도 파일

SLAM 지도는 보통 두 파일로 저장된다.

```text
.pgm
→ 실제 지도 이미지

.yaml
→ 지도 이미지를 ROS2가 어떻게 해석해야 하는지 알려주는 설정 파일
```

이번 Phase에서 생성한 파일:

```text
maps/phase04_slam/tb3_world_slam_map_01.pgm
maps/phase04_slam/tb3_world_slam_map_01.yaml
```

---

## 9. Phase 4에서 발생한 주요 이슈

## 9.1 PGM 파일 출력 시 깨진 문자처럼 보이는 문제

상황:

```bash
head -n 5 maps/phase04_slam/tb3_world_slam_map_01.pgm
```

출력 중 `����` 같은 깨진 문자처럼 보이는 내용이 나타났다.

판단:

```text
실패가 아니다.
PGM 파일의 앞부분에는 이미지 형식 정보가 있고, 그 뒤에는 픽셀 데이터가 들어 있다.
rawbits 방식의 PGM은 사람이 읽는 텍스트가 아니라 바이너리 이미지 데이터에 가깝기 때문에 터미널에서 깨진 문자처럼 보일 수 있다.
```

정상 근거:

```text
P5
112 103
255
```

그리고 `file` 명령어 결과:

```text
Netpbm image data, size = 112 x 103, rawbits, greymap
```

따라서 저장된 `.pgm` 파일은 정상적인 지도 이미지 파일로 판단했다.

---

## 10. Phase 4 기록 파일

Phase 4 관련 정리 파일:

```text
docs/phases/phase04_slam.md
notes/phase_summaries/phase04_slam_summary.md
docs/handoffs/MBROS2_Phase4_Handoff.md
docs/handoffs/MBROS2_Phase4_prompt.md
notes/experiment_log.md
```

README 업데이트 내용:

```text
Phase map에서 Phase 4 체크 완료
Result 섹션에 Phase 4 Summary 추가
```

experiment_log 업데이트 내용:

```text
P04-EXP-0001_slam_toolbox_mapping
```

지도 저장 결과:

```text
maps/phase04_slam/tb3_world_slam_map_01.pgm
maps/phase04_slam/tb3_world_slam_map_01.yaml
```

---

## 11. Phase 4 완료 판정

Phase 4는 다음 기준을 만족했으므로 완료로 판단한다.

```text
[x] SLAM Toolbox 패키지 인식 확인
[x] TurtleBot3 Gazebo World 실행
[x] /scan, /odom, /tf, /tf_static 확인
[x] SLAM Toolbox 실행
[x] use_sim_time:=True 적용
[x] /slam_toolbox node 확인
[x] /map topic 생성 확인
[x] /map 타입이 nav_msgs/msg/OccupancyGrid인지 확인
[x] RViz2 Fixed Frame을 map으로 설정
[x] Map display를 /map에 연결
[x] RViz2에서 지도 시각화 확인
[x] teleop으로 지도 확장 확인
[x] map_saver_cli로 지도 저장
[x] .pgm, .yaml 지도 파일 생성 확인
[x] .yaml 지도 설정 확인
[x] .pgm 이미지 파일 형식 확인
```

완료 의미:

```text
TurtleBot3의 /scan, /odom, /tf 정보를 SLAM Toolbox에 연결해 실제 /map 지도를 생성했다.

RViz2에서 지도 생성 과정을 시각적으로 확인했고, teleop 이동으로 지도 확장을 확인했다.

마지막으로 생성된 지도를 .pgm / .yaml 파일로 저장했다.
```

---

## 12. Phase 5 시작 목표

다음 Phase:

```text
Phase 5. Navigation2
```

Phase 5의 핵심 목표:

```text
Phase 4에서 저장한 map을 기반으로 Navigation2를 실행하고, TurtleBot3가 목표 지점까지 이동하는 흐름을 확인한다.
```

Phase 5에서 중요하게 연결될 개념:

```text
map
→ Navigation2가 경로 계획과 위치 추정을 수행할 기준 지도

AMCL
→ 저장된 map 위에서 로봇 위치를 추정하는 localization 구성 요소

Nav2 planner
→ 목표 지점까지의 경로를 계산

Nav2 controller
→ 계산된 경로를 따라 로봇을 이동

RViz2 2D Pose Estimate
→ map 위에서 초기 위치를 지정

RViz2 2D Nav Goal
→ 목표 지점을 지정
```

단, Phase 5 시작 시 처음부터 모든 Nav2 개념을 길게 설명하지 않는다.
첫 단계에서는 Navigation2 실행 전 환경과 저장된 map 파일 확인부터 시작한다.

---

## 13. Phase 5 시작 전 확인 명령

새 터미널에서 확인:

```bash
ros2 node list
echo $ROS_DISTRO
echo $TURTLEBOT3_MODEL
which ros2
which gazebo
which rviz2
ros2 pkg list | grep nav2_bringup
ros2 pkg list | grep nav2_map_server
ros2 pkg list | grep nav2_amcl
ros2 pkg list | grep turtlebot3_navigation2
ros2 pkg list | grep turtlebot3_gazebo
cd ~/projects/missionbot-ros2
pwd
ls -lh maps/phase04_slam
cat maps/phase04_slam/tb3_world_slam_map_01.yaml
```

정상 기대값:

```text
기존 노드 없음
humble
burger
/opt/ros/humble/bin/ros2
/usr/bin/gazebo
/opt/ros/humble/bin/rviz2
nav2_bringup
nav2_map_server
nav2_amcl
turtlebot3_navigation2
turtlebot3_gazebo
/home/user/projects/missionbot-ros2
tb3_world_slam_map_01.pgm
tb3_world_slam_map_01.yaml
```

만약 Nav2 관련 패키지가 나오지 않으면 설치 여부를 확인해야 한다.

---

## 14. Phase 5에서 주의할 점

```text
Phase 5에서는 MoveIt2, rosbag2, LLM/VLM으로 앞서가지 않는다.
우선 Navigation2로 저장된 map을 불러오고, TurtleBot3가 목표 지점까지 이동하는 흐름만 집중한다.
```

Phase 4와 Phase 5의 연결:

```text
Phase 4
→ SLAM Toolbox로 map 생성 및 저장

Phase 5
→ 저장된 map을 기반으로 Navigation2 실행
```

중요한 연결:

```text
maps/phase04_slam/tb3_world_slam_map_01.yaml
→ Navigation2가 불러올 지도 설정 파일

maps/phase04_slam/tb3_world_slam_map_01.pgm
→ 실제 지도 이미지 파일

/map
→ 지도 topic

/tf
→ map, odom, base_footprint 관계 확인

/scan
→ 위치 추정 및 장애물 감지에 필요한 센서 데이터
```

---

## 15. 다음 채팅 시작 지점

다음 채팅에서는 아래 상태에서 시작하면 된다.

```text
현재 MissionBot-ROS2는 Phase 4. SLAM을 완료했다.

완료한 것:
- ROS2 Humble, TurtleBot3 Burger 환경 확인
- slam_toolbox, turtlebot3_gazebo, turtlebot3_teleop 패키지 확인
- TurtleBot3 Gazebo World 실행
- /cmd_vel, /odom, /scan, /tf, /tf_static 확인
- SLAM Toolbox online_async_launch.py 실행
- use_sim_time:=True 적용
- /slam_toolbox node 확인
- /map topic 생성 확인
- /map type이 nav_msgs/msg/OccupancyGrid인 것 확인
- RViz2 실행
- Fixed Frame을 map으로 설정
- Map display를 /map에 연결
- TF, RobotModel, LaserScan 표시
- teleop_keyboard로 TurtleBot3 이동
- RViz2에서 지도 확장 확인
- map_saver_cli로 지도 저장
- maps/phase04_slam/tb3_world_slam_map_01.pgm 생성
- maps/phase04_slam/tb3_world_slam_map_01.yaml 생성
- yaml 설정 확인
- pgm 파일 형식 확인
- PGM 출력 시 깨진 문자처럼 보이는 것은 이미지 픽셀 데이터라 정상임을 확인

다음 목표:
- Phase 5. Navigation2 시작
- 첫 단계는 Navigation2 패키지 인식 확인과 저장된 map 파일 확인
```

추천 시작점:

```text
Phase 5-1. Navigation2 시작 전 환경 및 map 파일 확인
```

첫 단계에서 할 일:

```text
1. 기존 Gazebo/RViz2/SLAM 관련 노드가 남아 있지 않은지 확인
2. ROS2 Humble 환경 확인
3. TURTLEBOT3_MODEL=burger 확인
4. rviz2 실행 파일 인식 확인
5. nav2_bringup 패키지 인식 확인
6. nav2_map_server 패키지 인식 확인
7. nav2_amcl 패키지 인식 확인
8. turtlebot3_navigation2 패키지 인식 확인
9. turtlebot3_gazebo 패키지 인식 확인
10. 저장된 map 파일 확인
11. Phase 5에서 사용할 map, AMCL, Nav2, 2D Pose Estimate, 2D Nav Goal 개념을 가볍게 연결
12. Navigation2 실행 전 Gazebo TurtleBot3 World 재실행 준비
```
