# MissionBot-ROS2

### 개요
ROS2와 Gazebo 기반으로 TurtleBot3 주행, SLAM/Nav2, rosbag2 로그 분석, MoveIt2 조작 모듈, LLM/VLM 미션 이해를 연결하는 모바일 매니퓰레이션 시스템 프로젝트

#### motivation
- 매니퓰레이션을 하고 싶지만, 실제 로봇 작업은 로봇팔만으로 끝나지 않는다.
이동, 지도, 위치 추정, 센서, 제어, 실패 분석이 함께 필요하다.
그래서 ROS2 기반 이동로봇 시스템부터 단계적으로 이해한다.

#### project scope
- 포함: ROS2 기본 구조, Gazebo TurtleBot3 실행, TF2 & RViz2 확인, SLAM, Navigation2, rosbag2 logging, 실패 분석, MoveIt2 기초, LLM/VLM 미션 이해
- 제외: 대형 VLA 학습, 실제 로봇 하드웨어 제어, 복잡한 로봇팔 강화학습, 실물 로봇 기반 완전한 모바일 매니퓰레이션 구현

### 기술 스택
| Robotics System | Python, C++, ROS2, Gazebo, TurtleBot3, RViz2, TF2, rosbag2, URDF, Xacro |
| --- | --- |
| Navigation & Manipulation | SLAM Toolbox, Navigation2, MoveIt2, ros2_control, MuJoCo |
| AI & Analysis | OpenCV, YOLO, OpenAI API, Qwen2.5-VL(예정), Pandas, Matplotlib |

### Phase map
- [x] Phase 0. Project setup
- [x] Phase 1. ROS2 basics
- [ ] Phase 2. Gazebo + TurtleBot3
- [ ] Phase 3. RViz2 + TF2
- [ ] Phase 4. SLAM
- [ ] Phase 5. Navigation2
- [ ] Phase 6. rosbag2 logging
- [ ] Phase 7. Failure analysis
- [ ] Phase 8. Control basics
- [ ] Phase 9. MoveIt2 basics
- [ ] Phase 10. LLM/VLM extension

### 파일 구조

```text
missionbot-ros2/
├── docs/   (공부 + 구현 내용 정리)
│   ├── 학습용/   (llm 학습용 프롬프트)
│   ├── phases/   (Phase별 진행 정리)
│   ├── concepts/   (ROS2 핵심 개념 정리)
│   ├── templates/   (기록 양식 모음)
│   └── handoffs/   (새 채팅 인수인계 문서)
│
├── src/   (직접 작성할 ROS2 패키지)
│   ├── missionbot_basic/   (ROS2 기본 노드 실습)
│   ├── sensor_logger/   (센서·주행 토픽 기록)
│   ├── failure_analyzer/   (실패 원인 분석 코드)
│   ├── mission_parser/   (LLM 미션 해석)
│   └── vision_object_selector/   (VLM·YOLO 객체 선택)
│
├── configs/   (설정 파일)
│   ├── gazebo/   (Gazebo 실행 설정)
│   ├── rviz/   (RViz2 화면 설정)
│   ├── robot/   (로봇 모델 설정)
│   ├── slam_toolbox/   (SLAM 설정)
│   ├── nav2/   (Navigation2 설정)
│   ├── rosbag2/   (rosbag 기록 설정)
│   ├── moveit2/   (MoveIt2 설정)
│   └── ai/   (LLM·VLM 설정)
│
├── maps/   (SLAM으로 만든 맵)
│   ├── phase04_slam/   (SLAM 실험 맵)
│   └── test_maps/   (테스트용 맵)
│
├── rosbags/   (센서와 주행 로그)
│   ├── phase02_gazebo_turtlebot3/   (Gazebo 주행 로그)
│   ├── phase04_slam/   (SLAM 로그)
│   ├── phase05_navigation2/   (Nav2 주행 로그)
│   ├── phase06_logging/   (rosbag 기록 실험)
│   └── failure_cases/   (실패 상황 rosbag)
│
├── results/   (결과물)
│   ├── screenshots/   (화면 캡처)
│   │   ├── gazebo/   (Gazebo 캡처)
│   │   ├── rviz/   (RViz2 캡처)
│   │   ├── tf_tree/   (TF tree 캡처)
│   │   └── errors/   (오류 화면 캡처)
│   │
│   ├── videos/   (실행 영상)
│   │   ├── demos/   (성공 데모 영상)
│   │   └── failures/   (실패 상황 영상)
│   │
│   ├── logs/   (실행 로그)
│   │   ├── terminal/   (터미널 출력)
│   │   ├── launch/   (launch 실행 로그)
│   │   └── analysis/   (분석 결과 로그)
│   │
│   ├── metrics/   (실험 수치 결과)
│   └── failure_cases/   (실패 사례 정리)
│
└── notes/   (개인 학습 기록, 문제 해결 기록)
    ├── daily_logs/   (일일 진행 기록)
    ├── phase_summaries/   (Phase 종료 요약)
    └── handoff_notes/   (이어가기용 요약)
```

