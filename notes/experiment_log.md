# Experiment Log

이 문서는 MissionBot-ROS2 프로젝트의 전체 실험 기록 인덱스입니다.

각 실험은 Phase 번호와 실험 번호를 기준으로 기록합니다.

## 실험 ID 규칙

- 일반 실험: P{Phase번호}-EXP-{실험번호}_{실험요약}
- 실패 실험: P{Phase번호}-FAIL-{실패번호}_{실패요약}

예시:

- P02-EXP-0001_turtlebot3_gazebo_launch
- P03-EXP-0001_rviz2_tf_check
- P05-FAIL-0001_goal_unreachable

---

## 기록 항목 설명

| 항목 | 의미 |
|---|---|
| Date | 실험 날짜 |
| Phase | 어느 Phase 실험인지 |
| Goal | 실험 목적 |
| Environment | ROS2 버전, Gazebo 버전, TurtleBot3 모델 등 |
| Command | 실행한 명령어 |
| Topics | 확인한 ROS2 topic |
| Result | 결과 요약 |
| Success | 성공 여부 |
| Failure Type | 실패 유형 |
| Notes | 알게 된 점 |
| Related Files | 캡처, 영상, rosbag, 로그 경로 |

---
## 예시

### P00-EXP-0001_project_setup

- Date:
- Phase: Phase 0. Project setup
- Goal: 프로젝트 기본 폴더 구조와 README를 생성한다.
- Environment:
- Command:
- Topics:
- Result:
- Success:
- Failure Type:
- Notes:
- Related Files:

---

## 실제 실험 기록

---

## 실제 실험 기록

### P00-EXP-0001_project_setup

- Date: 2026-05-25
- Phase: Phase 0. Project setup
- Goal: MissionBot-ROS2 프로젝트의 GitHub 저장소, README, 기본 폴더 구조, 실험 기록 구조를 생성한다.
- Environment:
  - Repository: missionbot-ros2
  - Development Client: MacBook
  - Project Runtime Target: Ubuntu VM
- Command:
  - README.md 작성
  - .gitignore 작성
  - docs/00_project_overview.md 작성
  - notes/experiment_log.md 작성
  - notes/troubleshooting.md 작성
  - 기본 폴더 생성
- Topics:
  - 없음
- Result:
  - 프로젝트 기본 구조를 생성했다.
  - README에 프로젝트 개요, Motivation, Project Scope, 기술 스택, Phase Map, 파일 구조, 실험 기록 방식을 정리했다.
  - 실험 기록과 오류 해결 기록을 남길 문서 구조를 준비했다.
- Success: Yes
- Failure Type: None
- Notes:
  - Phase 0은 코드 구현보다 프로젝트 기준과 기록 구조를 만드는 단계로 진행했다.
  - maps, rosbags, results, notes, docs, src, configs 폴더를 기준 구조로 사용한다.
- Related Files:
  - README.md
  - .gitignore
  - docs/00_project_overview.md
  - notes/experiment_log.md
  - notes/troubleshooting.md

---

### P00-EXP-0002_remote_gui_connection_check

- Date: 2026-05-25
- Phase: Phase 0.5 Environment setup
- Goal: MacBook에서 Tailscale과 NoMachine을 이용해 Ubuntu VM의 GUI 화면에 접속할 수 있는지 확인한다.
- Environment:
  - Host: Windows Desktop
  - Virtualization: VMware Workstation 17
  - Guest OS: Ubuntu 22.04
  - Remote Network: Tailscale
  - Remote GUI: NoMachine
  - Client: MacBook
- Command:
  - tailscale status
  - tailscale ip -4
  - sudo /usr/NX/bin/nxserver --status
  - ss -lntp | grep 4000
  - nc -vz 100.95.184.79 4000
- Topics:
  - 없음
- Result:
  - MacBook에서 Ubuntu VM의 NoMachine 4000번 포트에 접근 가능함을 확인했다.
  - NoMachine의 nxserver, nxnode, nxd 서비스가 정상 활성화된 것을 확인했다.
  - MacBook에서 NoMachine을 통해 Ubuntu VM GUI 화면에 접속할 수 있음을 확인했다.
- Success: Yes
- Failure Type: None
- Notes:
  - 초기에는 NoMachine 흰 화면 문제가 있었으나, 서비스 재시작과 GUI 세션 정리 후 정상 접속을 확인했다.
  - SSH는 코드 수정과 터미널 작업용, NoMachine은 Gazebo와 RViz 같은 GUI 확인용으로 역할을 분리한다.
