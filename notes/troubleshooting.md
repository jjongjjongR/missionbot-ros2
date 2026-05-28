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