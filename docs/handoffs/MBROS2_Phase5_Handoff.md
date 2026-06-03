# MissionBot-ROS2 Phase 5 인수인계 문서

> 목적: 이 문서는 MissionBot-ROS2 프로젝트의 Phase 5. Navigation2 완료 상태를 정리하고, 다른 채팅창에서 Phase 6. rosbag2 logging을 바로 이어가기 위한 인수인계 문서다.
> 이 문서와 아래의 이어가기 프롬프트만 있으면 Phase 5 완료 상태를 복원하고 Phase 6을 시작할 수 있다.

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

이 흐름을 확인했고, Phase 4 SLAM에서 /scan과 TF가 왜 중요한지 이해할 준비가 되었다.
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
[x] /map type이 nav_msgs/msg/OccupancyGrid인지 확인
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
```

---

## Phase 5. Navigation2

상태: 완료

완료한 것:

```text
[x] Navigation2 실행 전 환경 확인
[x] ROS2 Humble 확인
[x] TURTLEBOT3_MODEL=burger 확인
[x] nav2_bringup 패키지 인식 확인
[x] nav2_map_server 패키지 인식 확인
[x] nav2_amcl 패키지 인식 확인
[x] turtlebot3_navigation2 패키지 인식 확인
[x] turtlebot3_gazebo 패키지 인식 확인
[x] Phase 4에서 저장한 map 파일 확인
[x] TurtleBot3 Gazebo World 실행
[x] /clock, /cmd_vel, /odom, /scan, /tf, /tf_static topic 확인
[x] 저장된 map yaml 파일 절대 경로 설정
[x] turtlebot3_navigation2 navigation2.launch.py 실행
[x] use_sim_time:=True 적용
[x] /map topic 생성 확인
[x] /map type이 nav_msgs/msg/OccupancyGrid인지 확인
[x] /amcl node 실행 확인
[x] /map_server node 실행 확인
[x] /planner_server node 실행 확인
[x] /controller_server node 실행 확인
[x] /bt_navigator node 실행 확인
[x] /behavior_server node 실행 확인
[x] /waypoint_follower node 실행 확인
[x] RViz2 Fixed Frame을 map으로 설정
[x] RViz2에서 Map, RobotModel, TF, LaserScan display 확인
[x] 2D Pose Estimate로 AMCL 초기 위치 지정
[x] /amcl_pose topic 출력 확인
[x] map → odom transform 생성 확인
[x] transform timeout 로그가 초기 위치 지정 후 사라지는 것 확인
[x] 2D Nav Goal로 목표 지점 지정
[x] TurtleBot3가 목표 지점 방향으로 이동하는 것 확인
[x] /plan topic으로 global path 생성 확인
[x] /cmd_vel topic으로 속도 명령 발행 확인
[x] 두 번째 2D Nav Goal 반복 이동 테스트 성공
[x] 주요 Nav2 lifecycle node가 active [3] 상태인지 확인
```

Phase 5 완료 의미:

```text
Phase 4에서 생성한 지도를 Navigation2에 연결했고, TurtleBot3가 저장된 map 위에서 현재 위치를 추정한 뒤 RViz2에서 지정한 목표 지점까지 이동하는 것을 확인했다.

이를 통해 MissionBot-ROS2는 수동 조작 중심의 이동로봇 확인 단계를 넘어, 저장된 map 기반 자율 주행 흐름을 처음으로 검증했다.

이제 Phase 6에서는 Navigation2 주행 중 발생하는 주요 topic을 rosbag2로 기록할 준비가 되었다.
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
│   │   └── phase05_navigation2.md
│   ├── concepts/
│   ├── templates/
│   └── handoffs/
│       ├── MBROS2_Phase5_Handoff.md
│       └── MBROS2_Phase5_prompt.md
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
    │   └── phase05_navigation2_summary.md
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

## 6. Phase 5 시작 전 환경 확인 결과

