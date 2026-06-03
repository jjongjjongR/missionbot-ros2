# MissionBot-ROS2

### 개요
ROS2와 Gazebo 기반으로 TurtleBot3 주행, SLAM/Nav2, rosbag2 로그 분석, MoveIt2 조작 모듈, LLM/VLM 미션 이해를 연결하는 모바일 매니퓰레이션 시스템 프로젝트

#### motivation
- 매니퓰레이션을 하고 싶지만, 실제 로봇 작업은 로봇팔만으로 끝나지 않는다.
이동, 지도, 위치 추정, 센서, 제어, 실패 분석이 함께 필요하다.
그래서 ROS2 기반 이동로봇 시스템부터 단계적으로 이해한다.

#### project scope
- 포함: ROS2 기본 구조, Gazebo TurtleBot3 실행, TF2 & RViz2 확인, SLAM, Navigation2, rosbag2 logging, 실패 분석, MoveIt2 기초, LLM/VLM 미션 이해
- 제외: 대형 VLA 학습, 실제 로봇 하드웨어 제어, 복잡한 로봇팔 강화학습, 실물 로봇 기반 완전한 모바일 매니퓰레이션 구현

### 기술 스택
| Robotics System | Python, C++, ROS2, Gazebo, TurtleBot3, RViz2, TF2, rosbag2, URDF, Xacro |
| --- | --- |
| Navigation & Manipulation | SLAM Toolbox, Navigation2, MoveIt2, ros2_control, MuJoCo |
| AI & Analysis | OpenCV, YOLO, OpenAI API, Qwen2.5-VL(예정), Pandas, Matplotlib |

### Phase map
- [x] Phase 0. Project setup
- [x] Phase 1. ROS2 basics
- [x] Phase 2. Gazebo + TurtleBot3
- [x] Phase 3. RViz2 + TF2
- [x] Phase 4. SLAM
- [x] Phase 5. Navigation2
- [x] Phase 6. rosbag2 logging
- [x] Phase 7. Failure analysis
- [ ] Phase 8. Control basics
- [ ] Phase 9. MoveIt2 basics
- [ ] Phase 10. LLM/VLM extension

### 파일 구조

```text
missionbot-ros2/
├── docs/   (공부 + 구현 내용 정리)
│   ├── 학습용/   (llm 학습용 프롬프트)
│   ├── phases/   (Phase별 진행 정리)
│   ├── concepts/   (ROS2 핵심 개념 정리)
│   ├── templates/   (기록 양식 모음)
│   └── handoffs/   (새 채팅 인수인계 문서)
│
├── src/   (직접 작성할 ROS2 패키지)
│   ├── missionbot_basic/   (ROS2 기본 노드 실습)
│   ├── sensor_logger/   (센서·주행 토픽 기록)
│   ├── failure_analyzer/   (실패 원인 분석 코드)
│   ├── mission_parser/   (LLM 미션 해석)
│   └── vision_object_selector/   (VLM·YOLO 객체 선택)
│
├── configs/   (설정 파일)
│   ├── gazebo/   (Gazebo 실행 설정)
│   ├── rviz/   (RViz2 화면 설정)
│   ├── robot/   (로봇 모델 설정)
│   ├── slam_toolbox/   (SLAM 설정)
│   ├── nav2/   (Navigation2 설정)
│   ├── rosbag2/   (rosbag 기록 설정)
│   ├── moveit2/   (MoveIt2 설정)
│   └── ai/   (LLM·VLM 설정)
│
├── maps/   (SLAM으로 만든 맵)
│   ├── phase04_slam/   (SLAM 실험 맵)
│   └── test_maps/   (테스트용 맵)
│
├── rosbags/   (센서와 주행 로그)
│   ├── phase02_gazebo_turtlebot3/   (Gazebo 주행 로그)
│   ├── phase04_slam/   (SLAM 로그)
│   ├── phase05_navigation2/   (Nav2 주행 로그)
│   ├── phase06_logging/   (rosbag 기록 실험)
│   └── failure_cases/   (실패 상황 rosbag)
│
├── results/   (결과물)
│   ├── screenshots/   (화면 캡처)
│   │   ├── gazebo/   (Gazebo 캡처)
│   │   ├── rviz/   (RViz2 캡처)
│   │   ├── tf_tree/   (TF tree 캡처)
│   │   └── errors/   (오류 화면 캡처)
│   │
│   ├── videos/   (실행 영상)
│   │   ├── demos/   (성공 데모 영상)
│   │   └── failures/   (실패 상황 영상)
│   │
│   ├── logs/   (실행 로그)
│   │   ├── terminal/   (터미널 출력)
│   │   ├── launch/   (launch 실행 로그)
│   │   └── analysis/   (분석 결과 로그)
│   │
│   ├── metrics/   (실험 수치 결과)
│   └── failure_cases/   (실패 사례 정리)
│
└── notes/   (개인 학습 기록, 문제 해결 기록)
    ├── daily_logs/   (일일 진행 기록)
    ├── phase_summaries/   (Phase 종료 요약)
    └── handoff_notes/   (이어가기용 요약)
```

