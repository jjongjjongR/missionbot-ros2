# Phase 1. ROS2 Basics

## 1. 목적

이 문서는 MissionBot-ROS2 Phase 1에서 학습한 ROS2 기본 개념과 구현 패턴을 정리한다.

Phase 1의 목적은 turtlesim을 사용해 ROS2의 가장 기본적인 실행 구조를 직접 확인하는 것이다.

이 Phase는 다음 Phase인 Gazebo + TurtleBot3 실습으로 넘어가기 전, ROS2 시스템이 어떻게 node를 실행하고 topic, service, launch를 통해 구성되는지 이해하기 위한 기초 단계다.

## 2. 핵심 학습 흐름

Phase 1은 다음 흐름으로 진행했다.

1. ROS2 Python 패키지 생성
2. turtlesim 실행
3. topic 확인
4. subscriber 노드 작성
5. publisher 노드 작성
6. setup.py entry_points 등록
7. colcon build
8. source install/setup.bash
9. ros2 run으로 노드 실행
10. rqt_graph로 연결 확인
11. service 호출
12. launch 파일 작성
13. ros2 launch로 여러 노드 동시 실행

## 3. 패키지 구조

작성한 패키지:

- missionbot_basic

위치:

- src/missionbot_basic

주요 파일:

- src/missionbot_basic/package.xml
- src/missionbot_basic/setup.py
- src/missionbot_basic/missionbot_basic/pose_subscriber.py
- src/missionbot_basic/missionbot_basic/velocity_publisher.py
- src/missionbot_basic/launch/turtlesim_pubsub.launch.py

## 4. Node

node는 ROS2에서 실행되는 하나의 기능 단위다.

이번 Phase에서 실행한 node:

- /turtlesim
- /pose_subscriber
- /velocity_publisher

MissionBot에서의 의미:

- 나중에 sensor_logger, failure_analyzer, mission_parser, vision_object_selector도 각각 node 구조로 확장될 수 있다.

## 5. Topic

topic은 계속 흐르는 데이터 통로다.

이번 Phase에서 사용한 topic:

- /turtle1/pose
- /turtle1/cmd_vel

topic 구조:

- /turtlesim → /turtle1/pose → /pose_subscriber
- /velocity_publisher → /turtle1/cmd_vel → /turtlesim

MissionBot에서의 연결:

- /turtle1/pose → /odom
- /turtle1/cmd_vel → /cmd_vel

## 6. Subscriber

subscriber는 topic 데이터를 받는 기능이다.

작성 파일:

- pose_subscriber.py

구독 topic:

- /turtle1/pose

메시지 타입:

- turtlesim/msg/Pose

핵심 코드 구조:

- rclpy 초기화
- Node 상속
- create_subscription()으로 subscriber 생성
- callback 함수에서 메시지 처리
- rclpy.spin()으로 노드 유지

MissionBot에서의 연결:

- 나중에 /odom, /scan, /camera/image_raw 같은 topic을 구독하는 sensor_logger 구조의 기초가 된다.

## 7. Publisher

publisher는 topic으로 메시지를 보내는 기능이다.

작성 파일:

- velocity_publisher.py

publish topic:

- /turtle1/cmd_vel

메시지 타입:

- geometry_msgs/msg/Twist

핵심 코드 구조:

- rclpy 초기화
- Node 상속
- create_publisher()로 publisher 생성
- create_timer()로 주기적 callback 생성
- Twist 메시지 생성
- publish()로 메시지 발행

MissionBot에서의 연결:

- 나중에 TurtleBot3의 /cmd_vel로 속도 명령을 보내는 구조와 연결된다.

## 8. Service

service는 짧은 요청-응답 구조다.

이번 Phase에서 사용한 service:

- /clear
- /spawn

