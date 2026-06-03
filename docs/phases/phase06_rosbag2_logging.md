# Phase 6. rosbag2 Logging

## 1. 목적

이 문서는 MissionBot-ROS2 Phase 6에서 학습한 rosbag2 기록, 확인, 재생, RViz2 시각화 흐름을 정리한다.

Phase 6의 목적은 Navigation2 주행 중 발생하는 주요 ROS2 topic을 rosbag2로 저장하고, 저장된 bag 파일을 다시 재생하여 센서 데이터, 위치 추정, 좌표계, 속도 명령, 경로 계획 정보를 확인하는 것이다.

이 Phase는 다음 Phase인 Failure Analysis로 넘어가기 전, 로봇 주행 데이터를 실험 로그로 남기고 다시 확인할 수 있는 기반을 만드는 단계다.

## 2. 핵심 학습 흐름

Phase 6은 다음 흐름으로 진행했다.

1. rosbag2 기록 전 환경 확인
2. 기존 Gazebo / RViz2 / Navigation2 노드 정리
3. ros2 bag 명령어 인식 확인
4. rosbag2 관련 패키지 확인
5. TurtleBot3 Gazebo World 재실행
6. Navigation2 재실행
7. RViz2에서 2D Pose Estimate로 초기 위치 지정
8. 기록 대상 topic 선정
9. ros2 bag record로 Navigation2 주행 topic 기록
10. RViz2에서 2D Nav Goal 지정
11. TurtleBot3 목표 이동 수행
12. Ctrl + C로 rosbag 기록 종료
13. ros2 bag info로 기록 결과 확인
14. metadata.yaml로 bag 파일 구조 확인
15. ros2 bag play로 저장된 topic 재생 확인
16. topic echo로 playback 메시지 확인
17. --topics 옵션으로 일부 topic 선택 재생
18. --rate 옵션으로 playback 속도 조절
19. RViz2에서 rosbag playback 데이터 시각화
20. use_sim_time과 --clock 옵션 필요성 확인

## 3. rosbag2

rosbag2는 ROS2 topic 메시지를 파일로 기록하고, 나중에 다시 재생할 수 있는 도구다.

쉽게 말하면 rosbag2는 ROS2 시스템에서 흐르는 topic 데이터를 녹화하는 기능이다.

이번 Phase에서 사용한 핵심 명령은 다음과 같다.

```
ros2 bag record
ros2 bag info
ros2 bag play
```

각 명령의 의미는 다음과 같다.

* ros2 bag record: topic 메시지를 bag 파일로 저장한다.
* ros2 bag info: 저장된 bag 파일의 정보와 topic별 메시지 수를 확인한다.
* ros2 bag play: 저장된 bag 파일을 다시 재생하여 topic을 다시 발행한다.

MissionBot에서의 의미:

* Navigation2 주행 중 발생하는 센서와 주행 데이터를 저장한다.
* 이후 실패 분석, 주행 비교, 경로 계획 확인, 위치 추정 분석의 기반이 된다.
* Gazebo나 Navigation2를 매번 다시 실행하지 않아도 저장된 데이터를 재생해 확인할 수 있다.

## 4. 기록 대상 topic

이번 Phase에서 기록한 topic은 다음 7개다.

* /scan
* /odom
* /tf
* /tf_static
* /cmd_vel
* /amcl_pose
* /plan

각 topic의 역할은 다음과 같다.

| Topic      | 메시지 타입                                      | 기록한 이유                        |
| ---------- | ------------------------------------------- | ----------------------------- |
| /scan      | sensor_msgs/msg/LaserScan                   | LiDAR 센서가 주변을 어떻게 감지했는지 확인    |
| /odom      | nav_msgs/msg/Odometry                       | 로봇의 odometry 위치, 자세, 속도 추정 확인 |
| /tf        | tf2_msgs/msg/TFMessage                      | 움직이는 좌표계 관계 확인                |
| /tf_static | tf2_msgs/msg/TFMessage                      | 고정 좌표계 관계 확인                  |
| /cmd_vel   | geometry_msgs/msg/Twist                     | Nav2가 실제로 발행한 속도 명령 확인        |
| /amcl_pose | geometry_msgs/msg/PoseWithCovarianceStamped | AMCL이 추정한 map 기준 현재 위치 확인     |
| /plan      | nav_msgs/msg/Path                           | 목표 지점까지 생성된 global path 확인    |

MissionBot에서의 연결:

* /scan은 장애물과 주변 구조물 확인에 사용된다.
* /odom은 로봇의 실제 이동 흐름을 확인하는 데 사용된다.
* /tf와 /tf_static은 좌표계 연결 상태를 확인하는 데 사용된다.
* /cmd_vel은 제어 명령이 실제로 발행되었는지 확인하는 데 사용된다.
* /amcl_pose는 저장된 map 위에서 로봇 위치 추정이 어떻게 이루어졌는지 확인하는 데 사용된다.
* /plan은 Navigation2가 어떤 경로를 만들었는지 확인하는 데 사용된다.

## 5. 기록 전 환경 확인

rosbag2 기록 전에는 기존 실행 상태가 남아 있지 않은지 확인했다.

확인 명령:

```
ros2 node list
```

기존 Gazebo, RViz2, Navigation2 관련 노드가 남아 있으면 기록 결과가 섞일 수 있다.

남아 있으면 안 되는 대표 노드는 다음과 같다.

* /gazebo
* /rviz2
* /amcl
* /map_server
* /planner_server
* /controller_server
* /bt_navigator
* /turtlebot3_diff_drive
* /turtlebot3_laserscan

기존 노드를 정리한 뒤 rosbag2 기록을 시작했다.

## 6. rosbag2 명령어와 패키지 확인

rosbag2 명령어가 현재 터미널에서 인식되는지 확인했다.

확인 명령:

```
ros2 bag --help
```

출력에서 확인한 주요 sub-command:

* record
* info
* play
* list
* convert
* reindex

rosbag2 관련 패키지도 확인했다.

확인 명령:

```
ros2 pkg list | grep rosbag2
```

확인된 주요 패키지:

* rosbag2
* rosbag2_compression
* rosbag2_compression_zstd
* rosbag2_cpp
* rosbag2_interfaces
* rosbag2_py
* rosbag2_storage
* rosbag2_storage_default_plugins
* rosbag2_transport

이를 통해 Phase 6에서 rosbag2 기록과 재생을 진행할 준비가 되어 있음을 확인했다.

## 7. Gazebo와 Navigation2 재실행

rosbag2 기록을 위해 TurtleBot3 Gazebo World와 Navigation2를 다시 실행했다.

Gazebo 실행 명령:

```
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

Navigation2 실행 명령:

```
cd ~/projects/missionbot-ros2
MAP_FILE=$(pwd)/maps/phase04_slam/tb3_world_slam_map_01.yaml
ros2 launch turtlebot3_navigation2 navigation2.launch.py use_sim_time:=True map:=$MAP_FILE
```

Navigation2 실행 후 RViz2에서 2D Pose Estimate를 사용해 AMCL 초기 위치를 지정했다.

그다음 기록 대상 topic이 존재하는지 확인했다.

확인 명령:

```
ros2 topic list | grep -E "scan|odom|tf|cmd_vel|amcl_pose|plan|map|clock"
```

확인한 주요 topic:

* /scan
* /odom
* /tf
* /tf_static
* /cmd_vel
* /amcl_pose
* /plan
* /map
* /clock

topic 타입 확인 명령:

```
ros2 topic info /scan
ros2 topic info /odom
ros2 topic info /tf
ros2 topic info /tf_static
ros2 topic info /cmd_vel
ros2 topic info /amcl_pose
ros2 topic info /plan
```

확인한 타입:

* /scan: sensor_msgs/msg/LaserScan
  topic info /amcl_pose
  ros2 topic info /plan

확인한 타입:

* /scan: sensor_msgs/msg/LaserScan
* /odom: nav_msgs/msg/Odometry
* /tf: tf2_msgs/msg/TFMessage
* /tf_static: tf2_msgs/msg/TFMessage
* /cmd_vel: geometry_msgs/msg/Twist
* /amcl_pose: geometry_msgs/msg/PoseWithCovarianceStamped
* /plan: nav_msgs/msg/Path

## 8. ros2 bag record

Navigation2가 실행된 상태에서 ros2 bag record를 사용해 주요 topic을 기록했다.

실행 명령:

```
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

명령어 구성:

* ros2 bag record: topic 메시지를 bag 파일로 기록한다.
* /scan: LiDAR 센서 데이터 기록
* /odom: odometry 데이터 기록
* /tf: 동적 좌표계 관계 기록
* /tf_static: 정적 좌표계 관계 기록
* /cmd_vel: 속도 명령 기록
* /amcl_pose: AMCL 위치 추정 기록
* /plan: Navigation2 global path 기록
* -o rosbags/phase06_logging/p06_nav2_goal_01: 저장 경로와 bag 이름 지정

