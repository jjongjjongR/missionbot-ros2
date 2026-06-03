# Phase 7. Failure Analysis

## 1. Phase Goal

Phase 7의 목표는 Navigation2 주행 중 발생할 수 있는 실패 상황을 rosbag2 기록과 ROS2 topic 흐름을 기준으로 분류하는 것이다.

이번 Phase에서는 먼저 Phase 6에서 기록한 정상 주행 bag을 baseline으로 사용한다.

정상 주행 기준을 먼저 정의한 뒤, 이후 실패 bag을 기록하고 정상 bag과 비교하여 실패 원인을 분류한다.

---

## 2. Baseline Bag

### 2.1 Baseline Bag Path

```text
rosbags/phase06_logging/p06_nav2_goal_01
```

### 2.2 Baseline Bag Files

```text
metadata.yaml
p06_nav2_goal_01_0.db3
```

### 2.3 Bag Info

```text
Storage id: sqlite3
Duration: 164.287617550s
Messages: 14935
Bag size: 8.8 MiB
```

### 2.4 Recorded Topics

| Topic        | Type                                          | Count |
| ------------ | --------------------------------------------- | ----: |
| `/scan`      | `sensor_msgs/msg/LaserScan`                   |   793 |
| `/odom`      | `nav_msgs/msg/Odometry`                       |  4664 |
| `/tf_static` | `tf2_msgs/msg/TFMessage`                      |     1 |
| `/cmd_vel`   | `geometry_msgs/msg/Twist`                     |   840 |
| `/tf`        | `tf2_msgs/msg/TFMessage`                      |  8557 |
| `/plan`      | `nav_msgs/msg/Path`                           |    41 |
| `/amcl_pose` | `geometry_msgs/msg/PoseWithCovarianceStamped` |    39 |

---

## 3. Baseline Interpretation

이 bag은 Navigation2가 저장된 map 위에서 목표 지점 이동을 수행하는 동안 기록된 정상 주행 데이터다.

정상 기준은 다음과 같이 해석한다.

| Topic        | 정상 bag에서의 의미                  | 실패 분석에서 보는 기준                     |
| ------------ | ----------------------------- | --------------------------------- |
| `/scan`      | LiDAR 센서 데이터가 지속적으로 기록됨       | 센서 누락, 장애물 감지 여부 확인               |
| `/odom`      | 로봇의 위치, 자세, 속도 추정이 계속 기록됨     | 실제 이동 여부, 정지 여부 확인                |
| `/tf_static` | 고정 좌표계 관계가 기록됨                | base_link, base_scan 같은 고정 프레임 확인 |
| `/cmd_vel`   | Navigation2가 로봇 이동 속도 명령을 발행함 | controller 동작 여부, 진동 여부 확인        |
| `/tf`        | 동적 좌표계 관계가 계속 기록됨             | map, odom, base_footprint 관계 확인   |
| `/plan`      | 목표 지점까지의 global path가 생성됨     | path planning 성공 여부 확인            |
| `/amcl_pose` | AMCL 위치 추정 결과가 기록됨            | localization 안정성 확인               |

---

## 4. Normal Navigation2 Flow

정상적인 Navigation2 주행 흐름은 다음과 같이 볼 수 있다.

```text
/amcl_pose
→ 현재 위치 추정

/plan
→ 목표 지점까지의 global path 생성

/cmd_vel
→ 경로를 따라가기 위한 속도 명령 발행

/odom
→ 로봇 이동 상태 기록

/scan
→ 주변 환경 거리 센서 기록

/tf, /tf_static
→ 좌표계 관계 기록
```

따라서 이후 실패 분석에서는 단순히 “로봇이 못 갔다”라고 기록하지 않고, 어떤 topic에서 어떤 증거가 보였는지를 기준으로 실패 유형을 분류한다.

---

## 5. Failure Type Candidates