확인 명령:

    ros2 service list
    ros2 service type /clear
    ros2 service call /clear std_srvs/srv/Empty
    ros2 service type /spawn
    ros2 interface show turtlesim/srv/Spawn
    ros2 service call /spawn turtlesim/srv/Spawn "{x: 2.0, y: 2.0, theta: 0.0, name: 'mission_turtle'}"

topic과 service의 차이:

- topic은 계속 흐르는 데이터다.
- service는 필요할 때 한 번 요청하고 응답받는 구조다.

MissionBot에서의 연결:

- 실험 초기화
- 지도 저장
- rosbag 기록 시작
- rosbag 기록 종료
- 특정 분석 작업 요청

## 9. Launch

launch는 여러 ROS2 node를 한 번에 실행하는 구조다.

작성 파일:

- turtlesim_pubsub.launch.py

실행한 노드:

- turtlesim_node
- pose_subscriber
- velocity_publisher

실행 명령:

    ros2 launch missionbot_basic turtlesim_pubsub.launch.py

launch 파일의 핵심 구성:

- LaunchDescription
- launch_ros.actions.Node
- generate_launch_description()

MissionBot에서의 연결:

- Gazebo 실행
- TurtleBot3 spawn
- RViz2 실행
- SLAM Toolbox 실행
- Navigation2 실행
- sensor_logger 실행

복잡한 로봇 시스템에서는 launch 파일이 실행 관리의 중심이 된다.

## 10. Build와 Source

Python ROS2 패키지라도 파일만 작성해서는 ROS2가 바로 인식하지 못한다.

기본 흐름:

1. Python 노드 파일 작성
2. setup.py entry_points 등록
3. colcon build 실행
4. source install/setup.bash 실행
5. ros2 run 또는 ros2 launch 실행

사용 명령:

    cd ~/projects/missionbot-ros2
    colcon build --packages-select missionbot_basic
    source install/setup.bash

중요한 구분:

- source ~/.bashrc는 ROS2 기본 환경과 TurtleBot3 workspace를 적용한다.
- source install/setup.bash는 현재 MissionBot workspace에서 빌드한 패키지를 터미널에 인식시킨다.

## 11. rqt_graph

rqt_graph는 ROS2 graph를 시각적으로 확인하는 도구다.

확인한 구조:

- /turtlesim → /turtle1/pose → /pose_subscriber
- /velocity_publisher → /turtle1/cmd_vel → /turtlesim

MissionBot에서의 의미:

- 나중에 /cmd_vel, /odom, /scan, /tf, /sensor_logger 연결 상태를 확인할 때 사용한다.

## 12. Phase 1 완료 기준

다음 항목을 모두 완료했으므로 Phase 1을 완료로 판단한다.

- missionbot_basic 패키지 생성
- pose_subscriber 작성 및 실행
- velocity_publisher 작성 및 실행
- /turtle1/pose topic 연결 확인
- /turtle1/cmd_vel topic 연결 확인
- service 호출 확인
- launch 파일 작성 및 실행
- rqt_graph 연결 확인
- troubleshooting 기록
- experiment_log 기록
- phase summary 작성

## 13. 다음 Phase와 연결

Phase 2에서는 turtlesim이 아니라 Gazebo와 TurtleBot3를 대상으로 같은 구조를 확인한다.

Phase 1에서 배운 것:

- /turtle1/pose
- /turtle1/cmd_vel
- turtlesim_node
- rqt_graph
- launch

Phase 2에서 연결될 것:

- /odom
- /cmd_vel
- /scan
- turtlebot3_diff_drive
- Gazebo TurtleBot3
- RViz2와 TF2 준비

## 14. 결론

Phase 1은 MissionBot-ROS2 프로젝트의 ROS2 기본기를 잡는 단계였다.

이제 사용자는 ROS2 패키지를 만들고, 노드를 작성하고, topic을 주고받고, service를 호출하고, launch 파일로 여러 노드를 실행하는 전체 흐름을 한 번 경험했다.

이 흐름은 이후 모든 Phase에서 반복되는 기본 작업 패턴이다.