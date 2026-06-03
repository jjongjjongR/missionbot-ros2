# Phase 6. rosbag2 Logging Summary

## 1. Phase 개요

Phase 6에서는 Navigation2 주행 중 발생하는 주요 ROS2 topic을 rosbag2로 기록하고, 저장된 bag 파일을 다시 재생하여 확인하는 흐름을 실습했다.

이 Phase의 핵심 목표는 단순히 bag 파일을 생성하는 것이 아니라, TurtleBot3가 Navigation2로 목표 지점까지 이동하는 동안 발생하는 센서 데이터, 위치 추정, 좌표계, 속도 명령, 경로 계획 데이터를 함께 저장하고, 이를 나중에 다시 재생해 분석 가능한 상태로 만드는 것이었다.

## 2. 완료 상태

상태: 완료

완료한 것:

```text
[x] 기존 Gazebo / RViz2 / Navigation2 노드 정리
[x] ROS2 Humble 환경 확인
[x] TURTLEBOT3_MODEL=burger 확인
[x] ros2 bag 명령어 인식 확인
[x] rosbag2 관련 패키지 확인
[x] turtlebot3_gazebo 패키지 확인
[x] turtlebot3_navigation2 패키지 확인
[x] MissionBot 프로젝트 루트 확인
[x] rosbags/phase06_logging 폴더 생성
[x] TurtleBot3 Gazebo World 실행
[x] Navigation2 실행
[x] RViz2에서 2D Pose Estimate로 AMCL 초기 위치 지정
[x] 기록 대상 topic 선정
[x] /scan, /odom, /tf, /tf_static, /cmd_vel, /amcl_pose, /plan topic 확인
[x] ros2 bag record로 Navigation2 주행 topic 기록
[x] RViz2에서 2D Nav Goal 지정
[x] TurtleBot3 목표 이동 기록
[x] Ctrl + C로 rosbag 기록 종료
[x] ros2 bag info로 기록 결과 확인
[x] metadata.yaml로 bag 파일 구조 확인
[x] ros2 bag play로 playback 확인
[x] topic echo로 /odom playback 메시지 확인
[x] --topics 옵션으로 일부 topic 선택 재생 확인
[x] --rate 옵션으로 playback 속도 조절 확인
[x] RViz2에서 rosbag playback 시각화 확인
[x] use_sim_time=true와 --clock 옵션 필요성 확인
```

## 3. 기록한 rosbag

Bag path:

```text
rosbags/phase06_logging/p06_nav2_goal_01
```

생성된 파일:

```text
rosbags/phase06_logging/p06_nav2_goal_01/metadata.yaml
rosbags/phase06_logging/p06_nav2_goal_01/p06_nav2_goal_01_0.db3
```

bag 정보:

```text
Storage id: sqlite3
Duration: 164.287617550s
Message count: 14,935
Bag size: 8.8 MiB
```

## 4. 기록한 topic

이번 Phase에서 기록한 topic은 다음과 같다.

```text
/scan
/odom
/tf
/tf_static
/cmd_vel
/amcl_pose
/plan
```

topic별 메시지 수:

```text
/scan       793
/odom       4,664
/tf_static  1
/cmd_vel    840
/tf         8,557
/plan       41
/amcl_pose  39
```

## 5. 기록 topic 선정 이유

| Topic      | 선정 이유                                             |
| ---------- | ------------------------------------------------- |
| /scan      | LiDAR 센서가 주변 벽과 장애물을 어떻게 감지했는지 확인하기 위해 기록         |
| /odom      | 로봇의 odometry 위치, 자세, 속도 추정 흐름을 확인하기 위해 기록         |
| /tf        | map, odom, base_footprint 등 동적 좌표계 관계를 확인하기 위해 기록 |
| /tf_static | base_link, base_scan 등 고정 좌표계 관계를 확인하기 위해 기록      |
| /cmd_vel   | Navigation2가 실제로 발행한 속도 명령을 확인하기 위해 기록            |
| /amcl_pose | AMCL이 저장된 map 위에서 추정한 현재 위치를 확인하기 위해 기록           |
| /plan      | Navigation2 planner가 생성한 global path를 확인하기 위해 기록  |

