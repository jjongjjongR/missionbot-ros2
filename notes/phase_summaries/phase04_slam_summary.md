# Phase 4 Summary - SLAM

## 1. Phase 개요

Phase 4에서는 TurtleBot3 Gazebo World 환경에서 SLAM Toolbox를 실행하고, LiDAR `/scan` 데이터와 TF 정보를 기반으로 지도를 생성했다.

이전 Phase 3에서는 RViz2와 TF2를 사용해 TurtleBot3의 센서 데이터와 좌표계 구조를 확인했다. Phase 4에서는 그 흐름을 확장하여 SLAM Toolbox가 `/scan`, `/odom`, `/tf`, `/tf_static` 정보를 사용해 `/map` topic을 생성하는 과정을 실습했다.

최종적으로 RViz2에서 생성 중인 지도를 확인했고, teleop_keyboard로 TurtleBot3를 이동시키며 지도가 확장되는 것을 확인했다. 이후 `map_saver_cli`를 사용해 생성된 지도를 `.pgm`, `.yaml` 파일로 저장했다.

---

## 2. 이번 Phase의 목표

```text
TurtleBot3가 Gazebo World 안에서 이동하면서
LiDAR와 TF 정보를 기반으로 SLAM 지도를 생성하고,
그 결과를 RViz2에서 확인한 뒤 파일로 저장한다.
```

세부 목표는 다음과 같다.

```text
[x] SLAM Toolbox 설치 및 패키지 인식 확인
[x] TurtleBot3 Gazebo World 실행
[x] `/scan`, `/odom`, `/tf`, `/tf_static` topic 확인
[x] SLAM Toolbox 실행
[x] `/map` topic 생성 확인
[x] RViz2에서 SLAM 지도 시각화
[x] teleop으로 TurtleBot3를 움직이며 지도 확장 확인
[x] 생성된 지도 저장
[x] `.pgm`, `.yaml` 지도 파일 확인
```

---

## 3. 진행 환경

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
Gazebo Classic

Robot:
TurtleBot3 Burger

Visualization:
RViz2

SLAM:
slam_toolbox

Project path:
~/projects/missionbot-ros2
```

---

## 4. 실행 전 환경 확인

Phase 4 시작 전 아래 항목을 확인했다.

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

확인 결과:

```text
ROS2 distribution:
humble

TurtleBot3 model:
burger

ros2 path:
/opt/ros/humble/bin/ros2

gazebo path:
/usr/bin/gazebo

rviz2 path:
/opt/ros/humble/bin/rviz2

SLAM Toolbox:
slam_toolbox

TurtleBot3 Gazebo:
turtlebot3_gazebo

TurtleBot3 Teleop:
turtlebot3_teleop

Project path:
/home/user/projects/missionbot-ros2
```

이 결과를 기준으로 Phase 4 SLAM 실습을 진행할 준비가 완료된 것으로 판단했다.

---

## 5. TurtleBot3 World 실행

Phase 3에서는 `empty_world`를 사용했지만, SLAM에서는 벽과 구조물이 있는 환경이 필요하다.

따라서 Phase 4에서는 아래 명령어로 TurtleBot3 기본 월드를 실행했다.

```bash
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

이 월드는 SLAM 실습에 더 적합하다.

```text
empty_world
→ 감지할 벽과 장애물이 거의 없어 `/scan` 값이 inf 위주로 나올 수 있음

turtlebot3_world
→ 벽과 구조물이 있어 LiDAR가 실제 거리값을 감지할 수 있음
```

확인한 주요 topic:

```text
/cmd_vel
/odom
/scan
/tf
/tf_static
```

---

## 6. SLAM Toolbox 실행

TurtleBot3 World가 실행된 상태에서 아래 명령어로 SLAM Toolbox를 실행했다.

```bash
ros2 launch slam_toolbox online_async_launch.py use_sim_time:=True
```

명령어 의미:

```text
slam_toolbox
→ SLAM 기능을 제공하는 ROS2 패키지

online_async_launch.py
→ 로봇이 움직이는 동안 실시간으로 지도를 생성하는 launch 파일

use_sim_time:=True
→ Gazebo의 `/clock` 시뮬레이션 시간을 사용하도록 설정
```

Gazebo 시뮬레이션 환경에서는 실제 컴퓨터 시간이 아니라 `/clock` 기반 시뮬레이션 시간이 사용되므로, SLAM Toolbox 실행 시 `use_sim_time:=True` 설정이 중요하다.

---

## 7. SLAM Toolbox 실행 확인

SLAM Toolbox 실행 후 아래 명령어로 node와 topic을 확인했다.

```bash
ros2 node list
```

확인된 주요 node:

```text
/gazebo
/robot_state_publisher
/slam_toolbox
/turtlebot3_diff_drive
/turtlebot3_imu
/turtlebot3_joint_state
/turtlebot3_laserscan
```

topic 확인:

```bash
ros2 topic list | grep -E "map|scan|tf|odom"
```

확인된 topic:

```text
/map
/map_metadata
/odom
/scan
/slam_toolbox/scan_visualization
/tf
/tf_static
```

`/map` topic 정보 확인:

```bash
ros2 topic info /map
```

결과:

```text
Type: nav_msgs/msg/OccupancyGrid
Publisher count: 1
Subscription count: 1
```

이를 통해 SLAM Toolbox가 `/map` topic을 정상적으로 생성하고 있음을 확인했다.

---

## 8. RViz2에서 지도 시각화

SLAM Toolbox 실행 후 RViz2를 실행했다.

```bash
rviz2
```

RViz2 설정:

```text
Global Options
→ Fixed Frame: map
```

추가한 Display:

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

RViz2에서 확인한 것:

```text
[x] Fixed Frame을 map으로 설정
[x] Map display가 `/map` topic을 표시
[x] TF 좌표계 표시
[x] RobotModel 표시
[x] LaserScan 점 표시
[x] SLAM 지도 영역 표시
```

---

## 9. teleop으로 지도 확장

SLAM 지도는 한 번에 완성되지 않는다.

로봇이 움직이면서 새로운 벽과 구조물을 관측해야 지도 영역이 넓어진다.

아래 명령어로 TurtleBot3를 조작했다.

```bash
ros2 run turtlebot3_teleop teleop_keyboard
```

조작 키:

```text
w: 전진
x: 후진
a: 왼쪽 회전
d: 오른쪽 회전
s: 정지
```

지도 확장 시 주의한 점:

```text
전진은 짧게
회전은 천천히
급회전 금지
벽과 구조물을 충분히 관측
중간중간 멈추며 RViz2에서 지도 확인
```

확인 결과:

```text
[x] TurtleBot3 이동에 따라 LaserScan 데이터가 변함
[x] RViz2에서 지도 영역이 넓어짐
[x] 검은색 벽/장애물 영역과 흰색 자유 공간이 확장됨
[x] RobotModel이 map 위에서 이동함
```

---

## 10. 지도 저장

지도가 어느 정도 확장된 뒤, 로봇을 정지하고 생성된 `/map`을 파일로 저장했다.

지도 저장 폴더 생성:

```bash
mkdir -p maps/phase04_slam
```

`nav2_map_server` 패키지 확인:

```bash
ros2 pkg list | grep nav2_map_server
```

지도 저장 명령어:

```bash
ros2 run nav2_map_server map_saver_cli -f maps/phase04_slam/tb3_world_slam_map_01
```

저장 결과 확인:

```bash
ls -lh maps/phase04_slam
```

생성된 파일:

```text
tb3_world_slam_map_01.pgm
tb3_world_slam_map_01.yaml
```

파일 크기:

```text
tb3_world_slam_map_01.pgm   12K
tb3_world_slam_map_01.yaml  139
```

---

## 11. 저장된 지도 파일 확인

저장된 `.yaml` 파일을 확인했다.

```bash
cat maps/phase04_slam/tb3_world_slam_map_01.yaml
```

확인된 내용:

```yaml
image: tb3_world_slam_map_01.pgm
mode: trinary
resolution: 0.05
origin: [-2.94, -2.57, 0]
negate: 0
occupied_thresh: 0.65
free_thresh: 0.25
```

각 항목의 의미:

```text
image
→ 연결된 지도 이미지 파일 이름

mode
→ 지도 해석 방식

resolution
→ 지도 1픽셀이 실제 몇 m인지 의미
→ 0.05는 1픽셀 = 5cm

origin
→ 지도 이미지의 원점 위치

negate
→ 색상 해석 반전 여부

occupied_thresh
→ 장애물로 판단할 점유 확률 기준

free_thresh
→ 자유 공간으로 판단할 기준
```

`.pgm` 파일 타입 확인:

```bash
file maps/phase04_slam/tb3_world_slam_map_01.pgm
```

확인 결과:

```text
Netpbm image data, size = 112 x 103, rawbits, greymap
```

이를 통해 `.pgm` 파일이 실제 지도 이미지 파일로 저장되었음을 확인했다.

`head` 명령어로 `.pgm` 앞부분도 확인했다.

```bash
head -n 5 maps/phase04_slam/tb3_world_slam_map_01.pgm
```

확인된 주요 헤더:

```text
P5
112 103
255
```

의미:

```text
P5
→ 바이너리 PGM 이미지 형식

112 103
→ 가로 112픽셀, 세로 103픽셀

255
→ 픽셀 밝기 최댓값
```

헤더 이후 깨진 문자처럼 보이는 내용은 이미지 픽셀 데이터이므로 정상으로 판단했다.

---

## 12. 이번 Phase에서 배운 핵심 개념

## 12.1 SLAM

```text
SLAM은 로봇이 움직이면서 자기 위치를 추정하고 동시에 주변 지도를 만드는 과정이다.
```

이번 Phase에서는 SLAM Toolbox를 사용해 TurtleBot3의 LiDAR `/scan`과 TF 정보를 기반으로 `/map`을 생성했다.

---

## 12.2 `/map`

```text
/map은 SLAM 결과로 생성되는 지도 topic이다.
```

타입은 다음과 같다.

```text
nav_msgs/msg/OccupancyGrid
```

OccupancyGrid는 공간을 격자 형태로 나누고, 각 칸이 점유 공간인지 자유 공간인지 알 수 있게 표현하는 지도 메시지다.

---

## 12.3 map frame

Phase 3에서는 RViz2 Fixed Frame을 `odom`으로 사용했다.

하지만 SLAM 실행 후에는 `map` frame이 생기므로 RViz2 기준 좌표계를 `map`으로 설정했다.

SLAM 이후 TF 구조는 다음과 같이 확장된다.

```text
map
→ odom
→ base_footprint
→ base_link
→ base_scan
```

---

## 12.4 `use_sim_time`

Gazebo는 시뮬레이션 시간이 `/clock` topic으로 흐른다.

따라서 Gazebo 환경에서 SLAM Toolbox를 실행할 때는 다음 옵션을 사용했다.

```bash
use_sim_time:=True
```

이 설정은 SLAM Toolbox가 Gazebo의 시간 기준에 맞춰 `/scan`, `/tf`, `/odom` 데이터를 해석하게 한다.

---

## 12.5 PGM / YAML 지도 파일

SLAM 지도는 보통 두 파일로 저장된다.

```text
.pgm
→ 실제 지도 이미지

.yaml
→ 지도 이미지를 ROS2가 어떻게 해석해야 하는지 알려주는 설정 파일
```

이번 Phase에서는 다음 두 파일을 생성했다.

```text
maps/phase04_slam/tb3_world_slam_map_01.pgm
maps/phase04_slam/tb3_world_slam_map_01.yaml
```

---

## 13. Phase 3와 Phase 4의 연결

Phase 3에서 확인한 것:

```text
/scan
/tf
/tf_static
/odom
RobotModel
LaserScan
RViz2 Fixed Frame = odom
```

Phase 4에서 확장한 것:

```text
SLAM Toolbox 실행
/map 생성
RViz2 Fixed Frame = map
Map display 추가
teleop으로 지도 확장
map_saver_cli로 지도 저장
```

연결 의미:

```text
Phase 3에서는 센서와 좌표계가 정상적으로 발행되는지 확인했다.
Phase 4에서는 그 센서와 좌표계 정보를 SLAM Toolbox에 연결해 실제 지도를 생성했다.
```

---

## 14. Phase 5와의 연결

Phase 5에서는 Navigation2를 다룰 예정이다.

Navigation2는 로봇이 목표 지점까지 이동하기 위해 지도가 필요하다.

Phase 4에서 저장한 지도는 Phase 5에서 사용할 수 있는 기반 map이 된다.

```text
Phase 4
→ SLAM으로 map 생성 및 저장

Phase 5
→ 저장된 map을 기반으로 Navigation2 실행
→ 목표 지점 이동
```

---

## 15. 발생한 주요 이슈와 판단

## 15.1 PGM 파일 출력 시 깨진 문자처럼 보이는 문제

상황:

```bash
head -n 5 maps/phase04_slam/tb3_world_slam_map_01.pgm
```

출력 중 `����` 같은 깨진 문자처럼 보이는 내용이 나타났다.

판단:

```text
실패가 아니다.
PGM 파일의 앞부분에는 이미지 형식 정보가 있고, 그 뒤에는 픽셀 데이터가 들어 있다.
rawbits 방식의 PGM은 사람이 읽는 텍스트가 아니라 바이너리 이미지 데이터에 가깝기 때문에 터미널에서 깨진 문자처럼 보일 수 있다.
```

정상 근거:

```text
P5
112 103
255
```

그리고 `file` 명령어 결과:

```text
Netpbm image data, size = 112 x 103, rawbits, greymap
```

따라서 저장된 `.pgm` 파일은 정상적인 지도 이미지 파일로 판단했다.

---

## 16. 완료 판정

Phase 4는 다음 기준을 만족했으므로 완료로 판단한다.

```text
[x] SLAM Toolbox 패키지 인식 확인
[x] TurtleBot3 Gazebo World 실행
[x] `/scan`, `/odom`, `/tf`, `/tf_static` 확인
[x] SLAM Toolbox 실행
[x] `use_sim_time:=True` 적용
[x] `/slam_toolbox` node 확인
[x] `/map` topic 생성 확인
[x] `/map` 타입이 `nav_msgs/msg/OccupancyGrid`인지 확인
[x] RViz2 Fixed Frame을 `map`으로 설정
[x] Map display를 `/map`에 연결
[x] RViz2에서 지도 시각화 확인
[x] teleop으로 지도 확장 확인
[x] `map_saver_cli`로 지도 저장
[x] `.pgm`, `.yaml` 지도 파일 생성 확인
[x] `.yaml` 지도 설정 확인
[x] `.pgm` 이미지 파일 형식 확인
```

---

## 17. 최종 결과물

생성된 지도 파일:

```text
maps/phase04_slam/tb3_world_slam_map_01.pgm
maps/phase04_slam/tb3_world_slam_map_01.yaml
```

확인된 핵심 topic:

```text
/map
/map_metadata
/odom
/scan
/slam_toolbox/scan_visualization
/tf
/tf_static
```

확인된 핵심 node:

```text
/slam_toolbox
/gazebo
/robot_state_publisher
/turtlebot3_diff_drive
/turtlebot3_imu
/turtlebot3_joint_state
/turtlebot3_laserscan
```

---

## 18. 다음 단계

다음 Phase는 다음과 같다.

```text
Phase 5. Navigation2
```

Phase 5에서는 Phase 4에서 저장한 지도를 기반으로 Navigation2를 실행하고, TurtleBot3가 목표 지점까지 이동하는 흐름을 확인한다.

다음 Phase 시작 전 확인할 것:

```text
[ ] 저장된 map 파일 경로 확인
[ ] nav2 관련 패키지 인식 확인
[ ] RViz2에서 map 불러오기 준비
[ ] Gazebo TurtleBot3 World 실행 준비
```