Phase 5 시작 전 아래 명령어로 환경을 확인했다.

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

정상 확인한 항목:

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

ros2 pkg list | grep nav2_bringup
→ nav2_bringup

ros2 pkg list | grep nav2_map_server
→ nav2_map_server

ros2 pkg list | grep nav2_amcl
→ nav2_amcl

ros2 pkg list | grep turtlebot3_navigation2
→ turtlebot3_navigation2

ros2 pkg list | grep turtlebot3_gazebo
→ turtlebot3_gazebo

pwd
→ /home/user/projects/missionbot-ros2
```

저장된 map 파일:

```text
maps/phase04_slam/tb3_world_slam_map_01.pgm
maps/phase04_slam/tb3_world_slam_map_01.yaml
```

---

## 7. Phase 5에서 실행한 주요 명령어

## 7.1 TurtleBot3 World 실행

```bash
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

의미:

```text
turtlebot3_gazebo 패키지 안의 turtlebot3_world.launch.py를 실행한다.
벽과 구조물이 있는 Gazebo World에 TurtleBot3 Burger를 spawn한다.
Phase 4에서 만든 map도 이 world를 기준으로 생성했기 때문에 Phase 5에서도 같은 world를 사용했다.
```

확인한 주요 topic:

```text
/clock
/cmd_vel
/odom
/scan
/tf
/tf_static
```

확인 명령:

```bash
ros2 topic list | grep -E "cmd_vel|odom|scan|tf|clock"
```

---

## 7.2 Navigation2 실행

프로젝트 루트로 이동:

```bash
cd ~/projects/missionbot-ros2
```

map 파일 경로 변수 생성:

```bash
MAP_FILE=$(pwd)/maps/phase04_slam/tb3_world_slam_map_01.yaml
```

map 경로 확인:

```bash
echo $MAP_FILE
ls -lh $MAP_FILE
```

Navigation2 실행:

```bash
ros2 launch turtlebot3_navigation2 navigation2.launch.py use_sim_time:=True map:=$MAP_FILE
```

의미:

```text
turtlebot3_navigation2
→ TurtleBot3용 Navigation2 설정 패키지

navigation2.launch.py
→ TurtleBot3 Navigation2 실행 launch 파일

use_sim_time:=True
→ Gazebo의 /clock 시뮬레이션 시간을 사용

map:=$MAP_FILE
→ Phase 4에서 저장한 map yaml 파일을 Navigation2에 전달
```

Gazebo 환경에서는 실제 컴퓨터 시간이 아니라 `/clock` 기준의 시뮬레이션 시간을 사용하므로 `use_sim_time:=True` 설정이 중요하다.

---

## 7.3 Navigation2 node 확인

```bash
ros2 node list | grep -E "map|amcl|planner|controller|bt|behavior|lifecycle|waypoint"
```

확인한 주요 node:

```text
/amcl
/behavior_server
/bt_navigator
/bt_navigator_navigate_through_poses_rclcpp_node
/bt_navigator_navigate_to_pose_rclcpp_node
/controller_server
/global_costmap/global_costmap
/lifecycle_manager_localization
/lifecycle_manager_navigation
/local_costmap/local_costmap
/map_server
/planner_server
/waypoint_follower
```

---

## 7.4 Navigation2 topic 확인

```bash
ros2 topic list | grep -E "map|amcl|plan|cmd_vel|costmap|particlecloud"
```

확인한 주요 topic:

```text
/amcl_pose
/cmd_vel
/cmd_vel_nav
/global_costmap/costmap
/global_costmap/costmap_raw
/global_costmap/costmap_updates
/local_costmap/costmap
/local_costmap/costmap_raw
/local_costmap/costmap_updates
/local_plan
/map
/map_updates
/plan
/plan_smoothed
/received_global_plan
/transformed_global_plan
```

`/map` 정보 확인:

```bash
ros2 topic info /map
```

확인 결과:

```text
Type: nav_msgs/msg/OccupancyGrid
Publisher count: 1
Subscription count: 3
```

---

## 7.5 AMCL 초기 위치 지정

Navigation2 실행 직후 다음 로그가 발생했다.

```text
Timed out waiting for transform from base_link to map to become available
Invalid frame ID "map" passed to canTransform argument target_frame - frame does not exist
```

판단:

```text
실제 실행 실패가 아니라, 2D Pose Estimate를 하기 전 AMCL 초기 위치가 지정되지 않아 map → odom transform이 아직 생성되지 않은 상태였다.
```

해결:

```text
RViz2
→ 2D Pose Estimate
→ map 위에서 현재 TurtleBot3 위치 클릭
→ 바라보는 방향으로 드래그
→ 마우스 놓기
```

확인 명령:

```bash
ros2 topic echo /amcl_pose --once
```

출력 예시:

```text
header:
  frame_id: map
pose:
  pose:
    position:
      x: ...
      y: ...
```

`map → odom` transform 확인:

```bash
ros2 run tf2_ros tf2_echo map odom
```

정상 출력 예시:

```text
At time ...
- Translation: [...]
- Rotation: [...]
```

2D Pose Estimate 이후 transform timeout 로그가 사라졌다.

---

## 7.6 RViz2 설정

RViz2에서 다음 설정을 확인했다.

```text
Global Options
→ Fixed Frame: map
```

켜둔 주요 Display:

```text
Map
RobotModel
TF
LaserScan
Global Planner
Controller
```

필요 시 꺼도 되는 Display:

```text
Amcl Particle Swarm
MarkerArray
Realsense
Bumper Hit
```

LaserScan은 map과 완벽히 일치하지 않을 수 있다.

이 경우 2D Pose Estimate를 다시 찍어 위치와 방향을 대략 맞춘다.

---

## 7.7 2D Nav Goal 이동

RViz2에서 목표 지점을 지정했다.

```text
RViz2
→ 2D Nav Goal
→ map 위의 흰색 빈 공간 클릭
→ 최종 방향으로 드래그
→ 마우스 놓기
```

처음 목표는 가까운 흰색 빈 공간으로 지정했다.

확인한 action:

```bash
ros2 action list | grep navigate
```

확인 결과:

```text
/navigate_to_pose
/navigate_through_poses
```

추가 확인:

```bash
ros2 action info /navigate_to_pose
```

목표 이동 중 속도 명령 확인:

```bash
ros2 topic echo /cmd_vel
```

경로 생성 확인:

```bash
ros2 topic echo /plan --once
```

확인 결과:

```text
[x] RViz2에서 목표 지점 지정 가능
[x] TurtleBot3가 목표 방향으로 이동
[x] /cmd_vel로 속도 명령 발행
[x] /plan으로 global path 생성
[x] 목표 이동 반복 테스트 성공
```

---

## 7.8 lifecycle 상태 확인

주요 Navigation2 node들이 실제 동작 가능한 상태인지 확인했다.

```bash
ros2 lifecycle get /map_server
ros2 lifecycle get /amcl
ros2 lifecycle get /planner_server
ros2 lifecycle get /controller_server
ros2 lifecycle get /bt_navigator
ros2 lifecycle get /behavior_server
ros2 lifecycle get /waypoint_follower
```

확인 결과:

```text
active [3]
```

의미:

```text
각 Nav2 구성 요소가 실행만 된 것이 아니라 실제 동작 가능한 active 상태로 전환되었음을 의미한다.
```

---

## 8. Phase 5에서 배운 핵심 개념

## 8.1 Navigation2

Navigation2는 저장된 지도 위에서 로봇이 목표 지점까지 이동하도록 도와주는 ROS2 navigation stack이다.

단일 node가 아니라 여러 node가 역할을 나눠 함께 동작한다.

핵심 흐름:

```text
map_server
→ amcl
→ planner_server
→ controller_server
→ /cmd_vel
→ TurtleBot3 이동
```

