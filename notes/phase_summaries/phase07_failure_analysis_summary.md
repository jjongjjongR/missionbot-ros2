# Phase 7 Summary - Failure Analysis

## 1. Phase Overview

Phase 7의 목표는 Navigation2 주행 중 발생할 수 있는 실패 상황을 rosbag2 기록과 ROS2 topic 흐름을 기준으로 분류하는 것이다.

이번 Phase에서는 Phase 6에서 기록한 정상 Navigation2 주행 bag을 baseline으로 사용하고, 이후 의도적으로 실패 상황을 만들어 정상 bag과 실패 bag을 비교했다.

핵심은 단순히 “로봇이 실패했다”라고 기록하는 것이 아니라, 어떤 topic에서 어떤 증거가 보였는지를 기준으로 실패 유형을 판단하는 것이다.

---

## 2. Baseline Bag

정상 기준으로 사용한 bag은 다음과 같다.

```text
rosbags/phase06_logging/p06_nav2_goal_01
```

정상 bag 정보:

```text
Bag size: 8.8 MiB
Duration: 164.287617550s
Messages: 14935
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

이 bag은 Navigation2가 저장된 map 위에서 목표 지점 이동을 수행한 정상 주행 기록이다.

---

## 3. Failure Type Candidates

Phase 7에서 정의한 실패 유형 후보는 다음과 같다.

```text
goal_unreachable
path_planning_failure
localization_failure
obstacle_blocked
control_oscillation
sensor_missing
timeout
unknown
```

각 실패 유형은 topic 증거를 기준으로 판단한다.

예를 들어 `/plan`이 없으면 `path_planning_failure` 가능성이 있고, `/cmd_vel`은 발행되지만 `/odom` 변화가 거의 없으면 `obstacle_blocked` 또는 `goal_unreachable` 가능성이 있다.

---

## 4. Topic-based Judgment Criteria

이번 Phase에서 정리한 주요 topic별 판단 기준은 다음과 같다.

### /plan

`/plan`은 목표 지점까지의 global path를 의미한다.

```text
/plan 있음
→ planner_server가 경로를 생성했다.

/plan 없음
→ path_planning_failure 가능성이 있다.
```

### /cmd_vel

`/cmd_vel`은 로봇에게 전달되는 속도 명령이다.

```text
/cmd_vel 있음
→ controller_server가 이동 명령을 생성했다.

/cmd_vel 없음
→ 경로는 만들어졌지만 controller가 이동 명령을 만들지 못했을 가능성이 있다.
```

### /odom

`/odom`은 로봇의 위치, 자세, 속도 추정 정보다.

```text
/cmd_vel 있음 + /odom 변화 있음
→ 로봇이 실제로 움직였을 가능성이 높다.

/cmd_vel 있음 + /odom 변화 거의 없음
→ 명령은 나갔지만 로봇이 실제로 움직이지 못한 상황일 수 있다.
```

### /amcl_pose

`/amcl_pose`는 저장된 map 위에서 추정한 로봇의 현재 위치다.

```text
/amcl_pose 있음
→ AMCL 위치 추정이 동작하고 있다.

/amcl_pose 없음
→ 초기 위치 지정 실패 또는 localization_failure 가능성이 있다.
```

### /scan

`/scan`은 LiDAR 거리 센서 데이터다.

```text
/scan 있음
→ 주변 환경 감지 데이터가 들어오고 있다.

/scan 없음
→ sensor_missing 가능성이 있다.

