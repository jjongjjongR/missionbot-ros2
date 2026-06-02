# Phase 4. SLAM

## 1. Phase 개요

Phase 4에서는 TurtleBot3 Gazebo World 환경에서 SLAM Toolbox를 실행하고, LiDAR `/scan` 데이터와 TF 정보를 기반으로 지도를 생성했다.

이전 Phase 3에서는 RViz2와 TF2를 사용해 TurtleBot3의 센서 데이터와 좌표계 구조를 확인했다. Phase 4에서는 그 흐름을 확장하여, SLAM Toolbox가 `/scan`, `/odom`, `/tf`, `/tf_static` 정보를 사용해 `/map` topic을 생성하는 과정을 실습했다.

이번 Phase의 최종 목표는 다음과 같다.

```text
Gazebo TurtleBot3 World 실행
→ SLAM Toolbox 실행
→ /map topic 생성 확인
→ RViz2에서 지도 시각화
→ teleop으로 지도 확장
→ map_saver_cli로 지도 저장
→ .pgm / .yaml 지도 파일 확인
```

---

## 2. Phase 3와 Phase 4의 연결

Phase 3에서는 다음을 확인했다.

```text
/scan
→ TurtleBot3 LiDAR 거리 센서 데이터

/odom
→ TurtleBot3의 위치, 자세, 속도 추정 정보

/tf
→ 계속 변하는 좌표계 관계

/tf_static
→ 고정된 좌표계 관계

RViz2
→ RobotModel, LaserScan, TF 시각화
```

Phase 3의 핵심 TF 구조는 다음과 같았다.

```text
odom
→ base_footprint
→ base_link
→ base_scan
```

Phase 4에서는 여기에 SLAM 결과인 `map` frame이 추가된다.

```text
map
→ odom
→ base_footprint
→ base_link
→ base_scan
```

즉, Phase 3에서는 로봇과 센서의 좌표계가 정상적으로 연결되어 있는지 확인했고, Phase 4에서는 그 좌표계와 센서 데이터를 SLAM Toolbox에 연결해 실제 지도를 생성했다.

---

## 3. 이번 Phase의 목표

이번 Phase의 목표는 다음과 같다.

```text
TurtleBot3가 Gazebo World 안에서 이동하면서
LiDAR와 TF 정보를 기반으로 SLAM 지도를 생성하고,
그 결과를 RViz2에서 확인한 뒤 파일로 저장한다.
```

세부 목표는 다음과 같다.

```text
[x] SLAM Toolbox 패키지 인식 확인
[x] TurtleBot3 Gazebo World 실행
[x] /scan, /odom, /tf, /tf_static topic 확인
[x] SLAM Toolbox 실행
[x] /map topic 생성 확인
[x] RViz2에서 SLAM 지도 시각화
[x] teleop으로 TurtleBot3를 움직이며 지도 확장 확인
[x] 생성된 지도 저장
[x] .pgm, .yaml 지도 파일 확인
```

---

## 4. 핵심 개념 정리

## 4.1 SLAM

SLAM은 Simultaneous Localization and Mapping의 약자다.

쉽게 말하면 다음과 같다.

```text
로봇이 움직이면서
자기 위치를 추정하고
동시에 주변 지도를 만드는 과정
```

SLAM은 단순히 지도를 그리는 기능만 의미하지 않는다. 로봇이 “내가 지도 안에서 어디에 있는지”를 추정하면서, 동시에 “내 주변 공간이 어떻게 생겼는지”를 갱신한다.

이번 Phase에서는 SLAM Toolbox를 사용했다.

SLAM Toolbox는 TurtleBot3의 `/scan` 데이터와 TF 정보를 사용해서 `/map` topic을 생성한다.

---

## 4.2 `/scan`

`/scan`은 TurtleBot3의 2D LiDAR 거리 센서 데이터다.

메시지 타입은 다음과 같다.

```text
sensor_msgs/msg/LaserScan
```

`/scan` 안에는 여러 방향의 거리값이 배열 형태로 들어 있다.

중요한 필드는 다음과 같다.

```text
angle_min
→ LiDAR 측정 시작 각도

angle_max
→ LiDAR 측정 끝 각도

angle_increment
→ 각 측정 사이의 각도 간격

range_min
→ 측정 가능한 최소 거리

range_max
→ 측정 가능한 최대 거리

ranges
→ 각 방향별 거리값 배열
```

