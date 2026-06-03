# Phase 5. Navigation2 Summary

## 1. Phase 정보

```text
Phase: Phase 5. Navigation2
Status: 완료
Date: 2026-06-02
```

---

## 2. Phase 목표

Phase 5의 목표는 Phase 4에서 SLAM Toolbox로 생성하고 저장한 map을 기반으로 Navigation2를 실행하고, TurtleBot3가 RViz2에서 지정한 목표 지점까지 이동하는 흐름을 확인하는 것이다.

이번 Phase에서는 단순히 Navigation2 패키지가 실행되는지만 확인하지 않고, 저장된 지도 위에서 다음 흐름이 실제로 연결되는지 확인했다.

```text
저장된 map
→ Navigation2 실행
→ AMCL 위치 추정
→ 2D Pose Estimate로 초기 위치 지정
→ 2D Nav Goal로 목표 지점 지정
→ planner_server 경로 생성
→ controller_server 속도 명령 생성
→ /cmd_vel 발행
→ Gazebo TurtleBot3 이동
```

---

## 3. 사용한 환경

```text
OS: Ubuntu 22.04 LTS
ROS2: Humble Hawksbill
Simulator: Gazebo Classic
Robot: TurtleBot3 Burger
Visualization: RViz2
Navigation: Navigation2
Map source: Phase 4 SLAM result
Project path: ~/projects/missionbot-ros2
```

---

## 4. 사용한 map 파일

Phase 4에서 저장한 SLAM 지도 파일을 사용했다.

```text
maps/phase04_slam/tb3_world_slam_map_01.pgm
maps/phase04_slam/tb3_world_slam_map_01.yaml
```

Navigation2 실행 시에는 `.pgm` 파일이 아니라 `.yaml` 파일을 인자로 전달했다.

```text
maps/phase04_slam/tb3_world_slam_map_01.yaml
```

`.yaml` 파일은 실제 지도 이미지인 `.pgm` 파일의 경로와 해상도, origin, threshold 정보를 담고 있다.

---

## 5. 진행한 작업

이번 Phase에서 완료한 작업은 다음과 같다.

```text
[x] Navigation2 실행 전 환경 확인
[x] nav2_bringup 패키지 인식 확인
[x] nav2_map_server 패키지 인식 확인
[x] nav2_amcl 패키지 인식 확인
[x] turtlebot3_navigation2 패키지 인식 확인
[x] turtlebot3_gazebo 패키지 인식 확인
[x] Phase 4에서 저장한 map 파일 확인
[x] TurtleBot3 Gazebo World 실행
[x] /clock, /cmd_vel, /odom, /scan, /tf, /tf_static topic 확인
[x] 저장된 map yaml 파일 절대 경로 설정
[x] Navigation2 실행
[x] use_sim_time:=True 적용
[x] /map topic 생성 확인
[x] /map type이 nav_msgs/msg/OccupancyGrid인지 확인
[x] AMCL, planner, controller, bt_navigator node 확인
[x] RViz2 Fixed Frame을 map으로 설정
[x] RViz2에서 Map, RobotModel, TF, LaserScan display 확인
[x] 2D Pose Estimate로 초기 위치 지정
[x] /amcl_pose topic 출력 확인
[x] map → odom transform 생성 확인
[x] 2D Nav Goal로 목표 지점 지정
[x] TurtleBot3 목표 지점 이동 확인
[x] /plan topic으로 global path 생성 확인
[x] /cmd_vel topic으로 속도 명령 발행 확인
[x] 두 번째 목표 지점 이동 테스트
[x] Nav2 주요 lifecycle node가 active [3] 상태인지 확인
```

---

## 6. 실행한 주요 명령어

### 6.1 Gazebo TurtleBot3 World 실행

```bash
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

이 명령어로 Phase 4에서 지도를 만들 때 사용했던 TurtleBot3 World를 다시 실행했다.

확인한 주요 topic은 다음과 같다.

```text
/clock
/cmd_vel
/odom
/scan
/tf
/tf_static
```

---

### 6.2 Navigation2 실행

```bash
cd ~/projects/missionbot-ros2
MAP_FILE=$(pwd)/maps/phase04_slam/tb3_world_slam_map_01.yaml
ros2 launch turtlebot3_navigation2 navigation2.launch.py use_sim_time:=True map:=$MAP_FILE
```

각 인자의 의미는 다음과 같다.

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

---

### 6.3 Navigation2 node 확인

```bash
ros2 node list | grep -E "map|amcl|planner|controller|bt|behavior|lifecycle|waypoint"
```

확인한 주요 node는 다음과 같다.

```text
/amcl
/behavior_server
/bt_navigator
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