---

## 8.2 map_server

```text
/map_server는 저장된 .yaml / .pgm 지도 파일을 읽고 /map topic으로 발행한다.
```

Phase 5에서는 Phase 4에서 저장한 다음 지도 파일을 사용했다.

```text
maps/phase04_slam/tb3_world_slam_map_01.yaml
maps/phase04_slam/tb3_world_slam_map_01.pgm
```

---

## 8.3 AMCL

```text
AMCL은 저장된 map 위에서 로봇의 현재 위치를 추정하는 localization 구성 요소다.
```

RViz2의 2D Pose Estimate로 초기 위치를 지정한 뒤, AMCL이 `/amcl_pose`를 발행하고 `map → odom` transform을 생성하는 것을 확인했다.

---

## 8.4 planner_server

```text
planner_server는 현재 위치에서 목표 지점까지 갈 전체 경로를 계산한다.
```

생성된 경로는 `/plan` topic으로 확인했다.

---

## 8.5 controller_server

```text
controller_server는 planner가 만든 경로를 따라가기 위해 실제 속도 명령을 생성한다.
```

생성된 속도 명령은 `/cmd_vel` topic으로 확인했다.

---

## 8.6 bt_navigator

```text
bt_navigator는 목표 이동의 전체 순서를 관리한다.
```

RViz2에서 2D Nav Goal을 찍으면 내부적으로 `/navigate_to_pose` action 요청이 들어가고, bt_navigator가 목표 이동 과정을 관리한다.

---

## 8.7 behavior_server

```text
behavior_server는 이동 실패나 장애물 상황에서 회전, 후진 같은 복구 행동을 담당한다.
```

이번 Phase에서는 복구 행동을 자세히 실험하지는 않았지만, Navigation2 구성 요소로 실행되는 것을 확인했다.

---

## 8.8 costmap

```text
costmap은 로봇이 이동 가능한 영역과 장애물을 판단하기 위해 사용하는 지도다.
```

구분:

```text
global_costmap
→ 전체 map 기준 장애물 판단

local_costmap
→ 로봇 주변 기준 장애물 판단
```

---

## 8.9 lifecycle node

```text
Navigation2의 주요 node는 lifecycle node로 관리된다.
```

단순히 실행된 것만으로는 충분하지 않고, `active` 상태가 되어야 실제 동작할 수 있다.

이번 Phase에서는 주요 lifecycle node가 모두 `active [3]` 상태임을 확인했다.

---

## 9. Phase 5 주요 node 정리

| Node                              | 쉬운 의미            | 핵심 역할                                     |
| --------------------------------- | ---------------- | ----------------------------------------- |
| `/map_server`                     | 지도 담당            | `.yaml` / `.pgm` map 파일을 읽어서 `/map`으로 발행  |
| `/amcl`                           | 현재 위치 추정 담당      | 저장된 map 위에서 로봇의 현재 위치 추정                  |
| `/planner_server`                 | 경로 계산 담당         | 현재 위치에서 목표 지점까지 갈 전체 경로 생성                |
| `/controller_server`              | 실제 주행 담당         | planner가 만든 경로를 따라가도록 속도 명령 생성            |
| `/bt_navigator`                   | 전체 이동 흐름 담당      | 목표 이동을 어떤 순서로 수행할지 관리                     |
| `/behavior_server`                | 예외 행동 담당         | 막히거나 실패했을 때 회전, 후진 같은 복구 행동 수행            |
| `/waypoint_follower`              | 여러 지점 이동 담당      | 여러 목표 지점을 순서대로 따라갈 때 사용                   |
| `/lifecycle_manager_localization` | localization 관리자 | `map_server`, `amcl` 상태 관리                |
| `/lifecycle_manager_navigation`   | navigation 관리자   | planner, controller, bt_navigator 등 상태 관리 |
| `/global_costmap/global_costmap`  | 전체 장애물 지도        | 전체 map 기준으로 이동 가능 영역과 장애물 판단              |
| `/local_costmap/local_costmap`    | 주변 장애물 지도        | 로봇 주변의 장애물과 안전거리 판단                       |

