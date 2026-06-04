# Phase 8. Control Basics

## 1. Phase Goal

Phase 8의 목표는 TurtleBot3의 `/cmd_vel` 속도 명령과 `/odom` 반응을 기준으로 이동로봇 제어의 기초를 이해하는 것이다.

이번 Phase에서는 복잡한 PID, MPC, 강화학습 제어를 다루지 않는다.

우선 가장 기본적인 흐름을 확인했다.

```text
/cmd_vel
→ 로봇에게 보내는 속도 명령

/odom
→ 로봇이 실제로 어떻게 움직였는지 추정한 결과
```

핵심 목표는 다음과 같다.

```text
1. /cmd_vel topic 구조 확인
2. /odom topic 구조 확인
3. linear.x와 angular.z 의미 이해
4. open-loop control 실습
5. 전진 명령과 회전 명령의 /odom 반응 비교
6. Python ROS2 node로 /cmd_vel 제어
```

---

## 2. Background

Phase 5에서는 Navigation2가 목표 지점까지 이동하기 위해 `/cmd_vel`을 발행했다.

Phase 6에서는 Navigation2 주행 중 `/cmd_vel`, `/odom`, `/scan`, `/tf`, `/amcl_pose`, `/plan` 등을 rosbag2로 기록했다.

Phase 7에서는 정상 주행 bag과 실패 bag을 비교하면서 `/cmd_vel`과 `/odom`을 실패 분석 증거로 사용했다.

Phase 8에서는 이 관계를 더 기초부터 직접 확인했다.

```text
/cmd_vel이 어떤 명령을 보내는가?
/odom이 실제 움직임을 어떻게 보여주는가?
```

---

## 3. Key Concepts

## 3.1 Control

Control은 로봇을 원하는 방향과 속도로 움직이게 만드는 과정이다.

이번 Phase에서는 TurtleBot3를 대상으로 가장 기본적인 속도 명령을 확인했다.

```text
앞으로 이동
제자리 회전
정지
```

---

## 3.2 /cmd_vel

`/cmd_vel`은 로봇에게 속도 명령을 보내는 topic이다.

TurtleBot3에서는 `geometry_msgs/msg/Twist` 타입을 사용한다.

중요한 필드는 다음 두 개다.

```text
linear.x
→ 로봇 기준 전진/후진 속도

angular.z
→ 로봇 기준 회전 속도
```

예시:

```text
linear.x = 0.10
angular.z = 0.0
```

의미:

```text
현재 로봇이 바라보는 방향으로 전진
```

예시:

```text
linear.x = 0.0
angular.z = 0.5
```

의미:

```text
제자리 회전
```

---

## 3.3 /odom

`/odom`은 로봇의 위치, 자세, 속도 추정 정보를 담는 topic이다.

TurtleBot3에서는 `nav_msgs/msg/Odometry` 타입을 사용한다.

중요하게 확인한 필드는 다음과 같다.

```text
header.frame_id: odom
child_frame_id: base_footprint

pose.pose.position.x
pose.pose.position.y

pose.pose.orientation.z
pose.pose.orientation.w

twist.twist.linear.x
twist.twist.angular.z
```

의미:

```text
position.x, position.y
→ odom 좌표계 기준 로봇 위치 변화

orientation.z, orientation.w
→ 로봇 방향 변화

twist.twist.linear.x
→ 현재 전진 속도 추정

twist.twist.angular.z
→ 현재 회전 속도 추정
```

---

## 3.4 Open-loop Control

Open-loop control은 피드백을 사용하지 않고, 정해진 명령을 정해진 시간 동안 보내는 제어 방식이다.

이번 Phase에서는 `/odom` 값을 읽어 실시간으로 보정하지 않았다.

대신 다음처럼 명령을 보냈다.

```text
2초 동안 전진
2초 동안 회전
정지
```

즉, 명령을 먼저 보내고, 이후 `/odom`으로 결과를 확인했다.

---

## 4. Phase 8-1. Environment Check and /cmd_vel - /odom Review

