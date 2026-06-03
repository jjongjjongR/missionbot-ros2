# P07-FAIL-0001_unreachable_goal_test

## 1. Failure Case ID

```text
P07-FAIL-0001_unreachable_goal_test
```

---

## 2. Date

```text
2026-06-03
```

---

## 3. Phase

```text
Phase 7. Failure Analysis
```

---

## 4. Failure Hypothesis

이동하기 어려운 목표 지점을 RViz2의 2D Nav Goal로 지정하면, Navigation2가 경로를 만들지 못하거나 목표 지점에 도달하지 못할 수 있다.

예상 가능한 Failure Type은 다음과 같다.

```text
path_planning_failure
goal_unreachable
obstacle_blocked
unknown
```

최종 Failure Type은 실험 후 rosbag topic 증거를 기준으로 판단한다.

---

## 5. Situation Plan

RViz2에서 저장된 map 위에 2D Nav Goal을 지정한다.

목표 지점은 다음 조건 중 하나로 선택한다.

```text
검은 벽 영역
장애물 내부
이동 가능한 흰색 영역과 장애물 경계가 애매한 지점
좁은 통로 안쪽의 접근 어려운 위치
```

---

## 6. Expected Behavior

정상적인 목표 지점이라면 Navigation2는 다음 흐름으로 동작해야 한다.

```text
/amcl_pose
→ 현재 위치 추정

/plan
→ 목표 지점까지 global path 생성

/cmd_vel
→ 경로를 따라가기 위한 속도 명령 발행

/odom
→ 로봇 이동 상태 기록
```

하지만 이번 실험에서는 목표 지점이 이동하기 어렵거나 불가능한 위치일 수 있으므로, 위 흐름 중 일부가 끊길 것으로 예상한다.

---

## 7. Actual Behavior

RViz2에서 장애물 내부 또는 장애물과 가까운 위치를 2D Nav Goal로 지정했다.

Navigation2는 목표 지점에 대해 path를 생성했고, TurtleBot3는 목표 근처까지 이동했다.

하지만 목표 지점이 장애물 내부에 가까웠기 때문에 최종 목표에는 도달하지 못했다.

목표 근처에서 path가 바뀌는 현상이 보였고, TurtleBot3가 제자리에서 빙글빙글 도는 듯한 회전 동작을 반복했다.

---

## 8. Related Bag File

```text
rosbags/failure_cases/P07-FAIL-0001_unreachable_goal_test
```

Bag info:

```text
Files:             P07-FAIL-0001_unreachable_goal_test_0.db3
Bag size:          5.2 MiB
Storage id:        sqlite3
Duration:          92.231500380s
Messages:          9038
```

Topic count:

```text
/cmd_vel     1034
/plan        51
/amcl_pose   58
/scan        447
/odom        2628
/tf_static   1
/tf          4819
```

---

## 9. Compared Baseline Bag

```text
rosbags/phase06_logging/p06_nav2_goal_01
```

정상 baseline bag의 topic count:

```text
/scan       793
/odom       4664
/tf_static  1
/cmd_vel    840
/tf         8557
/plan       41
/amcl_pose  39
```

---

## 10. Topics to Record

```text
[x] /scan
[x] /odom
[x] /tf
[x] /tf_static
[x] /cmd_vel
[x] /amcl_pose
[x] /plan
```

---

## 11. Evidence Checklist

```text
[x] ros2 bag info 확인
[x] /scan 기록 여부 확인
[x] /odom 기록 여부 확인
[x] /tf 기록 여부 확인
[x] /tf_static 기록 여부 확인
[x] /cmd_vel 기록 여부 확인
[x] /amcl_pose 기록 여부 확인
[x] /plan 기록 여부 확인
```

---

## 12. Judgment Criteria

### 12.1 path_planning_failure 가능성

```text
판정: 낮음
```

근거:

```text
/plan이 51개 기록되었다.
따라서 경로 계획 자체가 완전히 실패한 상황으로 보기는 어렵다.
```

### 12.2 goal_unreachable 가능성

```text
판정: 높음
```

근거:

```text
/plan이 생성되었고 /cmd_vel도 발행되었다.
TurtleBot3는 목표 근처까지 이동했지만, 목표 지점이 장애물 내부에 가까워 최종 도달하지 못했다.
```

### 12.3 obstacle_blocked 가능성

```text
판정: 중간
```

근거:

```text
목표 지점이 장애물 내부 또는 장애물 근처였기 때문에 장애물에 의해 최종 접근이 제한되었을 가능성이 있다.
다만 로봇이 목표 근처까지 이동했기 때문에 완전히 막혀 처음부터 움직이지 못한 상황은 아니다.
```

### 12.4 control_oscillation 가능성

```text
판정: 보조 증상으로 존재
```

근거:

```text
목표 근처에서 TurtleBot3가 빙글빙글 도는 회전 동작을 보였다.
이는 목표 근처에서 controller가 안정적으로 수렴하지 못했거나, 도달 불가능한 목표 주변에서 recovery/replanning이 반복된 현상으로 볼 수 있다.
```

### 12.5 sensor_missing 가능성

```text
판정: 낮음
```

근거:

```text
/scan, /odom, /tf, /tf_static이 모두 기록되었다.
따라서 센서 topic 누락으로 인한 실패로 보기는 어렵다.
```

### 12.6 localization_failure 가능성

```text
판정: 낮음
```

근거:

```text
/amcl_pose와 /tf가 기록되었고, 로봇이 목표 근처까지 이동했다.
현재 증거만으로는 위치 추정 실패가 주원인이라고 보기 어렵다.
```

---

## 13. Final Judgment

```text
Failure Type: goal_unreachable
Root Cause: 장애물 내부 또는 도달하기 어려운 위치를 2D Nav Goal로 지정하여, Navigation2가 목표 근처까지 이동했지만 최종 목표에 도달하지 못했다.
Secondary Symptom: control_oscillation
Confidence: high
```

최종 해석:

```text
이번 실패는 경로 계획 자체가 완전히 실패한 사례라기보다, 도달하기 어려운 목표 지점 때문에 Navigation2가 목표 근처에서 수렴하지 못한 goal_unreachable 사례로 판단한다.

목표 근처에서 로봇이 빙글빙글 도는 현상이 있었으므로 control_oscillation은 주 실패 원인이라기보다 보조 증상으로 기록한다.
```

---

## 14. Notes

```text
첫 실패 bag 기록에 성공했다.
정상 baseline bag과 동일한 핵심 topic 7개를 모두 기록했다.
이번 케이스에서는 /plan과 /cmd_vel이 모두 존재하므로 path_planning_failure보다는 goal_unreachable에 가깝다.
목표 근처에서 회전이 반복되었기 때문에 추후 /cmd_vel의 angular.z 패턴을 확인하면 control_oscillation 여부를 더 정밀하게 분석할 수 있다.
```

---

### 15.1 /cmd_vel Evidence Result

실패 bag의 뒤쪽 구간부터 `/cmd_vel`을 재생하여 목표 근처에서의 속도 명령 패턴을 확인했다.

사용한 재생 방식:

```bash
ros2 bag play rosbags/failure_cases/P07-FAIL-0001_unreachable_goal_test \
  --topics /cmd_vel \
  --start-offset 62 \
  --rate 0.5 \
  --clock
```

확인 결과, `/cmd_vel`에서 `linear.x`는 대부분 `0.0` 또는 매우 작은 값으로 유지되었고, `angular.z`는 큰 양수와 음수 값이 반복적으로 나타났다.

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

판단:

```text
이번 실패 사례의 Primary Failure Type은 goal_unreachable로 유지한다.
다만 /cmd_vel의 angular.z 반복 패턴과 RViz2에서 관찰한 회전 동작이 일치하므로, control_oscillation은 보조 증상으로 강하게 기록할 수 있다.
```

업데이트된 최종 판단:

```text
Failure Type: goal_unreachable
Root Cause: 장애물 내부 또는 도달하기 어려운 위치를 2D Nav Goal로 지정하여, Navigation2가 목표 근처까지 접근했지만 최종 목표에 도달하지 못했다.
Secondary Symptom: control_oscillation
Confidence: high
```
