# MissionBot-ROS2 Phase 6 인수인계 문서

> 목적: 이 문서는 MissionBot-ROS2 프로젝트의 Phase 6. rosbag2 logging 완료 상태를 정리하고, 다른 채팅창에서 Phase 7. Failure Analysis를 바로 이어가기 위한 인수인계 문서다.
> 이 문서와 아래의 이어가기 프롬프트만 있으면 Phase 6 완료 상태를 복원하고 Phase 7을 시작할 수 있다.

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
[x] ROS2 Humble 환경 확인
[x] TURTLEBOT3_MODEL=burger 확인
[x] ros2 bag 명령어 인식 확인
[x] rosbag2 관련 패키지 확인
[x] turtlebot3_gazebo 패키지 확인
[x] turtlebot3_navigation2 패키지 확인
[x] MissionBot 프로젝트 루트 확인
[x] rosbags/phase06_logging 폴더 생성
[x] TurtleBot3 Gazebo World 실행
[x] Navigation2 실행
[x] RViz2에서 2D Pose Estimate로 AMCL 초기 위치 지정
[x] 기록 대상 topic 선정
[x] /scan, /odom, /tf, /tf_static, /cmd_vel, /amcl_pose, /plan topic 확인
[x] ros2 bag record로 Navigation2 주행 topic 기록
[x] RViz2에서 2D Nav Goal 지정
[x] TurtleBot3 목표 이동 기록
[x] Ctrl + C로 rosbag 기록 종료
[x] ros2 bag info로 기록 결과 확인
[x] metadata.yaml로 bag 파일 구조 확인
[x] ros2 bag play로 playback 확인
[x] topic echo로 /odom playback 메시지 확인
[x] --topics 옵션으로 일부 topic 선택 재생 확인
[x] --rate 옵션으로 playback 속도 조절 확인
[x] RViz2에서 rosbag playback 시각화 확인
[x] use_sim_time=true와 --clock 옵션 필요성 확인
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
│   │   └── phase06_rosbag2_logging.md
│   ├── concepts/
│   ├── templates/
│   └── handoffs/
│       ├── MBROS2_Phase6_Handoff.md
│       └── MBROS2_Phase6_prompt.md
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
│   └── phase06_logging/
│       └── p06_nav2_goal_01/
│           ├── metadata.yaml
│           └── p06_nav2_goal_01_0.db3
│
├── results/
└── notes/
    ├── experiment_log.md
    ├── troubleshooting.md
    ├── daily_logs/
    ├── phase_summaries/
    │   ├── phase05_navigation2_summary.md
    │   └── phase06_rosbag2_logging_summary.md
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

## 6. Phase 6 시작 전 환경 확인 결과

Phase 6 시작 전 아래 명령어로 환경을 확인했다.

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

mkdir -p rosbags/phase06_logging
ls -lh rosbags/phase06_logging
```

정상 확인한 항목:

```text
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

ros2 bag --help
→ record, info, play 등 sub-command 확인

ros2 pkg list | grep rosbag2
→ rosbag2 관련 패키지 확인

ros2 pkg list | grep turtlebot3_gazebo
→ turtlebot3_gazebo

ros2 pkg list | grep turtlebot3_navigation2
→ turtlebot3_navigation2

pwd
→ /home/user/projects/missionbot-ros2

ls -lh maps/phase04_slam
→ tb3_world_slam_map_01.pgm
→ tb3_world_slam_map_01.yaml
```

주의:

```text
처음 확인 시 기존 Phase 5에서 실행했던 Gazebo / RViz2 / Navigation2 노드가 남아 있었다.
따라서 rosbag 기록 전 기존 실행을 Ctrl + C로 정리했다.
```

---

## 7. Phase 6에서 실행한 주요 명령어

## 7.1 Navigation2 주행 재실행

Gazebo TurtleBot3 World 실행:

```bash
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

Navigation2 실행:

```bash
cd ~/projects/missionbot-ros2
MAP_FILE=$(pwd)/maps/phase04_slam/tb3_world_slam_map_01.yaml
echo $MAP_FILE
ls -lh $MAP_FILE
ros2 launch turtlebot3_navigation2 navigation2.launch.py use_sim_time:=True map:=$MAP_FILE
```

의미:

```text
Phase 4에서 저장한 map을 사용해 Phase 5와 같은 Navigation2 목표 이동 환경을 다시 구성했다.
```

---

## 7.2 기록 대상 topic 확인

topic 목록 확인:

```bash
ros2 topic list | grep -E "scan|odom|tf|cmd_vel|amcl_pose|plan|map|clock"
```

확인된 주요 topic:

```text
/amcl_pose
/clock
/cmd_vel
/cmd_vel_nav
/global_costmap/costmap
/local_costmap/costmap
/local_plan
/map
/map_updates
/odom
/plan
/plan_smoothed
/received_global_plan
/scan
/tf
/tf_static
/transformed_global_plan
```

topic 타입 확인:

```bash
ros2 topic info /scan
ros2 topic info /odom
ros2 topic info /tf
ros2 topic info /tf_static
ros2 topic info /cmd_vel
ros2 topic info /amcl_pose
ros2 topic info /plan
```

확인한 타입:

```text
/scan
→ sensor_msgs/msg/LaserScan

/odom
→ nav_msgs/msg/Odometry

/tf
→ tf2_msgs/msg/TFMessage

/tf_static
→ tf2_msgs/msg/TFMessage

/cmd_vel
→ geometry_msgs/msg/Twist

/amcl_pose
→ geometry_msgs/msg/PoseWithCovarianceStamped

/plan
→ nav_msgs/msg/Path
```

---

## 7.3 rosbag 기록

기록 명령:

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
  -o rosbags/phase06_logging/p06_nav2_goal_01
```

기록 중 출력된 주요 로그:

```text
[INFO] [rosbag2_recorder]: Press SPACE for pausing/resuming
[INFO] [rosbag2_storage]: Opened database 'rosbags/phase06_logging/p06_nav2_goal_01/p06_nav2_goal_01_0.db3' for READ_WRITE.
[INFO] [rosbag2_recorder]: Listening for topics...
[INFO] [rosbag2_recorder]: Recording...
[INFO] [rosbag2_recorder]: Subscribed to topic '/amcl_pose'
[INFO] [rosbag2_recorder]: Subscribed to topic '/plan'
[INFO] [rosbag2_recorder]: Subscribed to topic '/tf'
[INFO] [rosbag2_recorder]: Subscribed to topic '/cmd_vel'
[INFO] [rosbag2_recorder]: Subscribed to topic '/tf_static'
[INFO] [rosbag2_recorder]: Subscribed to topic '/odom'
[INFO] [rosbag2_recorder]: Subscribed to topic '/scan'
[INFO] [rosbag2_recorder]: All requested topics are subscribed. Stopping discovery...
```

해석:

```text
All requested topics are subscribed. Stopping discovery...
→ 기록이 멈춘 것이 아니다.
→ 요청한 topic을 모두 찾았고, 더 이상 새 topic을 찾는 discovery 과정만 멈춘 상태다.
→ record 자체는 계속 진행 중이다.
```

이후 RViz2에서 2D Nav Goal을 지정했고, TurtleBot3가 목표 지점 방향으로 이동하는 동안 topic 기록을 진행했다.

목표 이동이 끝난 뒤 record 터미널에서 Ctrl + C로 기록을 종료했다.

---

## 7.4 rosbag 정보 확인

기록 종료 후 아래 명령을 실행했다.

```bash
ros2 bag info rosbags/phase06_logging/p06_nav2_goal_01
```

확인 결과:

```text
Files:             p06_nav2_goal_01_0.db3
Bag size:          8.8 MiB
Storage id:        sqlite3
Duration:          164.287617550s
Messages:          14935
```

topic별 메시지 수:

```text
/scan       793
/odom       4664
/tf_static  1
/cmd_vel    840
/tf         8557
/plan       41
/amcl_pose  39
```

판단:

```text
기록 대상 7개 topic이 모두 정상적으로 저장되었다.
```

---

## 7.5 metadata.yaml 확인

확인 명령:

```bash
cat rosbags/phase06_logging/p06_nav2_goal_01/metadata.yaml | head -n 80
```

확인한 주요 항목:

```text
rosbag2_bagfile_information:
  version: 5
  storage_identifier: sqlite3
  duration:
    nanoseconds: 164287617550
  starting_time:
    nanoseconds_since_epoch: 1780466000860563541
  message_count: 14935
  topics_with_message_count:
```

확인한 파일 정보:

```text
relative_file_paths:
  - p06_nav2_goal_01_0.db3

files:
  - path: p06_nav2_goal_01_0.db3
    duration:
      nanoseconds: 164287617550
    message_count: 14935
```

정리:

```text
metadata.yaml
→ rosbag 정보와 topic별 기록 요약

p06_nav2_goal_01_0.db3
→ 실제 ROS2 메시지 데이터
```

---

## 7.6 rosbag playback 확인

기본 playback 명령:

```bash
cd ~/projects/missionbot-ros2
ros2 bag play rosbags/phase06_logging/p06_nav2_goal_01
```

playback 중 topic info 확인:

```bash
ros2 topic info /scan
ros2 topic info /odom
ros2 topic info /cmd_vel
ros2 topic info /amcl_pose
ros2 topic info /plan
```

확인 결과:

```text
Publisher count: 1
Subscription count: 0
```

해석:

```text
Publisher count: 1
→ rosbag2 player가 해당 topic을 다시 발행하고 있음

Subscription count: 0
→ 현재 그 topic을 구독하는 node가 없음
```

이는 정상이다.

`ros2 topic echo`를 실행하면 echo 명령이 잠깐 subscriber가 되어 메시지를 받을 수 있다.

---

## 7.7 /odom playback 메시지 확인

확인 명령:

```bash
ros2 topic echo /odom --once
```

확인한 주요 필드:

```text
header.frame_id: odom
child_frame_id: base_footprint
pose.pose.position.x
pose.pose.position.y
twist.twist.linear.x
twist.twist.angular.z
```

의미:

```text
저장된 odometry 메시지가 ros2 bag play를 통해 다시 발행되는 것을 확인했다.
```

---

## 7.8 일부 topic 선택 재생

play 옵션 확인:

```bash
ros2 bag play --help | grep -E "topics|rate"
```

/odom, /cmd_vel만 선택 재생:

```bash
cd ~/projects/missionbot-ros2

ros2 bag play rosbags/phase06_logging/p06_nav2_goal_01 \
  --topics /odom /cmd_vel \
  --rate 0.5
```

의미:

```text
--topics /odom /cmd_vel
→ bag 전체 topic 중 /odom과 /cmd_vel만 재생

--rate 0.5
→ 원래 속도의 절반 속도로 재생
```

선택 재생 중 확인한 topic:

```text
/odom
/cmd_vel
```

이를 통해 rosbag playback에서 필요한 topic만 골라 확인할 수 있음을 확인했다.

---

## 7.9 RViz2 playback 시각화

처음에는 일반 RViz2 실행과 bag play만으로는 RViz2에서 움직임이 잘 보이지 않았다.

해결 방법:

```bash
rviz2 --ros-args -p use_sim_time:=true
```

bag play 명령:

```bash
ros2 bag play rosbags/phase06_logging/p06_nav2_goal_01 --rate 0.5 --clock
```

RViz2 설정:

```text
Global Options
→ Fixed Frame: odom