- Related Files:
  - notes/troubleshooting.md

---

### P00-EXP-0003_ros2_humble_basic_check

- Date: 2026-05-25
- Phase: Phase 0.5 Environment setup
- Goal: Ubuntu VM에서 ROS2 Humble이 정상 활성화되고 기본 ROS2 명령이 동작하는지 확인한다.
- Environment:
  - Guest OS: Ubuntu 22.04
  - ROS2: Humble Hawksbill
  - Shell: bash
- Command:
  - source ~/.bashrc
  - echo $ROS_DISTRO
  - which ros2
  - ls /opt/ros
  - ros2 node list
  - ros2 node info /turtlesim
- Topics:
  - /turtle1/cmd_vel
  - /turtle1/pose
  - /turtle1/color_sensor
- Result:
  - ROS_DISTRO가 humble로 출력되는 것을 확인했다.
  - ros2 명령어 경로가 /opt/ros/humble/bin/ros2로 잡힌 것을 확인했다.
  - turtlesim 노드를 통해 ROS2 node, topic, service 구조가 정상 동작하는 것을 확인했다.
- Success: Yes
- Failure Type: None
- Notes:
  - ros2 --version은 Humble 환경에서 지원되지 않을 수 있으므로 echo $ROS_DISTRO, which ros2, ls /opt/ros를 기준 확인 명령으로 사용한다.
  - .bashrc에서 ROS2 Humble 자동 활성화 메시지가 중복 출력되던 문제를 정리했다.
- Related Files:
  - notes/troubleshooting.md

---

### P00-EXP-0004_turtlebot3_gazebo_environment_check

- Date: 2026-05-25
- Phase: Phase 0.5 Environment setup
- Goal: Gazebo에서 TurtleBot3 Burger를 실행하고 teleop, odom, scan, cmd_vel 연결을 확인한다.
- Environment:
  - Guest OS: Ubuntu 22.04
  - ROS2: Humble Hawksbill
  - Simulator: Gazebo Classic 11.10.2
  - Robot: TurtleBot3 Burger
  - Remote GUI: NoMachine
- Command:
  - source ~/.bashrc
  - export TURTLEBOT3_MODEL=burger
  - ros2 launch turtlebot3_gazebo empty_world.launch.py
  - ros2 run turtlebot3_teleop teleop_keyboard
  - ros2 topic list
  - ros2 topic echo /odom --once
  - ros2 topic hz /scan
  - ros2 topic info /cmd_vel -v
- Topics:
  - /cmd_vel
  - /odom
  - /scan
  - /tf
  - /tf_static
  - /clock
  - /imu
  - /joint_states
  - /robot_description
- Result:
  - Gazebo에서 TurtleBot3 Burger가 spawn되는 것을 확인했다.
  - teleop_keyboard 입력이 /cmd_vel로 publish되는 것을 확인했다.
  - turtlebot3_diff_drive가 /cmd_vel을 subscribe하는 것을 확인했다.
  - /odom 데이터가 출력되는 것을 확인했다.
  - /scan 데이터가 약 5Hz로 publish되는 것을 확인했다.
  - Gazebo 화면에서 LiDAR ray 때문에 로봇 외형이 잘 안 보였지만, 확대 후 바퀴 두 개가 달린 TurtleBot3 Burger 본체를 확인했고 teleop으로 실제 이동하는 것을 확인했다.
- Success: Yes
- Failure Type: None
- Notes:
  - Gazebo 화면에서 파란 부채꼴 형태로 보이는 것은 LiDAR scan/ray 시각화로 보인다.
  - TurtleBot3 본체는 작게 보이므로 Gazebo에서 확대하거나 시점을 조정해야 한다.
  - /cmd_vel 연결 결과:
    - Publisher: teleop_keyboard
    - Subscriber: turtlebot3_diff_drive
  - /scan은 ros2 topic hz /scan 기준 약 4.95Hz로 확인했다.
  - TurtleBot3 mesh가 보이지 않던 문제는 GAZEBO_MODEL_PATH에 TurtleBot3 model 경로를 추가해 해결했다.
- Related Files:
  - notes/troubleshooting.md
  - results/screenshots/
  - results/videos/

---

### P00-EXP-0005_gazebo_mesh_path_fix

- Date: 2026-05-25
- Phase: Phase 0.5 Environment setup
- Goal: Gazebo가 TurtleBot3 mesh 파일을 찾지 못해 로봇 외형이 보이지 않는 문제를 해결한다.
- Environment:
  - Guest OS: Ubuntu 22.04
  - ROS2: Humble Hawksbill
  - Simulator: Gazebo Classic 11.10.2
  - Robot: TurtleBot3 Burger
