# Phase 2 Summary. Gazebo + TurtleBot3

## 1. Phase 개요

Phase 2의 목표는 turtlesim이 아니라 Gazebo 환경에서 TurtleBot3 Burger를 실행하고, 실제 이동로봇 시뮬레이션에서 사용되는 핵심 ROS2 topic 구조를 확인하는 것이었다.

이번 Phase에서는 SLAM, Navigation2, MoveIt2로 앞서가지 않고, 다음 세 topic을 중심으로 확인했다.

```text
/cmd_vel
/odom
/scan
```

---

## 2. 완료 상태

상태: 완료

완료한 것:

```text
[x] 기존 turtlesim 관련 노드 종료 확인
[x] ROS2 Humble 환경 확인
[x] TURTLEBOT3_MODEL=burger 확인
[x] turtlebot3_gazebo 패키지 인식 확인
[x] turtlebot3_teleop 패키지 인식 확인
[x] Gazebo TurtleBot3 empty_world 실행
[x] TurtleBot3 Burger spawn 확인
[x] gzclient crash 발생 후 GUI 재연결 확인
[x] /cmd_vel topic 확인
[x] /odom topic 확인
[x] /scan topic 확인
[x] teleop_keyboard로 TurtleBot3 이동 확인
[x] /cmd_vel Twist 메시지 확인
[x] /odom Odometry 메시지 확인
[x] TurtleBot3 이동 전후 /odom position 값 변화 확인
[x] /scan LaserScan 메시지 확인
[x] rqt_graph로 node-topic 연결 확인
```

---

## 3. 실행한 주요 명령어

### 3.1 환경 확인

```bash
ros2 node list
echo $ROS_DISTRO
echo $TURTLEBOT3_MODEL
which ros2
which gazebo
ros2 pkg list | grep turtlebot3_gazebo
ros2 pkg list | grep turtlebot3_teleop
cd ~/projects/missionbot-ros2
pwd
ls
```

확인 결과:

```text
ROS_DISTRO=humble
TURTLEBOT3_MODEL=burger
ros2=/opt/ros/humble/bin/ros2
gazebo=/usr/bin/gazebo
turtlebot3_gazebo 인식
turtlebot3_teleop 인식
```

---

### 3.2 Gazebo TurtleBot3 실행

```bash
ros2 launch turtlebot3_gazebo empty_world.launch.py
```

확인한 주요 로그:

```text
Spawn status: SpawnEntity: Successfully spawned entity [burger]
```

---

### 3.3 Gazebo GUI 재연결

최초 실행 중 `gzclient` crash가 발생했다.

오류 메시지:

```text
gzclient: Assertion `px != 0' failed.
[ERROR] [gzclient-2]: process has died
```

하지만 다음 topic이 살아 있는 것을 확인했다.

```bash
ros2 topic list | grep -E "cmd_vel|odom|scan"
```

확인 결과:

```text
/cmd_vel
/odom
/scan
```

GUI는 아래 명령어로 다시 연결했다.

```bash
gzclient --verbose
```

확인 로그:

```text
Connected to gazebo master @ http://127.0.0.1:11345
```

---

### 3.4 teleop 실행

```bash
ros2 run turtlebot3_teleop teleop_keyboard
```

확인한 조작:

```text
w: 앞으로 이동
x: 뒤로 이동
a: 왼쪽 회전
d: 오른쪽 회전
s: 정지
```

---

### 3.5 topic 확인

```bash
ros2 topic info /cmd_vel
ros2 topic echo /cmd_vel
ros2 topic info /odom
ros2 topic echo /odom --once
ros2 topic info /scan
ros2 topic echo /scan --once
```

---

### 3.6 rqt_graph 확인

```bash
rqt_graph
```

확인한 연결:

```text
/teleop_keyboard
→ /cmd_vel
→ Gazebo/TurtleBot3 관련 node
```

---

## 4. 핵심 개념 정리

## 4.1 gzserver와 gzclient

Gazebo는 크게 `gzserver`와 `gzclient`로 나뉜다.

```text
gzserver
→ 실제 시뮬레이션 서버
→ 물리 계산, 센서, 로봇 plugin, topic 발행 담당

gzclient
→ 사람이 보는 Gazebo GUI
→ 창, 카메라, 모델 시각화 담당
```

이번 Phase에서 `gzclient`가 죽어도 `gzserver`와 ROS2 topic은 살아 있을 수 있다는 것을 확인했다.

---

## 4.2 /cmd_vel

`/cmd_vel`은 로봇에게 속도 명령을 보내는 topic이다.

메시지 타입:

```text
geometry_msgs/msg/Twist
```

주요 필드:

```text
linear.x
→ 전진/후진 속도

