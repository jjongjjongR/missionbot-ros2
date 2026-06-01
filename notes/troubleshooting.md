# Troubleshooting

이 문서는 MissionBot-ROS2 프로젝트를 진행하면서 발생한 오류와 해결 과정을 기록하는 문서입니다.

오류를 해결한 뒤에는 반드시 원인, 해결 방법, 배운 점을 함께 기록합니다.

---

## 기록 규칙

각 오류는 아래 형식으로 기록합니다.

- TS-{번호}_{오류요약}

예시:

- TS-0001_ros2_package_build_error
- TS-0002_turtlebot3_model_not_found
- TS-0003_gazebo_launch_failed

---

## TS-0001_example_error

### 1. 발생 날짜

- Date:

### 2. 발생 단계

- Phase:
- 작업 내용:

### 3. 오류 상황

오류 메시지:

    여기에 오류 메시지를 붙여넣기

### 4. 사용 환경

- OS:
- ROS2 version:
- Gazebo version:
- Python version:
- TurtleBot3 model:
- 기타:

### 5. 원인 추정

-

### 6. 해결 방법

사용한 명령어:

    여기에 해결에 사용한 명령어 작성

### 7. 해결 결과

-

### 8. 배운 점

-

### 9. 다시 발생하지 않도록 주의할 점

-


---

## TS-0003_missionbot_basic_package_not_found

### 1. 발생 날짜

- Date: 2026-05-25

### 2. 발생 단계

- Phase: Phase 1. ROS2 basics
- 작업 내용: missionbot_basic launch 파일 실행

### 3. 오류 상황

오류 메시지:

    Package 'missionbot_basic' not found: "package 'missionbot_basic' not found, searching: ['/home/user/turtlebot3_ws/install/turtlebot3_simulations', '/home/user/turtlebot3_ws/install/turtlebot3_manipulation_gazebo', '/home/user/turtlebot3_ws/install/turtlebot3_gazebo', '/home/user/turtlebot3_ws/install/turtlebot3_fake_node', '/opt/ros/humble']"

실행한 명령어:

    ros2 launch missionbot_basic turtlesim_pubsub.launch.py

### 4. 사용 환경

- OS: Ubuntu 22.04 LTS
- ROS2 version: Humble Hawksbill
- Gazebo version: Gazebo Classic 11.10.2
- Python version:
- TurtleBot3 model: burger
- Project path: ~/projects/missionbot-ros2

### 5. 원인 추정

현재 터미널에 MissionBot workspace의 `install/setup.bash`가 source되지 않았다.

에러 메시지의 searching 경로에는 다음만 포함되어 있었다.

- /home/user/turtlebot3_ws/install/...
- /opt/ros/humble

하지만 missionbot_basic 패키지는 다음 workspace에 있다.

- /home/user/projects/missionbot-ros2/install

따라서 ROS2가 현재 터미널 환경에서 missionbot_basic 패키지를 찾지 못했다.

### 6. 해결 방법

사용한 명령어:

    cd ~/projects/missionbot-ros2
    source install/setup.bash
    ros2 pkg list | grep missionbot_basic
    ros2 launch missionbot_basic turtlesim_pubsub.launch.py

### 7. 해결 결과

- `ros2 pkg list | grep missionbot_basic` 명령에서 missionbot_basic 패키지가 확인되었다.
- `ros2 launch missionbot_basic turtlesim_pubsub.launch.py` 명령이 정상 실행되었다.
- turtlesim_node, pose_subscriber, velocity_publisher가 launch 파일로 함께 실행되었다.

### 8. 배운 점

ROS2 기본 환경과 내가 만든 workspace 환경은 다르다.

`.bashrc`에서 자동으로 적용되는 것은 주로 다음 환경이다.

- /opt/ros/humble/setup.bash
- ~/turtlebot3_ws/install/setup.bash

하지만 MissionBot 프로젝트에서 직접 만든 패키지를 실행하려면 다음 설정을 현재 터미널에 추가로 적용해야 한다.

- ~/projects/missionbot-ros2/install/setup.bash

즉, colcon build 후에는 다음 명령을 실행해야 한다.

    source install/setup.bash

### 9. 다시 발생하지 않도록 주의할 점

- missionbot_basic 같은 직접 만든 패키지가 안 보이면 먼저 `ros2 pkg list | grep missionbot_basic`으로 확인한다.
- 패키지가 안 나오면 프로젝트 루트에서 `source install/setup.bash`를 실행한다.
- 그래도 안 나오면 `colcon build --packages-select missionbot_basic` 후 다시 source한다.
- `source ~/.bashrc`와 `source install/setup.bash`의 역할을 구분한다.

---

---

## TS-0003_gzclient_camera_assertion_failed

### 1. 발생 날짜

- Date: 2026-06-01

### 2. 발생 단계

- Phase: Phase 2. Gazebo + TurtleBot3 / Phase 3. RViz2 + TF2
- 작업 내용: TurtleBot3 Gazebo empty_world 실행

### 3. 오류 상황

TurtleBot3 Gazebo launch 실행 중 `gzclient` 프로세스가 종료되었다.

실행 명령:

```bash
ros2 launch turtlebot3_gazebo empty_world.launch.py
```

오류 메시지:

```text
[gzclient-2] libcurl: (6) Could not resolve host: fuel.ignitionrobotics.org
[gzclient-2] gzclient: /usr/include/boost/smart_ptr/shared_ptr.hpp:728:
typename boost::detail::sp_member_access<T>::type boost::shared_ptr<T>::operator->() const
[with T = gazebo::rendering::Camera;
typename boost::detail::sp_member_access<T>::type = gazebo::rendering::Camera*]:
Assertion `px != 0' failed.
[ERROR] [gzclient-2]: process has died
cmd 'gzclient --gui-client-plugin=libgazebo_ros_eol_gui.so'
```

동시에 확인된 정상 로그:

```text
Spawn status: SpawnEntity: Successfully spawned entity [burger]
[turtlebot3_diff_drive]: Subscribed to [/cmd_vel]
[turtlebot3_diff_drive]: Advertise odometry on [/odom]
[turtlebot3_diff_drive]: Publishing odom transforms between [odom] and [base_footprint]
```

### 4. 사용 환경

- OS: Ubuntu 22.04 LTS
- ROS2 version: Humble Hawksbill
- Gazebo version: Gazebo Classic 11.10.2
- TurtleBot3 model: burger
- Virtualization: VMware Workstation 17
- Remote GUI: NoMachine
- Development Client: MacBook

### 5. 원인 추정

이 오류는 TurtleBot3 spawn 실패가 아니라 Gazebo GUI 클라이언트인 `gzclient` 문제로 판단했다.

근거:

```text
1. TurtleBot3 Burger spawn은 성공했다.
2. gzserver는 계속 살아 있었다.
3. /cmd_vel, /odom, /scan, /tf, /tf_static topic이 정상적으로 생성되었다.
4. robot_state_publisher도 정상적으로 실행되었다.
5. odom → base_footprint transform도 발행되었다.
```

따라서 문제는 다음 쪽에 가깝다.

```text
Gazebo Classic GUI client
VMware 그래픽 렌더링
NoMachine GUI 환경
Gazebo GUI plugin
카메라 렌더링 관련 assertion
```

### 6. 확인 방법

Gazebo GUI가 죽어도 바로 실패로 판단하지 않고, 새 터미널에서 아래 topic을 확인한다.

```bash
ros2 topic list | grep -E "cmd_vel|odom|scan|tf"
```

정상 기준:

```text
/cmd_vel
/odom
/scan
/tf
/tf_static
```

위 topic이 살아 있다면 Gazebo 시뮬레이션 서버와 TurtleBot3 ROS2 데이터는 정상으로 판단한다.

### 7. 해결 또는 우회 방법

현재 프로젝트에서는 근본 해결보다는 우회 진행 방식을 사용한다.

우회 기준:

```text
1. TurtleBot3 spawn 성공 여부를 먼저 본다.
2. /cmd_vel, /odom, /scan, /tf, /tf_static topic 존재 여부를 확인한다.
3. topic이 살아 있으면 Gazebo GUI가 죽어도 Phase 진행 가능으로 판단한다.
4. Phase 3부터는 RViz2 중심으로 로봇 모델, TF, LaserScan을 확인한다.
```

필요 시 Gazebo GUI 재연결:

```bash
gzclient --verbose
```

추가 우회 후보:

```bash
QT_X11_NO_MITSHM=1 LIBGL_ALWAYS_SOFTWARE=1 gzclient --verbose
```

단, 현재까지는 RViz2 중심 진행으로 충분했다.

### 8. 해결 결과

Phase 3에서는 `gzclient` crash가 발생했지만 다음을 확인했다.

```text
[x] TurtleBot3 Burger spawn 성공
[x] /cmd_vel 생성
[x] /odom 생성
[x] /scan 생성
[x] /tf 생성
[x] /tf_static 생성
[x] RViz2 실행 성공
[x] TF display 성공
[x] RobotModel display 성공
[x] LaserScan display 연결 성공
[x] TF tree 확인 성공
[x] teleop 이동 중 transform 변화 확인 성공
```

따라서 `gzclient` crash는 Phase 진행을 막는 치명적 오류가 아니라, GUI 렌더링 관련 반복 이슈로 분리했다.

### 9. 배운 점

```text
Gazebo는 gzserver와 gzclient로 나뉜다.

gzserver
→ 실제 시뮬레이션 서버
→ 물리 계산, 센서, robot plugin, ROS2 topic 발행 담당

gzclient
→ 사람이 보는 Gazebo GUI
→ 창, 카메라, 모델 렌더링 담당
```

`gzclient`가 죽어도 `gzserver`가 살아 있으면 ROS2 topic은 정상적으로 발행될 수 있다.

### 10. 다시 발생하지 않도록 주의할 점

```text
1. gzclient crash만 보고 TurtleBot3 실행 실패로 판단하지 않는다.
2. 반드시 /cmd_vel, /odom, /scan, /tf, /tf_static topic을 확인한다.
3. RViz2 단계에서는 Gazebo GUI보다 ROS2 topic과 TF 상태를 우선한다.
4. VMware + NoMachine + Gazebo GUI 환경에서는 GUI crash가 반복될 수 있음을 전제로 진행한다.
5. 실제 시각화가 필요하면 RViz2를 우선 사용한다.
```