- Command:
  - find ~/turtlebot3_ws -name burger_base.stl
  - find ~/turtlebot3_ws -name lds.stl
  - find ~/turtlebot3_ws -name left_tire.stl
  - export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:$HOME/turtlebot3_ws/install/turtlebot3_gazebo/share/turtlebot3_gazebo/models
  - export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:$HOME/turtlebot3_ws/src/turtlebot3_simulations/turtlebot3_gazebo/models
  - echo $GAZEBO_MODEL_PATH
- Topics:
  - 없음
- Result:
  - TurtleBot3 mesh 파일들이 실제로 존재하는 것을 확인했다.
  - Gazebo가 model://turtlebot3_common 경로를 찾지 못하던 문제를 GAZEBO_MODEL_PATH 설정으로 해결했다.
  - 이후 Gazebo에서 TurtleBot3 Burger 외형을 확인할 수 있었다.
- Success: Yes
- Failure Type: mesh_path_missing
- Notes:
  - Gazebo는 model:// 경로를 해석할 때 GAZEBO_MODEL_PATH를 사용한다.
  - TurtleBot3 simulation 패키지를 source build한 경우, install 경로와 src 경로를 GAZEBO_MODEL_PATH에 추가해야 할 수 있다.
  - 이 설정은 이후 .bashrc에 영구 등록할 예정이다.
- Related Files:
  - notes/troubleshooting.md

---

---

### P01-EXP-0001_ros2_basic_pubsub_service_launch

- Date: 2026-05-25
- Phase: Phase 1. ROS2 basics
- Goal: ROS2 Python 패키지를 생성하고, turtlesim 기반으로 publisher, subscriber, service, launch의 기본 구조를 실습한다.
- Environment:
  - OS: Ubuntu 22.04 LTS
  - ROS2: Humble Hawksbill
  - Simulator: turtlesim
  - Project path: ~/projects/missionbot-ros2
  - Package: missionbot_basic
- Command:
  - ros2 pkg create missionbot_basic --build-type ament_python --dependencies rclpy turtlesim
  - colcon build --packages-select missionbot_basic
  - source install/setup.bash
  - ros2 run turtlesim turtlesim_node
  - ros2 run missionbot_basic pose_subscriber
  - ros2 run missionbot_basic velocity_publisher
  - ros2 service call /clear std_srvs/srv/Empty
  - ros2 service call /spawn turtlesim/srv/Spawn "{x: 2.0, y: 2.0, theta: 0.0, name: 'mission_turtle'}"
  - ros2 launch missionbot_basic turtlesim_pubsub.launch.py
  - rqt_graph
- Topics:
  - /turtle1/pose
  - /turtle1/cmd_vel
- Services:
  - /clear
  - /spawn
- Result:
  - pose_subscriber가 /turtle1/pose를 정상 구독했다.
  - velocity_publisher가 /turtle1/cmd_vel로 Twist 메시지를 정상 publish했다.
  - turtlesim 거북이가 velocity_publisher의 속도 명령에 따라 움직였다.
  - /clear service 호출로 turtlesim 화면의 선을 지웠다.
  - /spawn service 호출로 새 거북이를 생성했다.
  - launch 파일로 turtlesim_node, pose_subscriber, velocity_publisher를 한 번에 실행했다.
  - rqt_graph로 publisher-topic-subscriber 연결을 확인했다.
- Success: Yes
- Failure Type:
  - None for final result
- Notes:
  - colcon build 후 source install/setup.bash를 해야 missionbot_basic 패키지를 현재 터미널이 인식한다.
  - topic은 계속 흐르는 데이터 구조이고, service는 짧은 요청-응답 구조다.
  - launch는 여러 node를 한 번에 실행하는 실행 관리 구조다.
  - Phase 2의 Gazebo + TurtleBot3에서도 /cmd_vel, /odom, /scan topic 구조를 같은 방식으로 확인할 수 있다.
- Related Files:
  - src/missionbot_basic/missionbot_basic/pose_subscriber.py
  - src/missionbot_basic/missionbot_basic/velocity_publisher.py
  - src/missionbot_basic/launch/turtlesim_pubsub.launch.py
  - src/missionbot_basic/setup.py
  - src/missionbot_basic/package.xml
  - notes/daily_logs/2026-05-25_phase1_ros2_basics.md