기록 중 출력된 주요 로그:

```
All requested topics are subscribed. Stopping discovery...
```

이 로그는 기록이 멈췄다는 뜻이 아니라, 요청한 모든 topic을 찾았고 더 이상 새로운 topic을 찾는 discovery 과정만 멈췄다는 뜻이다.

record 자체는 계속 진행 중인 상태였다.

## 9. Navigation2 목표 이동 기록

rosbag record가 실행 중인 상태에서 RViz2에서 2D Nav Goal을 지정했다.

진행 흐름:

1. ros2 bag record 실행
2. RViz2에서 2D Nav Goal 선택
3. map 위의 가까운 흰색 빈 공간 클릭
4. 목표 방향으로 드래그
5. TurtleBot3 목표 이동 확인
6. 목표 도착 또는 이동 정지 후 record 터미널에서 Ctrl + C
7. ros2 bag info로 기록 결과 확인

이번 기록은 Navigation2 주행 중 실제 /cmd_vel, /plan, /amcl_pose가 함께 기록되었기 때문에 성공으로 판단했다.

## 10. ros2 bag info

기록 종료 후 ros2 bag info로 저장 결과를 확인했다.

확인 명령:

```
ros2 bag info rosbags/phase06_logging/p06_nav2_goal_01
```

확인 결과:

```
Files:             p06_nav2_goal_01_0.db3
Bag size:          8.8 MiB
Storage id:        sqlite3
Duration:          164.287617550s
Messages:          14935
```

기록된 topic별 메시지 수:

| Topic      | Count |
| ---------- | ----: |
| /scan      |   793 |
| /odom      |  4664 |
| /tf_static |     1 |
| /cmd_vel   |   840 |
| /tf        |  8557 |
| /plan      |    41 |
| /amcl_pose |    39 |

판단:

* 기록 대상 7개 topic이 모두 저장되었다.
* /cmd_vel이 840개 기록되어 실제 속도 명령이 발행되었음을 확인했다.
* /plan이 41개 기록되어 Navigation2가 목표 이동 중 경로를 생성했음을 확인했다.
* /amcl_pose가 39개 기록되어 AMCL 위치 추정 결과도 함께 저장되었음을 확인했다.
* /tf_static은 고정 좌표계 정보이므로 메시지 수가 1개여도 정상이다.

## 11. metadata.yaml

rosbag2는 실제 메시지 데이터와 함께 metadata.yaml 파일을 생성한다.

이번 기록 결과 파일:

* rosbags/phase06_logging/p06_nav2_goal_01/metadata.yaml
* rosbags/phase06_logging/p06_nav2_goal_01/p06_nav2_goal_01_0.db3

metadata.yaml은 bag 파일의 설명서 역할을 한다.

포함된 주요 정보:

* storage_identifier
* duration
* starting_time
* message_count
* topics_with_message_count
* relative_file_paths
* files

실제 메시지 데이터는 .db3 파일에 저장된다.

정리하면 다음과 같다.

* metadata.yaml: rosbag 정보와 topic별 기록 요약
* p06_nav2_goal_01_0.db3: 실제 ROS2 메시지 데이터

## 12. ros2 bag play

저장된 bag 파일을 다시 재생했다.

실행 명령:

```
cd ~/projects/missionbot-ros2
ros2 bag play rosbags/phase06_logging/p06_nav2_goal_01
```

ros2 bag play는 Gazebo 로봇을 물리적으로 다시 움직이는 명령이 아니다.

저장된 topic 메시지를 다시 ROS2 topic으로 발행하는 명령이다.

즉, 다음과 같이 이해할 수 있다.

* record: topic을 파일로 저장
* play: 저장된 topic을 다시 발행

재생 중 topic 확인:

```
ros2 topic info /scan
ros2 topic info /odom
ros2 topic info /cmd_vel
ros2 topic info /amcl_pose
ros2 topic info /plan
```

확인 결과 각 topic의 Publisher count가 1로 나타났다.

이 Publisher는 rosbag2 player가 해당 topic을 다시 발행하고 있다는 뜻이다.

Subscription count가 0으로 나온 것은 문제 상황이 아니다.

그 topic을 현재 구독 중인 node가 없다는 뜻이다.

