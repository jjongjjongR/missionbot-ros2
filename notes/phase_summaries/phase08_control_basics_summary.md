# Phase 8 Summary - Control Basics

## 1. Phase Overview

Phase 8에서는 TurtleBot3의 `/cmd_vel` 속도 명령과 `/odom` 반응을 기준으로 이동로봇 제어의 기초를 확인했다.

이번 Phase의 목표는 복잡한 제어 알고리즘을 구현하는 것이 아니라, 가장 기본적인 속도 명령이 TurtleBot3의 실제 움직임에 어떻게 반영되는지 직접 확인하는 것이었다.

핵심 흐름은 다음과 같다.

```text
/cmd_vel
→ 로봇에게 보내는 속도 명령

/odom
→ 로봇이 실제로 어떻게 움직였는지 추정한 결과
```

Phase 8은 다음과 같은 흐름으로 진행했다.

```text
환경 확인
→ /cmd_vel, /odom 관계 복습
→ open-loop 전진 명령 실습
→ open-loop 회전 명령 실습
→ 전진/회전 반응 비교
→ Python ROS2 control node 작성
```

---

## 2. Completed Tasks

Phase 8에서 완료한 항목은 다음과 같다.

```text
[x] 기존 Gazebo / RViz2 / Navigation2 관련 노드 정리
[x] ROS2 Humble 환경 확인
[x] TURTLEBOT3_MODEL=burger 확인
[x] TurtleBot3 Gazebo empty_world 실행
[x] /cmd_vel topic 확인
[x] /odom topic 확인
[x] /tf, /tf_static topic 확인
[x] /cmd_vel 메시지 타입 확인
[x] /odom 메시지 타입 확인
[x] /cmd_vel publisher/subscriber 구조 확인
[x] turtlebot3_diff_drive가 /cmd_vel을 subscribe하는 것 확인
[x] /odom이 Gazebo TurtleBot3에서 publish되는 것 확인
[x] teleop_keyboard 입력에 따른 /cmd_vel 값 변화 확인
[x] TurtleBot3 이동 후 /odom position 및 orientation 변화 확인
[x] ros2 topic pub으로 전진 명령 직접 발행
[x] ros2 topic pub으로 회전 명령 직접 발행
[x] 전진 명령과 회전 명령의 /odom 반응 비교
[x] open_loop_controller.py 작성
[x] setup.py entry_points에 open_loop_controller 등록
[x] colcon build 성공
[x] source install/setup.bash 적용
[x] ros2 pkg executables로 open_loop_controller 등록 확인
[x] ros2 run missionbot_basic open_loop_controller 실행
[x] Gazebo에서 전진 → 정지 → 회전 → 정지 동작 확인
[x] 마지막 정지 확인
```

---

## 3. Key Concepts

## 3.1 /cmd_vel

`/cmd_vel`은 로봇에게 속도 명령을 보내는 topic이다.

TurtleBot3에서는 `geometry_msgs/msg/Twist` 타입을 사용한다.

중요하게 본 필드는 다음과 같다.

```text
linear.x
→ 로봇 기준 전진/후진 속도

angular.z
→ 로봇 기준 회전 속도
```

---

## 3.2 /odom

`/odom`은 로봇의 위치, 자세, 속도 추정 정보를 담는 topic이다.

TurtleBot3에서는 `nav_msgs/msg/Odometry` 타입을 사용한다.

중요하게 본 필드는 다음과 같다.

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

---

## 3.3 Open-loop Control

Open-loop control은 피드백 없이 정해진 명령을 정해진 시간 동안 보내는 방식이다.

이번 Phase에서는 `/odom` 값을 실시간으로 읽어 명령을 보정하지 않았다.

대신 다음과 같이 명령을 보냈다.

```text
2초 동안 전진
2초 또는 3초 동안 회전
정지
```

이후 `/odom` 값을 확인하여 실제 결과를 해석했다.

---

## 4. Phase 8-1. Environment Check and /cmd_vel - /odom Review

Phase 8-1에서는 TurtleBot3 Gazebo 환경에서 `/cmd_vel`과 `/odom` topic을 확인했다.

확인한 주요 topic은 다음과 같다.

```text
/cmd_vel
/odom
/tf
/tf_static
```

`/cmd_vel` 확인 결과:

```text
Type: geometry_msgs/msg/Twist
Publisher count: 0
Subscription count: 1
Node name: turtlebot3_diff_drive
```

해석:

```text
아직 /cmd_vel을 보내는 publisher는 없지만,
TurtleBot3 diff drive plugin이 /cmd_vel을 받을 준비가 되어 있었다.
```

`/odom` 확인 결과:

```text
Type: nav_msgs/msg/Odometry
Publisher count: 1
```

해석:

```text
Gazebo TurtleBot3가 /odom을 publish하고 있었다.
```

---

## 5. Phase 8-2. Open-loop Forward Control

Phase 8-2에서는 `/cmd_vel`에 직접 전진 명령을 보냈다.

사용한 명령의 핵심 값은 다음과 같다.

```text
linear.x = 0.10
angular.z = 0.0
```

이 명령은 로봇이 현재 바라보는 방향으로 전진하라는 의미다.

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

이론상 기대 이동 거리는 다음과 같았다.