### Result
#### Phase 1. ROS2 basics 완료

Phase 1에서는 `missionbot_basic` 패키지를 생성하고, turtlesim 기반으로 ROS2의 기본 구조를 실습했다.

완료한 내용:

- ROS2 Python 패키지 `missionbot_basic` 생성
- `/turtle1/pose`를 구독하는 `pose_subscriber` 노드 작성
- `/turtle1/cmd_vel`로 속도 명령을 보내는 `velocity_publisher` 노드 작성
- `setup.py`의 `entry_points`에 실행 노드 등록
- `colcon build` 및 `source install/setup.bash` 흐름 확인
- `ros2 run`으로 직접 작성한 노드 실행
- `rqt_graph`로 node-topic 연결 구조 확인
- turtlesim의 `/clear`, `/spawn` service 호출
- `turtlesim_pubsub.launch.py` launch 파일 작성
- `ros2 launch`로 turtlesim, subscriber, publisher 노드 동시 실행

확인한 핵심 구조:

- `/turtlesim` → `/turtle1/pose` → `/pose_subscriber`
- `/velocity_publisher` → `/turtle1/cmd_vel` → `/turtlesim`

다음 Phase에서는 Gazebo와 TurtleBot3를 대상으로 `/cmd_vel`, `/odom`, `/scan` topic 구조를 확인한다.



---

### Failure Analysis
- 이 프로젝트는 성공적인 주행 결과뿐만 아니라 위치 추정 실패, 장애물 차단, 경로 계획 실패, 제어 진동, 시간 초과와 같은 실패 사례도 기록합니다.

### Future Direction
Mobile Robot Foundation
→ Manipulation Basics
→ Mobile Manipulation
→ LLM/VLM-guided Mission Understanding


### 실험 기록 방식

이 프로젝트는 성공 결과뿐만 아니라 실행 과정, 센서 로그, 실패 원인, 수정 시도를 함께 기록한다.  
실험 기록은 README에 직접 누적하지 않고, 아래 위치에 분리해서 관리한다.

| 위치 | 역할 |
|---|---|
| `notes/experiment_log.md` | 전체 실험 인덱스 |
| `notes/troubleshooting.md` | 설치, 실행, 설정 오류와 해결 과정 |
| `results/screenshots/` | RViz2, Gazebo, TF tree 등 화면 캡처 |
| `results/videos/` | 주행, 실패 상황, 데모 영상 |
| `results/logs/` | 터미널 출력, 실행 로그 |
| `results/failure_cases/` | 실패 사례별 원인 분석 문서 |
| `rosbags/` | rosbag2로 저장한 센서 및 주행 로그 |

#### 실험 ID 규칙

실험은 Phase 번호와 실험 번호를 함께 사용한다.

```text
P02-EXP-0001_turtlebot3_gazebo_launch
P03-EXP-0001_rviz2_tf_tree_check
P05-EXP-0001_nav2_goal_success
P05-FAIL-0001_goal_unreachable

기본 기록 토픽
/scan
/odom
/tf
/tf_static
/cmd_vel
/map
+ (카메라, 객체 탐지 시)
/image_raw
/camera_info
/detection_result
```