ros2 topic echo를 실행하면 해당 명령이 잠깐 subscriber가 되어 메시지를 받을 수 있다.

## 13. playback 메시지 확인

rosbag play 중 /odom 메시지를 확인했다.

확인 명령:

```
ros2 topic echo /odom --once
```

확인한 주요 필드:

* header.frame_id: odom
* child_frame_id: base_footprint
* pose.pose.position.x
* pose.pose.position.y
* twist.twist.linear.x
* twist.twist.angular.z

이를 통해 저장된 odometry 메시지가 playback으로 다시 발행되는 것을 확인했다.

## 14. 선택 재생과 속도 조절

ros2 bag play는 일부 topic만 선택해서 재생할 수 있다.

선택 재생 예시:

```
ros2 bag play rosbags/phase06_logging/p06_nav2_goal_01 \
  --topics /odom /cmd_vel \
  --rate 0.5
```

명령어 의미:

* --topics /odom /cmd_vel: /odom과 /cmd_vel만 선택해서 재생
* --rate 0.5: 원래 속도의 절반 속도로 재생

이번 Phase에서는 /odom과 /cmd_vel만 선택 재생하여 위치 추정과 속도 명령 topic이 다시 발행되는 것을 확인했다.

MissionBot에서의 의미:

* 모든 topic을 한 번에 보지 않고 필요한 topic만 골라서 확인할 수 있다.
* 나중에 실패 분석 시 /odom과 /cmd_vel만 따로 보고 주행 명령과 실제 이동 흐름을 비교할 수 있다.
* /scan만 따로 재생해 센서 데이터 흐름을 확인할 수도 있다.

## 15. RViz2 playback 시각화

저장된 bag을 RViz2에서 시각화했다.

처음에는 일반 rviz2 실행과 bag play만으로는 움직임이 잘 보이지 않았다.

원인은 시간 기준 차이로 판단했다.

Gazebo에서 기록한 bag은 simulation time 기준 timestamp를 가진다.

따라서 RViz2도 simulation time 기준으로 실행하고, bag play도 /clock을 함께 발행해야 안정적으로 시각화된다.

RViz2 실행 명령:

```
rviz2 --ros-args -p use_sim_time:=true
```

bag play 명령:

```
ros2 bag play rosbags/phase06_logging/p06_nav2_goal_01 --rate 0.5 --clock
```

RViz2 설정:

* Fixed Frame: odom
* TF Display 추가
* LaserScan Display 추가
* Odometry Display 추가
* Path Display 추가

확인한 것:

* /tf 기반 좌표축 표시
* /scan LiDAR 점 표시
* /odom 기반 Odometry 표시
* /plan Path 표시

이를 통해 저장된 rosbag을 다시 재생하고 RViz2에서 기록 당시의 센서 데이터, odometry, TF, path를 시각화할 수 있음을 확인했다.

## 16. use_sim_time과 --clock

Gazebo 기반 실험에서는 실제 컴퓨터 시간이 아니라 simulation time이 사용된다.

Gazebo는 /clock topic으로 시뮬레이션 시간을 발행한다.

rosbag에 저장된 메시지들도 이 시간 기준을 가진다.

따라서 RViz2에서 rosbag playback 데이터를 제대로 보려면 다음 조건이 중요하다.

1. RViz2를 use_sim_time=true로 실행한다.
2. ros2 bag play에 --clock 옵션을 사용한다.
3. RViz2를 먼저 켜고 bag play를 실행한다.

정리:

```
rviz2 --ros-args -p use_sim_time:=true

ros2 bag play rosbags/phase06_logging/p06_nav2_goal_01 --rate 0.5 --clock
```

이 조합을 통해 RViz2가 bag play에서 발행하는 /clock을 기준으로 /tf, /scan, /odom, /plan 데이터를 안정적으로 표시할 수 있었다.

## 17. Phase 6에서 배운 핵심 개념

## 17.1 rosbag2

ROS2 topic 메시지를 파일로 기록하고 다시 재생할 수 있는 도구다.

## 17.2 bag file

rosbag2가 저장한 기록 단위다.

이번 Phase에서는 p06_nav2_goal_01이라는 bag을 생성했다.

## 17.3 metadata.yaml

bag의 전체 정보를 담는 설명 파일이다.

기록 시간, 메시지 수, topic 목록, 데이터 파일 경로가 들어 있다.

## 17.4 db3 파일

실제 ROS2 메시지 데이터가 저장되는 sqlite3 기반 데이터 파일이다.