Displays:
→ TF
→ LaserScan
→ Odometry
→ Path
```

확인한 것:

```text
[x] RViz2 Global Status: Ok
[x] Fixed Frame: odom
[x] Odometry Status: Ok
[x] TF 표시
[x] LaserScan 점 표시
[x] Odometry 이동 궤적 표시
[x] Path 표시
```

의미:

```text
rosbag으로 저장된 Navigation2 주행 데이터를 다시 재생하고 RViz2에서 시각화하는 데 성공했다.
```

---

## 8. Phase 6에서 배운 핵심 개념

## 8.1 rosbag2

```text
rosbag2는 ROS2 topic 메시지를 파일로 기록하고 다시 재생할 수 있는 도구다.
```

MissionBot에서의 의미:

```text
주행 중 발생한 센서 데이터, 위치 추정, 경로, 속도 명령을 저장해 이후 분석에 사용할 수 있다.
```

---

## 8.2 ros2 bag record

```text
ROS2 topic 메시지를 bag 파일로 저장하는 명령이다.
```

이번 Phase에서는 다음 topic을 기록했다.

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

## 8.3 ros2 bag info

```text
저장된 bag 파일의 정보와 topic별 메시지 수를 확인하는 명령이다.
```

이번 Phase에서는 다음을 확인했다.

```text
Bag size
Storage id
Duration
Messages
Topic information
```

---

## 8.4 metadata.yaml

```text
metadata.yaml은 bag 파일의 설명서 역할을 한다.
```

포함된 정보:

```text
저장 방식
기록 시간
전체 메시지 수
topic 목록
topic별 메시지 수
실제 데이터 파일 경로
```

---

## 8.5 db3 파일

```text
.db3 파일은 실제 ROS2 메시지 데이터가 저장되는 sqlite3 기반 데이터 파일이다.
```

이번 Phase에서 생성된 파일:

```text
rosbags/phase06_logging/p06_nav2_goal_01/p06_nav2_goal_01_0.db3
```

---

## 8.6 ros2 bag play

```text
저장된 bag 파일을 다시 재생하여 기록된 topic 메시지를 다시 발행하는 명령이다.
```

중요:

```text
ros2 bag play는 Gazebo 로봇을 실제로 다시 움직이는 것이 아니다.
저장된 topic 메시지를 다시 publish하는 기능이다.
```

---

## 8.7 --topics

```text
bag play 시 일부 topic만 선택해서 재생하는 옵션이다.
```

사용 예시:

```bash
ros2 bag play rosbags/phase06_logging/p06_nav2_goal_01 \
  --topics /odom /cmd_vel \
  --rate 0.5
```

---

## 8.8 --rate

```text
bag play 속도를 조절하는 옵션이다.
```

예시:

```text
--rate 1.0
→ 원래 속도

--rate 0.5
→ 절반 속도

--rate 2.0
→ 두 배 속도
```

---

## 8.9 --clock

```text
bag play 중 /clock을 발행하여 simulation time 기준으로 데이터를 재생하게 돕는 옵션이다.
```

Gazebo에서 기록한 bag을 RViz2에서 볼 때 중요하다.

---

## 8.10 use_sim_time

```text
ROS2 node가 실제 컴퓨터 시간이 아니라 /clock topic의 simulation time을 사용하도록 하는 설정이다.
```

RViz2 playback 시 사용한 명령:

```bash
rviz2 --ros-args -p use_sim_time:=true
```

---

## 9. Phase 6 주요 결과물

## 9.1 기록된 rosbag

```text
rosbags/phase06_logging/p06_nav2_goal_01
```

내부 파일:

```text
metadata.yaml
p06_nav2_goal_01_0.db3
```

## 9.2 실험 로그 ID

```text
P06-EXP-0001_nav2_goal_rosbag_record
```

기록 위치:

```text
notes/experiment_log.md
```

## 9.3 Phase 문서

```text
docs/phases/phase06_rosbag2_logging.md
```

## 9.4 Phase 요약

```text
notes/phase_summaries/phase06_rosbag2_logging_summary.md
```

---

## 10. Phase 6에서 발생한 주요 현상

## 10.1 기존 노드가 남아 있던 상태

Phase 6 시작 전 `ros2 node list`에서 기존 Gazebo / RViz2 / Navigation2 노드가 남아 있었다.

예시:

```text
/gazebo
/rviz2
/amcl
/map_server
/planner_server
/controller_server
/bt_navigator
/turtlebot3_diff_drive
/turtlebot3_laserscan
```

판단:

```text
기존 실행 상태가 남아 있으면 새 기록과 섞일 수 있으므로, rosbag 기록 전 반드시 정리해야 한다.
```

해결:

```text
각 실행 터미널에서 Ctrl + C로 Gazebo, RViz2, Navigation2를 종료했다.
```

---

## 10.2 All requested topics are subscribed. Stopping discovery...

ros2 bag record 중 다음 로그가 출력되었다.

```text
All requested topics are subscribed. Stopping discovery...
```

처음에는 기록이 멈춘 것처럼 보일 수 있지만, 실제로는 정상 로그다.

의미:

```text
요청한 모든 topic을 찾고 subscribe했다.
더 이상 새 topic을 찾는 discovery 과정만 멈춘 것이다.
record 자체는 계속 진행 중이다.
```

---

## 10.3 Subscription count가 0으로 보이는 현상

ros2 bag play 중 topic info를 확인했을 때 다음처럼 보였다.

```text
Publisher count: 1
Subscription count: 0
```

판단:

```text
Publisher count 1은 rosbag2 player가 해당 topic을 다시 발행하고 있다는 뜻이다.
Subscription count 0은 현재 그 topic을 구독 중인 node가 없다는 뜻이다.
```

해결 또는 확인:

```bash
ros2 topic echo /odom --once
```

echo 명령은 실행되는 동안 잠깐 subscriber가 되어 메시지를 받을 수 있다.

---

## 10.4 RViz2 playback이 처음에 잘 움직여 보이지 않음

처음에는 일반 rviz2 실행과 bag play만으로는 움직임이 잘 보이지 않았다.

판단:

```text
Gazebo에서 기록한 bag은 simulation time 기준 timestamp를 가진다.
RViz2가 실제 컴퓨터 시간 기준으로 데이터를 보면 TF와 센서 시각화가 안정적으로 보이지 않을 수 있다.
```

해결:

```bash
rviz2 --ros-args -p use_sim_time:=true
```

```bash
ros2 bag play rosbags/phase06_logging/p06_nav2_goal_01 --rate 0.5 --clock
```

결과:

```text
RViz2에서 TF, LaserScan, Odometry, Path가 정상적으로 표시되었다.
```

주의:

```text
이 내용은 정식 troubleshooting이라기보다 Phase 6의 중요한 주의사항으로 기록한다.
```

---

## 11. Phase 5와 Phase 6의 연결

Phase 5에서 확인한 것:

```text
저장된 map 기반 Navigation2 실행
AMCL 초기 위치 추정
2D Nav Goal로 목표 지점 이동
/cmd_vel 발행 확인
/plan 생성 확인
```

Phase 6에서 확장한 것:

```text
Navigation2 주행 중 /scan 기록
/odom 기록
/tf, /tf_static 기록
/cmd_vel 기록
/amcl_pose 기록
/plan 기록
저장된 bag 재생
RViz2에서 playback 데이터 시각화
```

연결 의미:

```text
Phase 5에서는 Navigation2 주행을 실시간으로 확인했다.
Phase 6에서는 그 주행 데이터를 rosbag2로 저장하고, 이후 다시 재생하여 확인할 수 있게 만들었다.
```

---

## 12. 다음 Phase 시작 목표

다음 Phase:

```text
Phase 7. Failure Analysis
```

Phase 7의 핵심 목표:

```text
Phase 6에서 저장한 정상 주행 rosbag을 기준 데이터로 삼고, 실패 유형을 정의한 뒤, 실패 상황을 어떻게 기록하고 분류할지 정리한다.
```

Phase 7에서 중요하게 연결될 개념:

```text
normal run bag
→ 정상 주행 기준 데이터

