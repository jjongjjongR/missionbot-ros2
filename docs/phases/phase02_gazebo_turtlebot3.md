# Phase 2. Gazebo + TurtleBot3

## 1. Phase 목표

Phase 2의 목표는 turtlesim이 아니라 Gazebo 환경에서 TurtleBot3 Burger를 실행하고, 실제 이동로봇 시뮬레이션에서 사용되는 핵심 ROS2 topic 구조를 확인하는 것이다.

이번 Phase에서는 처음부터 SLAM, Navigation2, MoveIt2로 넘어가지 않고, 다음 세 topic을 중심으로 확인했다.

```text
/cmd_vel
/odom
/scan
```

---

## 2. 이번 Phase에서 진행한 것

```text
[x] ROS2 Humble 환경 확인
[x] TURTLEBOT3_MODEL=burger 확인
[x] turtlebot3_gazebo 패키지 인식 확인
[x] turtlebot3_teleop 패키지 인식 확인
[x] Gazebo TurtleBot3 empty_world 실행
[x] TurtleBot3 Burger spawn 확인
[x] gzclient crash 발생 후 gzclient --verbose로 GUI 재연결 확인
[x] /cmd_vel topic 확인
[x] /odom topic 확인
[x] /scan topic 확인
[x] teleop_keyboard로 TurtleBot3 이동 확인
[x] /cmd_vel 실제 메시지 값 확인
[x] /odom 이동 전후 값 변화 확인
[x] /scan LaserScan 데이터 확인
[x] rqt_graph로 node-topic 연결 확인
```

---

## 3. Gazebo 실행 구조

Gazebo는 크게 두 부분으로 나뉜다.

```text
gzserver
→ 실제 시뮬레이션을 실행하는 서버
→ 물리 계산, 센서, 로봇 plugin, topic 발행 담당

gzclient
→ 사람이 보는 GUI 화면
→ Gazebo 창, 카메라, 모델 시각화 담당
```

이번 Phase에서 `gzclient`가 한 번 crash 되었지만, `gzserver`는 살아 있었고 TurtleBot3도 정상 spawn되어 있었다.

이를 통해 Gazebo GUI가 죽어도 시뮬레이션 서버와 ROS2 topic은 살아 있을 수 있다는 점을 확인했다.

---

## 4. TurtleBot3 empty_world 실행

사용한 명령어는 다음과 같다.

```bash
ros2 launch turtlebot3_gazebo empty_world.launch.py
```

이 명령어는 `turtlebot3_gazebo` 패키지 안의 `empty_world.launch.py`를 실행한다.

실행 결과 Gazebo 빈 월드에 TurtleBot3 Burger가 spawn되었다.

확인한 주요 로그는 다음과 같다.

```text
Spawn status: SpawnEntity: Successfully spawned entity [burger]
```

이 로그를 통해 TurtleBot3 Burger가 Gazebo 서버 안에 정상적으로 생성된 것을 확인했다.

---

## 5. gzclient crash와 재연결

처음 launch 실행 중 다음과 같은 오류가 발생했다.

```text
gzclient: Assertion `px != 0' failed.
[ERROR] [gzclient-2]: process has died
```

하지만 같은 로그에서 TurtleBot3 spawn은 성공했고, `/cmd_vel`, `/odom`, `/scan` topic도 살아 있었다.

따라서 이 문제는 TurtleBot3 spawn 실패가 아니라 Gazebo GUI 클라이언트인 `gzclient` 쪽 문제로 판단했다.

새 터미널에서 다음 명령어를 실행해 GUI를 다시 연결했다.

```bash
gzclient --verbose
```

재연결 후 Gazebo master에 연결되는 것을 확인했다.

```text
Connected to gazebo master @ http://127.0.0.1:11345
```

---

## 6. /cmd_vel topic

`/cmd_vel`은 로봇에게 속도 명령을 보내는 topic이다.

메시지 타입은 다음과 같다.

```text
geometry_msgs/msg/Twist
```

`Twist` 메시지는 크게 두 부분으로 나뉜다.

```text
linear
→ 직선 이동 속도

angular
→ 회전 속도
```

TurtleBot3에서는 주로 다음 값을 확인했다.

```text
linear.x
→ 전진/후진 속도

