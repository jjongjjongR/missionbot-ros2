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

## TS-0002_turtlebot3_model_not_found

### 1. 발생 날짜

- Date:

### 2. 발생 단계

- Phase: Phase 2. Gazebo + TurtleBot3
- 작업 내용: TurtleBot3 Gazebo 실행

### 3. 오류 상황

오류 메시지:

    TurtleBot3 model is not selected

### 4. 사용 환경

- OS:
- ROS2 version:
- Gazebo version:
- Python version:
- TurtleBot3 model:

### 5. 원인 추정

- TurtleBot3 모델 환경변수가 설정되지 않은 것으로 추정

### 6. 해결 방법

사용한 명령어:

    export TURTLEBOT3_MODEL=burger

### 7. 해결 결과

- TurtleBot3 Gazebo 실행 성공 여부 기록

### 8. 배운 점

- TurtleBot3 실행 전에는 TURTLEBOT3_MODEL 환경변수가 필요하다.

### 9. 다시 발생하지 않도록 주의할 점

- 자주 사용하는 모델이면 .bashrc 또는 zsh 설정 파일에 환경변수를 추가할 수 있다.