| Failure Type            | Meaning               | Main Topics                                   |
| ----------------------- | --------------------- | --------------------------------------------- |
| `goal_unreachable`      | 목표 지점에 도달하지 못함        | `/plan`, `/cmd_vel`, `/odom`, `/amcl_pose`    |
| `path_planning_failure` | 경로 계획이 실패함            | `/plan`                                       |
| `localization_failure`  | 위치 추정이 흔들리거나 틀어짐      | `/amcl_pose`, `/tf`, `/odom`                  |
| `obstacle_blocked`      | 장애물 때문에 이동이 막힘        | `/scan`, `/cmd_vel`, `/odom`                  |
| `control_oscillation`   | 로봇이 목표 근처에서 진동함       | `/cmd_vel`, `/odom`, `/amcl_pose`             |
| `sensor_missing`        | 필요한 센서 topic이 없거나 부족함 | `/scan`, `/odom`, `/tf`                       |
| `timeout`               | 제한 시간 안에 목표를 수행하지 못함  | `Duration`, `/cmd_vel`, `/odom`, `/amcl_pose` |

```
```

---

## 6. Failure Analysis Decision Table

Failure Analysis에서는 단순히 로봇이 실패했다는 결과만 기록하지 않는다.

각 실패 상황을 ROS2 topic 증거와 연결해 판단한다.

아래 표는 Phase 7에서 사용할 초기 실패 판단 기준이다.

| Failure Type            | Primary Evidence                                              | Main Topics                                   | Interpretation                             |
| ----------------------- | ------------------------------------------------------------- | --------------------------------------------- | ------------------------------------------ |
| `sensor_missing`        | 필요한 sensor topic이 없거나 message count가 0에 가까움                   | `/scan`, `/odom`, `/tf`                       | 로봇이 주변 환경, 위치, 좌표계 정보를 충분히 받지 못한 상태        |
| `path_planning_failure` | `/plan`이 생성되지 않거나 count가 0에 가까움                               | `/plan`, `/amcl_pose`, `/map`                 | 현재 위치에서 목표 지점까지의 global path를 만들지 못한 상태    |
| `localization_failure`  | `/amcl_pose`가 없거나 위치 추정이 크게 흔들림                               | `/amcl_pose`, `/tf`, `/odom`, `/scan`         | map 위에서 로봇의 현재 위치를 안정적으로 추정하지 못한 상태        |
| `obstacle_blocked`      | `/cmd_vel`은 발행되지만 `/odom` 위치 변화가 거의 없고, `/scan`에서 가까운 장애물이 보임 | `/scan`, `/cmd_vel`, `/odom`                  | 이동 명령은 나갔지만 장애물 또는 막힌 공간 때문에 실제 이동이 제한된 상태 |
| `control_oscillation`   | `/cmd_vel`의 angular.z가 반복적으로 크게 변하고, `/odom` 이동이 안정적이지 않음     | `/cmd_vel`, `/odom`, `/amcl_pose`             | 로봇이 목표 근처 또는 경로 추종 중 흔들리며 안정적으로 수렴하지 못한 상태 |
| `goal_unreachable`      | `/plan`과 `/cmd_vel`은 존재하지만 목표 지점에 도달하지 못함                     | `/plan`, `/cmd_vel`, `/odom`, `/amcl_pose`    | 경로 생성과 제어 명령은 있었지만 최종 목표 수행에 실패한 상태        |
| `timeout`               | bag duration이 길지만 목표 도달 증거가 없고, 이동이 충분히 완료되지 않음               | `Duration`, `/cmd_vel`, `/odom`, `/amcl_pose` | 제한 시간 안에 목표 수행을 완료하지 못한 상태                 |
| `unknown`               | topic 증거만으로 명확히 분류하기 어려움                                      | 전체 topic                                      | 추가 실험이나 추가 로그가 필요한 상태                      |

---

## 7. Failure Type 판단 흐름

실패 분석은 다음 순서로 진행한다.

```text
1. ros2 bag info로 기록된 topic 목록과 message count를 확인한다.
2. 정상 baseline bag과 topic count를 비교한다.
3. /plan이 생성되었는지 확인한다.
4. /cmd_vel이 발행되었는지 확인한다.
5. /odom에서 실제 위치 변화가 있었는지 확인한다.
6. /amcl_pose로 위치 추정이 유지되었는지 확인한다.
7. /scan으로 주변 장애물 또는 센서 누락 가능성을 확인한다.
8. topic 증거를 종합해 Failure Type을 결정한다.
```