## 6. 핵심 실행 명령

rosbag 기록 명령:

```bash
cd ~/projects/missionbot-ros2

ros2 bag record \
  /scan \
  /odom \
  /tf \
  /tf_static \
  /cmd_vel \
  /amcl_pose \
  /plan \
  -o rosbags/phase06_logging/p06_nav2_goal_01
```

bag 정보 확인:

```bash
ros2 bag info rosbags/phase06_logging/p06_nav2_goal_01
```

metadata 확인:

```bash
cat rosbags/phase06_logging/p06_nav2_goal_01/metadata.yaml | head -n 80
```

기본 playback:

```bash
ros2 bag play rosbags/phase06_logging/p06_nav2_goal_01
```

일부 topic 선택 재생:

```bash
ros2 bag play rosbags/phase06_logging/p06_nav2_goal_01 \
  --topics /odom /cmd_vel \
  --rate 0.5
```

RViz2 playback 시각화:

```bash
rviz2 --ros-args -p use_sim_time:=true
```

```bash
ros2 bag play rosbags/phase06_logging/p06_nav2_goal_01 --rate 0.5 --clock
```

## 7. 확인한 결과

이번 Phase에서 확인한 결과는 다음과 같다.

```text
[x] rosbag2가 기록 대상 topic을 모두 subscribe함
[x] Navigation2 주행 중 /cmd_vel이 기록됨
[x] 목표 이동 중 /plan이 기록됨
[x] AMCL 위치 추정 결과인 /amcl_pose가 기록됨
[x] /scan, /odom, /tf, /tf_static이 함께 기록됨
[x] ros2 bag info에서 topic별 메시지 수 확인
[x] metadata.yaml에서 duration, message_count, topic 정보 확인
[x] ros2 bag play로 저장된 topic 재발행 확인
[x] ros2 topic echo /odom --once로 playback 메시지 확인
[x] --topics로 /odom, /cmd_vel만 선택 재생 확인
[x] --rate 0.5로 playback 속도 조절 확인
[x] RViz2에서 /scan, /odom, /tf, /plan 시각화 확인
```

## 8. 발생한 주요 현상

## 8.1 All requested topics are subscribed. Stopping discovery...

ros2 bag record 실행 중 다음 로그가 출력되었다.

```text
All requested topics are subscribed. Stopping discovery...
```

처음에는 기록이 멈춘 것처럼 보일 수 있지만, 실제로는 정상 로그다.

의미:

```text
요청한 모든 topic을 찾았고 subscribe했다.
새로운 topic을 더 찾는 discovery 과정만 멈췄다.
record 자체는 계속 진행 중이다.
```

따라서 이 로그 이후 RViz2에서 2D Nav Goal을 지정하고, 주행이 끝난 뒤 Ctrl + C로 기록을 종료하면 된다.

## 8.2 Subscription count가 0으로 보이는 현상

ros2 bag play 중 topic info를 확인했을 때 다음과 같이 보였다.

```text
Publisher count: 1
Subscription count: 0
```

이는 정상이다.

의미:

```text
Publisher count: 1
→ rosbag2 player가 해당 topic을 다시 발행하고 있음

Subscription count: 0
→ 현재 해당 topic을 구독 중인 node가 없음
```

ros2 topic echo를 실행하면 해당 명령이 잠깐 subscriber가 되어 메시지를 받을 수 있다.

## 8.3 RViz2에서 playback이 처음에 잘 움직여 보이지 않음

처음에는 일반 rviz2 실행과 bag play만으로는 RViz2에서 움직임이 잘 보이지 않았다.

원인은 Gazebo simulation time 기준으로 기록된 데이터를 RViz2가 실제 컴퓨터 시간 기준으로 보려고 했기 때문으로 판단했다.

해결 방법:

```bash
rviz2 --ros-args -p use_sim_time:=true
```

