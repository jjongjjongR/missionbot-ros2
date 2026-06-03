# Phase 5. Navigation2

## 1. Phase 목표

Phase 5의 목표는 Phase 4에서 생성하고 저장한 SLAM map을 기반으로 Navigation2를 실행하고, TurtleBot3가 RViz2에서 지정한 목표 지점까지 이동하는 흐름을 확인하는 것이다.

이번 Phase에서는 단순히 Navigation2 패키지가 설치되어 있는지 확인하는 것을 넘어, 다음 흐름이 실제로 연결되는지 확인했다.

```text
Gazebo TurtleBot3 World
→ 저장된 map 로드
→ Navigation2 실행
→ AMCL 위치 추정
→ 2D Pose Estimate로 초기 위치 지정
→ 2D Nav Goal로 목표 지점 지정
→ planner_server 경로 생성
→ controller_server 속도 명령 생성
→ /cmd_vel 발행
→ TurtleBot3 목표 지점 이동
```

---

## 2. Phase 4와 Phase 5의 연결

Phase 4에서는 SLAM Toolbox를 사용해 TurtleBot3 World 환경의 지도를 생성하고 저장했다.

저장된 지도 파일은 다음과 같다.

```text
maps/phase04_slam/tb3_world_slam_map_01.pgm
maps/phase04_slam/tb3_world_slam_map_01.yaml
```

Phase 5에서는 이 중 `.yaml` 파일을 Navigation2 실행 인자로 전달했다.

```text
maps/phase04_slam/tb3_world_slam_map_01.yaml
```

`.yaml` 파일은 실제 지도 이미지인 `.pgm` 파일을 어떻게 해석해야 하는지 알려주는 설정 파일이다.

즉, Phase 4에서 만든 지도는 Phase 5에서 로봇이 목표 지점까지 이동할 기준 map으로 사용된다.

---

## 3. 사용 환경

```text
OS: Ubuntu 22.04 LTS
ROS2: Humble Hawksbill
Simulator: Gazebo Classic
Robot: TurtleBot3 Burger
Visualization: RViz2
Navigation: Navigation2
SLAM map: Phase 4에서 저장한 map
Project path: ~/projects/missionbot-ros2
```

---

## 4. 시작 전 확인

Navigation2를 실행하기 전에 다음 항목을 확인했다.

```text
[x] 기존 Gazebo / RViz2 / SLAM 관련 node가 남아 있지 않은지 확인
[x] ROS2 Humble 환경 확인
[x] TURTLEBOT3_MODEL=burger 확인
[x] rviz2 실행 파일 인식 확인
[x] nav2_bringup 패키지 인식 확인
[x] nav2_map_server 패키지 인식 확인
[x] nav2_amcl 패키지 인식 확인
[x] turtlebot3_navigation2 패키지 인식 확인
[x] turtlebot3_gazebo 패키지 인식 확인
[x] Phase 4에서 저장한 map 파일 확인
```

확인 명령어는 다음과 같다.

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

---

## 5. Gazebo TurtleBot3 World 실행

Navigation2는 실제 로봇 또는 시뮬레이션 로봇에서 발행되는 `/odom`, `/scan`, `/tf`, `/clock` 정보를 사용한다.

따라서 먼저 TurtleBot3 Gazebo World를 실행했다.

```bash
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

이 명령은 벽과 구조물이 있는 TurtleBot3 World에 TurtleBot3 Burger를 spawn한다.

Phase 4에서 이 world를 기반으로 SLAM map을 만들었기 때문에, Phase 5에서도 같은 world를 사용했다.

---

## 6. Navigation2 입력 topic 확인

Gazebo 실행 후 Navigation2가 사용할 기본 topic이 살아 있는지 확인했다.

```bash
ros2 topic list | grep -E "cmd_vel|odom|scan|tf|clock"
```

확인한 주요 topic은 다음과 같다.

```text
/clock
/cmd_vel
/odom
/scan
/tf
/tf_static
```

각 topic의 의미는 다음과 같다.

```text
/clock
→ Gazebo 시뮬레이션 시간

