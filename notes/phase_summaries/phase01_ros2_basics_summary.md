# Phase 1 Summary. ROS2 Basics

## 1. Phase 상태

- Phase: Phase 1. ROS2 basics
- Status: 완료
- Date: 2026-05-25
- Main package: missionbot_basic

## 2. Phase 목표

Phase 1의 목표는 MissionBot-ROS2 프로젝트에서 사용할 ROS2 기본 구조를 turtlesim 기반으로 직접 실습하는 것이다.

이번 Phase에서는 실제 Gazebo TurtleBot3로 바로 들어가기 전에, 작은 예제 환경에서 다음 개념을 먼저 확인했다.

- node
- topic
- publisher
- subscriber
- callback
- timer
- message type
- service
- launch
- colcon build
- workspace source
- rqt_graph

## 3. 완료한 작업

### 3.1 missionbot_basic 패키지 생성

생성 위치:

- src/missionbot_basic

생성 명령:

    ros2 pkg create missionbot_basic --build-type ament_python --dependencies rclpy turtlesim

패키지 역할:

- ROS2 기본 노드 실습
- turtlesim 기반 publisher/subscriber 실습
- service 호출 실습
- launch 파일 실습

### 3.2 pose_subscriber 작성

파일 위치:

- src/missionbot_basic/missionbot_basic/pose_subscriber.py

역할:

- `/turtle1/pose` topic 구독
- 메시지 타입: turtlesim/msg/Pose
- 수신한 x, y, theta 값 로그 출력

확인한 구조:

- /turtlesim → /turtle1/pose → /pose_subscriber

### 3.3 velocity_publisher 작성

파일 위치:

- src/missionbot_basic/missionbot_basic/velocity_publisher.py

역할:

- `/turtle1/cmd_vel` topic으로 속도 명령 publish
- 메시지 타입: geometry_msgs/msg/Twist
- 0.5초마다 linear.x, angular.z 속도 명령 발행

확인한 구조:

- /velocity_publisher → /turtle1/cmd_vel → /turtlesim

### 3.4 setup.py entry_points 등록

등록한 실행 명령:

- pose_subscriber = missionbot_basic.pose_subscriber:main
- velocity_publisher = missionbot_basic.velocity_publisher:main

확인 명령:

    ros2 pkg executables missionbot_basic

확인 결과:

- missionbot_basic pose_subscriber
- missionbot_basic velocity_publisher

### 3.5 service 기초 확인

확인한 service:

- /clear
- /spawn

사용한 명령:

    ros2 service list
    ros2 service type /clear
    ros2 service call /clear std_srvs/srv/Empty
    ros2 service type /spawn
    ros2 interface show turtlesim/srv/Spawn
    ros2 service call /spawn turtlesim/srv/Spawn "{x: 2.0, y: 2.0, theta: 0.0, name: 'mission_turtle'}"

배운 점:

- topic은 계속 흐르는 데이터다.
- service는 필요할 때 한 번 요청하고 응답받는 구조다.
- service interface에서 `---` 위는 request, 아래는 response다.

### 3.6 launch 파일 작성

작성 파일:

- src/missionbot_basic/launch/turtlesim_pubsub.launch.py

역할:

- turtlesim_node 실행
- pose_subscriber 실행
- velocity_publisher 실행

실행 명령:

    ros2 launch missionbot_basic turtlesim_pubsub.launch.py

확인한 node:

- /turtlesim
- /pose_subscriber
- /velocity_publisher

확인한 topic:

- /turtle1/pose
- /turtle1/cmd_vel

## 4. 최종 성공 기준

Phase 1은 다음 기준을 만족했으므로 완료로 판단한다.

- missionbot_basic 패키지 생성 완료
- pose_subscriber 노드 작성 및 실행 성공
- velocity_publisher 노드 작성 및 실행 성공
- /turtle1/pose topic 연결 확인
- /turtle1/cmd_vel topic 연결 확인
- turtlesim service 호출 성공
- launch 파일 실행 성공
- rqt_graph로 전체 pub/sub 구조 확인
- Package not found 오류 해결 및 troubleshooting 기록

## 5. 발생한 주요 오류

### Package 'missionbot_basic' not found

상황:

- `ros2 launch missionbot_basic turtlesim_pubsub.launch.py` 실행 시 발생

원인:

- 현재 터미널에 MissionBot workspace의 `install/setup.bash`가 source되지 않음

해결:

    cd ~/projects/missionbot-ros2
    source install/setup.bash
    ros2 launch missionbot_basic turtlesim_pubsub.launch.py

기록 위치:

- notes/troubleshooting.md
- TS-0003_missionbot_basic_package_not_found

## 6. Phase 1에서 배운 핵심

### node

ROS2에서 실행되는 기능 단위다.

### topic

계속 흐르는 데이터 통로다.

### publisher

topic으로 메시지를 보내는 쪽이다.

### subscriber

topic 메시지를 받는 쪽이다.

### callback

메시지가 들어오거나 timer가 동작했을 때 자동으로 실행되는 함수다.

### service

짧은 요청-응답 구조다.

### launch

여러 node를 한 번에 실행하는 구조다.

### source install/setup.bash

현재 workspace에서 빌드한 패키지를 현재 터미널이 인식하도록 만드는 과정이다.

## 7. Phase 2로 넘어가기 위한 상태

현재 상태:

- ROS2 Humble 정상
- MissionBot 프로젝트 workspace 빌드 가능
- missionbot_basic 패키지 실행 가능
- turtlesim 기반 pub/sub/service/launch 실습 완료
- Phase 2 진입 가능

Phase 2 시작 전 확인할 것:

    cd ~/projects/missionbot-ros2
    source install/setup.bash
    ros2 pkg list | grep missionbot_basic

## 8. 다음 Phase

다음 Phase:

- Phase 2. Gazebo + TurtleBot3

다음 Phase에서 확인할 것:

- TurtleBot3 Gazebo 실행
- /cmd_vel topic 확인
- /odom topic 확인
- /scan topic 확인
- teleop_keyboard와 turtlebot3_diff_drive 연결 확인
- rqt_graph로 Gazebo TurtleBot3 ROS graph 확인

## 9. MissionBot에서의 의미

Phase 1은 MissionBot-ROS2의 가장 작은 ROS2 실행 구조를 이해하는 단계였다.

이번에 배운 구조는 Phase 2 이후 다음과 같이 연결된다.

- /turtle1/pose 구독 → TurtleBot3 /odom 구독
- /turtle1/cmd_vel publish → TurtleBot3 /cmd_vel publish
- rqt_graph 확인 → Gazebo TurtleBot3 graph 확인
- service 호출 → 실험 초기화, 지도 저장, 로깅 제어
- launch 파일 → Gazebo, RViz2, SLAM, Navigation2 실행 관리