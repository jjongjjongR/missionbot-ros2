# MissionBot-ROS2 Project Overview

## 1. 프로젝트 개요

MissionBot-ROS2는 ROS2와 Gazebo를 기반으로 이동로봇 시스템을 구성하고, SLAM, Navigation2, rosbag2 기반 로그 분석, MoveIt2 조작 모듈, LLM/VLM 기반 미션 이해를 단계적으로 연결하는 모바일 매니퓰레이션 시스템 프로젝트입니다.

이 프로젝트는 처음부터 완전한 실물 모바일 매니퓰레이터를 구현하는 것이 아니라, 모바일 매니퓰레이션을 이해하기 위해 필요한 로봇 시스템 구성 요소를 단계적으로 구현하고 분석하는 것을 목표로 합니다.

---

## 2. 프로젝트 동기

매니퓰레이션은 단순히 로봇팔을 움직이는 문제만으로 끝나지 않습니다.

실제 로봇 작업에서는 다음 요소가 함께 필요합니다.

- 로봇이 목표 위치까지 이동하는 능력
- 주변 환경을 인식하는 센서 구조
- 지도 생성과 위치 추정
- 목표 지점까지의 경로 계획
- 센서와 제어 명령의 로그 기록
- 실패 상황 분석
- 로봇팔 조작 모듈과의 연결
- 자연어 명령을 로봇 미션으로 변환하는 상위 이해 모듈

따라서 이 프로젝트는 ROS2 기반 이동로봇 시스템에서 출발하여, 이후 조작과 AI 기반 미션 이해로 확장합니다.

---

## 3. 프로젝트 범위

### 3.1 포함하는 것

- ROS2 기본 구조 이해
- Gazebo 기반 TurtleBot3 실행
- RViz2와 TF2를 통한 센서 및 좌표계 확인
- SLAM Toolbox를 활용한 지도 생성
- Navigation2를 활용한 목표 지점 이동
- rosbag2를 활용한 센서 및 주행 로그 기록
- 실패 상황 분류 및 분석
- 제어 기초 개념 정리
- MoveIt2 기반 로봇팔 조작 기초 이해
- LLM 기반 Mission Parser 설계
- VLM 또는 Object Detection 기반 Object Selector 확장

### 3.2 포함하지 않는 것

- 대형 VLA 모델 직접 학습
- 실제 로봇 하드웨어 제어
- 복잡한 로봇팔 강화학습
- 실물 로봇 기반 완전한 모바일 매니퓰레이션 구현
- 저수준 제어기 직접 설계

---

## 4. 핵심 기술 스택

| 구분 | 기술 |
|---|---|
| Robotics System | Python, C++, ROS2, Gazebo, TurtleBot3, RViz2, TF2, rosbag2, URDF, Xacro |
| Navigation & Manipulation | SLAM Toolbox, Navigation2, MoveIt2, ros2_control |
| AI & Analysis | OpenCV, YOLO, OpenAI API, Qwen2.5-VL, Pandas, Matplotlib |

---

## 5. Phase Map

| Phase | 내용 | 핵심 결과물 |
|---|---|---|
| Phase 0 | 프로젝트 세팅 | README, 폴더 구조, 실험 기록 구조 |
| Phase 1 | ROS2 기본 구조 | publisher, subscriber, service, launch |
| Phase 2 | Gazebo + TurtleBot3 | TurtleBot3 시뮬레이션 실행 |
| Phase 3 | RViz2 + TF2 | 센서와 좌표계 확인 |
| Phase 4 | SLAM | 지도 생성 및 저장 |
| Phase 5 | Navigation2 | 목표 지점 이동 |
| Phase 6 | rosbag2 logging | 센서 및 주행 로그 저장 |
| Phase 7 | Failure Analysis | 실패 사례 분류 |
| Phase 8 | Control Basics | 제어 기초 개념 정리 |
| Phase 9 | MoveIt2 Basics | 로봇팔 조작 기초 이해 |
| Phase 10 | LLM/VLM Extension | 미션 이해와 객체 선택 구조 설계 |

---

## 6. 실패 분석 기준

이 프로젝트는 성공 결과뿐 아니라 실패 사례도 함께 기록합니다.

대표 실패 유형은 다음과 같습니다.

| 실패 유형 | 의미 |
|---|---|
| goal_unreachable | 목표 지점에 도달하지 못함 |
| obstacle_blocked | 장애물 때문에 경로가 막힘 |
| localization_failure | 위치 추정이 흔들리거나 틀어짐 |
| path_planning_failure | 경로 계획이 실패함 |
| control_oscillation | 로봇이 목표 근처에서 흔들리거나 진동함 |
| sensor_missing | 필요한 센서 토픽이 들어오지 않음 |
| timeout | 제한 시간 안에 목표를 수행하지 못함 |

---

## 7. 실험 기록 원칙

모든 실험은 다음 파일에 기록합니다.

- notes/experiment_log.md

실패 사례는 다음 위치에 따로 정리합니다.

- results/failure_cases/

rosbag 데이터는 용량이 크기 때문에 GitHub에는 직접 올리지 않고, 실험 기록에는 경로와 요약만 남깁니다.

---

## 8. 최종 방향

이 프로젝트의 최종 방향은 다음 흐름으로 정리합니다.

Mobile Robot Foundation  
→ Manipulation Basics  
→ Mobile Manipulation  
→ LLM/VLM-guided Mission Understanding

즉, 이동로봇 시스템을 먼저 이해하고, 이후 로봇팔 조작과 자연어 기반 미션 이해를 연결하여 모바일 매니퓰레이션 시스템으로 확장하는 것이 목표입니다.