---

## 10. Phase 5 주요 topic 정리

| Topic                     | 쉬운 의미      | 핵심 역할                             |
| ------------------------- | ---------- | --------------------------------- |
| `/map`                    | 저장된 지도     | map_server가 발행하는 OccupancyGrid 지도 |
| `/map_updates`            | 지도 업데이트    | map 갱신 정보                         |
| `/amcl_pose`              | 현재 위치 추정   | AMCL이 추정한 로봇의 현재 위치               |
| `/plan`                   | 전역 경로      | 목표 지점까지의 전체 경로                    |
| `/plan_smoothed`          | 다듬어진 경로    | 부드럽게 보정된 경로                       |
| `/local_plan`             | 로컬 경로      | 로봇 주변 기준의 짧은 주행 경로                |
| `/cmd_vel`                | 속도 명령      | TurtleBot3를 실제로 움직이는 속도 명령        |
| `/cmd_vel_nav`            | Nav2 속도 명령 | Nav2 controller 쪽 속도 명령           |
| `/global_costmap/costmap` | 전체 장애물 지도  | 전체 map 기준 장애물 판단                  |
| `/local_costmap/costmap`  | 주변 장애물 지도  | 로봇 주변 장애물 판단                      |
| `/odom`                   | odometry   | 로봇의 위치, 자세, 속도 추정                 |
| `/scan`                   | LiDAR 데이터  | TurtleBot3 거리 센서 데이터              |
| `/tf`                     | 동적 좌표계     | 계속 변하는 좌표계 관계                     |
| `/tf_static`              | 정적 좌표계     | 고정된 좌표계 관계                        |
| `/initialpose`            | 초기 위치      | 2D Pose Estimate가 발행하는 초기 위치      |
| `/goal_pose`              | 목표 위치      | 2D Nav Goal이 발행하는 목표 위치           |

---

## 11. Phase 5 주요 action 정리

| Action                    | 의미                |
| ------------------------- | ----------------- |
| `/navigate_to_pose`       | 하나의 목표 지점까지 이동    |
| `/navigate_through_poses` | 여러 목표 지점을 순서대로 이동 |

RViz2에서 2D Nav Goal을 찍으면 내부적으로 `/navigate_to_pose` action 요청이 들어간다.

---

## 12. Phase 5에서 발생한 주요 현상

## 12.1 map → odom transform 대기 로그

상황:

```text
Timed out waiting for transform from base_link to map to become available
Invalid frame ID "map" passed to canTransform argument target_frame - frame does not exist
```

판단:

```text
실제 실행 실패가 아니다.
2D Pose Estimate를 하기 전 AMCL 초기 위치가 지정되지 않아 map → odom transform이 아직 생성되지 않은 상태였다.
```

해결:

```text
RViz2
→ 2D Pose Estimate
→ map 위에서 TurtleBot3의 초기 위치와 방향 지정
```

결과:

```text
/amcl_pose 출력 확인
tf2_echo map odom 출력 확인
transform timeout 로그 사라짐
```

---

## 12.2 LaserScan과 map이 완전히 겹치지 않는 현상

상황:

```text
RViz2에서 빨간 LaserScan 점이 검은 map 벽과 완전히 일치하지 않았다.
```

판단:

```text
AMCL 초기 위치 또는 방향이 약간 어긋났을 때 발생할 수 있는 현상이다.
```

해결:

```text
2D Pose Estimate를 다시 찍어 로봇의 위치와 방향을 map 위에서 대략 맞춘다.
```

주의:

```text
완벽하게 1픽셀 단위로 맞을 필요는 없다.
목표 이동 전 LaserScan과 map 구조가 대략 맞는지 확인하면 된다.
```

---