SLAM에서는 이 `/scan` 데이터가 지도 생성의 주요 입력으로 사용된다.

---

## 4.3 `/odom`

`/odom`은 TurtleBot3의 위치, 자세, 속도 추정 정보를 담는 topic이다.

메시지 타입은 다음과 같다.

```text
nav_msgs/msg/Odometry
```

중요하게 볼 필드는 다음과 같다.

```text
header.frame_id: odom
child_frame_id: base_footprint
pose.pose.position.x
pose.pose.position.y
pose.pose.orientation
twist.twist.linear
twist.twist.angular
```

`/odom`은 로봇이 얼마나 움직였는지 추정하는 기준이다.

다만 odom은 시간이 지나면 오차가 누적될 수 있다. 그래서 SLAM은 `/scan`과 TF를 함께 사용해 지도 기준의 위치를 보정한다.

---

## 4.4 `/tf`와 `/tf_static`

TF는 좌표계 사이의 관계를 표현하는 ROS2 시스템이다.

`/tf`는 계속 변하는 좌표계 관계를 담는다.

예시:

```text
odom → base_footprint
```

로봇이 움직이면 `odom` 기준에서 `base_footprint`의 위치가 계속 변하므로 `/tf`로 발행된다.

`/tf_static`은 고정된 좌표계 관계를 담는다.

예시:

```text
base_link → base_scan
```

LiDAR는 로봇 본체에 고정되어 있으므로 `base_link` 기준 `base_scan`의 위치는 거의 변하지 않는다. 이런 관계는 `/tf_static`으로 발행된다.

SLAM은 LiDAR 데이터만 보고 지도를 만들지 않는다. `/scan`이 어느 위치와 방향에서 측정된 데이터인지 알아야 하므로 TF 정보가 반드시 필요하다.

---

## 4.5 `map` frame

SLAM이 실행되기 전에는 RViz2의 Fixed Frame을 `odom`으로 사용했다.

하지만 SLAM이 실행되면 새로운 기준 좌표계인 `map` frame이 생긴다.

SLAM 이후 TF 구조는 다음과 같다.

```text
map
→ odom
→ base_footprint
→ base_link
→ base_scan
```

`map` frame은 SLAM이 만든 지도 기준 좌표계다.

Phase 4에서 RViz2의 Fixed Frame을 `map`으로 바꾼 이유는, 이제 지도 기준으로 로봇과 센서 데이터를 보고 싶기 때문이다.

---

## 4.6 `/map`

`/map`은 SLAM 결과로 생성되는 지도 topic이다.

메시지 타입은 다음과 같다.

```text
nav_msgs/msg/OccupancyGrid
```

OccupancyGrid는 공간을 작은 격자 칸으로 나누고, 각 칸이 어떤 상태인지 표현한다.

대표적인 상태는 다음과 같다.

```text
occupied
→ 벽 또는 장애물

free
→ 이동 가능한 빈 공간

unknown
→ 아직 관측하지 못한 공간
```

RViz2에서 Map display를 추가하고 Topic을 `/map`으로 설정하면 SLAM 결과 지도를 시각적으로 볼 수 있다.

---

## 4.7 `use_sim_time`

Gazebo는 실제 컴퓨터 시간이 아니라 시뮬레이션 시간을 사용한다.

Gazebo의 시뮬레이션 시간은 `/clock` topic으로 발행된다.

SLAM Toolbox가 Gazebo에서 발행되는 `/scan`, `/tf`, `/odom` 데이터를 올바르게 해석하려면 같은 시간 기준을 사용해야 한다.

그래서 SLAM Toolbox 실행 시 다음 옵션을 사용했다.

```bash
use_sim_time:=True
```

이 설정은 SLAM Toolbox가 Gazebo의 `/clock` 시간을 사용하도록 만든다.

이 옵션을 사용하지 않으면 TF 시간 관련 문제가 발생할 수 있다.

예시:

```text
SLAM Toolbox가 생각하는 시간 기준
≠
Gazebo와 TF가 발행하는 시간 기준

→ transform 조회 실패
→ laser pose 계산 실패
→ 지도 생성 문제 발생 가능
```

---

## 4.8 `.pgm`과 `.yaml` 지도 파일