## Goal

TurtleBot3 Gazebo 환경에서 `/cmd_vel`과 `/odom` topic을 확인하고, 속도 명령과 이동 결과의 관계를 복습한다.

## Checked Topics

```text
/cmd_vel
/odom
/tf
/tf_static
```

## Key Result

`/cmd_vel` 확인 결과:

```text
Type: geometry_msgs/msg/Twist
Publisher count: 0
Subscription count: 1
Node name: turtlebot3_diff_drive
```

의미:

```text
아직 /cmd_vel을 보내는 publisher는 없지만,
TurtleBot3 diff drive plugin이 /cmd_vel을 받을 준비가 되어 있다.
```

`/odom` 확인 결과:

```text
Type: nav_msgs/msg/Odometry
Publisher count: 1
```

의미:

```text
Gazebo TurtleBot3가 /odom을 publish하고 있다.
```

## Meaning

Phase 8-1을 통해 다음 관계를 확인했다.

```text
/cmd_vel
→ 로봇에게 보내는 명령

/odom
→ 로봇이 실제로 움직인 결과 추정
```

---

## 5. Phase 8-2. Open-loop Forward Control

## Goal

`/cmd_vel`에 직접 전진 속도 명령을 보내고, `/odom` 위치 값이 어떻게 변하는지 확인한다.

## Command

```bash
ros2 topic pub --rate 10 /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.10, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}" &
PUB_PID=$!
sleep 2
kill $PUB_PID
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"
```

## Result

전진 전 `/odom` position:

```text
x: 0.4280005964
y: 0.2159413832
```

전진 후 `/odom` position:

```text
x: 0.4684945049
y: 0.4435689256
```

변화량:

```text
Δx ≈ 0.0405
Δy ≈ 0.2276
```

대략 이동 거리:

```text
약 0.231 m
```

이론상 기대 이동 거리:

```text
0.10 m/s × 2 s = 0.20 m
```

## Meaning

실제 이동 거리는 약 0.231m로, 기대값 0.20m와 비교적 가깝게 나왔다.

또한 orientation 값은 거의 변하지 않았으므로, 회전 없이 현재 로봇이 바라보는 방향으로 전진한 것으로 판단했다.

정리하면 다음과 같다.

```text
/cmd_vel linear.x = 0.10
→ /odom position 변화
```

---

## 6. Phase 8-3. Open-loop Rotation Control

## Goal

`/cmd_vel`에 직접 회전 속도 명령을 보내고, `/odom` orientation 값이 어떻게 변하는지 확인한다.

## Command

```bash
ros2 topic pub --rate 10 /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 1.0}}" &
PUB_PID=$!
sleep 3
kill $PUB_PID
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"
```

## Result

회전 전 `/odom` orientation:

```text
orientation.z: 0.0000182608
orientation.w: 0.9999958917
```

회전 후 `/odom` orientation:

```text
orientation.z: 0.7499511629
orientation.w: -0.6614871319
```

position 변화:

```text
position.x: 0.0001432495 → 0.0021648843
position.y: -0.0000011391 → -0.0019984518
```

## Meaning

position 변화는 매우 작았고, orientation 값은 크게 변했다.

따라서 `angular.z = 1.0` 회전 명령이 TurtleBot3의 방향 변화로 이어지는 것을 확인했다.

정리하면 다음과 같다.

```text
/cmd_vel angular.z = 1.0
→ /odom orientation 변화
```

## Note

회전 실험 중 정지 명령을 `--once`로 한 번만 보냈을 때 로봇이 바로 멈추지 않는 현상이 있었다.

이후에는 정지 명령을 한 번만 보내지 않고, 일정 시간 동안 반복 발행하는 방식이 더 안전하다고 판단했다.

예시:

```bash
timeout 1 ros2 topic pub --rate 20 /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"
```

---

## 7. Phase 8-4. Forward vs Rotation Response Comparison

## Goal