angular.z
→ 회전 속도
```

Phase 2에서는 `teleop_keyboard`가 `/cmd_vel`을 publish하고, Gazebo TurtleBot3가 이를 subscribe하여 움직이는 구조를 확인했다.

---

## 4.3 /odom

`/odom`은 로봇의 위치, 자세, 속도 추정 정보를 담는 topic이다.

메시지 타입:

```text
nav_msgs/msg/Odometry
```

중요하게 본 항목:

```text
header.frame_id: odom
child_frame_id: base_footprint
pose.pose.position.x
pose.pose.position.y
```

TurtleBot3 이동 전후로 `position.x` 또는 `position.y` 값이 변하는 것을 확인했다.

---

## 4.4 /scan

`/scan`은 TurtleBot3의 LiDAR 거리 센서 데이터 topic이다.

메시지 타입:

```text
sensor_msgs/msg/LaserScan
```

중요하게 본 항목:

```text
angle_min
angle_max
angle_increment
range_min
range_max
ranges
```

`ranges`는 각 방향에 대한 거리 배열이다.

`inf`는 해당 방향에 측정 가능한 장애물이 없거나 너무 멀다는 의미로 볼 수 있다.

---

## 4.5 rqt_graph

`rqt_graph`는 현재 실행 중인 ROS2 node와 topic 연결 구조를 시각적으로 보여주는 도구다.

이번 Phase에서는 다음 연결을 확인했다.

```text
/teleop_keyboard
→ /cmd_vel
→ Gazebo/TurtleBot3 관련 node
```

---

## 5. Phase 1과 Phase 2의 연결

Phase 1에서 확인한 turtlesim 구조:

```text
/velocity_publisher
→ /turtle1/cmd_vel
→ /turtlesim
→ /turtle1/pose
→ /pose_subscriber
```

Phase 2에서 확인한 TurtleBot3 구조:

```text
/teleop_keyboard
→ /cmd_vel
→ TurtleBot3 diff drive
→ /odom

TurtleBot3 LiDAR
→ /scan
```

연결 의미:

```text
/turtle1/cmd_vel
→ /cmd_vel

/turtle1/pose
→ /odom

turtlesim_node
→ Gazebo TurtleBot3 plugin
```

즉, Phase 1에서 배운 publisher, subscriber, topic, launch 개념이 Phase 2에서 Gazebo TurtleBot3 구조로 확장되었다.

---

## 6. 발생한 이슈

## 6.1 gzclient crash

발생 상황:

```bash
ros2 launch turtlebot3_gazebo empty_world.launch.py
```

오류 메시지:

```text
gzclient: Assertion `px != 0' failed.
[ERROR] [gzclient-2]: process has died
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

해결:

```bash
gzclient --verbose
```

결과:

```text
Gazebo master에 다시 연결되었고, Gazebo GUI를 다시 확인할 수 있었다.
```

---

## 7. 완료 판정

Phase 2는 완료로 판단한다.

완료 이유:

```text
[x] Gazebo TurtleBot3 empty_world 실행 성공
[x] TurtleBot3 Burger spawn 확인
[x] /cmd_vel topic 확인
[x] teleop_keyboard로 TurtleBot3 이동 확인
[x] /cmd_vel Twist 메시지 확인
[x] /odom Odometry 메시지 확인
[x] TurtleBot3 이동 전후 /odom 값 변화 확인
[x] /scan LaserScan 메시지 확인
[x] rqt_graph로 node-topic 연결 확인
[x] gzclient crash 원인 분리 및 재연결 확인
```

---

## 8. 다음 Phase

다음 Phase는 다음과 같다.

```text
Phase 3. RViz2 + TF2
```

Phase 3의 목표:

```text
Gazebo에서 실행 중인 TurtleBot3를 RViz2에서 시각화하고, TF2를 통해 로봇 좌표계 구조를 확인한다.
```

Phase 3에서 확인할 내용:

```text
RViz2 실행
Fixed Frame 설정
RobotModel 표시
LaserScan 표시
/tf topic 확인
/tf_static topic 확인
odom → base_footprint → base_link → base_scan 좌표계 연결 확인
TF tree 확인
```

---

## 9. MissionBot에서의 의미

Phase 2는 MissionBot의 Mobile Robot Foundation에 해당한다.

이번 Phase를 통해 다음 흐름을 확인했다.

```text
속도 명령
→ /cmd_vel
→ Gazebo TurtleBot3 이동

로봇 위치 변화
→ /odom

LiDAR 센서 데이터
→ /scan
```

즉, 앞으로 SLAM, Navigation2, rosbag2, Failure Analysis로 넘어가기 전 필요한 이동로봇 topic 기반을 확인한 단계다.