SLAM으로 만든 지도는 보통 두 파일로 저장된다.

```text
.pgm
→ 실제 지도 이미지 파일

.yaml
→ 지도 이미지 해석을 위한 설정 파일
```

이번 Phase에서 생성한 파일은 다음과 같다.

```text
maps/phase04_slam/tb3_world_slam_map_01.pgm
maps/phase04_slam/tb3_world_slam_map_01.yaml
```

`.pgm`은 지도 이미지다.

보통 색상 의미는 다음과 같다.

```text
검은색
→ 벽 또는 장애물

흰색
→ 이동 가능한 자유 공간

회색
→ 아직 모르는 공간
```

`.yaml`은 지도 설정 파일이다.

이번에 저장된 `.yaml` 파일은 다음과 같다.

```yaml
image: tb3_world_slam_map_01.pgm
mode: trinary
resolution: 0.05
origin: [-2.94, -2.57, 0]
negate: 0
occupied_thresh: 0.65
free_thresh: 0.25
```

각 항목의 의미는 다음과 같다.

```text
image
→ 이 yaml 파일이 참조하는 지도 이미지 파일

mode
→ 지도 해석 방식

resolution
→ 지도 1픽셀이 실제 몇 m인지 의미
→ 0.05는 1픽셀 = 0.05m = 5cm

origin
→ 지도 이미지의 원점 위치

negate
→ 색상 해석 반전 여부

occupied_thresh
→ 장애물로 판단할 점유 확률 기준

free_thresh
→ 자유 공간으로 판단할 기준
```

---

## 5. 전체 실행 구조

이번 Phase의 전체 실행 구조는 다음과 같다.

```text
터미널 1
→ Gazebo TurtleBot3 World 실행

터미널 2
→ SLAM Toolbox 실행

터미널 3
→ RViz2 실행

터미널 4
→ teleop_keyboard 실행

터미널 5
→ map 저장 및 확인 명령 실행
```

전체 데이터 흐름은 다음과 같다.

```text
Gazebo TurtleBot3 World
→ /scan
→ /tf, /tf_static
→ /odom
→ SLAM Toolbox
→ /map
→ RViz2 Map display
→ map_saver_cli
→ .pgm / .yaml 저장
```

---

## 6. 실습 순서

## 6.1 실행 전 환경 확인

먼저 현재 ROS2, TurtleBot3, Gazebo, RViz2, SLAM Toolbox 환경을 확인했다.

```bash
ros2 node list
echo $ROS_DISTRO
echo $TURTLEBOT3_MODEL
which ros2
which gazebo
which rviz2
ros2 pkg list | grep slam_toolbox
ros2 pkg list | grep turtlebot3_gazebo
ros2 pkg list | grep turtlebot3_teleop
cd ~/projects/missionbot-ros2
pwd
ls
```

정상 확인 결과는 다음과 같았다.

```text
ROS2 distribution: humble
TurtleBot3 model: burger
ros2 path: /opt/ros/humble/bin/ros2
gazebo path: /usr/bin/gazebo
rviz2 path: /opt/ros/humble/bin/rviz2
SLAM Toolbox: slam_toolbox
TurtleBot3 Gazebo: turtlebot3_gazebo
TurtleBot3 Teleop: turtlebot3_teleop
Project path: /home/user/projects/missionbot-ros2
```

---

## 6.2 TurtleBot3 World 실행

SLAM에서는 빈 공간보다 벽과 구조물이 있는 환경이 필요하다.

따라서 `empty_world`가 아니라 `turtlebot3_world`를 실행했다.

