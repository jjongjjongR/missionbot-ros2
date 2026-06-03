# Failure Case Template

## 1. Failure Case ID

```text
P07-FAIL-000X_failure_summary
```

예시:

```text
P07-FAIL-0001_goal_unreachable
P07-FAIL-0002_path_planning_failure
P07-FAIL-0003_localization_failure
```

---

## 2. Date

```text
YYYY-MM-DD
```

---

## 3. Phase

```text
Phase 7. Failure Analysis
```

---

## 4. Failure Type

아래 후보 중 하나를 선택한다.

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

---

## 5. Situation Summary

실패 상황을 짧게 요약한다.

```text
예시:
RViz2에서 2D Nav Goal을 지정했지만 TurtleBot3가 목표 지점까지 도달하지 못했다.
```

---

## 6. Expected Behavior

원래 기대한 동작을 적는다.

```text
예시:
TurtleBot3가 저장된 map 위에서 현재 위치를 추정하고, /plan으로 생성된 경로를 따라 목표 지점까지 이동해야 한다.
```

---

## 7. Actual Behavior

실제로 일어난 일을 적는다.

```text
예시:
목표 지점은 지정되었지만 로봇이 거의 움직이지 않았고, 일정 시간이 지난 뒤 목표 도달을 확인하지 못했다.
```

---

## 8. Related Bag File

실패 상황을 기록한 rosbag 경로를 적는다.

```text
rosbags/failure_cases/P07-FAIL-000X_failure_summary
```

---

## 9. Compared Baseline Bag

정상 기준 bag을 적는다.

```text
rosbags/phase06_logging/p06_nav2_goal_01
```

정상 기준 bag 의미:

```text
Phase 6에서 기록한 정상 Navigation2 목표 이동 rosbag이다.
이 bag에는 /scan, /odom, /tf, /tf_static, /cmd_vel, /amcl_pose, /plan topic이 정상적으로 기록되어 있다.
```

---

## 10. Checked Topics

실패 분석에 사용한 topic을 체크한다.

```text
[ ] /scan
[ ] /odom
[ ] /tf
[ ] /tf_static
[ ] /cmd_vel
[ ] /amcl_pose
[ ] /plan
```

---

## 11. Topic Evidence

각 topic에서 확인한 증거를 적는다.

### 11.1 /scan

```text
확인 내용:
-
```

판단 기준:

```text
/scan이 없거나 count가 0에 가까우면 sensor_missing 가능성이 있다.
/scan은 존재하지만 특정 방향 거리가 매우 짧으면 obstacle_blocked 가능성이 있다.
```

---

### 11.2 /odom

```text
확인 내용:
-
```

판단 기준:

```text
/cmd_vel이 발행되는데 /odom 위치 변화가 거의 없으면 로봇이 실제로 이동하지 못한 상황일 수 있다.
```

---

### 11.3 /tf, /tf_static

```text
확인 내용:
-
```

판단 기준:

```text
map, odom, base_footprint, base_link, base_scan 관계가 끊기면 localization 또는 frame 관련 문제가 있을 수 있다.
```

---

### 11.4 /cmd_vel

```text
확인 내용:
-
```

판단 기준:

```text
/cmd_vel이 거의 없으면 controller가 속도 명령을 만들지 못한 상황일 수 있다.
/cmd_vel의 angular.z가 계속 크게 반복되면 control_oscillation 가능성이 있다.
```

---

### 11.5 /amcl_pose

```text
확인 내용:
-
```

판단 기준:

```text
/amcl_pose가 없거나 위치 추정이 크게 흔들리면 localization_failure 가능성이 있다.
```

---

### 11.6 /plan

```text
확인 내용:
-
```

판단 기준:

```text
/plan이 생성되지 않으면 path_planning_failure 가능성이 있다.
/plan은 생성되지만 로봇이 움직이지 못하면 controller, obstacle, localization 문제를 추가로 확인한다.
```

---

## 12. Initial Judgment

초기 판단을 적는다.

```text
예시:
현재 증거만 보면 /plan은 생성되었으나 /cmd_vel이 거의 없으므로 path planning보다는 controller 또는 local costmap 문제 가능성이 있다.
```

---

## 13. Final Judgment

최종 실패 원인을 적는다.

```text
Failure Type:
Root Cause:
Confidence:
```

예시:

```text
Failure Type: goal_unreachable
Root Cause: 목표 지점은 지정되었지만 로봇이 실제로 충분히 이동하지 못했다.
Confidence: medium
```

---

## 14. Notes

추가로 배운 점이나 다음에 확인할 점을 적는다.

```text
-
```

---

## 15. Related Files

```text
rosbag:
screenshot:
terminal log:
rviz config:
```
