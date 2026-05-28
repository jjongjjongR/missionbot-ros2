# 2026-05-25 Phase 1 ROS2 Basics Daily Log

## 1. 현재 Phase

Phase 1. ROS2 basics

## 2. 오늘의 목표

MissionBot-ROS2 프로젝트의 첫 ROS2 패키지인 `missionbot_basic`을 생성하고, ROS2의 기본 통신 구조인 node, topic, publisher, subscriber, service, launch를 turtlesim 기반으로 직접 실습한다.

이번 Phase의 목적은 Gazebo와 TurtleBot3로 바로 넘어가기 전에, ROS2 시스템이 어떤 방식으로 노드들을 실행하고 topic을 주고받는지 작은 예제로 이해하는 것이다.

## 3. 오늘 만든 기능

### 3.1 missionbot_basic 패키지 생성

`src/missionbot_basic` 위치에 Python 기반 ROS2 패키지를 생성했다.

사용한 명령어:

- cd ~/projects/missionbot-ros2/src
- ros2 pkg create missionbot_basic --build-type ament_python --dependencies rclpy turtlesim

생성된 핵심 구조:

- src/missionbot_basic/package.xml
- src/missionbot_basic/setup.py
- src/missionbot_basic/setup.cfg
- src/missionbot_basic/resource/missionbot_basic
- src/missionbot_basic/missionbot_basic/__init__.py

## 4. 오늘 작성한 파일

### 4.1 pose_subscriber.py

작성 위치:

- src/missionbot_basic/missionbot_basic/pose_subscriber.py

역할:

- turtlesim이 publish하는 `/turtle1/pose` topic을 구독한다.
- 메시지 타입은 `turtlesim/msg/Pose`를 사용한다.
- callback 함수에서 `x`, `y`, `theta` 값을 로그로 출력한다.

핵심 개념:

- subscriber는 topic 데이터를 받는 기능이다.
- callback은 메시지가 들어왔을 때 자동으로 실행되는 함수다.
- message type과 topic 이름이 맞아야 subscriber가 정상 연결된다.
- `rclpy.spin(node)`은 노드가 계속 메시지를 기다리도록 유지한다.

## 5. pose_subscriber 실행 등록

수정한 파일:

- src/missionbot_basic/setup.py

추가한 entry point:

- pose_subscriber = missionbot_basic.pose_subscriber:main

의미:

- `ros2 run missionbot_basic pose_subscriber` 명령으로 `pose_subscriber.py` 안의 `main()` 함수를 실행할 수 있게 등록했다.

사용한 명령어:

- cd ~/projects/missionbot-ros2
- colcon build --packages-select missionbot_basic
- source install/setup.bash
- ros2 run missionbot_basic pose_subscriber

확인한 것:

- `/pose_subscriber` node 실행 확인
- `/turtle1/pose` topic 구독 확인
- `ros2 topic info /turtle1/pose`에서 Subscription count가 1로 표시됨

## 6. rqt_graph 확인

실행한 명령어:

- rqt_graph

확인한 구조:

- /turtlesim → /turtle1/pose → /pose_subscriber

배운 점:

- ROS graph는 현재 실행 중인 node와 topic의 연결 관계를 보여준다.
- rqt_graph는 ROS graph를 GUI로 확인하는 도구다.
- topic 연결이 보이면 publisher와 subscriber가 정상적으로 연결된 것이다.

MissionBot에서의 의미:

- 나중에 Gazebo TurtleBot3, `/cmd_vel`, `/odom`, `/scan`, `sensor_logger` 연결 상태를 확인할 때 rqt_graph를 사용한다.

## 7. velocity_publisher.py 작성

작성 위치:

- src/missionbot_basic/missionbot_basic/velocity_publisher.py

역할:

- `/turtle1/cmd_vel` topic으로 `geometry_msgs/msg/Twist` 메시지를 publish한다.
- 0.5초마다 속도 명령을 보내 turtlesim 거북이를 움직인다.

핵심 개념:

- publisher는 topic으로 데이터를 보내는 기능이다.
- Twist는 ROS2에서 속도 명령을 표현하는 표준 메시지 타입이다.
- `linear.x`는 전진 속도다.
- `angular.z`는 회전 속도다.
- `create_timer()`는 일정 주기마다 callback 함수를 실행한다.
- `publish()`는 완성된 메시지를 topic으로 발행한다.

문법 확인 명령어:

- cd ~/projects/missionbot-ros2/src/missionbot_basic/missionbot_basic
- python3 -m py_compile velocity_publisher.py

## 8. velocity_publisher 실행 등록

수정한 파일:

- src/missionbot_basic/setup.py

추가한 entry point:

- velocity_publisher = missionbot_basic.velocity_publisher:main

사용한 명령어:

- cd ~/projects/missionbot-ros2
- colcon build --packages-select missionbot_basic
- source install/setup.bash
- ros2 pkg executables missionbot_basic

확인한 실행 노드:

- missionbot_basic pose_subscriber
- missionbot_basic velocity_publisher

## 9. velocity_publisher 실행 확인

실행한 명령어:

- ros2 run turtlesim turtlesim_node
- cd ~/projects/missionbot-ros2
- source install/setup.bash
- ros2 run missionbot_basic velocity_publisher
- ros2 topic info /turtle1/cmd_vel
- ros2 topic echo /turtle1/cmd_vel --once
- rqt_graph

확인한 것:

- `/velocity_publisher` node 실행
- `/turtle1/cmd_vel` topic에 Twist 메시지 publish
- turtlesim 거북이 이동 확인
- `/turtle1/cmd_vel`에서 Publisher count 1, Subscription count 1 확인
- rqt_graph에서 `/velocity_publisher → /turtle1/cmd_vel → /turtlesim` 구조 확인

## 10. Service 기초 확인

사용한 turtlesim service:

- /clear
- /spawn

실행한 명령어:

- ros2 service list
- ros2 service type /clear
- ros2 service call /clear std_srvs/srv/Empty
- ros2 service type /spawn
- ros2 interface show turtlesim/srv/Spawn
- ros2 service call /spawn turtlesim/srv/Spawn "{x: 2.0, y: 2.0, theta: 0.0, name: 'mission_turtle'}"

배운 개념:

- service는 짧은 요청-응답 구조다.
- topic은 계속 흐르는 데이터이고, service는 필요할 때 한 번 호출한다.
- service type에서 `srv`는 service 인터페이스를 의미한다.
- `ros2 interface show` 명령으로 request와 response 구조를 확인할 수 있다.
- service 인터페이스에서 `---` 위는 request, 아래는 response다.

MissionBot에서의 의미:

- service는 나중에 실험 초기화, 지도 저장, 로깅 시작/종료처럼 한 번 요청하고 결과를 받는 기능에 활용할 수 있다.

## 11. Launch 기초 확인

작성한 파일:

- src/missionbot_basic/launch/turtlesim_pubsub.launch.py

수정한 파일:

- src/missionbot_basic/package.xml
- src/missionbot_basic/setup.py

launch 파일 역할:

- turtlesim_node, pose_subscriber, velocity_publisher를 한 번에 실행한다.

실행한 명령어:

- cd ~/projects/missionbot-ros2
- colcon build --packages-select missionbot_basic
- source install/setup.bash
- ros2 launch missionbot_basic turtlesim_pubsub.launch.py

확인한 노드:

- /turtlesim
- /pose_subscriber
- /velocity_publisher

확인한 topic:

- /turtle1/pose
- /turtle1/cmd_vel

확인한 구조:

- /velocity_publisher → /turtle1/cmd_vel → /turtlesim
- /turtlesim → /turtle1/pose → /pose_subscriber

배운 개념:

- launch는 여러 ROS2 node를 한 번에 실행하기 위한 실행 묶음이다.
- `ros2 run`은 노드 하나를 실행한다.
- `ros2 launch`는 launch 파일에 정의된 여러 노드를 실행한다.
- `LaunchDescription`은 launch 파일이 실행할 작업 목록을 담는다.
- `launch_ros.actions.Node`는 launch 파일 안에서 ROS2 node 실행 항목을 정의한다.
- `setup.py`의 `data_files`에 launch 파일을 포함해야 `ros2 launch`가 해당 파일을 찾을 수 있다.