```bash
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

이후 topic을 확인했다.

```bash
ros2 topic list | grep -E "cmd_vel|odom|scan|tf"
```

정상 기대값은 다음과 같다.

```text
/cmd_vel
/odom
/scan
/tf
/tf_static
```

---

## 6.3 `/scan` 값 확인

SLAM에서는 LiDAR가 실제 벽이나 장애물을 감지해야 한다.

아래 명령어로 `/scan` 값을 확인했다.

```bash
ros2 topic echo /scan --once --field ranges | head -n 20
```

`empty_world`에서는 `inf` 위주로 나올 수 있지만, `turtlebot3_world`에서는 벽과 구조물이 있기 때문에 숫자 거리값이 섞여 나올 수 있다.

숫자 값이 보인다는 것은 LiDAR가 주변 구조물을 감지하고 있다는 뜻이다.

---

## 6.4 SLAM Toolbox 실행

TurtleBot3 World가 실행된 상태에서 SLAM Toolbox를 실행했다.

```bash
ros2 launch slam_toolbox online_async_launch.py use_sim_time:=True
```

여기서 `online_async_launch.py`는 로봇이 움직이는 동안 실시간으로 지도를 생성하는 launch 파일이다.

`use_sim_time:=True`는 Gazebo의 시뮬레이션 시간을 사용하기 위한 설정이다.

---

## 6.5 SLAM Toolbox 실행 확인

SLAM Toolbox 실행 후 node를 확인했다.

```bash
ros2 node list
```

확인된 주요 node는 다음과 같다.

```text
/gazebo
/robot_state_publisher
/slam_toolbox
/transform_listener_impl_62b98f4d38e0
/turtlebot3_diff_drive
/turtlebot3_imu
/turtlebot3_joint_state
/turtlebot3_laserscan
```

topic도 확인했다.

```bash
ros2 topic list | grep -E "map|scan|tf|odom"
```

확인된 topic은 다음과 같다.

```text
/map
/map_metadata
/odom
/scan
/slam_toolbox/scan_visualization
/tf
/tf_static
```

`/map` topic 타입도 확인했다.

```bash
ros2 topic info /map
```

확인 결과는 다음과 같았다.

```text
Type: nav_msgs/msg/OccupancyGrid
Publisher count: 1
Subscription count: 1
```

이를 통해 SLAM Toolbox가 `/map`을 정상적으로 생성하고 있음을 확인했다.

---

## 6.6 RViz2에서 SLAM 지도 시각화

RViz2를 실행했다.

```bash
rviz2
```

RViz2에서 Fixed Frame을 `map`으로 설정했다.

```text
Global Options
→ Fixed Frame: map
```

이후 필요한 Display를 추가했다.

```text
Map
→ Topic: /map

TF
→ map, odom, base_footprint, base_link, base_scan 확인

RobotModel
→ Description Source: Topic
→ Description Topic: /robot_description

LaserScan
→ Topic: /scan
→ Style: Points
```

확인한 것은 다음과 같다.

```text
[x] Fixed Frame = map
[x] Map display Topic = /map
[x] TF 표시
[x] RobotModel 표시
[x] LaserScan 표시
[x] SLAM 지도 영역 표시
```

---

## 6.7 teleop으로 지도 확장

SLAM 지도는 한 번에 완성되지 않는다.

로봇이 이동하면서 새로운 벽과 구조물을 관측해야 지도 영역이 넓어진다.

teleop_keyboard를 실행했다.

```bash
ros2 run turtlebot3_teleop teleop_keyboard
```

조작 키는 다음과 같다.

```text
w: 전진
x: 후진
a: 왼쪽 회전
d: 오른쪽 회전
s: 정지
```

지도 확장 시에는 빠르게 움직이지 않고 천천히 이동했다.

주의한 점은 다음과 같다.

```text
전진은 짧게
회전은 천천히
급회전 금지
벽과 구조물을 충분히 관측
중간중간 멈추며 RViz2에서 지도 확인
```

확인한 것은 다음과 같다.

```text
[x] TurtleBot3 이동에 따라 LaserScan 데이터가 변함
[x] RViz2에서 지도 영역이 넓어짐
[x] 검은색 벽/장애물 영역과 흰색 자유 공간이 확장됨
[x] RobotModel이 map 위에서 이동함
```

---

## 6.8 지도 저장

지도가 어느 정도 확장된 뒤 로봇을 멈추고 `/map`을 파일로 저장했다.

먼저 지도 저장 폴더를 만들었다.

```bash
cd ~/projects/missionbot-ros2
mkdir -p maps/phase04_slam
```

지도 저장 도구인 `nav2_map_server` 패키지가 인식되는지 확인했다.

```bash
ros2 pkg list | grep nav2_map_server
```

이후 `map_saver_cli`로 지도를 저장했다.

```bash
ros2 run nav2_map_server map_saver_cli -f maps/phase04_slam/tb3_world_slam_map_01
```

저장 결과를 확인했다.

```bash
ls -lh maps/phase04_slam
```

확인된 결과는 다음과 같다.

```text
-rw-rw-r-- 1 user user 12K Jun  2 13:03 tb3_world_slam_map_01.pgm
-rw-rw-r-- 1 user user 139 Jun  2 13:03 tb3_world_slam_map_01.yaml
```

---

## 6.9 저장된 지도 파일 확인

저장된 `.yaml` 파일 내용을 확인했다.

```bash
cat maps/phase04_slam/tb3_world_slam_map_01.yaml
```

확인된 내용은 다음과 같다.

```yaml
image: tb3_world_slam_map_01.pgm
mode: trinary
resolution: 0.05
origin: [-2.94, -2.57, 0]
negate: 0
occupied_thresh: 0.65
free_thresh: 0.25
```

`.pgm` 파일이 실제 지도 이미지인지 확인했다.

```bash
file maps/phase04_slam/tb3_world_slam_map_01.pgm
```

확인 결과는 다음과 같다.

```text
maps/phase04_slam/tb3_world_slam_map_01.pgm: Netpbm image data, size = 112 x 103, rawbits, greymap
```

또한 `.pgm` 파일 앞부분을 확인했다.

```bash
head -n 5 maps/phase04_slam/tb3_world_slam_map_01.pgm
```

확인된 주요 헤더는 다음과 같다.

```text
P5
112 103
255
```

이후 깨진 문자처럼 보이는 출력은 이미지 픽셀 데이터이므로 정상으로 판단했다.

---

## 7. 주요 명령어 정리

## 7.1 TurtleBot3 World 실행

```bash
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