/cmd_vel
→ TurtleBot3 속도 명령 topic

/odom
→ TurtleBot3 위치, 자세, 속도 추정 topic

/scan
→ TurtleBot3 LiDAR 거리 센서 topic

/tf
→ 계속 변하는 좌표계 관계 topic

/tf_static
→ 고정된 좌표계 관계 topic
```

추가로 각 topic의 타입도 확인했다.

```bash
ros2 topic info /odom
ros2 topic info /scan
ros2 topic info /tf
ros2 topic info /tf_static
ros2 topic echo /clock --once
```

`/scan`이 실제 거리값을 발행하는지도 확인했다.

```bash
ros2 topic echo /scan --once --field ranges | head -n 20
```

`turtlebot3_world`에는 벽과 구조물이 있기 때문에 `/scan` ranges에 숫자 거리값이 섞여 나오는 것을 확인할 수 있다.

---

## 7. Navigation2 실행

Navigation2 실행 전, Phase 4에서 저장한 map yaml 파일의 절대 경로를 변수로 만들었다.

```bash
cd ~/projects/missionbot-ros2

MAP_FILE=$(pwd)/maps/phase04_slam/tb3_world_slam_map_01.yaml

echo $MAP_FILE

ls -lh $MAP_FILE
```

이후 Navigation2를 실행했다.

```bash
ros2 launch turtlebot3_navigation2 navigation2.launch.py use_sim_time:=True map:=$MAP_FILE
```

명령어 구성은 다음과 같다.

```text
ros2 launch
→ ROS2 launch 파일 실행

turtlebot3_navigation2
→ TurtleBot3용 Navigation2 설정 패키지

navigation2.launch.py
→ TurtleBot3 Navigation2 실행 launch 파일

use_sim_time:=True
→ Gazebo의 /clock 시뮬레이션 시간을 사용

map:=$MAP_FILE
→ Phase 4에서 저장한 map yaml 파일을 Navigation2에 전달
```

Gazebo 환경에서는 실제 컴퓨터 시간이 아니라 `/clock`으로 흐르는 시뮬레이션 시간을 사용하기 때문에 `use_sim_time:=True` 설정이 중요하다.

---

## 8. Navigation2 실행 확인

Navigation2 실행 후 주요 node가 생성되었는지 확인했다.

```bash
ros2 node list | grep -E "map|amcl|planner|controller|bt|behavior|lifecycle|recover|waypoint"
```

확인한 주요 node는 다음과 같다.

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

Navigation2 관련 topic도 확인했다.

```bash
ros2 topic list | grep -E "map|amcl|plan|cmd_vel|costmap|particlecloud"
```

확인한 주요 topic은 다음과 같다.

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

`/map` topic 타입도 확인했다.

```bash
ros2 topic info /map
```

확인 결과는 다음과 같았다.

```text
Type: nav_msgs/msg/OccupancyGrid
Publisher count: 1
Subscription count: 3
```

이를 통해 `map_server`가 저장된 map을 `/map` topic으로 정상 발행하고 있음을 확인했다.

---

## 9. RViz2 설정

Navigation2 실행 후 RViz2에서 다음 설정을 확인했다.

```text
Global Options
→ Fixed Frame: map
```

확인한 주요 Display는 다음과 같다.

```text
Map
RobotModel
TF
LaserScan
Global Planner
Controller
```

각 Display의 의미는 다음과 같다.

```text
Map
→ 저장된 지도 시각화

RobotModel
→ TurtleBot3 모델 시각화

TF
→ map, odom, base_footprint, base_link, base_scan 등 좌표계 관계 시각화

LaserScan
→ 현재 LiDAR가 보고 있는 거리 데이터 시각화

Global Planner
→ 목표 지점까지의 전역 경로 시각화

