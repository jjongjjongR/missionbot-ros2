# Phase 3 Summary - RViz2 + TF2

## 1. Phase 정보

```text
Phase: Phase 3. RViz2 + TF2
Status: 완료
Date: 2026-06-02
```

---

## 2. Phase 목표

Gazebo에서 실행 중인 TurtleBot3 Burger를 RViz2에서 시각화하고, TF2를 통해 로봇 좌표계 구조를 확인한다.

핵심 목표는 다음과 같다.

```text
1. RViz2 실행
2. Fixed Frame 설정
3. TF display 확인
4. RobotModel display 확인
5. LaserScan display 확인
6. TF tree 확인
7. tf2_echo로 특정 transform 직접 조회
8. teleop 이동 중 TF 변화 확인
```

---

## 3. 완료한 것

```text
[x] RViz2 실행 전 환경 확인
[x] ROS2 Humble 확인
[x] TURTLEBOT3_MODEL=burger 확인
[x] rviz2 실행 파일 확인
[x] turtlebot3_gazebo 패키지 확인
[x] turtlebot3_teleop 패키지 확인
[x] Gazebo TurtleBot3 empty_world 실행
[x] TurtleBot3 Burger spawn 성공
[x] /cmd_vel 확인
[x] /odom 확인
[x] /scan 확인
[x] /tf 확인
[x] /tf_static 확인
[x] RViz2 실행
[x] Fixed Frame을 odom으로 설정
[x] TF display 추가
[x] RobotModel display 추가
[x] LaserScan display 추가
[x] /scan ranges가 empty_world에서 inf 위주로 나오는 것 확인
[x] view_frames로 frames.pdf 생성
[x] TF tree 구조 확인
[x] tf2_echo로 odom → base_footprint 확인
[x] tf2_echo로 base_link → base_scan 확인
[x] teleop 이동 중 odom → base_footprint transform 변화 확인
```

---

## 4. 확인한 주요 topic

```text
/cmd_vel
/odom
/scan
/tf
/tf_static
/robot_description
```

---

## 5. 확인한 주요 frame

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

---

## 6. 사용한 주요 명령어

```bash
ros2 node list
echo $ROS_DISTRO
echo $TURTLEBOT3_MODEL
which ros2
which gazebo
which rviz2
ros2 pkg list | grep turtlebot3_gazebo
ros2 pkg list | grep turtlebot3_teleop

ros2 launch turtlebot3_gazebo empty_world.launch.py

ros2 topic list | grep -E "cmd_vel|odom|scan|tf"
ros2 topic info /tf
ros2 topic info /tf_static

rviz2

ros2 topic echo /scan --once --field ranges | head -n 20

ros2 run tf2_tools view_frames

ros2 run tf2_ros tf2_echo odom base_footprint
ros2 run tf2_ros tf2_echo base_link base_scan

ros2 run turtlebot3_teleop teleop_keyboard
```

---

## 7. RViz2에서 설정한 것

```text
Global Options
→ Fixed Frame: odom

Add
→ TF

Add
→ RobotModel
→ Description Source: Topic
→ Description Topic: /robot_description

Add
→ LaserScan
→ Topic: /scan
→ Style: Points
```

---

## 8. 핵심 개념 요약

## 8.1 RViz2

```text
RViz2는 ROS2 데이터를 시각화하는 도구다.
Gazebo가 시뮬레이션을 실행한다면, RViz2는 topic, TF, 로봇 모델, 센서 데이터를 보여준다.
```

## 8.2 Fixed Frame

```text
RViz2가 모든 데이터를 그릴 기준 좌표계다.
Phase 3에서는 odom을 Fixed Frame으로 사용했다.
```

## 8.3 TF2

```text
TF2는 좌표계 사이의 관계를 관리하는 시스템이다.
로봇 본체, 센서, 바퀴, IMU 등이 각각 어떤 위치 관계를 갖는지 표현한다.
```

## 8.4 /tf

```text
계속 변하는 좌표계 관계를 담는 topic이다.
예: odom → base_footprint
```

## 8.5 /tf_static

```text
고정된 좌표계 관계를 담는 topic이다.
예: base_link → base_scan
```

## 8.6 RobotModel

```text
RViz2에서 로봇의 URDF 기반 외형을 표시하는 기능이다.
```

## 8.7 LaserScan

```text
2D LiDAR 거리 센서 데이터다.
TurtleBot3에서는 /scan topic으로 발행된다.
empty_world에서는 감지할 물체가 거의 없어 ranges 값이 inf 위주로 나올 수 있다.
```

---

## 9. 발생한 이슈

## 9.1 gzclient crash

오류:

```text
gzclient: /usr/include/boost/smart_ptr/shared_ptr.hpp:728:
Assertion `px != 0' failed.
[ERROR] [gzclient-2]: process has died
```

판단:

```text
TurtleBot3 spawn 실패가 아니다.
gzserver와 ROS2 topic은 살아 있다.
죽은 것은 Gazebo GUI 클라이언트인 gzclient다.
```

대응:

```text
Gazebo GUI에 의존하지 않고 RViz2 중심으로 진행했다.
필요하면 gzclient --verbose 또는 소프트웨어 렌더링 옵션을 검토한다.
```

---

## 9.2 LaserScan 점이 RViz2에서 잘 보이지 않음

상황:

```text
LaserScan display 추가 성공
Topic: /scan 설정 성공
에러 없음
하지만 RViz2 화면에서 LiDAR 점이 잘 보이지 않음
```

확인:

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
empty_world에서 감지할 벽이나 장애물이 거의 없기 때문에 inf가 많이 나온다.
따라서 RViz2에서 표시될 점도 거의 없을 수 있다.
```

---

## 10. Phase 3 완료 의미

Phase 3를 통해 다음 흐름을 확인했다.

```text
Gazebo TurtleBot3
→ /cmd_vel
→ /odom
→ /scan
→ /tf, /tf_static
→ RViz2 시각화
```

또한 teleop 이동 중 transform 변화까지 확인했다.

```text
teleop_keyboard
→ /cmd_vel
→ turtlebot3_diff_drive
→ /odom
→ /tf
→ RViz2 RobotModel 이동
```

---

## 11. 다음 Phase로 넘길 내용

다음 Phase는 Phase 4. SLAM이다.

Phase 4에서 이어질 핵심 개념:

```text
/scan
→ 지도 생성을 위한 LiDAR 입력

/tf
→ 로봇 위치와 센서 좌표계 연결

odom
→ 로봇 이동 추정 기준

map
→ SLAM을 통해 새로 생성될 지도 좌표계
```

주의:

```text
Phase 4에서는 map frame이 새롭게 등장할 수 있다.
Phase 3에서는 Fixed Frame을 odom으로 사용했지만, SLAM 단계에서는 map frame과 odom frame의 관계가 중요해진다.
```