### Result
#### Phase 1. ROS2 basics 완료

Phase 1에서는 `missionbot_basic` 패키지를 생성하고, turtlesim 기반으로 ROS2의 기본 구조를 실습했다.

완료한 내용:

- ROS2 Python 패키지 `missionbot_basic` 생성
- `/turtle1/pose`를 구독하는 `pose_subscriber` 노드 작성
- `/turtle1/cmd_vel`로 속도 명령을 보내는 `velocity_publisher` 노드 작성
- `setup.py`의 `entry_points`에 실행 노드 등록
- `colcon build` 및 `source install/setup.bash` 흐름 확인
- `ros2 run`으로 직접 작성한 노드 실행
- `rqt_graph`로 node-topic 연결 구조 확인
- turtlesim의 `/clear`, `/spawn` service 호출
- `turtlesim_pubsub.launch.py` launch 파일 작성
- `ros2 launch`로 turtlesim, subscriber, publisher 노드 동시 실행

확인한 핵심 구조:

- `/turtlesim` → `/turtle1/pose` → `/pose_subscriber`
- `/velocity_publisher` → `/turtle1/cmd_vel` → `/turtlesim`

다음 Phase에서는 Gazebo와 TurtleBot3를 대상으로 `/cmd_vel`, `/odom`, `/scan` topic 구조를 확인한다.



---

### Failure Analysis
- 이 프로젝트는 성공적인 주행 결과뿐만 아니라 위치 추정 실패, 장애물 차단, 경로 계획 실패, 제어 진동, 시간 초과와 같은 실패 사례도 기록합니다.

### Future Direction
Mobile Robot Foundation
→ Manipulation Basics
→ Mobile Manipulation
→ LLM/VLM-guided Mission Understanding


### 실험 기록 방식

이 프로젝트는 성공 결과뿐만 아니라 실행 과정, 센서 로그, 실패 원인, 수정 시도를 함께 기록한다.  
실험 기록은 README에 직접 누적하지 않고, 아래 위치에 분리해서 관리한다.

| 위치 | 역할 |
|---|---|
| `notes/experiment_log.md` | 전체 실험 인덱스 |
| `notes/troubleshooting.md` | 설치, 실행, 설정 오류와 해결 과정 |
| `results/screenshots/` | RViz2, Gazebo, TF tree 등 화면 캡처 |
| `results/videos/` | 주행, 실패 상황, 데모 영상 |
| `results/logs/` | 터미널 출력, 실행 로그 |
| `results/failure_cases/` | 실패 사례별 원인 분석 문서 |
| `rosbags/` | rosbag2로 저장한 센서 및 주행 로그 |

#### 실험 ID 규칙

실험은 Phase 번호와 실험 번호를 함께 사용한다.

```text
P02-EXP-0001_turtlebot3_gazebo_launch
P03-EXP-0001_rviz2_tf_tree_check
P05-EXP-0001_nav2_goal_success
P05-FAIL-0001_goal_unreachable

기본 기록 토픽
/scan
/odom
/tf
/tf_static
/cmd_vel
/map
+ (카메라, 객체 탐지 시)
/image_raw
/camera_info
/detection_result
```

### Result