Controller
→ 로컬 주행 경로 또는 제어 관련 시각화
```

AMCL Particle Swarm, MarkerArray 등은 필요에 따라 꺼서 화면을 정리했다.

---

## 10. AMCL 초기 위치 지정

Navigation2 실행 직후 다음과 같은 로그가 발생했다.

```text
Timed out waiting for transform from base_link to map to become available
Invalid frame ID "map" passed to canTransform argument target_frame - frame does not exist
```

처음에는 에러처럼 보였지만, 실제 원인은 AMCL에 초기 위치를 아직 지정하지 않아 `map → odom` transform이 생성되지 않은 상태였기 때문이다.

Navigation2에서 저장된 map 기반으로 위치 추정을 하려면 AMCL이 로봇이 map 위의 어디에 있는지 알아야 한다.

이를 위해 RViz2에서 2D Pose Estimate를 사용했다.

```text
RViz2 상단 툴바
→ 2D Pose Estimate
→ map 위에서 현재 로봇 위치 클릭
→ 로봇이 바라보는 방향으로 드래그
→ 마우스 놓기
```

2D Pose Estimate 이후 `/amcl_pose`를 확인했다.

```bash
ros2 topic echo /amcl_pose --once
```

출력 예시는 다음과 같다.

```text
header:
  frame_id: map
pose:
  pose:
    position:
      x: ...
      y: ...
    orientation:
      z: ...
      w: ...
