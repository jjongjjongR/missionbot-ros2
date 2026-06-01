# MissionBot-ROS2 Phase 3. RViz2 + TF2

## 1. Phase 목표

Phase 3의 목표는 Gazebo에서 실행 중인 TurtleBot3 Burger를 RViz2에서 시각화하고, TF2를 통해 로봇 좌표계 구조를 확인하는 것이다.

Phase 2에서는 Gazebo TurtleBot3 환경에서 `/cmd_vel`, `/odom`, `/scan`을 확인했다.

Phase 3에서는 여기에 RViz2와 TF2를 연결해 다음 내용을 확인했다.

```text
Gazebo TurtleBot3 실행
→ /cmd_vel, /odom, /scan, /tf, /tf_static 확인
→ RViz2 실행
→ Fixed Frame 설정
→ TF 표시
→ RobotModel 표시
→ LaserScan 표시
→ TF tree 확인
→ tf2_echo로 특정 transform 직접 조회
→ teleop 이동 중 odom → base_footprint transform 변화 확인
```

---

## 2. Phase 3 완료 상태

```text
[x] RViz2 실행 전 환경 확인
[x] ROS2 Humble 확인
[x] TURTLEBOT3_MODEL=burger 확인
[x] rviz2 실행 경로 확인
[x] turtlebot3_gazebo 패키지 확인
[x] turtlebot3_teleop 패키지 확인
[x] Gazebo TurtleBot3 empty_world 실행
[x] TurtleBot3 Burger spawn 확인
[x] gzclient crash 발생 확인
[x] gzserver와 ROS2 topic은 살아 있는 것 확인
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
[x] view_frames로 TF tree 생성
[x] frames.pdf 확인
[x] tf2_echo로 odom → base_footprint 확인
[x] tf2_echo로 base_link → base_scan 확인
[x] teleop 이동 중 odom → base_footprint transform 변화 확인
```

---

## 3. Phase 3에서 사용한 환경

```text
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

Remote GUI:
NoMachine

Development Client:
MacBook

Project path:
~/projects/missionbot-ros2

TurtleBot3 workspace:
~/turtlebot3_ws
```

---

## 4. Phase 3 시작 전 환경 확인

실행 명령:

```bash
ros2 node list
echo $ROS_DISTRO
echo $TURTLEBOT3_MODEL
which ros2
which gazebo
which rviz2
ros2 pkg list | grep turtlebot3_gazebo
ros2 pkg list | grep turtlebot3_teleop
cd ~/projects/missionbot-ros2
pwd
ls
```

확인 결과:

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

ros2 pkg list | grep turtlebot3_gazebo
→ turtlebot3_gazebo

ros2 pkg list | grep turtlebot3_teleop
→ turtlebot3_teleop

pwd
→ /home/user/projects/missionbot-ros2
```

프로젝트 루트에서 확인된 주요 폴더:

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

---

## 5. Gazebo TurtleBot3 실행

실행 명령:

```bash
ros2 launch turtlebot3_gazebo empty_world.launch.py
```

확인한 주요 로그:

```text
Spawn status: SpawnEntity: Successfully spawned entity [burger]
[turtlebot3_diff_drive]: Subscribed to [/cmd_vel]
[turtlebot3_diff_drive]: Advertise odometry on [/odom]
[turtlebot3_diff_drive]: Publishing odom transforms between [odom] and [base_footprint]
```

의미:

```text
TurtleBot3 Burger가 Gazebo 서버에 정상 spawn되었다.
Gazebo diff drive plugin이 /cmd_vel을 구독한다.
Gazebo diff drive plugin이 /odom을 발행한다.
odom → base_footprint transform도 발행한다.
```

---

## 6. gzclient crash 이슈

Phase 3에서도 Phase 2와 동일하게 gzclient crash가 발생했다.

오류 메시지:

```text
libcurl: (6) Could not resolve host: fuel.ignitionrobotics.org
gzclient: /usr/include/boost/smart_ptr/shared_ptr.hpp:728:
Assertion `px != 0' failed.
[ERROR] [gzclient-2]: process has died
cmd 'gzclient --gui-client-plugin=libgazebo_ros_eol_gui.so'
```