전진 명령과 회전 명령을 비교하여, `linear.x`와 `angular.z`가 `/odom`에서 각각 어떤 결과로 나타나는지 정리한다.

## Comparison

| Item                 | Forward Control        | Rotation Control             |
| -------------------- | ---------------------- | ---------------------------- |
| `/cmd_vel linear.x`  | 0.10                   | 0.0                          |
| `/cmd_vel angular.z` | 0.0                    | 1.0                          |
| Main `/odom` change  | position.x, position.y | orientation.z, orientation.w |
| Position change      | Large                  | Small                        |
| Orientation change   | Very small             | Large                        |
| Interpretation       | Forward motion         | In-place rotation            |

## Key Takeaway

```text
linear.x
→ 로봇 기준 앞 방향 속도
→ /odom position 변화로 확인

angular.z
→ 로봇 기준 회전 속도
→ /odom orientation 변화로 확인
```

---

## 8. Phase 8-5. Simple Python Open-loop Control Node

## Goal

터미널 명령어로 `/cmd_vel`을 직접 publish하던 실습을 Python ROS2 node로 옮겨서 실행한다.

## File

```text
src/missionbot_basic/missionbot_basic/open_loop_controller.py
```

## Entry Point

```text
open_loop_controller = missionbot_basic.open_loop_controller:main
```

## Control Sequence

```text
0~2초
→ 전진

2~3초
→ 정지

3~5초
→ 제자리 회전

5~6초
→ 정지

6초 이후
→ 종료
```

## Result

`open_loop_controller` node를 실행했을 때 Gazebo에서 TurtleBot3가 다음 순서로 움직이는 것을 확인했다.

```text
전진
→ 정지
→ 회전
→ 정지
```

마지막에는 로봇이 정상적으로 멈췄다.

## Meaning

터미널 명령어가 아니라, 직접 작성한 Python ROS2 node가 `/cmd_vel`을 publish하여 TurtleBot3를 제어할 수 있음을 확인했다.

정리하면 다음과 같다.

```text
open_loop_controller.py
→ /cmd_vel publish
→ TurtleBot3 이동
→ /odom 변화
```

---

## 9. Final Result

Phase 8에서는 이동로봇 제어의 가장 기본 관계를 확인했다.

핵심 결과는 다음과 같다.

```text
/cmd_vel은 로봇에게 보내는 속도 명령이다.
/odom은 로봇이 실제로 어떻게 움직였는지 추정한 결과다.

linear.x는 로봇 기준 전진 속도이며, /odom position 변화로 확인된다.
angular.z는 로봇 기준 회전 속도이며, /odom orientation 변화로 확인된다.

open-loop control은 피드백 없이 정해진 시간 동안 정해진 속도 명령을 보내는 방식이다.
Python ROS2 node를 통해 /cmd_vel을 직접 publish할 수 있다.
```

Phase 8 완료 의미:

```text
MissionBot-ROS2는 이제 Navigation2가 자동으로 생성하던 /cmd_vel 명령을
기초 제어 관점에서 직접 이해하고,
간단한 Python node로 속도 명령을 발행할 수 있게 되었다.
```

---

## 10. Completed Checklist

```text
[x] /cmd_vel topic 확인
[x] /odom topic 확인
[x] linear.x 의미 확인
[x] angular.z 의미 확인
[x] open-loop forward control 실습
[x] open-loop rotation control 실습
[x] 전진 명령과 회전 명령의 /odom 반응 비교
[x] open_loop_controller.py 작성
[x] setup.py entry point 등록
[x] colcon build 성공
[x] ros2 run으로 open_loop_controller 실행
[x] Gazebo에서 전진 → 정지 → 회전 → 정지 확인
[x] 마지막 정지 확인
```

---

## 11. Next Phase

다음 Phase는 다음과 같다.

```text
Phase 9. MoveIt2 Basics
```

단, Phase 9로 바로 넘어가기 전에 Phase 8의 README Result, experiment_log, phase summary, handoff, prompt를 정리한다.