### 6.4 Navigation2 topic 확인

```bash
ros2 topic list | grep -E "map|amcl|plan|cmd_vel|costmap|particlecloud"
```

확인한 주요 topic은 다음과 같다.

```text
/map
/amcl_pose
/cmd_vel
/cmd_vel_nav
/plan
/plan_smoothed
/local_plan
/global_costmap/costmap
/local_costmap/costmap
/map_updates
```

---

### 6.5 /map topic 확인

```bash
ros2 topic info /map
```

확인 결과는 다음과 같았다.

```text
Type: nav_msgs/msg/OccupancyGrid
Publisher count: 1
Subscription count: 3
```

이를 통해 map_server가 저장된 지도를 `/map` topic으로 정상 발행하고 있음을 확인했다.

---

### 6.6 AMCL 위치 확인

```bash
ros2 topic echo /amcl_pose --once
```

확인 결과 `frame_id: map` 기준으로 로봇의 위치가 출력되었다.

```text
/amcl_pose
→ AMCL이 저장된 map 위에서 추정한 로봇의 현재 위치
```

---

### 6.7 map → odom transform 확인

```bash
ros2 run tf2_ros tf2_echo map odom
```

2D Pose Estimate 이후 `map → odom` transform이 출력되는 것을 확인했다.

이 transform은 저장된 map 기준 좌표계와 로봇의 odom 기준 좌표계를 연결한다.

---

### 6.8 Navigation action 확인

```bash
ros2 action list | grep navigate
```

확인한 action은 다음과 같다.

```text
/navigate_to_pose
/navigate_through_poses
```

RViz2에서 2D Nav Goal을 찍으면 내부적으로 `/navigate_to_pose` action 요청이 사용된다.

---

### 6.9 속도 명령 확인

```bash
ros2 topic echo /cmd_vel
```

TurtleBot3가 목표 지점으로 이동하는 동안 `/cmd_vel` topic으로 속도 명령이 발행되는 것을 확인했다.

```text
/cmd_vel
→ TurtleBot3를 실제로 움직이는 속도 명령 topic
```

---

### 6.10 경로 확인

```bash
ros2 topic echo /plan --once
```

Nav2 planner가 현재 위치에서 목표 지점까지의 global path를 생성하는 것을 확인했다.

```text
/plan
→ 목표 지점까지의 전역 경로
```

---

### 6.11 lifecycle 상태 확인

```bash
ros2 lifecycle get /map_server
ros2 lifecycle get /amcl
ros2 lifecycle get /planner_server
ros2 lifecycle get /controller_server
ros2 lifecycle get /bt_navigator
ros2 lifecycle get /behavior_server
ros2 lifecycle get /waypoint_follower
```

주요 lifecycle node들이 다음 상태임을 확인했다.

```text
active [3]
```

`active [3]`는 해당 Nav2 구성 요소가 실제 동작 가능한 상태로 전환되었음을 의미한다.

---

## 7. Navigation2 주요 node 정리

이번 Phase에서 확인한 주요 node와 역할은 다음과 같다.

```text
/map_server
→ 저장된 map yaml / pgm 파일을 읽고 /map topic으로 발행한다.

/amcl
→ 저장된 map 위에서 로봇의 현재 위치를 추정한다.

/planner_server
→ 현재 위치에서 목표 지점까지 갈 전체 경로를 계산한다.

/controller_server
→ planner가 만든 경로를 따라가기 위한 속도 명령을 생성한다.

/bt_navigator
→ 목표 이동의 전체 흐름을 Behavior Tree 기반으로 관리한다.

/behavior_server
→ 이동 실패나 장애물 상황에서 회전, 후진 같은 복구 행동을 담당한다.

/waypoint_follower
→ 여러 개의 목표 지점을 순서대로 따라갈 때 사용된다.

/lifecycle_manager_localization
→ map_server와 amcl 같은 localization 관련 node의 lifecycle을 관리한다.

/lifecycle_manager_navigation
→ planner, controller, bt_navigator 등 navigation 관련 node의 lifecycle을 관리한다.

/global_costmap/global_costmap
→ 전체 map 기준으로 장애물과 이동 가능 영역을 판단한다.

/local_costmap/local_costmap
→ 로봇 주변의 장애물과 안전거리 영역을 판단한다.
```