failure case
→ 실패 상황 기록 단위

failure type
→ 실패 원인 분류 기준

goal_unreachable
→ 목표 지점에 도달하지 못한 실패

localization_failure
→ 위치 추정이 흔들리거나 틀어진 실패

path_planning_failure
→ 경로 계획이 실패하거나 비정상적인 실패

control_oscillation
→ 목표 근처에서 로봇이 흔들리거나 진동하는 실패

sensor_missing
→ 필요한 센서 topic이 없거나 기록되지 않은 실패

timeout
→ 제한 시간 안에 목표를 완료하지 못한 실패
```

단, Phase 7 시작 시 처음부터 복잡한 분석 코드를 만들지 않는다.

첫 단계에서는 Failure Analysis의 목적, 실패 유형 정의, 정상 bag 기준 데이터 확인부터 시작한다.

---

## 13. Phase 7 시작 전 확인할 것

Phase 7 시작 전 확인할 기본 항목:

```bash
cd ~/projects/missionbot-ros2
pwd
ls -lh rosbags/phase06_logging/p06_nav2_goal_01
ros2 bag info rosbags/phase06_logging/p06_nav2_goal_01
```

정상 기대값:

```text
metadata.yaml
p06_nav2_goal_01_0.db3

Duration: 164.287617550s
Messages: 14935
Topic information:
  /scan
  /odom
  /tf_static
  /cmd_vel
  /tf
  /plan
  /amcl_pose