의미:

```text
turtlebot3_gazebo 패키지의 turtlebot3_world.launch.py를 실행한다.
벽과 구조물이 있는 Gazebo World에 TurtleBot3 Burger를 spawn한다.
SLAM 실습에 필요한 /scan, /odom, /tf, /tf_static topic을 생성한다.
```

---

## 7.2 SLAM Toolbox 실행

```bash
ros2 launch slam_toolbox online_async_launch.py use_sim_time:=True
```

의미:

```text
slam_toolbox 패키지의 online_async_launch.py를 실행한다.
TurtleBot3가 움직이는 동안 실시간으로 SLAM 지도를 생성한다.
use_sim_time:=True 옵션으로 Gazebo의 /clock 시뮬레이션 시간을 사용한다.
```

---

## 7.3 `/map` 확인

```bash
ros2 topic info /map
```

의미:

```text
SLAM Toolbox가 /map topic을 발행하고 있는지 확인한다.
정상 타입은 nav_msgs/msg/OccupancyGrid이다.
```

---

## 7.4 RViz2 실행

```bash
rviz2
```

의미:

```text
ROS2 데이터를 시각화한다.
Phase 4에서는 Fixed Frame을 map으로 설정하고 /map, TF, RobotModel, LaserScan을 함께 확인한다.
```

---

## 7.5 teleop 실행

```bash
ros2 run turtlebot3_teleop teleop_keyboard
```

의미:

```text
키보드 입력을 /cmd_vel 속도 명령으로 변환한다.
TurtleBot3를 움직여 SLAM 지도를 확장한다.
```

---

## 7.6 지도 저장

```bash
ros2 run nav2_map_server map_saver_cli -f maps/phase04_slam/tb3_world_slam_map_01
```

의미:

```text
현재 /map topic을 파일로 저장한다.
결과로 .pgm 지도 이미지와 .yaml 지도 설정 파일이 생성된다.
```

---

## 8. 성공 기준

Phase 4의 성공 기준은 다음과 같다.

```text
[x] slam_toolbox 패키지 인식
[x] turtlebot3_world 실행
[x] /scan, /odom, /tf, /tf_static 존재
[x] slam_toolbox 실행
[x] /slam_toolbox node 확인
[x] /map topic 생성
[x] /map 타입이 nav_msgs/msg/OccupancyGrid
[x] RViz2 Fixed Frame = map
[x] Map display Topic = /map
[x] TF, RobotModel, LaserScan, Map 표시
[x] teleop으로 지도 확장 확인
[x] map_saver_cli로 지도 저장
[x] .pgm / .yaml 파일 생성
[x] .yaml 설정 확인
[x] .pgm 이미지 파일 형식 확인
```

---

## 9. 발생한 이슈와 판단