```

또한 `map → odom` transform이 생성되었는지 확인했다.

```bash
ros2 run tf2_ros tf2_echo map odom
```

정상적으로 Translation과 Rotation 값이 출력되는 것을 확인했다.

이후 transform timeout 로그가 사라졌다.

---

## 11. LaserScan과 map 정렬 확인

RViz2에서 빨간 LaserScan 점들이 검은 map 벽과 완전히 일치하지 않는 현상이 있었다.

이 현상은 AMCL 초기 위치나 방향이 약간 어긋났을 때 발생할 수 있다.

해결 방법은 다음과 같다.

```text
2D Pose Estimate를 다시 찍어
로봇의 위치와 방향을 map 위에서 대략 맞춘다.
```

판단 기준은 다음과 같다.

```text
1. 빨간 LaserScan 점들이 검은 map 벽과 대략 겹치는지 확인
2. RobotModel이 map 안쪽에 자연스럽게 위치하는지 확인
3. TF 축이 RobotModel 근처에 있는지 확인
4. transform 관련 에러 로그가 반복되지 않는지 확인
```

완벽하게 1픽셀 단위로 맞을 필요는 없지만, 목표 이동 전에는 LaserScan과 map 구조가 대략 맞는지 확인하는 것이 좋다.

---

## 12. 2D Nav Goal로 목표 지점 이동

AMCL 초기 위치를 지정한 후, RViz2에서 2D Nav Goal을 사용해 목표 지점을 지정했다.

```text
RViz2 상단 툴바
→ 2D Nav Goal
→ map 위의 흰색 빈 공간 클릭
→ 최종 방향으로 드래그
→ 마우스 놓기
```

처음 목표 지점은 다음 기준으로 선택했다.

```text
- 로봇 근처의 흰색 빈 공간
- 검은 벽이나 장애물 위가 아닌 곳
- 너무 멀지 않은 곳
- 벽과 너무 가깝지 않은 곳
```

2D Nav Goal을 찍으면 Navigation2는 내부적으로 `/navigate_to_pose` action을 사용한다.

action server가 살아 있는지 확인했다.

```bash
ros2 action list | grep navigate
```

확인한 action은 다음과 같다.

```text
/navigate_to_pose
/navigate_through_poses
```

추가 확인 명령어는 다음과 같다.

```bash
ros2 action info /navigate_to_pose
```

목표 지점 이동 중 `/cmd_vel` topic도 확인했다.

```bash
ros2 topic echo /cmd_vel
```

`/cmd_vel`은 TurtleBot3를 실제로 움직이는 속도 명령 topic이다.

경로 생성도 확인했다.

```bash
ros2 topic echo /plan --once
```

`/plan` topic을 통해 planner_server가 현재 위치에서 목표 지점까지의 global path를 생성하는 것을 확인했다.

---

## 13. 반복 목표 이동 테스트

첫 번째 목표 이동이 성공한 뒤, 한 번 더 다른 가까운 목표 지점을 지정해 반복 이동 테스트를 진행했다.

두 번째 목표도 다음 기준으로 지정했다.

```text
- 첫 번째 목표와 다른 방향
- 로봇과 너무 멀지 않은 곳
- 흰색 빈 공간 중앙
- 장애물이나 벽에서 떨어진 곳
```

반복 테스트를 통해 Navigation2가 한 번만 우연히 동작한 것이 아니라, 목표 지점을 다시 지정해도 경로 계획과 이동이 정상적으로 이어지는 것을 확인했다.

---

## 14. lifecycle 상태 확인

Navigation2의 주요 node들은 lifecycle node로 관리된다.

실행만 되어 있는 것이 아니라 실제 동작 가능한 상태인지 확인하기 위해 lifecycle 상태를 확인했다.

```bash
ros2 lifecycle get /map_server
ros2 lifecycle get /amcl
ros2 lifecycle get /planner_server
ros2 lifecycle get /controller_server
ros2 lifecycle get /bt_navigator
ros2 lifecycle get /behavior_server
ros2 lifecycle get /waypoint_follower
```

확인 결과는 모두 다음 상태였다.

```text
active [3]
```

`active [3]`는 해당 node가 실제 동작 가능한 상태로 전환되었음을 의미한다.

---

## 15. Navigation2 주요 node 정리

이번 Phase에서 확인한 주요 node는 다음과 같다.

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

핵심 흐름은 다음과 같다.

```text
map_server
→ amcl
→ planner_server
→ controller_server
→ /cmd_vel
→ TurtleBot3 이동
```

---

## 16. Navigation2 주요 topic 정리

이번 Phase에서 확인한 주요 topic은 다음과 같다.

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

## 17. 주요 action 정리

Navigation2의 목표 이동은 단순 topic만으로 이루어지지 않고 action 구조를 사용한다.

확인한 action은 다음과 같다.

| Action                    | 의미                |
| ------------------------- | ----------------- |
| `/navigate_to_pose`       | 하나의 목표 지점까지 이동    |
| `/navigate_through_poses` | 여러 목표 지점을 순서대로 이동 |

RViz2에서 2D Nav Goal을 찍으면 내부적으로 `/navigate_to_pose` action 요청이 들어간다.

---

## 18. 이번 Phase에서 배운 핵심 개념

## 18.1 Navigation2

Navigation2는 저장된 지도 위에서 로봇이 목표 지점까지 이동하도록 도와주는 ROS2 navigation stack이다.

단일 node가 아니라 map_server, amcl, planner_server, controller_server, bt_navigator, costmap 등 여러 구성 요소가 함께 동작한다.

---

## 18.2 AMCL

AMCL은 저장된 map 위에서 로봇의 현재 위치를 추정하는 localization 구성 요소다.

이번 Phase에서는 RViz2의 2D Pose Estimate를 사용해 초기 위치를 지정했고, 이후 `/amcl_pose`와 `map → odom` transform이 생성되는 것을 확인했다.

---

## 18.3 2D Pose Estimate

2D Pose Estimate는 RViz2에서 로봇의 초기 위치와 방향을 지정하는 도구다.

Navigation2 실행 직후에는 AMCL이 로봇이 map 위의 어디에 있는지 모를 수 있다.

따라서 2D Pose Estimate로 초기 위치를 지정해야 `map → odom` transform이 생성되고, costmap과 planner가 정상 동작할 수 있다.

---

## 18.4 2D Nav Goal

2D Nav Goal은 RViz2에서 로봇의 목표 지점과 최종 방향을 지정하는 도구다.

2D Nav Goal을 찍으면 Navigation2는 경로를 계산하고, controller가 `/cmd_vel`을 발행해 로봇을 움직인다.

---

## 18.5 Costmap

Costmap은 로봇이 이동 가능한 영역과 장애물을 판단하기 위해 사용하는 지도다.

```text
global_costmap
→ 전체 map 기준 장애물 판단