## 13. Phase 5 기록 파일

Phase 5 관련 정리 파일:

```text
README.md
notes/experiment_log.md
docs/phases/phase05_navigation2.md
notes/phase_summaries/phase05_navigation2_summary.md
docs/handoffs/MBROS2_Phase5_Handoff.md
docs/handoffs/MBROS2_Phase5_prompt.md
```

README 업데이트 내용:

```text
Phase map에서 Phase 5 체크 완료
Result 섹션에 Phase 5 Summary 추가
```

experiment_log 업데이트 내용:

```text
P05-EXP-0001_nav2_map_based_goal_navigation
```

troubleshooting 정리 여부:

```text
정식 troubleshooting 항목은 필수로 추가하지 않는다.

초기 transform timeout 로그는 실제 오류라기보다 2D Pose Estimate 전 자연스럽게 발생할 수 있는 상태였으므로 docs/phases/phase05_navigation2.md의 주의사항으로 정리했다.
```

---

## 14. Phase 5 완료 판정

Phase 5는 다음 기준을 만족했으므로 완료로 판단한다.

```text
[x] Navigation2 관련 패키지 인식 확인
[x] Phase 4에서 저장한 map 파일 확인
[x] TurtleBot3 Gazebo World 실행
[x] /clock, /odom, /scan, /tf, /tf_static 확인
[x] 저장된 map 기반 Navigation2 실행
[x] use_sim_time:=True 적용
[x] /map topic 생성 확인
[x] /map type이 nav_msgs/msg/OccupancyGrid인지 확인
[x] AMCL node 실행 확인
[x] planner_server 실행 확인
[x] controller_server 실행 확인
[x] bt_navigator 실행 확인
[x] RViz2 Fixed Frame을 map으로 설정
[x] 2D Pose Estimate로 초기 위치 지정
[x] /amcl_pose 출력 확인
[x] map → odom transform 생성 확인
[x] 2D Nav Goal로 목표 지점 지정
[x] TurtleBot3 목표 이동 확인
[x] /plan topic 생성 확인
[x] /cmd_vel topic 발행 확인
[x] 반복 목표 이동 테스트 성공
[x] 주요 lifecycle node가 active [3] 상태
```

완료 의미:

```text
TurtleBot3가 저장된 map 위에서 현재 위치를 추정하고, RViz2에서 지정한 목표 지점까지 이동하는 것을 확인했다.

수동 조작이 아니라 Navigation2 기반 자율 이동 흐름을 처음으로 검증했다.
```

---

## 15. 다음 Phase 시작 목표

다음 Phase:

```text
Phase 6. rosbag2 logging
```

Phase 6의 핵심 목표:

```text
Navigation2 주행 중 발생하는 주요 ROS2 topic을 rosbag2로 기록하고, 기록된 bag 파일을 다시 확인한다.
```

Phase 6에서 중요하게 연결될 개념:

```text
rosbag2
→ ROS2 topic 데이터를 파일로 기록하는 도구

record
→ topic 데이터를 저장

info
→ 저장된 bag 파일 정보 확인

play
→ 저장된 topic 데이터를 다시 재생

Navigation2 logging
→ Nav2 주행 중 /scan, /odom, /tf, /cmd_vel, /map, /amcl_pose, /plan 등을 기록
```

단, Phase 6 시작 시 처음부터 분석 코드나 Failure Analysis로 넘어가지 않는다.

첫 단계에서는 rosbag2가 설치되어 있는지 확인하고, 어떤 topic을 기록할지 선정하는 것부터 시작한다.

---

## 16. Phase 6 시작 전 확인 명령

새 터미널에서 확인:

```bash
ros2 node list
echo $ROS_DISTRO
echo $TURTLEBOT3_MODEL
which ros2
which gazebo
which rviz2
ros2 bag --help
ros2 pkg list | grep rosbag2
ros2 pkg list | grep turtlebot3_gazebo
ros2 pkg list | grep turtlebot3_navigation2
cd ~/projects/missionbot-ros2
pwd
ls
ls -lh maps/phase04_slam
```