---

## 8. Navigation2 주요 topic 정리

이번 Phase에서 확인한 주요 topic과 의미는 다음과 같다.

```text
/map
→ 저장된 지도

/map_updates
→ map 업데이트 정보

/amcl_pose
→ AMCL이 추정한 현재 로봇 위치

/plan
→ planner_server가 생성한 전역 경로

/plan_smoothed
→ 부드럽게 다듬어진 경로

/local_plan
→ controller_server가 참고하는 로컬 경로

/cmd_vel
→ TurtleBot3를 실제로 움직이는 속도 명령

/cmd_vel_nav
→ Navigation2 쪽에서 생성되는 속도 명령

/global_costmap/costmap
→ 전체 지도 기준 장애물 판단 지도

/local_costmap/costmap
→ 로봇 주변 기준 장애물 판단 지도

/odom
→ 로봇의 odometry 정보

/scan
→ TurtleBot3 LiDAR 거리 센서 데이터

/tf
→ 계속 변하는 좌표계 관계

/tf_static
→ 고정된 좌표계 관계

/initialpose
→ RViz2 2D Pose Estimate로 입력되는 초기 위치

/goal_pose
→ RViz2 2D Nav Goal로 입력되는 목표 위치
```

---

## 9. 주요 개념 정리

## 9.1 Navigation2

Navigation2는 저장된 map 위에서 로봇이 목표 지점까지 이동하도록 도와주는 ROS2 navigation stack이다.

이번 Phase에서는 Navigation2를 사용해 TurtleBot3가 RViz2에서 지정한 목표 지점까지 이동하는 것을 확인했다.

---

## 9.2 AMCL

AMCL은 저장된 map 위에서 로봇의 현재 위치를 추정하는 localization 구성 요소다.

이번 Phase에서는 RViz2의 2D Pose Estimate로 초기 위치를 지정한 뒤, `/amcl_pose` topic과 `map → odom` transform을 확인했다.

---

## 9.3 2D Pose Estimate

2D Pose Estimate는 RViz2에서 로봇의 초기 위치와 방향을 지정하는 도구다.

Navigation2 실행 직후에는 AMCL이 로봇이 map 위의 어디에 있는지 모를 수 있다.

따라서 2D Pose Estimate를 통해 AMCL에게 로봇의 초기 위치를 알려줘야 한다.

---

## 9.4 2D Nav Goal

2D Nav Goal은 RViz2에서 로봇의 목표 지점과 최종 방향을 지정하는 도구다.

2D Nav Goal을 찍으면 Navigation2는 내부적으로 `/navigate_to_pose` action을 사용해 목표 이동을 수행한다.

---

## 9.5 Costmap

Costmap은 Navigation2가 로봇이 갈 수 있는 영역과 장애물을 판단하기 위해 사용하는 지도다.

이번 Phase에서는 global costmap과 local costmap 관련 topic을 확인했다.

```text
global_costmap
→ 전체 map 기준 장애물 판단

local_costmap
→ 로봇 주변 기준 장애물 판단
```

---

## 10. 발생한 현상과 해결

## 10.1 map → odom transform 대기 로그

Navigation2 실행 직후 다음과 같은 로그가 발생했다.

```text
Timed out waiting for transform from base_link to map to become available
Invalid frame ID "map" passed to canTransform argument target_frame - frame does not exist
```

처음에는 에러처럼 보였지만, 실제 원인은 AMCL 초기 위치가 아직 지정되지 않아 `map → odom` transform이 생성되지 않은 상태였기 때문이다.

해결 방법은 다음과 같았다.

```text
RViz2
→ 2D Pose Estimate
→ map 위에서 TurtleBot3의 초기 위치와 방향 지정
```