```

---

## 14. Phase 7에서 주의할 점

```text
Phase 7에서는 MoveIt2, LLM/VLM으로 앞서가지 않는다.
우선 Phase 6에서 저장한 rosbag을 기반으로 실패 분석의 기준을 잡는다.
```

처음부터 복잡한 Python 분석 코드나 자동 분류기를 만들지 않는다.

Phase 7의 첫 목표는 다음과 같다.

```text
1. 정상 주행 bag을 기준 데이터로 정의
2. 실패 유형을 문서로 정리
3. 어떤 topic을 보면 어떤 실패를 판단할 수 있는지 연결
4. 실패 case를 저장할 폴더와 기록 양식 확인
```

---

## 15. Phase 6 기록 파일

Phase 6 관련 정리 파일:

```text
README.md
notes/experiment_log.md
docs/phases/phase06_rosbag2_logging.md
notes/phase_summaries/phase06_rosbag2_logging_summary.md
docs/handoffs/MBROS2_Phase6_Handoff.md
docs/handoffs/MBROS2_Phase6_prompt.md
```

experiment_log 업데이트 내용:

```text
P06-EXP-0001_nav2_goal_rosbag_record
```

troubleshooting 정리 여부:

```text
정식 troubleshooting 항목은 필수로 추가하지 않는다.

다만 RViz2 playback에서 use_sim_time=true와 --clock 옵션이 필요했던 내용은 docs/phases/phase06_rosbag2_logging.md의 주의사항으로 정리한다.
```

---

## 16. Phase 6 완료 판정

Phase 6은 다음 기준을 만족했으므로 완료로 판단한다.

```text
[x] rosbag2 기록 전 환경 확인
[x] ros2 bag 명령어 인식 확인
[x] rosbag2 관련 패키지 확인
[x] Navigation2 주행 환경 재구성
[x] 기록 대상 topic 선정
[x] ros2 bag record로 주행 topic 기록
[x] ros2 bag info로 저장 결과 확인
[x] metadata.yaml 확인
[x] ros2 bag play로 playback 확인
[x] topic echo로 playback 메시지 확인
[x] --topics로 선택 재생 확인
[x] --rate로 재생 속도 조절 확인
[x] RViz2에서 playback 시각화 확인
[x] use_sim_time=true와 --clock 옵션 필요성 확인
[x] experiment_log 기록
[x] phase 문서 작성
[x] phase summary 작성
```

완료 의미:

```text
Navigation2 주행
→ 핵심 ROS2 topic 기록
→ bag 파일 저장
→ bag 정보 확인
→ playback
→ RViz2 시각화

위 흐름을 성공적으로 검증했다.
```

---

## 17. 다음 채팅 시작 지점

다음 채팅에서는 아래 상태에서 시작하면 된다.

```text
현재 MissionBot-ROS2는 Phase 6. rosbag2 logging을 완료했다.

완료한 것:
- Navigation2 주행 중 /scan, /odom, /tf, /tf_static, /cmd_vel, /amcl_pose, /plan 기록
- ros2 bag info로 bag 정보 확인
- metadata.yaml로 bag 구조 확인
- ros2 bag play로 저장 topic 재생 확인
- /odom echo로 playback 메시지 확인
- --topics로 일부 topic 선택 재생 확인
- --rate로 playback 속도 조절 확인
- RViz2에서 rosbag playback 시각화 확인
- use_sim_time=true와 --clock 옵션 필요성 확인

주요 결과물:
- rosbags/phase06_logging/p06_nav2_goal_01
- notes/experiment_log.md의 P06-EXP-0001_nav2_goal_rosbag_record
- docs/phases/phase06_rosbag2_logging.md
- notes/phase_summaries/phase06_rosbag2_logging_summary.md

다음 목표:
- Phase 7. Failure Analysis 시작
- 첫 단계는 실패 분석의 목적과 실패 유형 정의
- 정상 주행 bag인 p06_nav2_goal_01을 기준 데이터로 사용
```

추천 시작점:

```text
Phase 7-1. Failure Analysis 기준 정의와 정상 bag 확인
```

첫 단계에서 할 일:

```text
1. Phase 7의 목표 확인
2. 정상 주행 bag 경로 확인
3. ros2 bag info로 정상 bag 정보 재확인
4. 실패 유형 후보 정의
5. 각 실패 유형과 확인할 topic 연결
6. failure_cases 폴더 구조 확인
7. 첫 실패 분석 기록 양식 정리
```