---

## 8. Topic별 우선 확인 기준

### 8.1 /plan

`/plan`은 목표 지점까지의 global path를 의미한다.

```text
/plan 있음
→ planner_server가 경로를 만들었다.

/plan 없음
→ path_planning_failure 가능성이 있다.
```

---

### 8.2 /cmd_vel

`/cmd_vel`은 로봇에게 전달되는 속도 명령이다.

```text
/cmd_vel 있음
→ controller_server가 이동 명령을 만들었다.

/cmd_vel 없음
→ controller가 경로를 따라가기 위한 명령을 만들지 못했을 수 있다.
```

---

### 8.3 /odom

`/odom`은 로봇의 위치, 자세, 속도 추정 정보다.

```text
/cmd_vel 있음 + /odom 변화 있음
→ 로봇이 실제로 움직였을 가능성이 높다.

/cmd_vel 있음 + /odom 변화 거의 없음
→ 명령은 나갔지만 로봇이 움직이지 못한 상황일 수 있다.
```

---

### 8.4 /amcl_pose

`/amcl_pose`는 map 위에서 추정한 로봇의 현재 위치다.

```text
/amcl_pose 있음
→ AMCL 위치 추정이 동작하고 있다.

/amcl_pose 없음
→ 초기 위치 지정 실패 또는 localization 문제 가능성이 있다.
```

---

### 8.5 /scan

`/scan`은 LiDAR 거리 센서 데이터다.

```text
/scan 있음
→ 주변 환경 감지 데이터가 들어오고 있다.

/scan 없음
→ sensor_missing 가능성이 있다.

/scan에서 가까운 거리값 반복
→ 장애물에 막힌 상황일 수 있다.
```

---

### 8.6 /tf, /tf_static

`/tf`와 `/tf_static`은 좌표계 관계를 담는다.

```text
/tf 있음
→ 동적 좌표계 관계가 기록되고 있다.

/tf_static 있음
→ 고정 좌표계 관계가 기록되고 있다.

map → odom → base_footprint 관계가 깨짐
→ localization 또는 frame 문제 가능성이 있다.
```

---

## 9. Baseline Comparison 기준

Phase 6 정상 bag의 기준은 다음과 같다.

```text
Baseline Bag:
rosbags/phase06_logging/p06_nav2_goal_01
```

정상 bag의 topic count:

```text
/scan       793
/odom       4664
/tf_static  1
/cmd_vel    840
/tf         8557
/plan       41
/amcl_pose  39
```

실패 bag을 분석할 때는 이 값을 절대적인 정답으로 보지는 않는다.

다만 다음 기준으로 비교한다.

```text
정상 bag에 있던 topic이 실패 bag에 없는가?
정상 bag보다 특정 topic count가 지나치게 적은가?
/plan은 있는데 /cmd_vel이 없는가?
/cmd_vel은 있는데 /odom 변화가 없는가?
/amcl_pose가 없거나 불안정한가?
/scan이 없거나 장애물 근접값이 반복되는가?
```

---

## 10. Judgment Rule

최종 판단은 하나의 topic만 보고 결정하지 않는다.

가능하면 다음 세 가지를 함께 본다.

```text
1. topic 존재 여부
2. message count
3. 실제 메시지 내용
```

예시:

```text
/plan count가 0이다.
→ path_planning_failure 가능성

/plan은 있다.
/cmd_vel도 있다.
/odom 변화가 거의 없다.
→ obstacle_blocked 또는 goal_unreachable 가능성

/amcl_pose가 없다.
/tf에서 map → odom 관계도 확인되지 않는다.
→ localization_failure 가능성

/scan이 없다.
→ sensor_missing 가능성
```

최종 실패 유형은 가장 강한 증거를 기준으로 선택한다.

다만 증거가 부족하면 `unknown`으로 두고 추가 실험을 진행한다.

---

## 11. Baseline Bag Inspection Commands