이후 `/amcl_pose`가 출력되었고, `tf2_echo map odom` 명령으로 `map → odom` transform이 생성된 것을 확인했다.

---

## 10.2 LaserScan이 map과 완전히 겹치지 않는 현상

RViz2에서 빨간 LaserScan 점들이 검은 map 벽과 완전히 일치하지 않는 현상이 있었다.

이는 AMCL 초기 위치나 방향이 약간 어긋났을 때 발생할 수 있다.

해결 방법은 다음과 같았다.

```text
2D Pose Estimate를 다시 찍어
로봇의 위치와 방향을 map 위에서 대략 맞춘다.
```

완벽하게 1픽셀 단위로 맞을 필요는 없지만, 목표 이동 전에는 LaserScan과 map 구조가 대략 맞는지 확인해야 한다.

---

## 11. 성공 기준

Phase 5는 다음 기준을 만족했으므로 완료로 판단한다.

```text
[x] Phase 4에서 저장한 map yaml 파일 확인
[x] Gazebo TurtleBot3 World 실행
[x] Navigation2 실행
[x] use_sim_time:=True 적용
[x] /map topic 생성 확인
[x] /map type이 nav_msgs/msg/OccupancyGrid인지 확인
[x] AMCL 관련 node 실행 확인
[x] planner_server 실행 확인
[x] controller_server 실행 확인
[x] bt_navigator 실행 확인
[x] RViz2 Fixed Frame을 map으로 설정
[x] 2D Pose Estimate로 초기 위치 지정
[x] /amcl_pose 출력 확인
[x] map → odom transform 생성 확인
[x] 2D Nav Goal로 목표 지점 지정
[x] TurtleBot3가 목표 지점으로 이동
[x] /plan topic 생성 확인
[x] /cmd_vel topic 발행 확인
[x] 목표 이동 반복 테스트 성공
[x] 주요 lifecycle node가 active [3] 상태
```

---

## 12. 이번 Phase에서 배운 점

이번 Phase를 통해 Navigation2는 단일 노드가 아니라 여러 역할의 node가 함께 동작하는 navigation stack이라는 것을 확인했다.

핵심 구조는 다음과 같다.

```text
map_server
→ amcl
→ planner_server
→ controller_server
→ /cmd_vel
→ TurtleBot3 이동
```

또한 저장된 map 기반 navigation에서는 `2D Pose Estimate`가 중요하다는 점을 확인했다.

Navigation2가 map을 불러오더라도, AMCL이 로봇의 초기 위치를 알지 못하면 `map → odom` transform이 생성되지 않아 costmap과 RViz2에서 transform 관련 로그가 발생할 수 있다.

따라서 저장된 map 기반 Navigation2 실행 흐름은 다음 순서로 정리할 수 있다.

```text
Gazebo World 실행
→ Navigation2 실행
→ map 로드
→ 2D Pose Estimate로 초기 위치 지정
→ map → odom TF 생성 확인
→ 2D Nav Goal로 목표 이동
→ /plan, /cmd_vel 확인
```

---

## 13. MissionBot에서의 의미

Phase 5는 MissionBot-ROS2가 수동 조작 중심의 이동로봇 확인 단계를 넘어, 저장된 map 기반 자율 주행 흐름을 처음으로 검증한 단계다.

Phase 4에서 생성한 지도를 Navigation2에 연결했고, TurtleBot3가 목표 지점까지 이동하는 것을 확인했다.

이 결과는 이후 단계에서 다음 작업의 기반이 된다.

```text
Phase 6. rosbag2 logging
→ Navigation2 주행 중 /scan, /odom, /tf, /cmd_vel, /map 등을 기록

Phase 7. Failure Analysis
→ 목표 도달 실패, localization failure, path planning failure, control oscillation 등을 분류

Phase 8 이후
→ 모바일 매니퓰레이션에서 로봇이 작업 위치까지 이동하는 기반
```

---

## 14. 다음 Phase로 넘길 내용

다음 Phase는 다음과 같다.

```text
Phase 6. rosbag2 logging
```

Phase 6에서는 Navigation2 주행 중 발생하는 주요 topic을 rosbag2로 기록하는 흐름을 확인한다.

다음 Phase에서 기록 후보 topic은 다음과 같다.

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