## 9.1 PGM 파일 출력 시 깨진 문자처럼 보이는 문제

상황:

```bash
head -n 5 maps/phase04_slam/tb3_world_slam_map_01.pgm
```

출력 중 깨진 문자처럼 보이는 내용이 나타났다.

처음에는 파일이 잘못 저장된 것처럼 보일 수 있다.

하지만 `.pgm` 파일은 사람이 읽기 위한 텍스트 파일이 아니라 이미지 파일이다. 앞부분에는 파일 형식 정보가 나오고, 그 뒤부터는 픽셀 데이터가 들어 있다.

정상으로 판단한 근거는 다음과 같다.

```text
P5
112 103
255
```

그리고 `file` 명령어 결과도 정상이다.

```text
Netpbm image data, size = 112 x 103, rawbits, greymap
```

따라서 깨진 문자처럼 보이는 부분은 이미지 픽셀 데이터이며, 지도 저장 실패가 아니다.

---

## 10. Phase 4에서 배운 점

이번 Phase를 통해 배운 점은 다음과 같다.

```text
1. SLAM은 /scan만으로 동작하는 것이 아니라, TF와 odom 정보를 함께 사용한다.
2. Gazebo 환경에서는 use_sim_time:=True 설정이 중요하다.
3. SLAM 실행 후 RViz2의 Fixed Frame은 odom이 아니라 map으로 설정해야 한다.
4. /map은 nav_msgs/msg/OccupancyGrid 타입의 지도 topic이다.
5. SLAM 지도는 로봇이 움직이며 새로운 환경을 관측할수록 확장된다.
6. 빠른 주행보다 천천히 이동하고 회전하는 것이 안정적인 지도 생성에 유리하다.
7. 지도 저장 결과는 .pgm과 .yaml 파일 한 쌍으로 생성된다.
8. .pgm은 지도 이미지, .yaml은 지도 해석 설정 파일이다.
9. PGM 파일을 터미널로 직접 열면 깨진 문자처럼 보일 수 있지만, rawbits 이미지 데이터이므로 정상일 수 있다.
```

---

## 11. 최종 결과물

생성된 지도 파일은 다음과 같다.

```text
maps/phase04_slam/tb3_world_slam_map_01.pgm
maps/phase04_slam/tb3_world_slam_map_01.yaml
```

확인된 지도 설정은 다음과 같다.

```yaml
image: tb3_world_slam_map_01.pgm
mode: trinary
resolution: 0.05
origin: [-2.94, -2.57, 0]
negate: 0
occupied_thresh: 0.65
free_thresh: 0.25
```

확인된 주요 topic은 다음과 같다.

```text
/map
/map_metadata
/odom
/scan
/slam_toolbox/scan_visualization
/tf
/tf_static
/cmd_vel
```

확인된 주요 node는 다음과 같다.

```text
/gazebo
/robot_state_publisher
/slam_toolbox
/transform_listener_impl_62b98f4d38e0
/turtlebot3_diff_drive
/turtlebot3_imu
/turtlebot3_joint_state
/turtlebot3_laserscan
```

---

## 12. 다음 Phase와의 연결

다음 Phase는 다음과 같다.

```text
Phase 5. Navigation2
```

Phase 5에서는 Phase 4에서 저장한 지도를 기반으로 Navigation2를 실행한다.

연결 흐름은 다음과 같다.

```text
Phase 4
→ SLAM으로 map 생성 및 저장

Phase 5
→ 저장된 map을 불러옴
→ Navigation2 실행
→ TurtleBot3가 목표 지점까지 이동
```

Phase 4에서 만든 지도는 Navigation2가 경로 계획과 위치 추정을 수행하는 기반 데이터가 된다.

---

## 13. Phase 4 완료 판정

Phase 4는 완료로 판단한다.

완료 근거는 다음과 같다.

```text
SLAM Toolbox 실행 성공
/map topic 생성 확인
RViz2에서 SLAM 지도 시각화 성공
teleop으로 지도 확장 확인
map_saver_cli로 지도 저장 성공
.pgm / .yaml 지도 파일 생성 확인
저장된 지도 파일 내용 및 형식 확인
```

이번 Phase를 통해 TurtleBot3의 센서 데이터와 TF 정보가 실제 SLAM 지도 생성으로 이어지는 흐름을 확인했다.