#### Phase 1. ROS2 basics

Phase 1에서는 ROS2의 기본 실행 흐름을 turtlesim 기반으로 확인했다.

완료한 내용:

* `missionbot_basic` Python ROS2 패키지 생성
* `/turtle1/pose` topic 구독 노드 작성
* `/turtle1/cmd_vel` topic 발행 노드 작성
* `geometry_msgs/msg/Twist` 메시지 발행 확인
* `/clear`, `/spawn` service 호출 확인
* `turtlesim_pubsub.launch.py` 작성
* `ros2 run`, `ros2 launch`, `rqt_graph` 확인
* build 후 `source install/setup.bash`를 해야 직접 만든 패키지를 현재 터미널이 인식한다는 점 확인

Phase 1 완료 의미:

```text
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

#### Phase 2. Gazebo + TurtleBot3

Phase 2에서는 turtlesim이 아니라 Gazebo 환경의 TurtleBot3 Burger를 실행하고, 실제 이동로봇 시뮬레이션에서 사용되는 핵심 topic 구조를 확인했다.

완료한 내용:

* ROS2 Humble 환경 확인
* `TURTLEBOT3_MODEL=burger` 확인
* `turtlebot3_gazebo`, `turtlebot3_teleop` 패키지 인식 확인
* `ros2 launch turtlebot3_gazebo empty_world.launch.py` 실행
* TurtleBot3 Burger spawn 확인
* `gzclient` crash 발생 후 `gzclient --verbose`로 GUI 재연결
* `/cmd_vel` topic 확인
* `teleop_keyboard`로 TurtleBot3 이동 확인
* `/cmd_vel`의 `geometry_msgs/msg/Twist` 메시지 확인
* `/odom`의 `nav_msgs/msg/Odometry` 메시지 확인
* TurtleBot3 이동 전후 `/odom` position 값 변화 확인
* `/scan`의 `sensor_msgs/msg/LaserScan` 메시지 확인
* `rqt_graph`로 `/teleop_keyboard → /cmd_vel → Gazebo/TurtleBot3` 연결 확인

Phase 2 완료 의미:

```text
Gazebo launch
→ TurtleBot3 spawn
→ /cmd_vel 명령
→ teleop 이동
→ /odom 위치 변화 확인
→ /scan LiDAR 데이터 확인
→ rqt_graph 연결 확인
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
```

다음 단계:

```text
Phase 3. RViz2 + TF2
```

Phase 3에서는 Gazebo에서 실행 중인 TurtleBot3를 RViz2에서 시각화하고, `/tf`, `/tf_static`을 통해 로봇 좌표계 구조를 확인한다.



#### Phase 3. RViz2 + TF2 완료

Phase 3에서는 Gazebo에서 실행 중인 TurtleBot3 Burger를 RViz2에서 시각화하고, TF2를 통해 로봇 좌표계 구조를 확인했다.

완료한 내용:

```text
[x] RViz2 실행
[x] Fixed Frame을 odom으로 설정
[x] TF display 추가
[x] RobotModel display 추가
[x] LaserScan display 추가
[x] /cmd_vel, /odom, /scan, /tf, /tf_static 확인
[x] /scan ranges가 empty_world에서 inf 위주로 나오는 것 확인
[x] view_frames로 TF tree 확인
[x] tf2_echo로 odom → base_footprint transform 확인
[x] tf2_echo로 base_link → base_scan transform 확인
[x] teleop 이동 중 odom → base_footprint transform 변화 확인
```

핵심 연결:

```text
Gazebo TurtleBot3
→ /cmd_vel
→ /odom
→ /scan
→ /tf, /tf_static
→ RViz2
```

확인한 주요 frame:

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

주요 이슈:

```text
gzclient crash가 반복되었지만, TurtleBot3 spawn과 ROS2 topic은 정상 동작했다.
따라서 Gazebo GUI가 아니라 RViz2 중심으로 Phase 3를 진행했다.
```

다음 단계:

```text
Phase 4. SLAM
→ /scan과 TF를 기반으로 SLAM Toolbox에서 지도 생성을 진행한다.
```

---

#### Phase 4 Summary - SLAM

Phase 4에서는 TurtleBot3 Gazebo World 환경에서 SLAM Toolbox를 실행하고, LiDAR `/scan` 데이터와 TF 정보를 기반으로 지도를 생성했다.

이번 Phase의 핵심 목표는 단순히 `/scan`, `/tf`, `/odom` topic을 확인하는 것을 넘어, SLAM Toolbox가 실제로 `/map` topic을 생성하고 RViz2에서 지도 형태로 시각화되는지 확인하는 것이었다.

완료한 작업은 다음과 같다.

```text
[x] SLAM Toolbox 패키지 인식 확인
[x] TurtleBot3 Gazebo World 실행
[x] `/scan`, `/odom`, `/tf`, `/tf_static` topic 확인
[x] `slam_toolbox` online async 모드 실행
[x] `use_sim_time:=True` 적용
[x] `/slam_toolbox` node 실행 확인
[x] `/map` topic 생성 확인
[x] `/map` type이 `nav_msgs/msg/OccupancyGrid`인지 확인
[x] RViz2 Fixed Frame을 `map`으로 설정
[x] RViz2에서 Map display를 `/map`에 연결
[x] TF, RobotModel, LaserScan, Map을 함께 시각화
[x] teleop_keyboard로 TurtleBot3를 천천히 이동시키며 지도 확장 확인
[x] `map_saver_cli`를 사용해 SLAM 지도 저장
[x] `.pgm`, `.yaml` 지도 파일 생성 확인
[x] 저장된 `.yaml` 설정 파일 확인
[x] 저장된 `.pgm` 파일이 실제 PGM 이미지로 인식되는 것 확인
```

실행한 주요 명령어는 다음과 같다.

```bash
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