/scan에서 가까운 거리값 반복
→ 장애물에 막힌 상황일 수 있다.
```

### /tf, /tf_static

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

## 5. Failure Case Template

실패 상황을 일관된 형식으로 기록하기 위해 failure case template을 작성했다.

파일 위치:

```text
results/failure_cases/failure_case_template.md
```

템플릿에는 다음 항목을 포함했다.

```text
Failure Case ID
Date
Phase
Failure Type
Situation Summary
Expected Behavior
Actual Behavior
Related Bag File
Compared Baseline Bag
Checked Topics
Topic Evidence
Initial Judgment
Final Judgment
Notes
Related Files
```

이 템플릿은 이후 실패 사례를 추가로 기록할 때 복사해서 사용할 수 있다.

---

## 6. Failure Analysis Workflow

이번 Phase에서는 실패 분석 절차도 정리했다.

기본 분석 순서는 다음과 같다.

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

## 7. First Failure Case

첫 실패 사례는 다음 ID로 기록했다.

```text
P07-FAIL-0001_unreachable_goal_test
```

실패 상황:

```text
RViz2에서 장애물 내부 또는 장애물과 가까운 위치를 2D Nav Goal로 지정했다.
TurtleBot3는 목표 근처까지 이동했지만 최종 목표에는 도달하지 못했다.
목표 근처에서 path가 바뀌는 현상이 보였고, TurtleBot3가 제자리에서 회전하는 동작을 반복했다.
```

실패 bag 위치:

```text
rosbags/failure_cases/P07-FAIL-0001_unreachable_goal_test
```

분석 문서 위치:

```text
results/failure_cases/P07-FAIL-0001_unreachable_goal_test.md
```

---

## 8. Failure Bag Result

실패 bag 정보:

```text
Files:             P07-FAIL-0001_unreachable_goal_test_0.db3
Bag size:          5.2 MiB
Storage id:        sqlite3
Duration:          92.231500380s
Messages:          9038
```

기록된 topic count:

```text
/cmd_vel     1034
/plan        51
/amcl_pose   58
/scan        447
/odom        2628
/tf_static   1
/tf          4819
```

정상 baseline과 같은 핵심 topic 7개가 모두 기록되었다.

```text
/scan
/odom
/tf
/tf_static
/cmd_vel
/amcl_pose
/plan
```

---

## 9. Final Judgment

이번 실패 사례의 최종 판정은 다음과 같다.

```text
Failure Type: goal_unreachable
Root Cause: 장애물 내부 또는 도달하기 어려운 위치를 2D Nav Goal로 지정하여, Navigation2가 목표 근처까지 접근했지만 최종 목표에 도달하지 못했다.
Secondary Symptom: control_oscillation
Confidence: high
```

판정 근거:

```text
/plan이 51개 기록되었으므로 path_planning_failure로 보기 어렵다.
/cmd_vel이 1034개 기록되었으므로 controller가 속도 명령을 발행한 것은 확인된다.
/scan, /odom, /tf, /tf_static, /amcl_pose가 모두 기록되었으므로 sensor_missing 또는 명확한 localization_failure 가능성은 낮다.
목표 근처까지 이동했지만 최종 도달하지 못했으므로 goal_unreachable로 판단했다.
```

---

## 10. /cmd_vel Oscillation Evidence

실패 bag의 뒤쪽 구간에서 `/cmd_vel`을 재생해 목표 근처의 속도 명령 패턴을 확인했다.

사용한 명령:

```bash
ros2 bag play rosbags/failure_cases/P07-FAIL-0001_unreachable_goal_test \
  --topics /cmd_vel \
  --start-offset 62 \
  --rate 0.5 \
  --clock
```

확인 결과, `linear.x`는 대부분 `0.0` 또는 매우 작은 값이었고, `angular.z`는 큰 양수와 음수 값이 반복적으로 나타났다.

대표 관찰 값:

```text
linear.x: 0.0
angular.z: -0.9979487179487179

linear.x: 0.0
angular.z: -0.9487179487179487

linear.x: 0.0
angular.z: 1.0000000000000004

linear.x: 0.0
angular.z: 0.8974358974358978
```

해석:

```text
전진 속도 명령은 거의 없고 회전 속도 명령이 반복적으로 발행되었다.
따라서 TurtleBot3가 목표 근처에서 전진해 목표에 수렴하기보다, 회전 동작을 반복한 것으로 볼 수 있다.
```

이 증거를 바탕으로 `control_oscillation`은 주 실패 원인이 아니라 `goal_unreachable` 상황에서 관찰된 보조 증상으로 기록했다.

---

## 11. Completed Tasks

Phase 7에서 완료한 작업은 다음과 같다.

```text
[x] Phase 6 정상 주행 bag baseline 확인
[x] 정상 bag topic count 확인
[x] Failure Type 후보 정의
[x] topic별 판단 기준 정리
[x] Failure Analysis Decision Table 작성
[x] Baseline Bag Inspection Commands 정리
[x] failure_case_template.md 작성
[x] Failure Analysis Workflow 작성
[x] 첫 실패 사례 계획 수립
[x] P07-FAIL-0001_unreachable_goal_test 실패 bag 기록
[x] ros2 bag info로 실패 bag 정보 확인
[x] P07-FAIL-0001_unreachable_goal_test.md 작성
[x] /cmd_vel 기반 control_oscillation 보조 증거 확인
[x] notes/experiment_log.md에 실패 실험 인덱싱
```

---

## 12. Related Files

```text
docs/phases/phase07_failure_analysis.md
results/failure_cases/failure_case_template.md
results/failure_cases/P07-FAIL-0001_unreachable_goal_test.md
rosbags/failure_cases/P07-FAIL-0001_unreachable_goal_test
notes/experiment_log.md
notes/phase_summaries/phase07_failure_analysis_summary.md
```

---

## 13. Phase Completion Judgment

Phase 7은 다음 기준을 만족했으므로 완료로 판단한다.

```text
[x] 정상 baseline bag 확인
[x] 실패 유형 후보 정의
[x] topic 기반 판단 기준 정리
[x] 첫 실패 bag 기록
[x] 실패 bag과 정상 bag 비교
[x] 실패 유형 최종 판정
[x] /cmd_vel 기반 보조 증거 확인
[x] failure report 작성
[x] experiment_log 인덱싱
[x] phase summary 작성
```

Phase 7 완료 의미:

```text
MissionBot-ROS2는 이제 단순히 Navigation2 주행을 성공시키는 것에서 나아가, 실패 상황을 rosbag2로 기록하고 topic 증거를 기반으로 실패 원인을 분류할 수 있게 되었다.
```

이번 Phase를 통해 정상 주행과 실패 주행을 비교하는 기본 분석 흐름을 만들었고, 이후 제어 기초나 더 복잡한 실패 분석으로 확장할 준비가 되었다.