## 12. 오늘 배운 핵심 개념 정리

### node

ROS2에서 실행되는 하나의 기능 단위다.

이번 Phase에서 확인한 node:

- /turtlesim
- /pose_subscriber
- /velocity_publisher

### topic

계속 흐르는 데이터 통로다.

이번 Phase에서 확인한 topic:

- /turtle1/pose
- /turtle1/cmd_vel

### publisher

topic으로 데이터를 보내는 쪽이다.

이번 Phase의 publisher:

- /turtlesim은 /turtle1/pose를 publish한다.
- /velocity_publisher는 /turtle1/cmd_vel을 publish한다.

### subscriber

topic 데이터를 받는 쪽이다.

이번 Phase의 subscriber:

- /pose_subscriber는 /turtle1/pose를 subscribe한다.
- /turtlesim은 /turtle1/cmd_vel을 subscribe한다.

### callback

메시지가 들어오거나 timer가 동작했을 때 자동으로 실행되는 함수다.

이번 Phase에서 사용한 callback:

- pose_callback
- publish_velocity

### service

필요할 때 한 번 요청하고 응답받는 구조다.

이번 Phase에서 확인한 service:

- /clear
- /spawn

### launch

여러 node를 한 번에 실행하는 구조다.

이번 Phase에서 작성한 launch 파일:

- turtlesim_pubsub.launch.py

## 13. 성공한 것

- missionbot_basic ROS2 Python 패키지 생성
- pose_subscriber 노드 작성
- velocity_publisher 노드 작성
- setup.py entry_points 등록
- colcon build 성공
- source install/setup.bash 적용
- ros2 run으로 직접 만든 노드 실행
- rqt_graph로 node-topic 연결 확인
- turtlesim service 호출 확인
- launch 파일로 여러 노드 동시 실행 확인

## 14. 막힌 것

### 문제

`ros2 launch missionbot_basic turtlesim_pubsub.launch.py` 실행 시 다음 오류가 발생했다.

- Package 'missionbot_basic' not found

### 원인

현재 터미널에 MissionBot workspace의 `install/setup.bash`가 source되지 않아, ROS2가 `missionbot_basic` 패키지를 찾지 못했다.

### 해결

다음 명령어로 해결했다.

- cd ~/projects/missionbot-ros2
- source install/setup.bash
- ros2 launch missionbot_basic turtlesim_pubsub.launch.py

## 15. MissionBot에서의 의미

이번 Phase 1은 MissionBot-ROS2의 가장 작은 ROS2 실행 구조를 이해하는 단계였다.

turtlesim은 실제 프로젝트 대상은 아니지만, ROS2의 기본 통신 구조를 작고 안전하게 실습하기 위한 도구다.

이번에 배운 구조는 Phase 2 이후 다음과 같이 연결된다.

- /turtle1/pose 구독 → 나중에 TurtleBot3 /odom 구독
- /turtle1/cmd_vel publish → 나중에 TurtleBot3 /cmd_vel publish
- rqt_graph 확인 → 나중에 Gazebo, RViz2, sensor_logger 연결 확인
- service 호출 → 나중에 실험 초기화, 지도 저장, 로깅 제어
- launch 파일 작성 → 나중에 Gazebo, TurtleBot3, RViz2, SLAM, Nav2 동시 실행

## 16. 다음에 할 일

Phase 2. Gazebo + TurtleBot3 단계로 넘어간다.

다음 Phase에서는 turtlesim이 아니라 Gazebo 환경의 TurtleBot3 Burger를 대상으로 다음을 확인한다.

- TurtleBot3 Gazebo 실행
- /cmd_vel 명령 구조 확인
- /odom topic 확인
- /scan topic 확인
- rqt_graph로 TurtleBot3 node-topic 구조 확인
- teleop과 Gazebo plugin 연결 확인