```bash
ros2 launch slam_toolbox online_async_launch.py use_sim_time:=True
```

```bash
rviz2
```

```bash
ros2 run turtlebot3_teleop teleop_keyboard
```

```bash
ros2 run nav2_map_server map_saver_cli -f maps/phase04_slam/tb3_world_slam_map_01
```

저장된 지도 파일은 다음 위치에 생성되었다.

```text
maps/phase04_slam/tb3_world_slam_map_01.pgm
maps/phase04_slam/tb3_world_slam_map_01.yaml
```

저장된 지도 설정 파일에는 다음과 같은 정보가 포함되었다.

```yaml
image: tb3_world_slam_map_01.pgm
mode: trinary
resolution: 0.05
origin: [-2.94, -2.57, 0]
negate: 0
occupied_thresh: 0.65
free_thresh: 0.25
```

이번 Phase를 통해 확인한 핵심 흐름은 다음과 같다.

```text
Gazebo TurtleBot3 World
→ `/scan`
→ `/tf`, `/tf_static`
→ SLAM Toolbox
→ `/map`
→ RViz2 Map 시각화
→ map_saver_cli 지도 저장
```

이번 Phase의 의미는 다음과 같다.

```text
Phase 3에서는 RViz2와 TF2를 통해 센서와 좌표계를 확인했다.
Phase 4에서는 그 센서 데이터와 좌표계 정보를 SLAM Toolbox에 연결해 실제 지도를 생성하고 저장했다.
이 지도는 다음 Phase인 Navigation2에서 목표 지점 이동을 위한 기반 map으로 사용될 수 있다.
```

---

#### Phase 5 Summary - Navigation2

Phase 5에서는 Phase 4에서 생성한 SLAM 지도 파일을 기반으로 Navigation2를 실행하고, RViz2의 2D Pose Estimate와 2D Nav Goal을 사용해 TurtleBot3가 목표 지점까지 이동하는 흐름을 확인했다.

이번 Phase의 핵심 목표는 단순히 Navigation2 패키지 실행 여부를 확인하는 것이 아니라, 저장된 map 위에서 AMCL 위치 추정, 경로 계획, 속도 명령 생성, 목표 지점 이동이 실제로 연결되는지 확인하는 것이었다.

완료한 작업은 다음과 같다.