## 17.5 ros2 bag record

topic 메시지를 파일로 저장하는 명령이다.

## 17.6 ros2 bag info

저장된 bag의 정보와 topic별 메시지 수를 확인하는 명령이다.

## 17.7 ros2 bag play

저장된 topic 메시지를 다시 ROS2 topic으로 발행하는 명령이다.

## 17.8 --topics

bag play 시 일부 topic만 선택해서 재생하는 옵션이다.

## 17.9 --rate

bag play 속도를 조절하는 옵션이다.

## 17.10 --clock

bag play 중 /clock을 발행하여 simulation time 기준으로 데이터를 재생하게 돕는 옵션이다.

## 17.11 use_sim_time

ROS2 node가 실제 컴퓨터 시간이 아니라 /clock topic의 simulation time을 사용하도록 하는 설정이다.

## 18. Phase 5와 Phase 6의 연결

Phase 5에서 확인한 것:

* 저장된 map 기반 Navigation2 실행
* AMCL 초기 위치 추정
* 2D Nav Goal로 목표 지점 이동
* /cmd_vel 발행 확인
* /plan 생성 확인

Phase 6에서 확장한 것:

* Navigation2 주행 중 /scan 기록
* /odom 기록
* /tf, /tf_static 기록
* /cmd_vel 기록
* /amcl_pose 기록
* /plan 기록
* 저장된 bag을 다시 재생
* RViz2에서 playback 데이터 시각화

연결 의미:

Phase 5에서는 Navigation2 주행을 실시간으로 확인했다.

Phase 6에서는 그 주행 데이터를 rosbag2로 저장하고, 이후 다시 재생하여 확인할 수 있게 만들었다.

즉, MissionBot-ROS2는 실시간 주행 확인에서 로그 기반 재현과 분석 단계로 넘어갈 준비를 갖추었다.

## 19. 다음 Phase와 연결

다음 Phase는 Failure Analysis다.

Phase 6에서 저장한 rosbag은 다음 Phase에서 실패 상황을 분석하기 위한 기반이 된다.

예를 들어 다음과 같은 분석이 가능하다.

* 목표 지점에 도달하지 못했을 때 /cmd_vel이 계속 발행되었는지 확인
* /plan이 생성되었지만 로봇이 움직이지 않았는지 확인
* /amcl_pose가 튀거나 흔들렸는지 확인
* /scan 데이터가 장애물을 어떻게 감지했는지 확인
* /tf 연결이 끊기거나 불안정했는지 확인

이번 Phase에서 기록한 정상 주행 bag은 이후 실패 bag과 비교할 기준 데이터로 사용할 수 있다.

## 20. Phase 6 완료 기준

다음 항목을 완료했으므로 Phase 6을 완료로 판단할 수 있다.

* ros2 bag 명령어 인식 확인
* rosbag2 관련 패키지 확인
* 기록 대상 topic 선정
* Gazebo TurtleBot3 World 실행
* Navigation2 실행
* RViz2에서 2D Pose Estimate 지정
* 2D Nav Goal로 목표 이동 수행
* ros2 bag record로 주행 topic 기록
* ros2 bag info로 저장 결과 확인
* metadata.yaml 확인
* ros2 bag play로 playback 확인
* topic echo로 playback 메시지 확인
* --topics로 선택 재생 확인
* --rate로 재생 속도 조절 확인
* RViz2에서 playback 시각화 확인
* use_sim_time=true와 --clock 옵션 필요성 확인
* experiment_log 기록

## 21. 결론

Phase 6은 MissionBot-ROS2 프로젝트에서 주행 데이터를 저장하고 다시 확인하는 기반을 만든 단계였다.

이전 Phase에서는 Gazebo, RViz2, SLAM, Navigation2를 통해 로봇이 움직이고 목표 지점까지 이동하는 것을 실시간으로 확인했다.

이번 Phase에서는 그 주행 중 발생하는 핵심 topic을 rosbag2로 기록하고, 저장된 bag을 다시 재생해 RViz2에서 시각화했다.

이를 통해 MissionBot-ROS2는 단순 실행 중심의 실습에서 벗어나, 주행 로그를 남기고 이후 분석할 수 있는 구조로 확장되었다.

다음 Phase에서는 이 기록 기반을 활용해 목표 도달 실패, localization 문제, path planning 문제, control oscillation 같은 실패 사례를 분류하고 분석하는 방향으로 넘어갈 수 있다.