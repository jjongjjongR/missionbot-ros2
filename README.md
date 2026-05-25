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
- [ ] Phase 0. Project setup
- [ ] Phase 1. ROS2 basics
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
missionbot-ros2/
├── README.md
├── docs/   (공부 + 구현 내용 정리)
├── src/   (코드)
├── configs/  (설정 파일)
├── maps/  (SLAM으로 만든 맵)
├── rosbags/  (센서와 주행 로그)
├── results/  (결과물)
└── notes/   (개인 학습 기록, 문제 해결 기록)

### Result

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