local_costmap
→ 로봇 주변 기준 장애물 판단
```

Navigation2는 costmap을 기반으로 목표 지점까지 갈 수 있는지, 장애물이 있는지, 안전하게 이동할 수 있는지 판단한다.

---

## 18.6 Lifecycle node

Navigation2의 주요 구성 요소는 lifecycle node로 관리된다.

단순히 node가 실행되었다고 바로 동작 가능한 것이 아니라, `active` 상태가 되어야 실제 기능을 수행할 수 있다.

이번 Phase에서는 주요 node가 모두 `active [3]` 상태임을 확인했다.

---

## 19. 발생한 주요 현상

## 19.1 초기 map → odom transform 대기 로그

Navigation2 실행 직후 다음 로그가 반복되었다.

```text
Timed out waiting for transform from base_link to map to become available
Invalid frame ID "map" passed to canTransform argument target_frame - frame does not exist
```

이 로그는 실제 실행 실패라기보다, 2D Pose Estimate를 하기 전 AMCL 초기 위치가 지정되지 않아 `map → odom` transform이 아직 생성되지 않은 상태에서 발생한 것이다.

해결 방법은 다음과 같다.

```text
RViz2
→ 2D Pose Estimate
→ map 위에서 현재 로봇 위치와 방향 지정
```

이후 `/amcl_pose`가 출력되고 `tf2_echo map odom`에서 transform 값이 출력되면서 해당 로그가 사라졌다.

---

## 19.2 LaserScan과 map이 완전히 겹치지 않는 현상

RViz2에서 LaserScan 점들이 map 벽과 완전히 겹치지 않는 현상이 있었다.

이는 AMCL 초기 위치나 방향이 약간 어긋났을 때 발생할 수 있다.

해결 방법은 다음과 같다.

```text
2D Pose Estimate를 다시 찍어
로봇의 위치와 방향을 map 위에서 대략 맞춘다.
```

완벽하게 맞출 필요는 없지만, 목표 이동 전에는 LaserScan과 map 구조가 대략 맞는지 확인하는 것이 좋다.

---

## 20. Phase 5 완료 기준

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

---

## 21. MissionBot에서의 의미

Phase 5는 MissionBot-ROS2가 수동 조작 중심의 이동로봇 확인 단계를 넘어, 저장된 map 기반 자율 주행 흐름을 처음으로 검증한 단계다.

Phase 4에서 생성한 지도를 Navigation2에 연결했고, TurtleBot3가 RViz2에서 지정한 목표 지점까지 이동하는 것을 확인했다.

이 결과는 이후 단계에서 다음 작업의 기반이 된다.

```text
Phase 6. rosbag2 logging
→ Navigation2 주행 중 /scan, /odom, /tf, /cmd_vel, /map 등을 기록

Phase 7. Failure Analysis
→ 목표 도달 실패, localization failure, path planning failure, control oscillation 등을 분류

Phase 8 이후
→ 모바일 매니퓰레이션에서 로봇이 작업 위치까지 이동하는 기반
```

즉, 이번 Phase는 이후 모바일 매니퓰레이션에서 로봇이 작업 위치까지 이동하기 위한 navigation foundation 역할을 한다.

---

## 22. 다음 Phase

다음 Phase는 다음과 같다.

```text
Phase 6. rosbag2 logging
```

Phase 6에서는 Navigation2 주행 중 발생하는 주요 topic을 rosbag2로 기록하는 흐름을 확인한다.

기록 후보 topic은 다음과 같다.

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

추천 시작 지점은 다음과 같다.

```text
Phase 6-1. rosbag2 기록 전 토픽 선정 및 저장 폴더 확인
```