정상 기대값:

```text
기존 노드 없음
humble
burger
/opt/ros/humble/bin/ros2
/usr/bin/gazebo
/opt/ros/humble/bin/rviz2
ros2 bag 명령어 도움말 출력
rosbag2 관련 패키지 출력
turtlebot3_gazebo
turtlebot3_navigation2
/home/user/projects/missionbot-ros2
tb3_world_slam_map_01.pgm
tb3_world_slam_map_01.yaml
```

---

## 17. Phase 6에서 주의할 점

```text
Phase 6에서는 MoveIt2, LLM/VLM으로 앞서가지 않는다.
우선 rosbag2로 Navigation2 주행 데이터를 기록하고, 기록된 bag 정보를 확인하는 것에 집중한다.
```

Phase 5와 Phase 6의 연결:

```text
Phase 5
→ 저장된 map 기반 Navigation2 목표 이동 성공

Phase 6
→ 목표 이동 중 발생하는 topic을 rosbag2로 기록
```

중요한 기록 후보 topic:

```text
/scan
/odom
/tf
/tf_static
/cmd_vel
/cmd_vel_nav
/map
/amcl_pose
/plan
```

처음부터 너무 많은 topic을 기록하지 않는다.

처음 기록 후보는 다음 정도가 적절하다.

```text
/scan
/odom
/tf
/tf_static
/cmd_vel
/amcl_pose
/plan
```

---

## 18. 다음 채팅 시작 지점

다음 채팅에서는 아래 상태에서 시작하면 된다.

```text
현재 MissionBot-ROS2는 Phase 5. Navigation2를 완료했다.

완료한 것:
- ROS2 Humble, TurtleBot3 Burger 환경 확인
- nav2_bringup, nav2_map_server, nav2_amcl 패키지 확인
- turtlebot3_navigation2, turtlebot3_gazebo 패키지 확인
- Phase 4에서 저장한 map 파일 확인
- TurtleBot3 Gazebo World 실행
- /clock, /odom, /scan, /tf, /tf_static 확인
- 저장된 map yaml 파일 절대 경로 설정
- turtlebot3_navigation2 navigation2.launch.py 실행
- use_sim_time:=True 적용
- /map topic 생성 확인
- /map type이 nav_msgs/msg/OccupancyGrid인 것 확인
- /amcl, /map_server, /planner_server, /controller_server, /bt_navigator 실행 확인
- RViz2 Fixed Frame을 map으로 설정
- 2D Pose Estimate로 AMCL 초기 위치 지정
- /amcl_pose 출력 확인
- tf2_echo map odom으로 map → odom transform 확인
- 2D Nav Goal로 목표 지점 지정
- TurtleBot3 목표 이동 확인
- /plan topic 생성 확인
- /cmd_vel topic 발행 확인
- 목표 이동 반복 테스트 성공
- 주요 lifecycle node가 active [3] 상태임을 확인

다음 목표:
- Phase 6. rosbag2 logging 시작
- 첫 단계는 rosbag2 명령어 인식 확인과 기록할 topic 선정
```

추천 시작점:

```text
Phase 6-1. rosbag2 기록 전 환경 확인 및 topic 선정
```

첫 단계에서 할 일:

```text
1. 기존 Gazebo/RViz2/Nav2 관련 노드가 남아 있지 않은지 확인
2. ROS2 Humble 환경 확인
3. TURTLEBOT3_MODEL=burger 확인
4. ros2 bag 명령어 인식 확인
5. rosbag2 관련 패키지 확인
6. turtlebot3_gazebo 패키지 확인
7. turtlebot3_navigation2 패키지 확인
8. MissionBot 프로젝트 위치 확인
9. rosbags/phase06_logging 폴더 생성 여부 확인
10. Phase 6에서 기록할 topic 후보 선정
```