angular.z
→ 제자리 회전 속도
```

이번 Phase에서는 `teleop_keyboard`를 실행해 키보드 입력이 `/cmd_vel` 메시지로 바뀌고, Gazebo TurtleBot3가 이를 받아 움직이는 것을 확인했다.

흐름은 다음과 같다.

```text
키보드 입력
→ teleop_keyboard
→ /cmd_vel
→ turtlebot3_diff_drive
→ TurtleBot3 이동
```

---

## 7. /odom topic

`/odom`은 odometry 정보를 담는 topic이다.

메시지 타입은 다음과 같다.

```text
nav_msgs/msg/Odometry
```

역할은 다음과 같다.

```text
로봇이 시작 위치 기준으로 얼마나 이동했는지,
어느 방향을 보고 있는지,
현재 속도가 어느 정도인지 알려준다.
```

확인한 주요 항목은 다음과 같다.

```text
header.frame_id: odom
child_frame_id: base_footprint
pose.pose.position.x
pose.pose.position.y
```

이번 Phase에서는 TurtleBot3를 움직이기 전과 후의 `/odom` 값을 비교했고, `position.x` 또는 `position.y` 값이 변하는 것을 확인했다.

Phase 1의 `/turtle1/pose`가 turtlesim 위치 확인이었다면, Phase 2의 `/odom`은 실제 이동로봇 구조에 가까운 위치 추정 topic이다.

---

## 8. /scan topic

`/scan`은 TurtleBot3의 LiDAR 센서 데이터 topic이다.

메시지 타입은 다음과 같다.

```text
sensor_msgs/msg/LaserScan
```

역할은 다음과 같다.

```text
로봇 주변의 벽이나 장애물까지의 거리를 여러 방향으로 측정한다.
```

확인한 주요 항목은 다음과 같다.

```text
angle_min
angle_max
angle_increment
range_min
range_max
ranges
```

`ranges`는 각 방향에 대한 거리 배열이다.

`inf` 값은 해당 방향에 측정 가능한 장애물이 없거나 너무 멀다는 뜻으로 볼 수 있다.

이번 Phase에서는 `/scan` 메시지가 정상 출력되는 것을 확인했다.

---

## 9. rqt_graph 확인

`rqt_graph`는 현재 실행 중인 ROS2 node와 topic 연결 구조를 시각적으로 보여주는 도구다.

이번 Phase에서는 다음 연결을 확인했다.

```text
/teleop_keyboard
→ /cmd_vel
→ Gazebo/TurtleBot3 관련 node
```

이를 통해 단순히 topic 이름만 확인한 것이 아니라, 실제 publisher와 subscriber가 연결되어 있는지도 확인했다.

---

## 10. Phase 1과 Phase 2의 연결

Phase 1에서 배운 turtlesim 구조는 다음과 같았다.

```text
/velocity_publisher
→ /turtle1/cmd_vel
→ /turtlesim
→ /turtle1/pose
→ /pose_subscriber
```

Phase 2에서는 이 구조가 실제 이동로봇 시뮬레이션 구조로 확장되었다.

```text
/teleop_keyboard
→ /cmd_vel
→ TurtleBot3 diff drive
→ /odom

TurtleBot3 LiDAR
→ /scan
```

즉, Phase 1에서 배운 publisher, subscriber, topic, launch 개념이 Phase 2에서 Gazebo TurtleBot3 구조로 이어졌다.

---

## 11. 이번 Phase에서 배운 점

* ROS2 작업을 시작하기 전에 현재 터미널 환경을 먼저 확인해야 한다.
* `TURTLEBOT3_MODEL=burger`가 설정되어 있어야 TurtleBot3 Burger를 실행할 수 있다.
* Gazebo는 `gzserver`와 `gzclient`가 분리되어 있다.
* GUI가 죽어도 시뮬레이션 서버와 ROS2 topic은 살아 있을 수 있다.
* `/cmd_vel`은 이동로봇 속도 명령의 기본 topic이다.
* `/odom`은 로봇 위치와 속도 추정 정보를 담는 topic이다.
* `/scan`은 LiDAR 거리 센서 데이터 topic이다.
* `rqt_graph`를 사용하면 node와 topic 연결 구조를 시각적으로 확인할 수 있다.

---

## 12. 다음 Phase로 연결

Phase 2에서 TurtleBot3 Gazebo 실행과 핵심 topic 확인을 완료했다.

다음 Phase에서는 RViz2와 TF2를 통해 다음 내용을 확인한다.

```text
RViz2에서 TurtleBot3 모델 확인
/tf, /tf_static 확인
odom → base_footprint → base_link → base_scan 좌표계 구조 확인
LaserScan 시각화
```

즉, Phase 3에서는 단순히 topic이 존재하는지 보는 것을 넘어서, 로봇의 센서와 좌표계가 RViz2에서 어떻게 표현되는지 확인한다.