```text
[x] Navigation2 실행 전 환경 확인
[x] `nav2_bringup`, `nav2_map_server`, `nav2_amcl` 패키지 인식 확인
[x] `turtlebot3_navigation2` 패키지 인식 확인
[x] Phase 4에서 저장한 map 파일 확인
[x] TurtleBot3 Gazebo World 실행
[x] `/clock`, `/cmd_vel`, `/odom`, `/scan`, `/tf`, `/tf_static` topic 확인
[x] 저장된 map yaml 파일 절대 경로 설정
[x] `turtlebot3_navigation2 navigation2.launch.py` 실행
[x] `use_sim_time:=True` 적용
[x] `/map` topic 생성 확인
[x] `/map` type이 `nav_msgs/msg/OccupancyGrid`인지 확인
[x] `/amcl`, `/map_server`, `/planner_server`, `/controller_server`, `/bt_navigator` node 확인
[x] RViz2 Fixed Frame을 `map`으로 설정
[x] RViz2에서 Map, RobotModel, TF, LaserScan display 확인
[x] 2D Pose Estimate로 AMCL 초기 위치 지정
[x] `/amcl_pose` topic 출력 확인
[x] `map → odom` transform 생성 확인
[x] 2D Nav Goal로 목표 지점 지정
[x] TurtleBot3가 목표 지점 방향으로 이동하는 것 확인
[x] `/plan` topic으로 global path 생성 확인
[x] `/cmd_vel` topic으로 속도 명령 발행 확인
[x] 주요 Nav2 lifecycle node가 `active [3]` 상태인지 확인
```

실행한 주요 명령어는 다음과 같다.

```bash
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

```bash
cd ~/projects/missionbot-ros2
MAP_FILE=$(pwd)/maps/phase04_slam/tb3_world_slam_map_01.yaml
ros2 launch turtlebot3_navigation2 navigation2.launch.py use_sim_time:=True map:=$MAP_FILE
```

```bash
ros2 node list | grep -E "map|amcl|planner|controller|bt|behavior|lifecycle|waypoint"
```

```bash
ros2 topic list | grep -E "map|amcl|plan|cmd_vel|costmap|particlecloud"
```

```bash
ros2 topic info /map
```

```bash
ros2 topic echo /amcl_pose --once
```

```bash
ros2 run tf2_ros tf2_echo map odom
```

```bash
ros2 action list | grep navigate
ros2 action info /navigate_to_pose
```

```bash
ros2 topic echo /cmd_vel
```

```bash
ros2 topic echo /plan --once
```

```bash
ros2 lifecycle get /map_server
ros2 lifecycle get /amcl
ros2 lifecycle get /planner_server
ros2 lifecycle get /controller_server
ros2 lifecycle get /bt_navigator
ros2 lifecycle get /behavior_server
ros2 lifecycle get /waypoint_follower
```

사용한 지도 파일은 다음 위치에 있다.

```text
maps/phase04_slam/tb3_world_slam_map_01.pgm
maps/phase04_slam/tb3_world_slam_map_01.yaml
```

이번 Phase에서 확인한 주요 node는 다음과 같다.

```text
/map_server
/amcl
/planner_server
/controller_server
/bt_navigator
/behavior_server
/waypoint_follower
/lifecycle_manager_localization
/lifecycle_manager_navigation
/global_costmap/global_costmap
/local_costmap/local_costmap
```

이번 Phase에서 확인한 주요 topic은 다음과 같다.

```text
/map
/amcl_pose
/plan
/plan_smoothed
/local_plan
/cmd_vel
/cmd_vel_nav
/global_costmap/costmap
/local_costmap/costmap
/odom
/scan
/tf
/tf_static
/initialpose
/goal_pose
```

이번 Phase를 통해 확인한 핵심 흐름은 다음과 같다.

```text
Gazebo TurtleBot3 World
→ `/odom`, `/scan`, `/tf`, `/clock`
→ 저장된 map yaml 로드
→ Navigation2 실행
→ `/map`
→ AMCL 초기 위치 추정
→ `map → odom` transform 생성
→ RViz2 2D Nav Goal
→ planner_server 경로 생성
→ controller_server 속도 명령 생성
→ `/cmd_vel`
→ TurtleBot3 목표 지점 이동
```

이번 Phase의 의미는 다음과 같다.

```text
Phase 4에서는 SLAM Toolbox를 사용해 TurtleBot3 World 지도를 생성하고 저장했다.
Phase 5에서는 그 저장된 지도를 Navigation2에 연결해, 로봇이 map 위에서 현재 위치를 추정하고 목표 지점까지 이동하는 흐름을 확인했다.