판단:

```text
이 문제는 TurtleBot3 spawn 실패가 아니다.
죽은 것은 Gazebo GUI 클라이언트인 gzclient다.
gzserver는 살아 있고, ROS2 topic도 정상적으로 생성되었다.
```

확인한 topic:

```bash
ros2 topic list | grep -E "cmd_vel|odom|scan|tf"
```

결과:

```text
/cmd_vel
/odom
/scan
/tf
/tf_static
```

따라서 Phase 3는 Gazebo GUI가 아니라 RViz2 중심으로 진행했다.

---

## 7. 주요 topic 확인

실행 명령:

```bash
ros2 topic list | grep -E "cmd_vel|odom|scan|tf"
```

확인 결과:

```text
/cmd_vel
/odom
/scan
/tf
/tf_static
```

의미:

```text
/cmd_vel
→ 로봇 속도 명령 topic

/odom
→ 로봇 위치, 자세, 속도 추정 topic

/scan
→ TurtleBot3 LiDAR LaserScan topic

/tf
→ 계속 변하는 좌표계 관계 topic

/tf_static
→ 고정된 좌표계 관계 topic
```

---

## 8. /tf, /tf_static 확인

실행 명령:

```bash
ros2 topic info /tf
ros2 topic info /tf_static
```

확인 결과:

```text
/tf
Type: tf2_msgs/msg/TFMessage
Publisher count: 2
Subscription count: 0

/tf_static
Type: tf2_msgs/msg/TFMessage
Publisher count: 1
Subscription count: 0
```

해석:

```text
/tf
→ 동적으로 변하는 좌표계 관계를 발행한다.
→ 예: odom → base_footprint

/tf_static
→ 정적으로 고정된 좌표계 관계를 발행한다.
→ 예: base_link → base_scan
```

`Subscription count: 0`은 RViz2를 켜기 전이라 구독자가 없다는 뜻이다.  
RViz2에서 TF display를 추가하면 RViz2가 `/tf`, `/tf_static`을 구독할 수 있다.

---

## 9. RViz2 실행

실행 명령:

```bash
rviz2
```

RViz2에서 설정한 것:

```text
Global Options
→ Fixed Frame: odom
```

`Fixed Frame`을 `odom`으로 설정한 이유:

```text
현재 Phase에서는 SLAM을 하지 않았기 때문에 map frame이 없다.
Gazebo TurtleBot3는 odom 기준으로 로봇 위치와 TF를 발행한다.
따라서 RViz2의 기준 좌표계는 odom으로 설정하는 것이 적절하다.
```

---

## 10. TF display 추가

RViz2 설정:

```text
Add
→ By display type
→ TF
→ OK
```

확인한 것:

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

의미:

```text
TurtleBot3의 이동 기준 좌표계, 본체 좌표계, 센서 좌표계, 바퀴 좌표계가 RViz2에서 확인되었다.
```

---

## 11. RobotModel display 추가

RViz2 설정:

```text
Add
→ By display type
→ RobotModel
→ OK
```

설정값:

```text
Description Source: Topic
Description Topic: /robot_description
```

확인한 것:

```text
TurtleBot3 Burger 본체 모델이 RViz2에 표시되었다.
TF 좌표계 위에 로봇 모델이 정상적으로 연결되었다.
```

의미:

```text
TF는 로봇의 좌표계 뼈대이고, RobotModel은 그 좌표계 구조에 로봇 외형을 입히는 역할을 한다.
```

---

## 12. LaserScan display 추가

RViz2 설정:

```text
Add
→ By display type
→ LaserScan
→ OK

Topic: /scan
Style: Points
```

확인한 것:

```text
LaserScan display 추가 성공
Topic /scan 설정 성공
에러 없음
```

다만 empty_world에서는 주변 장애물이나 벽이 거의 없기 때문에 RViz2에서 LiDAR 점이 잘 보이지 않았다.

