# Baseline Inspection 01

## 1. Purpose

Phase 6에서 기록한 정상 Navigation2 rosbag을 재생하고, Failure Analysis에서 사용할 핵심 topic 메시지를 확인한다.

이번 기록은 실패 사례가 아니라, 이후 실패 bag과 비교하기 위한 정상 기준 메시지 해석 기록이다.

---

## 2. Baseline Bag

```text
rosbags/phase06_logging/p06_nav2_goal_01
```

---

## 3. Playback Command

```bash
cd ~/projects/missionbot-ros2

ros2 bag play rosbags/phase06_logging/p06_nav2_goal_01 \
  --topics /odom /cmd_vel /plan /amcl_pose \
  --rate 0.5 \
  --clock
```

---

## 4. Checked Topics

```text
[ ] /odom
[ ] /cmd_vel
[ ] /plan
[ ] /amcl_pose
```

---

## 5. /odom Observation

확인 명령:

```bash
ros2 topic echo /odom --once
```

확인한 핵심 필드:

```text
header.frame_id:
child_frame_id:
pose.pose.position.x:
pose.pose.position.y:
twist.twist.linear.x:
twist.twist.angular.z:
```

해석:

```text
-
```

---

## 6. /cmd_vel Observation

확인 명령:

```bash
ros2 topic echo /cmd_vel --once
```

확인한 핵심 필드:

```text
linear.x:
angular.z:
```

해석:

```text
-
```

---

## 7. /plan Observation

확인 명령:

```bash
ros2 topic echo /plan --once
```

확인한 핵심 필드:

```text
header.frame_id:
poses 존재 여부:
```

해석:

```text
-
```

---

## 8. /amcl_pose Observation

확인 명령:

```bash
ros2 topic echo /amcl_pose --once
```

확인한 핵심 필드:

```text
header.frame_id:
pose.pose.position.x:
pose.pose.position.y:
```

해석:

```text
-
```

---

## 9. Baseline Interpretation

정상 Navigation2 주행에서는 다음 흐름이 확인되어야 한다.

```text
/amcl_pose
→ map 위 현재 위치 추정

/plan
→ 목표 지점까지 global path 생성

/cmd_vel
→ 경로를 따라가기 위한 속도 명령 발행

/odom
→ 로봇의 실제 이동 상태 기록
```

이번 baseline bag은 위 흐름을 확인하기 위한 정상 기준 데이터다.

---

## 10. Notes

```text
-
```