```bash
ros2 bag play rosbags/phase06_logging/p06_nav2_goal_01 --rate 0.5 --clock
```

결과:

```text
RViz2에서 TF, LaserScan, Odometry, Path가 정상적으로 표시되었다.
```

## 9. 배운 점

Phase 6에서 배운 점은 다음과 같다.

1. rosbag2는 ROS2 topic을 파일로 기록하고 다시 재생할 수 있는 도구다.
2. record는 topic을 저장하고, play는 저장된 topic을 다시 발행한다.
3. bag play는 Gazebo 로봇을 실제로 다시 움직이는 것이 아니다.
4. ros2 bag info를 통해 duration, message count, topic별 기록 수를 확인할 수 있다.
5. metadata.yaml은 bag의 설명서 역할을 한다.
6. .db3 파일에는 실제 메시지 데이터가 저장된다.
7. /tf_static은 고정 좌표계 정보이므로 메시지 수가 적어도 정상이다.
8. --topics 옵션으로 일부 topic만 선택 재생할 수 있다.
9. --rate 옵션으로 playback 속도를 조절할 수 있다.
10. Gazebo 기반 rosbag을 RViz2에서 볼 때는 use_sim_time=true와 --clock 옵션이 중요하다.
11. rosbag은 이후 실패 분석을 위한 핵심 데이터 기반이 된다.

## 10. Phase 5와의 연결

Phase 5에서는 Navigation2를 실행하고, RViz2에서 2D Nav Goal을 찍어 TurtleBot3가 목표 지점까지 이동하는 것을 확인했다.

Phase 6에서는 그 주행 중 발생하는 ROS2 topic을 rosbag2로 기록했다.

연결 흐름:

```text
Phase 5
→ Navigation2 목표 이동 확인

Phase 6
→ Navigation2 목표 이동 중 topic 기록
→ 저장된 bag 재생
→ RViz2에서 기록 데이터 시각화
```

즉, Phase 5가 실시간 주행 확인이었다면, Phase 6은 그 주행을 데이터로 남기고 다시 확인하는 단계였다.

## 11. 다음 Phase와의 연결

다음 Phase는 Failure Analysis다.

Phase 6에서 저장한 정상 주행 bag은 다음 Phase에서 실패 bag과 비교할 기준 데이터가 될 수 있다.

예를 들어 다음과 같은 질문을 분석할 수 있다.

```text
목표 이동 실패 시 /cmd_vel이 발행되었는가?
/plan은 생성되었는가?
/amcl_pose가 튀거나 흔들렸는가?
/scan에 장애물이 어떻게 잡혔는가?
/tf가 정상적으로 연결되어 있었는가?
```

따라서 Phase 6은 MissionBot-ROS2가 단순 실행 프로젝트에서 로그 기반 분석 프로젝트로 넘어가기 위한 기반 단계다.

## 12. 완료 판정

Phase 6은 다음 기준을 만족했으므로 완료로 판단한다.

```text
[x] rosbag2 기록 전 환경 확인
[x] 기록 topic 선정
[x] Navigation2 주행 중 topic 기록
[x] bag 파일 생성 확인
[x] bag 정보 확인
[x] metadata.yaml 확인
[x] playback 확인
[x] 선택 재생 확인
[x] playback 속도 조절 확인
[x] RViz2 playback 시각화 확인
[x] experiment_log 기록
```

## 13. 최종 결론

Phase 6에서는 Navigation2 주행 중 발생하는 핵심 topic을 rosbag2로 저장하고, 저장된 데이터를 다시 재생하여 RViz2에서 확인하는 전체 흐름을 검증했다.

이번 Phase의 가장 중요한 성과는 MissionBot-ROS2가 주행 결과를 단순히 실시간으로 보는 수준을 넘어, 재현 가능한 로그 데이터로 남길 수 있게 되었다는 점이다.

이제 다음 Phase에서는 이 로그 데이터를 기반으로 정상 주행과 실패 주행을 비교하고, 실패 원인을 분류하는 방향으로 넘어갈 수 있다.