Phase 7에서는 실패 bag을 분석하기 전에 Phase 6에서 기록한 정상 bag을 기준 데이터로 먼저 확인한다.

Baseline bag은 다음과 같다.

```text
rosbags/phase06_logging/p06_nav2_goal_01
```

이 bag은 Navigation2가 저장된 map 위에서 목표 지점 이동을 수행한 정상 주행 기록이다.

---

### 11.1 Playback Command

정상 bag에서 핵심 topic만 선택해 재생한다.

```bash
cd ~/projects/missionbot-ros2

ros2 bag play rosbags/phase06_logging/p06_nav2_goal_01 \
  --topics /odom /cmd_vel /plan /amcl_pose \
  --rate 0.5 \
  --clock
```

명령어 의미:

```text
--topics
→ bag 전체 topic 중 필요한 topic만 선택해서 재생한다.

--rate 0.5
→ 원래 속도의 절반 속도로 재생한다.

--clock
→ playback 중 /clock을 발행한다.
```

---

### 11.2 /odom 확인

```bash
ros2 topic echo /odom --once
```

확인 기준:

```text
header.frame_id: odom
child_frame_id: base_footprint
pose.pose.position.x
pose.pose.position.y
```

의미:

```text
/odom은 로봇의 위치, 자세, 속도 추정 정보를 담는다.
정상 bag에서는 로봇이 실제로 이동했기 때문에 /odom 메시지가 지속적으로 기록되어 있다.
```

---

### 11.3 /cmd_vel 확인

```bash
ros2 topic echo /cmd_vel --once
```

확인 기준:

```text
linear.x
angular.z
```

의미:

```text
/cmd_vel은 로봇을 움직이기 위한 속도 명령이다.
정상 bag에서는 Navigation2 controller가 목표 이동을 위해 /cmd_vel을 발행했다.
```

---

### 11.4 /plan 확인

```bash
ros2 topic echo /plan --once
```

확인 기준:

```text
header.frame_id: map
poses
```

의미:

```text
/plan은 목표 지점까지의 global path다.
정상 bag에서는 planner_server가 목표 지점까지의 경로를 생성했기 때문에 /plan 메시지가 기록되어 있다.
```

---

### 11.5 /amcl_pose 확인

```bash
ros2 topic echo /amcl_pose --once
```

확인 기준:

```text
header.frame_id: map
pose.pose.position.x
pose.pose.position.y
```

의미:

```text
/amcl_pose는 저장된 map 위에서 추정한 로봇의 현재 위치다.
정상 bag에서는 AMCL이 로봇의 위치를 추정했기 때문에 /amcl_pose 메시지가 기록되어 있다.
```

---

### 11.6 Inspection Result 기준

정상 bag에서는 다음 흐름이 확인되어야 한다.

```text
/amcl_pose
→ 현재 위치 추정

/plan
→ 목표 지점까지의 global path 생성

/cmd_vel
→ 경로를 따라가기 위한 속도 명령 발행

/odom
→ 로봇 이동 상태 기록
```

따라서 실패 bag 분석에서는 이 흐름 중 어디가 끊겼는지 확인한다.

예시:

```text
/plan 없음
→ path_planning_failure 가능성

/plan 있음, /cmd_vel 없음
→ controller 또는 local planning 문제 가능성

/cmd_vel 있음, /odom 변화 거의 없음
→ obstacle_blocked 또는 goal_unreachable 가능성

/amcl_pose 없음
→ localization_failure 가능성
```

## 12. Failure Analysis Workflow

Phase 7에서는 실패 상황을 감으로 판단하지 않는다.

rosbag2로 기록된 topic 정보를 기준으로 실패 원인을 단계적으로 좁혀간다.

---

### 12.1 분석 시작 기준

실패 분석은 다음 입력이 있을 때 시작한다.

```text
1. 실패 상황 설명
2. 실패 rosbag 경로
3. ros2 bag info 결과
4. 필요 시 topic echo 결과
5. 정상 baseline bag 정보
```

정상 baseline bag은 다음을 사용한다.

```text
rosbags/phase06_logging/p06_nav2_goal_01
```

---