```text
0.10 m/s × 2 s = 0.20 m
```

실제 이동 거리는 약 0.231m로, 기대값과 비교적 가까웠다.

전진 실험에서는 position 값이 변했고, orientation 값은 거의 유지되었다.

따라서 다음 관계를 확인했다.

```text
/cmd_vel linear.x
→ /odom position 변화
```

---

## 6. Phase 8-3. Open-loop Rotation Control

Phase 8-3에서는 `/cmd_vel`에 직접 회전 명령을 보냈다.

사용한 명령의 핵심 값은 다음과 같다.

```text
linear.x = 0.0
angular.z = 1.0
```

이 명령은 전진하지 않고 제자리에서 회전하라는 의미다.

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

해석:

```text
position 변화는 매우 작았고,
orientation 변화는 크게 나타났다.
```

따라서 다음 관계를 확인했다.

```text
/cmd_vel angular.z
→ /odom orientation 변화
```

회전 실험 중 정지 명령을 `--once`로 한 번만 보냈을 때 로봇이 바로 멈추지 않는 현상이 있었다.

이후 Python control node에서는 정지 명령을 일정 시간 동안 반복 발행하는 방식으로 보완했다.

---

## 7. Phase 8-4. Forward vs Rotation Response Comparison

Phase 8-4에서는 전진 명령과 회전 명령의 결과를 비교했다.

| 비교 항목                | 전진 실험                  | 회전 실험                        |
| -------------------- | ---------------------- | ---------------------------- |
| `/cmd_vel linear.x`  | 0.10                   | 0.0                          |
| `/cmd_vel angular.z` | 0.0                    | 1.0                          |
| 주로 변한 `/odom` 값      | position.x, position.y | orientation.z, orientation.w |
| position 변화          | 큼                      | 작음                           |
| orientation 변화       | 거의 없음                  | 큼                            |
| 해석                   | 현재 바라보는 방향으로 이동        | 제자리 회전                       |

핵심 결론은 다음과 같다.

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

Phase 8-5에서는 터미널에서 직접 `/cmd_vel`을 publish하던 실습을 Python ROS2 node로 옮겼다.

작성한 파일:

```text
src/missionbot_basic/missionbot_basic/open_loop_controller.py
```

수정한 파일:

```text
src/missionbot_basic/setup.py
```

등록한 entry point:

```text
open_loop_controller = missionbot_basic.open_loop_controller:main
```

실행 명령:

```bash
ros2 run missionbot_basic open_loop_controller
```

control sequence:

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

Gazebo에서 확인한 동작:

```text
전진
→ 정지
→ 회전
→ 정지
```

마지막에는 로봇이 정상적으로 멈췄다.

이 결과를 통해 직접 작성한 Python ROS2 node가 `/cmd_vel`을 publish하여 TurtleBot3를 제어할 수 있음을 확인했다.

---

## 9. Main Results

Phase 8의 핵심 결과는 다음과 같다.

```text
/cmd_vel은 로봇에게 보내는 속도 명령이다.
/odom은 로봇이 실제로 어떻게 움직였는지 추정한 결과다.
```

```text
/cmd_vel linear.x
→ /odom position 변화
```

```text
/cmd_vel angular.z
→ /odom orientation 변화
```

```text
open-loop control은 피드백 없이 정해진 시간 동안 정해진 속도 명령을 보내는 방식이다.
```

```text
Python ROS2 node를 통해 /cmd_vel을 직접 publish할 수 있다.
```

---

## 10. Issues and Notes

### 정지 명령 관련 이슈

회전 실험 중 정지 명령을 `--once`로 한 번만 보냈을 때 로봇이 바로 멈추지 않는 현상이 있었다.

해석:

```text
정지 명령을 한 번만 보내면 안정적으로 반영되지 않을 수 있다.
```

보완:

```text
정지 명령을 일정 시간 동안 반복 발행하는 방식이 더 안전하다.
```

예시:

```bash
timeout 1 ros2 topic pub --rate 20 /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"
```

Python control node에서는 정지 구간을 1초 동안 두어 정지 명령을 반복 발행했다.

---

## 11. Phase 8 Completion Meaning

Phase 8을 통해 MissionBot-ROS2는 Navigation2가 자동으로 생성하던 `/cmd_vel` 명령을 기초 제어 관점에서 직접 이해하게 되었다.

또한 직접 작성한 Python ROS2 node로 `/cmd_vel`을 publish하여 TurtleBot3를 전진, 정지, 회전, 정지 순서로 제어할 수 있게 되었다.

이제 MissionBot-ROS2는 다음 단계에서 MoveIt2 또는 더 복잡한 로봇 제어 구조를 학습하기 전에, 이동로봇의 가장 기본적인 속도 명령과 반응 구조를 이해한 상태가 되었다.

---

## 12. Next Step

다음으로 정리할 항목은 다음과 같다.

```text
README.md Result 섹션에 Phase 8 Summary 추가
notes/experiment_log.md에 Phase 8 실험 기록 추가
docs/handoffs/MBROS2_Phase8_Handoff.md 작성
docs/handoffs/MBROS2_Phase8_prompt.md 작성
```

이후 다음 Phase로 넘어간다.

```text
Phase 9. MoveIt2 Basics
```