확인 명령:

```bash
ros2 topic echo /scan --once --field ranges | head -n 20
```

확인 결과:

```text
inf 위주로 출력됨
```

해석:

```text
/scan이 죽은 것이 아니다.
empty_world에서 LiDAR가 감지할 물체가 거의 없기 때문에 ranges 값이 inf 위주로 나온 것이다.
따라서 RViz2에 찍힐 실제 점도 거의 없을 수 있다.
```

---

## 13. TF tree 확인

실행 명령:

```bash
ros2 run tf2_tools view_frames
```

생성 파일:

```text
frames.pdf
```

확인한 구조:

```text
odom
→ base_footprint
→ base_link
→ base_scan
```

추가로 확인한 링크:

```text
base_link
→ imu_link

base_link
→ wheel_left_link

base_link
→ wheel_right_link

base_link
→ caster_back_link
```

의미:

```text
TurtleBot3의 이동 기준 좌표계, 본체 좌표계, LiDAR 좌표계, 바퀴 좌표계가 하나의 TF tree로 연결되어 있음을 확인했다.
```

---

## 14. 특정 transform 직접 조회

실행 명령 1:

```bash
ros2 run tf2_ros tf2_echo odom base_footprint
```

확인한 것:

```text
odom 기준 base_footprint의 Translation과 Rotation 출력
```

의미:

```text
로봇이 odom 기준에서 어디에 있는지 확인하는 transform이다.
로봇이 움직이면 이 값은 변한다.
```

실행 명령 2:

```bash
ros2 run tf2_ros tf2_echo base_link base_scan
```

확인한 것:

```text
base_link 기준 base_scan의 Translation과 Rotation 출력
```

의미:

```text
LiDAR가 로봇 본체 기준 어디에 붙어 있는지 확인하는 transform이다.
LiDAR는 로봇 본체에 고정되어 있으므로 이 값은 거의 고정된다.
```

---

## 15. teleop 이동 중 TF 변화 확인

터미널 구성:

```text
터미널 1
→ ros2 launch turtlebot3_gazebo empty_world.launch.py

터미널 2
→ rviz2

터미널 3
→ ros2 run tf2_ros tf2_echo odom base_footprint

터미널 4
→ ros2 run turtlebot3_teleop teleop_keyboard
```

teleop 실행 명령:

```bash
ros2 run turtlebot3_teleop teleop_keyboard
```

조작:

```text
w: 전진
x: 후진
a: 왼쪽 회전
d: 오른쪽 회전
s: 정지
```

확인한 것:

```text
teleop 입력으로 TurtleBot3 이동 명령을 발행했다.
odom → base_footprint transform의 Translation 또는 Rotation 값이 변했다.
RViz2에서도 로봇 모델과 TF 좌표계 움직임을 확인했다.
```

의미:

```text
teleop_keyboard
→ /cmd_vel
→ turtlebot3_diff_drive
→ /odom
→ /tf
→ RViz2 시각화

위 흐름이 정상적으로 연결되어 있음을 확인했다.
```

---

## 16. Phase 2와 Phase 3의 연결

Phase 2에서 확인한 것:

```text
/cmd_vel
→ 로봇 이동 명령

/odom
→ 로봇 위치 추정

/scan
→ LiDAR 거리 센서
```

Phase 3에서 확인한 것:

```text
/tf
→ 움직이는 좌표계 관계

/tf_static
→ 고정 좌표계 관계

RViz2
→ /odom, /scan, /tf, /robot_description을 시각화
```

연결 의미:

```text
Phase 2에서는 데이터가 topic으로 흐르는지 확인했다.
Phase 3에서는 그 topic 데이터가 어떤 좌표계 기준으로 해석되고, RViz2에서 어떻게 보이는지 확인했다.
```

---

## 17. Phase 3 핵심 개념 정리

### 17.1 RViz2

```text
RViz2는 시뮬레이터가 아니라 ROS2 데이터 시각화 도구다.
Gazebo가 가상 세계를 실행한다면, RViz2는 ROS2 topic과 TF 데이터를 시각적으로 보여준다.
```