### 12.2 기본 분석 순서

실패 bag을 받으면 다음 순서로 확인한다.

```text
1. ros2 bag info로 전체 topic 목록과 message count를 확인한다.
2. 정상 baseline bag과 topic 구성을 비교한다.
3. /scan, /odom, /tf, /tf_static이 있는지 확인한다.
4. /amcl_pose가 있는지 확인한다.
5. /plan이 생성되었는지 확인한다.
6. /cmd_vel이 발행되었는지 확인한다.
7. /odom에서 실제 위치 변화가 있었는지 확인한다.
8. /scan에서 장애물 근접값 또는 센서 누락 가능성을 확인한다.
9. topic 증거를 종합해 Failure Type을 선택한다.
10. 판단 근거와 불확실한 점을 함께 기록한다.
```

---

### 12.3 빠른 판단 흐름

아래 흐름은 실패 유형을 빠르게 좁히기 위한 기준이다.

```text
/scan 없음
→ sensor_missing 가능성

/odom 없음
→ sensor_missing 또는 odometry 기록 문제 가능성

/tf 없음
→ frame 관계 문제 가능성

/amcl_pose 없음
→ localization_failure 가능성

/plan 없음
→ path_planning_failure 가능성

/plan 있음 + /cmd_vel 없음
→ controller 또는 local planning 문제 가능성

/plan 있음 + /cmd_vel 있음 + /odom 변화 거의 없음
→ obstacle_blocked 또는 goal_unreachable 가능성

/cmd_vel angular.z가 반복적으로 크게 변함
→ control_oscillation 가능성

Duration이 길고 목표 도달 증거가 없음
→ timeout 또는 goal_unreachable 가능성
```

---

### 12.4 Failure Analysis 기록 원칙

실패 기록에는 반드시 다음을 포함한다.

```text
1. Failure Case ID
2. Failure Type
3. 실패 상황 요약
4. 기대 동작
5. 실제 동작
6. 관련 rosbag 경로
7. 정상 baseline bag 경로
8. 확인한 topic
9. topic별 증거
10. 최종 판단
11. 불확실한 점
12. 다음 확인 계획
```

단순히 다음처럼 쓰지 않는다.

```text
로봇이 안 움직였다.
```

대신 다음처럼 쓴다.

```text
/plan은 생성되었고 /cmd_vel도 발행되었다.
하지만 /odom의 position 변화가 거의 없었다.
따라서 path_planning_failure보다는 obstacle_blocked 또는 goal_unreachable 가능성이 높다.
```

---

### 12.5 LLM 활용 메모

실무에서는 LLM을 Failure Analysis 보조 도구로 사용할 수 있다.

LLM이 도와줄 수 있는 부분은 다음과 같다.

```text
1. ros2 bag info 결과 요약
2. topic 누락 여부 확인
3. 정상 bag과 실패 bag의 차이 비교
4. /cmd_vel, /odom, /plan, /amcl_pose 출력 해석 보조
5. Failure Type 후보 추천
6. failure case 문서 초안 작성
```

하지만 최종 판단은 반드시 ROS2 topic 증거를 기준으로 검증해야 한다.

```text
LLM의 역할:
분석 속도 향상

엔지니어의 역할:
topic 증거 검증
실패 유형 최종 판단
재현 가능한 기록 작성
```

따라서 MissionBot-ROS2에서는 LLM을 사용하더라도 다음 원칙을 유지한다.

```text
LLM이 판단을 대신하지 않는다.
LLM은 로그 해석을 돕는다.
최종 문서에는 반드시 topic 기반 근거를 남긴다.
```

---

### 12.6 Phase 7에서의 현재 위치

현재 Phase 7에서는 아직 복잡한 자동 분석 코드를 만들지 않는다.

우선 다음을 정리하는 것이 목표다.

```text
1. 정상 baseline bag 확인
2. 실패 유형 후보 정의
3. topic별 판단 기준 정리
4. failure case 기록 양식 작성
5. 실패 분석 workflow 정리
```

이후 실제 실패 bag을 만들고, 위 기준에 따라 하나씩 분석한다.