이를 통해 단순한 수동 조작을 넘어, 저장된 지도 기반의 자율 주행 구조를 처음으로 검증했다.
이 구조는 이후 rosbag2 logging, 실패 분석, 제어 기초, 모바일 매니퓰레이션에서 로봇이 작업 위치까지 이동하는 기반이 된다.
```

---

#### Phase 6 Summary - rosbag2 Logging

Phase 6에서는 Navigation2 주행 중 발생하는 주요 ROS2 topic을 `rosbag2`로 기록하고, 저장된 bag 파일을 다시 재생하여 RViz2에서 시각화하는 흐름을 확인했다.

이번 Phase의 핵심 목표는 단순히 bag 파일을 생성하는 것이 아니라, Navigation2 기반 목표 이동 중 발생하는 센서 데이터, 위치 추정, 좌표계, 속도 명령, 경로 계획 데이터를 함께 저장하고, 이후 다시 재생하여 분석 가능한 형태로 남기는 것이었다.

완료한 작업은 다음과 같다.

```text
[x] rosbag2 기록 전 환경 확인
[x] ros2 bag 명령어 인식 확인
[x] rosbag2 관련 패키지 확인
[x] TurtleBot3 Gazebo World 재실행
[x] Navigation2 재실행
[x] RViz2에서 2D Pose Estimate로 초기 위치 지정
[x] 기록 대상 topic 선정
[x] /scan topic 기록
[x] /odom topic 기록
[x] /tf topic 기록
[x] /tf_static topic 기록
[x] /cmd_vel topic 기록
[x] /amcl_pose topic 기록
[x] /plan topic 기록
[x] ros2 bag record로 Navigation2 주행 로그 저장
[x] ros2 bag info로 bag 파일 정보 확인
[x] metadata.yaml로 기록 파일 구조 확인
[x] ros2 bag play로 저장된 topic 재생 확인
[x] /odom 메시지 echo로 playback 확인
[x] --topics 옵션으로 일부 topic 선택 재생 확인
[x] --rate 옵션으로 playback 속도 조절 확인
[x] RViz2에서 rosbag playback 데이터 시각화 확인
[x] use_sim_time=true와 --clock 옵션 필요성 확인
```

기록한 rosbag 결과는 다음과 같다.

```text
Bag path: rosbags/phase06_logging/p06_nav2_goal_01
Storage id: sqlite3
Duration: 164.287617550s
Message count: 14,935
Bag size: 8.8 MiB
Data file: p06_nav2_goal_01_0.db3
Metadata file: metadata.yaml
```

기록된 topic별 메시지 수는 다음과 같다.

```text
/scan       793
/odom       4,664
/tf_static  1
/cmd_vel    840
/tf         8,557
/plan       41
/amcl_pose  39
```

이번 Phase를 통해 MissionBot-ROS2는 Navigation2 주행 결과를 단순히 눈으로 확인하는 단계를 넘어, 센서와 주행 데이터를 rosbag2 파일로 저장하고 다시 재생할 수 있는 구조를 갖추었다.

특히 RViz2 playback 과정에서 Gazebo 기반 기록 데이터는 simulation time 기준으로 저장되므로, RViz2를 다음처럼 실행해야 안정적으로 시각화된다는 점을 확인했다.

```bash
rviz2 --ros-args -p use_sim_time:=true
```

또한 bag 재생 시 `/clock`을 함께 발행하기 위해 다음 옵션을 사용했다.

```bash
ros2 bag play rosbags/phase06_logging/p06_nav2_goal_01 --rate 0.5 --clock
```

이를 통해 `/scan`, `/odom`, `/tf`, `/plan`이 RViz2에서 정상적으로 표시되는 것을 확인했다.

Phase 6 완료 의미는 다음과 같다.

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

#### Phase 7 Summary - Failure Analysis

Phase 7에서는 Phase 6에서 기록한 정상 Navigation2 주행 rosbag을 baseline으로 삼고, 실패 상황을 topic 증거 기반으로 분류하는 Failure Analysis 흐름을 정리했다.

이번 Phase의 핵심 목표는 단순히 “로봇이 실패했다”라고 기록하는 것이 아니라, `/plan`, `/cmd_vel`, `/odom`, `/amcl_pose`, `/scan`, `/tf` 같은 ROS2 topic 기록을 근거로 실패 원인을 판단하는 것이었다.

먼저 정상 주행 bag을 기준 데이터로 확인했다.

```text
Baseline Bag:
rosbags/phase06_logging/p06_nav2_goal_01
```

정상 bag에는 다음 topic이 기록되어 있었다.

```text
/scan
/odom
/tf
/tf_static
/cmd_vel
/amcl_pose
/plan
```

이후 실패 유형 후보를 정의하고, 각 실패 유형을 어떤 topic 증거로 판단할지 정리했다.

대표 실패 유형은 다음과 같다.

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

이번 Phase에서는 첫 실패 사례로 `P07-FAIL-0001_unreachable_goal_test`를 기록했다.

실패 실험에서는 RViz2에서 장애물 내부 또는 도달하기 어려운 위치를 2D Nav Goal로 지정했고, TurtleBot3가 목표 근처까지 접근했지만 최종 목표에는 도달하지 못했다.

기록한 실패 bag은 다음 위치에 저장했다.

```text
rosbags/failure_cases/P07-FAIL-0001_unreachable_goal_test
```

실패 bag 정보는 다음과 같다.

```text
Bag size: 5.2 MiB
Duration: 92.231500380s
Messages: 9038
```

기록된 topic count는 다음과 같다.

```text
/cmd_vel     1034
/plan        51
/amcl_pose   58
/scan        447
/odom        2628
/tf_static   1
/tf          4819
```

분석 결과, `/plan`이 51개 기록되었고 `/cmd_vel`도 1034개 기록되었기 때문에 경로 계획 자체가 완전히 실패한 `path_planning_failure`로 보기는 어려웠다.

또한 `/scan`, `/odom`, `/tf`, `/tf_static`, `/amcl_pose`가 모두 기록되었으므로 `sensor_missing`이나 명확한 `localization_failure` 가능성도 낮다고 판단했다.

최종적으로 이번 실패 사례는 다음과 같이 분류했다.

```text
Failure Type: goal_unreachable
Secondary Symptom: control_oscillation
Confidence: high
```

특히 실패 bag의 뒤쪽 구간에서 `/cmd_vel`을 확인한 결과, `linear.x`는 대부분 `0.0` 또는 매우 작은 값이었고, `angular.z`는 큰 양수와 음수 값이 반복적으로 나타났다.

이는 TurtleBot3가 목표 근처에서 전진하여 목표에 수렴하기보다 회전 동작을 반복했다는 근거로 볼 수 있다.

따라서 이번 Phase에서는 정상 bag과 실패 bag을 비교하고, topic 기반 증거를 통해 실패 유형을 분류하는 기본 Failure Analysis 흐름을 검증했다.

완료한 작업은 다음과 같다.

```text
[x] Phase 6 정상 주행 bag baseline 확인
[x] Failure Type 후보 정의
[x] topic별 판단 기준 정리
[x] failure case 기록 양식 작성
[x] Failure Analysis workflow 정리
[x] 첫 실패 실험 계획 수립
[x] P07-FAIL-0001_unreachable_goal_test 실패 bag 기록
[x] ros2 bag info로 실패 bag 정보 확인
[x] /cmd_vel 기반 control_oscillation 보조 증거 확인
[x] failure report 작성
[x] experiment_log.md에 실패 실험 인덱싱
```

관련 파일은 다음과 같다.

```text
docs/phases/phase07_failure_analysis.md
results/failure_cases/failure_case_template.md
results/failure_cases/P07-FAIL-0001_unreachable_goal_test.md
rosbags/failure_cases/P07-FAIL-0001_unreachable_goal_test
notes/experiment_log.md
```