### 17.2 Fixed Frame

```text
RViz2가 모든 데이터를 그릴 기준 좌표계다.
이번 Phase에서는 odom을 Fixed Frame으로 사용했다.
```

### 17.3 TF2

```text
TF2는 ROS2에서 좌표계 사이의 관계를 관리하는 시스템이다.
로봇 본체, 바퀴, LiDAR, IMU 같은 부품들은 각각 좌표계를 갖고, TF2는 이 관계를 연결한다.
```

### 17.4 /tf

```text
계속 변하는 좌표계 관계를 담는 topic이다.
예: odom → base_footprint
```

### 17.5 /tf_static

```text
고정된 좌표계 관계를 담는 topic이다.
예: base_link → base_scan
```

### 17.6 RobotModel

```text
RViz2에서 로봇의 URDF 기반 외형을 표시하는 Display다.
TF 좌표계 구조 위에 로봇 모델을 연결해 보여준다.
```

### 17.7 LaserScan

```text
2D LiDAR 거리 센서 데이터다.
TurtleBot3에서는 /scan topic으로 발행된다.
empty_world에서는 감지할 물체가 거의 없어 ranges가 inf 위주로 나올 수 있다.
```

---

## 18. Phase 3에서 사용한 주요 명령어

```bash
# 환경 확인
ros2 node list
echo $ROS_DISTRO
echo $TURTLEBOT3_MODEL
which ros2
which gazebo
which rviz2
ros2 pkg list | grep turtlebot3_gazebo
ros2 pkg list | grep turtlebot3_teleop

# Gazebo TurtleBot3 실행
ros2 launch turtlebot3_gazebo empty_world.launch.py

# 주요 topic 확인
ros2 topic list | grep -E "cmd_vel|odom|scan|tf"

# TF topic 확인
ros2 topic info /tf
ros2 topic info /tf_static

# RViz2 실행
rviz2

# LaserScan 값 확인
ros2 topic echo /scan --once --field ranges | head -n 20

# TF tree 생성
ros2 run tf2_tools view_frames

# 특정 transform 확인
ros2 run tf2_ros tf2_echo odom base_footprint
ros2 run tf2_ros tf2_echo base_link base_scan

# teleop 실행
ros2 run turtlebot3_teleop teleop_keyboard
```

---

## 19. Phase 3 완료 판정

Phase 3는 다음 기준을 만족했으므로 완료로 판단한다.

```text
[x] RViz2 실행 성공
[x] Fixed Frame을 odom으로 설정
[x] TF display 추가 및 좌표계 확인
[x] RobotModel display 추가 및 TurtleBot3 모델 확인
[x] LaserScan display 추가 및 /scan 연결 확인
[x] /scan ranges가 empty_world에서 inf 위주로 나오는 이유 이해
[x] view_frames로 TF tree 확인
[x] tf2_echo로 특정 transform 직접 조회
[x] teleop 이동 중 odom → base_footprint transform 변화 확인
[x] gzclient crash를 Gazebo GUI 문제로 분리하고 RViz2 중심으로 진행
```

완료 의미:

```text
Phase 3에서는 TurtleBot3의 센서 데이터와 로봇 모델이 어떤 좌표계 기준으로 해석되는지 RViz2와 TF2를 통해 확인했다.

이제 다음 Phase인 SLAM에서 /scan과 TF가 왜 중요한지 이해할 준비가 되었다.
```

---

## 20. 다음 Phase 연결

다음 Phase:

```text
Phase 4. SLAM
```

Phase 4에서 연결될 개념:

```text
/scan
→ 지도 생성을 위한 LiDAR 입력

/tf
→ 로봇 위치와 센서 좌표계 연결

odom
→ 로봇 이동 추정 기준

map
→ SLAM을 통해 새로 생성될 지도 기준 좌표계
```

Phase 4에서는 SLAM Toolbox를 사용해 TurtleBot3가 이동하면서 `/scan`과 TF를 기반으로 지도를 생성하는 흐름을 확인한다.