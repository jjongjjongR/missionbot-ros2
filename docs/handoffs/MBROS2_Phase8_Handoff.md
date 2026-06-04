# MissionBot-ROS2 Phase 8 인수인계 문서

> 목적: 이 문서는 MissionBot-ROS2 프로젝트의 Phase 8. Control Basics 완료 상태를 정리하고, 다른 채팅창에서 Phase 9. MoveIt2 Basics를 바로 이어가기 위한 인수인계 문서다.
> 이 문서와 아래의 이어가기 프롬프트만 있으면 Phase 8 완료 상태를 복원하고 Phase 9를 시작할 수 있다.

---

## 1. 프로젝트 정체성

MissionBot-ROS2는 UNICON Lab 준비를 위한 ROS2 기반 모바일 매니퓰레이션 준비 프로젝트다.

이 프로젝트는 처음부터 복잡한 모바일 매니퓰레이션을 완성하는 것이 아니라, ROS2와 Gazebo 기반 이동로봇 시스템을 먼저 이해하고 이후 RViz2 / TF2, SLAM, Navigation2, 센서 로그 분석, 실패 분석, 제어 기초, MoveIt2 로봇팔 조작 기초, LLM/VLM 기반 미션 이해까지 단계적으로 연결하는 프로젝트다.

현재 핵심 흐름은 다음이다.

```text
ROS2 기본 구조 이해
→ Gazebo + TurtleBot3 이동로봇 실행
→ RViz2 / TF2로 센서와 좌표계 확인
→ SLAM Toolbox로 지도 생성
→ Navigation2로 목표 지점 이동
→ rosbag2로 센서와 주행 로그 저장
→ 실패 원인 분류
→ 제어 기초 정리
→ MoveIt2와 로봇팔 기초
→ LLM/VLM Mission Understanding
```

---

## 2. 현재 Phase 상태

```text
[x] Phase 0. Project setup
[x] Phase 0.5. Environment setup
[x] Phase 1. ROS2 basics
[x] Phase 2. Gazebo + TurtleBot3
[x] Phase 3. RViz2 + TF2
[x] Phase 4. SLAM
[x] Phase 5. Navigation2
[x] Phase 6. rosbag2 logging
[x] Phase 7. Failure Analysis
[x] Phase 8. Control basics
[ ] Phase 9. MoveIt2 Basics
```

---

## 3. Phase 0 / 0.5 완료 내용

## Phase 0. Project setup

상태: 완료

완료한 것:

```text
[x] GitHub repository 생성
[x] README.md 작성
[x] .gitignore 작성
[x] docs/00_project_overview.md 작성
[x] notes/experiment_log.md 작성
[x] notes/troubleshooting.md 작성
[x] 기본 폴더 구조 생성
```

## Phase 0.5. Environment setup

상태: 기능 검증 완료

완료한 것:

```text
[x] VMware Workstation 17 기반 Ubuntu 22.04 VM 구성
[x] ROS2 Humble 활성화 확인
[x] Gazebo Classic 설치 확인
[x] TurtleBot3 Gazebo 패키지 확인
[x] Tailscale 기반 원격 네트워크 연결 확인
[x] NoMachine 기반 MacBook → Ubuntu VM GUI 접속 확인
[x] VS Code Remote SSH 연결 가능
[x] Gazebo에서 TurtleBot3 Burger spawn 확인
[x] teleop_keyboard로 TurtleBot3 이동 확인
[x] /cmd_vel publisher/subscriber 연결 확인
[x] /odom 출력 확인
[x] /scan 약 5Hz 출력 확인
[x] TurtleBot3 본체가 Gazebo 화면에서 실제로 보이는 것 확인
```

---

## 4. Phase 1 완료 내용

Phase 1. ROS2 basics 상태: 완료

완료한 것:

```text
[x] missionbot_basic Python ROS2 패키지 생성
[x] turtlesim 실행
[x] /turtle1/pose topic 확인
[x] pose_subscriber.py 작성
[x] setup.py entry_points에 pose_subscriber 등록
[x] colcon build
[x] source install/setup.bash 적용
[x] ros2 run으로 pose_subscriber 실행
[x] rqt_graph로 /turtlesim → /turtle1/pose → /pose_subscriber 연결 확인
[x] velocity_publisher.py 작성
[x] setup.py entry_points에 velocity_publisher 등록
[x] /turtle1/cmd_vel topic으로 Twist 메시지 publish
[x] turtlesim 거북이 이동 확인
[x] /clear service 호출
[x] /spawn service 호출
[x] turtlesim_pubsub.launch.py 작성
[x] package.xml에 geometry_msgs, launch, launch_ros 의존성 추가
[x] setup.py data_files에 launch 파일 설치 설정 추가
[x] ros2 launch로 turtlesim_node, pose_subscriber, velocity_publisher 동시 실행
[x] Package not found 오류 해결
```

Phase 1 완료 의미:

```text
ROS2의 기본 실행 흐름을 한 번 경험했다.

패키지 생성
→ 노드 작성
→ setup.py 등록
→ colcon build
→ source install/setup.bash
→ ros2 run 실행
→ topic 확인
→ service 호출
→ launch 실행
→ rqt_graph 확인
```

---

## 5. Phase 2 완료 내용

Phase 2. Gazebo + TurtleBot3 상태: 완료

완료한 것:

```text
[x] 기존 turtlesim 관련 노드가 남아 있지 않은 것 확인
[x] ROS2 Humble 환경 확인
[x] TURTLEBOT3_MODEL=burger 확인
[x] ros2 실행 경로 확인
[x] gazebo 실행 경로 확인
[x] turtlebot3_gazebo 패키지 인식 확인
[x] turtlebot3_teleop 패키지 인식 확인
[x] Gazebo TurtleBot3 empty_world 실행
[x] TurtleBot3 Burger spawn 확인
[x] gzclient crash 발생 확인
[x] gzserver와 ROS2 topic은 살아 있는 것 확인
[x] /cmd_vel topic 확인
[x] /odom topic 확인
[x] /scan topic 확인
[x] teleop_keyboard 실행
[x] 키보드 입력으로 TurtleBot3 이동 확인
[x] /cmd_vel publisher/subscriber 연결 확인
[x] /cmd_vel 실제 Twist 메시지 값 확인
[x] /odom 메시지 출력 확인
[x] TurtleBot3 이동 전후 /odom position 값 변화 확인
[x] /scan LaserScan 메시지 출력 확인
[x] rqt_graph로 /teleop_keyboard → /cmd_vel → Gazebo/TurtleBot3 연결 확인
```

Phase 2 완료 의미:

```text
turtlesim이 아닌 Gazebo TurtleBot3 환경에서 실제 이동로봇 시뮬레이션의 기본 구조를 확인했다.

Gazebo launch
→ TurtleBot3 spawn
→ /cmd_vel 명령
→ teleop 이동
→ /odom 위치 변화 확인
→ /scan LiDAR 데이터 확인
→ rqt_graph 연결 확인
```

---

## 6. Phase 3 완료 내용

Phase 3. RViz2 + TF2 상태: 완료

완료한 것:

```text
[x] RViz2 실행 전 환경 확인
[x] ROS2 Humble 확인
[x] TURTLEBOT3_MODEL=burger 확인
[x] rviz2 실행 경로 확인
[x] TurtleBot3 Gazebo empty_world 실행
[x] /cmd_vel topic 확인
[x] /odom topic 확인
[x] /scan topic 확인
[x] /tf topic 확인
[x] /tf_static topic 확인
[x] RViz2 실행
[x] Fixed Frame을 odom으로 설정
[x] TF display 추가
[x] RobotModel display 추가
[x] LaserScan display 추가
[x] view_frames로 TF tree 생성
[x] odom → base_footprint → base_link → base_scan 연결 확인
[x] tf2_echo로 odom → base_footprint transform 확인
[x] tf2_echo로 base_link → base_scan transform 확인
[x] teleop 이동 중 odom → base_footprint transform 변화 확인
[x] RViz2에서 RobotModel / TF 좌표계 움직임 확인
```

Phase 3 완료 의미:

```text
Gazebo에서 생성되는 TurtleBot3의 topic과 TF 정보를 RViz2에서 시각화했다.

Gazebo TurtleBot3
→ /cmd_vel
→ /odom
→ /scan
→ /tf, /tf_static
→ RViz2
```

---

## 7. Phase 4 완료 내용

Phase 4. SLAM 상태: 완료

완료한 것:

```text
[x] SLAM Toolbox 시작 전 환경 확인
[x] TurtleBot3 Gazebo World 실행
[x] /cmd_vel topic 확인
[x] /odom topic 확인
[x] /scan topic 확인
[x] /tf topic 확인
[x] /tf_static topic 확인
[x] turtlebot3_world에서 /scan ranges에 실제 거리값이 나오는 것 확인
[x] SLAM Toolbox online async 모드 실행
[x] use_sim_time:=True 적용
[x] /slam_toolbox node 확인
[x] /map topic 생성 확인
[x] /map_metadata topic 생성 확인
[x] /map type이 nav_msgs/msg/OccupancyGrid인지 확인
[x] RViz2 Fixed Frame을 map으로 설정
[x] Map display를 /map에 연결
[x] RViz2에서 SLAM 지도 시각화 확인
[x] teleop_keyboard로 TurtleBot3 이동
[x] TurtleBot3 이동에 따라 지도 확장 확인
[x] map_saver_cli로 지도 저장
[x] tb3_world_slam_map_01.pgm 생성 확인
[x] tb3_world_slam_map_01.yaml 생성 확인
[x] PGM 출력 시 깨진 문자처럼 보이는 내용이 이미지 픽셀 데이터임을 확인
```

Phase 4 완료 의미:

```text
TurtleBot3의 /scan, /odom, /tf 정보를 SLAM Toolbox에 연결해 실제 /map 지도를 생성했다.

RViz2에서 지도 생성 과정을 시각적으로 확인했고, teleop 이동으로 지도 확장을 확인했다.

마지막으로 생성된 지도를 .pgm / .yaml 파일로 저장했다.
```

저장된 지도 파일:

```text
maps/phase04_slam/tb3_world_slam_map_01.pgm
maps/phase04_slam/tb3_world_slam_map_01.yaml
```

저장된 yaml 내용:

```yaml
image: tb3_world_slam_map_01.pgm
mode: trinary
resolution: 0.05
origin: [-2.94, -2.57, 0]
negate: 0
occupied_thresh: 0.65
free_thresh: 0.25
```

---

## 8. Phase 5 완료 내용

Phase 5. Navigation2 상태: 완료

완료한 것:

```text
[x] Navigation2 실행 전 환경 확인
[x] nav2_bringup 패키지 인식 확인
[x] nav2_map_server 패키지 인식 확인
[x] nav2_amcl 패키지 인식 확인
[x] turtlebot3_navigation2 패키지 인식 확인
[x] Phase 4에서 저장한 map 파일 확인
[x] TurtleBot3 Gazebo World 실행
[x] /clock, /cmd_vel, /odom, /scan, /tf, /tf_static topic 확인
[x] 저장된 map yaml 파일 절대 경로 설정
[x] turtlebot3_navigation2 navigation2.launch.py 실행
[x] use_sim_time:=True 적용
[x] /map topic 생성 확인
[x] /map type이 nav_msgs/msg/OccupancyGrid인지 확인
[x] /amcl node 실행 확인
[x] /map_server node 실행 확인
[x] /planner_server node 실행 확인
[x] /controller_server node 실행 확인
[x] /bt_navigator node 실행 확인
[x] RViz2 Fixed Frame을 map으로 설정
[x] RViz2에서 Map, RobotModel, TF, LaserScan display 확인
[x] 2D Pose Estimate로 AMCL 초기 위치 지정
[x] /amcl_pose topic 출력 확인
[x] map → odom transform 생성 확인
[x] 2D Nav Goal로 목표 지점 지정
[x] TurtleBot3가 목표 지점 방향으로 이동하는 것 확인
[x] /plan topic으로 global path 생성 확인
[x] /cmd_vel topic으로 속도 명령 발행 확인
[x] 주요 Nav2 lifecycle node가 active [3] 상태인지 확인
```

Phase 5 완료 의미:

```text
Phase 4에서 생성한 지도를 Navigation2에 연결했고, TurtleBot3가 저장된 map 위에서 현재 위치를 추정한 뒤 RViz2에서 지정한 목표 지점까지 이동하는 것을 확인했다.

이를 통해 MissionBot-ROS2는 수동 조작 중심의 이동로봇 확인 단계를 넘어, 저장된 map 기반 자율 주행 흐름을 처음으로 검증했다.
```

---

## 9. Phase 6 완료 내용

Phase 6. rosbag2 logging 상태: 완료

완료한 것:

```text
[x] 기존 Gazebo / RViz2 / Navigation2 노드 정리
[x] ROS2 Humble 환경 확인
[x] TURTLEBOT3_MODEL=burger 확인
[x] ros2 bag 명령어 인식 확인
[x] rosbag2 관련 패키지 확인
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

정상 bag:

```text
rosbags/phase06_logging/p06_nav2_goal_01
```

정상 bag 정보:

```text
Storage id: sqlite3
Duration: 164.287617550s
Messages: 14935
Bag size: 8.8 MiB
```

정상 bag topic count:

```text
/scan       793
/odom       4664
/tf_static  1
/cmd_vel    840
/tf         8557
/plan       41
/amcl_pose  39
```

Phase 6 완료 의미:

```text
Navigation2 주행 중 발생하는 핵심 ROS2 topic을 rosbag2로 기록하고, 저장된 bag 파일을 다시 재생하여 RViz2에서 확인하는 전체 흐름을 검증했다.

이를 통해 MissionBot-ROS2는 주행 결과를 실시간으로 보는 수준을 넘어, 재현 가능한 로그 데이터로 남길 수 있게 되었다.
```

---

## 10. Phase 7 완료 내용

Phase 7. Failure Analysis 상태: 완료

완료한 것:

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
[x] README.md Result 섹션에 Phase 7 Summary 추가
[x] notes/phase_summaries/phase07_failure_analysis_summary.md 작성
```

첫 실패 사례:

```text
P07-FAIL-0001_unreachable_goal_test
```

실패 bag:

```text
rosbags/failure_cases/P07-FAIL-0001_unreachable_goal_test
```

실패 분석 문서:

```text
results/failure_cases/P07-FAIL-0001_unreachable_goal_test.md
```

실패 bag 정보:

```text
Files:             P07-FAIL-0001_unreachable_goal_test_0.db3
Bag size:          5.2 MiB
Storage id:        sqlite3
Duration:          92.231500380s
Messages:          9038
```

실패 bag topic count:

```text
/cmd_vel     1034
/plan        51
/amcl_pose   58
/scan        447
/odom        2628
/tf_static   1
/tf          4819
```

최종 판정:

```text
Failure Type: goal_unreachable
Root Cause: 장애물 내부 또는 도달하기 어려운 위치를 2D Nav Goal로 지정하여, Navigation2가 목표 근처까지 접근했지만 최종 목표에 도달하지 못했다.
Secondary Symptom: control_oscillation
Confidence: high
```

Phase 7 완료 의미:

```text
Phase 6에서 기록한 정상 Navigation2 주행 bag을 baseline으로 삼고, 실패 상황을 rosbag2로 기록한 뒤 ROS2 topic 증거를 기준으로 실패 유형을 분류했다.

이를 통해 MissionBot-ROS2는 단순히 Navigation2 주행 성공 여부를 확인하는 수준에서 나아가, 실패 상황을 재현 가능한 로그 데이터로 남기고 원인을 분류하는 기본 Failure Analysis 흐름을 갖추게 되었다.
```

---

## 11. Phase 8 완료 내용

Phase 8. Control basics 상태: 완료

완료한 것:

```text
[x] 기존 Gazebo / RViz2 / Nav2 관련 노드 정리
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

Phase 8 완료 의미:

```text
MissionBot-ROS2는 이제 Navigation2가 자동으로 생성하던 /cmd_vel 명령을 기초 제어 관점에서 직접 이해하고, 간단한 Python ROS2 node로 속도 명령을 발행할 수 있게 되었다.

이를 통해 /cmd_vel 입력과 /odom 반응의 기본 관계를 직접 실습하고 검증했다.
```

---

## 12. Phase 8 핵심 개념 요약

## 12.1 Control

```text
Control은 로봇을 원하는 방향과 속도로 움직이게 만드는 과정이다.
```

이번 Phase에서는 복잡한 PID, MPC, 강화학습 제어로 가지 않고, 가장 기본적인 속도 명령과 반응만 확인했다.

---

## 12.2 /cmd_vel

```text
/cmd_vel은 로봇에게 보내는 속도 명령 topic이다.
```

메시지 타입:

```text
geometry_msgs/msg/Twist
```

중요 필드:

```text
linear.x
→ 로봇 기준 전진/후진 속도

angular.z
→ 로봇 기준 회전 속도
```

---

## 12.3 /odom

```text
/odom은 로봇의 위치, 자세, 속도 추정 정보를 담는 topic이다.
```

메시지 타입:

```text
nav_msgs/msg/Odometry
```

중요 필드:

```text
pose.pose.position.x
pose.pose.position.y
pose.pose.orientation.z
pose.pose.orientation.w
twist.twist.linear.x
twist.twist.angular.z
```

---

## 12.4 Open-loop Control

```text
Open-loop control은 피드백 없이 정해진 명령을 정해진 시간 동안 보내는 방식이다.
```

이번 Phase에서는 `/odom`을 읽어 실시간으로 명령을 보정하지 않았다.

대신 다음 방식으로 실습했다.

```text
전진 명령 발행
→ /odom position 변화 확인

회전 명령 발행
→ /odom orientation 변화 확인
```

---

## 12.5 Python Control Node

터미널에서 직접 `/cmd_vel`을 publish하던 실습을 Python ROS2 node로 옮겼다.

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

---

## 13. Phase 8 주요 실험 결과

## 13.1 /cmd_vel - /odom topic 확인

확인 결과:

```text
/cmd_vel
Type: geometry_msgs/msg/Twist
Publisher count: 0
Subscription count: 1
Node name: turtlebot3_diff_drive
```

해석:

```text
아직 /cmd_vel을 보내는 publisher는 없지만, TurtleBot3 diff drive plugin이 /cmd_vel을 받을 준비가 되어 있었다.
```

확인 결과:

```text
/odom
Type: nav_msgs/msg/Odometry
Publisher count: 1
```

해석:

```text
Gazebo TurtleBot3가 /odom을 publish하고 있었다.
```

---

## 13.2 전진 open-loop control 결과

사용한 명령의 핵심 값:

```text
linear.x = 0.10
angular.z = 0.0
```

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

해석:

```text
실제 이동 거리는 약 0.231m로 기대값 0.20m와 비교적 가까웠다.
전진 실험에서는 position 값이 변했고, orientation 값은 거의 유지되었다.
```

정리:

```text
/cmd_vel linear.x
→ /odom position 변화
```

---

## 13.3 회전 open-loop control 결과

사용한 명령의 핵심 값:

```text
linear.x = 0.0
angular.z = 1.0
```

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
position 변화는 매우 작았고, orientation 변화는 크게 나타났다.
```

정리:

```text
/cmd_vel angular.z
→ /odom orientation 변화
```

---

## 13.4 전진 / 회전 반응 비교

| 비교 항목                | 전진 실험                  | 회전 실험                        |
| -------------------- | ---------------------- | ---------------------------- |
| `/cmd_vel linear.x`  | 0.10                   | 0.0                          |
| `/cmd_vel angular.z` | 0.0                    | 1.0                          |
| 주로 변한 `/odom` 값      | position.x, position.y | orientation.z, orientation.w |
| position 변화          | 큼                      | 작음                           |
| orientation 변화       | 거의 없음                  | 큼                            |
| 해석                   | 현재 바라보는 방향으로 이동        | 제자리 회전                       |

핵심 결론:

```text
linear.x
→ 로봇 기준 앞 방향 속도
→ /odom position 변화로 확인

angular.z
→ 로봇 기준 회전 속도
→ /odom orientation 변화로 확인
```

---

## 14. Phase 8에서 발생한 주요 현상

## 14.1 /odom 명령 오타

상황:

```bash
ros2 topic echo /odom --onceros2 topic echo /odom --once
```

판단:

```text
명령어 두 개가 붙어서 ROS2가 --onceros2라는 잘못된 옵션으로 해석했다.
```

정상 명령:

```bash
ros2 topic echo /odom --once
```

처리:

```text
명령어를 한 줄씩 분리해서 다시 실행했고, /odom 메시지를 정상 확인했다.
```

---

## 14.2 정지 명령을 한 번만 보냈을 때 로봇이 바로 멈추지 않는 현상

상황:

```text
회전 실험 중 정지 명령을 --once로 한 번만 보냈을 때 로봇이 바로 멈추지 않았다.
사용자가 직접 정지시켰다.
```

판단:

```text
정지 명령을 한 번만 보내면 실제 제어에서 안정적으로 반영되지 않을 수 있다.
```

보완:

```text
정지 명령은 일정 시간 동안 반복 발행하는 방식이 더 안전하다.
```

예시:

```bash
timeout 1 ros2 topic pub --rate 20 /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"
```

Python `open_loop_controller.py`에서는 정지 구간을 1초 동안 두어 정지 명령을 반복 발행했다.

결과:

```text
Gazebo에서 전진 → 정지 → 회전 → 정지 동작을 확인했고, 마지막에 로봇이 정상적으로 멈췄다.
```

---

## 15. Phase 8 주요 명령어

## 15.1 /cmd_vel, /odom topic 확인

```bash
ros2 topic list | grep -E "cmd_vel|odom|tf"
ros2 topic info /cmd_vel -v
ros2 topic info /odom
ros2 topic echo /odom --once
```

---

## 15.2 전진 open-loop control

```bash
ros2 topic pub --rate 10 /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.10, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}" &
PUB_PID=$!
sleep 2
kill $PUB_PID
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"
```

---

## 15.3 회전 open-loop control

```bash
ros2 topic pub --rate 10 /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 1.0}}" &
PUB_PID=$!
sleep 3
kill $PUB_PID
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"
```

---

## 15.4 안전 정지 명령

```bash
timeout 1 ros2 topic pub --rate 20 /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"
```

---

## 15.5 Python control node 빌드 및 실행

```bash
cd ~/projects/missionbot-ros2

colcon build --packages-select missionbot_basic

source install/setup.bash

ros2 pkg executables missionbot_basic

ros2 run missionbot_basic open_loop_controller
```

---

## 16. Phase 8 기록 파일

Phase 8 관련 정리 파일:

```text
README.md
notes/experiment_log.md
docs/phases/phase08_control_basics.md
notes/phase_summaries/phase08_control_basics_summary.md
docs/handoffs/MBROS2_Phase8_Handoff.md
docs/handoffs/MBROS2_Phase8_prompt.md
```

Phase 8에서 추가된 코드 파일:

```text
src/missionbot_basic/missionbot_basic/open_loop_controller.py
```

Phase 8에서 수정된 파일:

```text
src/missionbot_basic/setup.py
```

README 업데이트 내용:

```text
Result 섹션에 Phase 8 Summary 추가
```

experiment_log 업데이트 내용:

```text
P08-EXP-0001_cmd_vel_odom_topic_check
P08-EXP-0002_open_loop_forward_control
P08-EXP-0003_open_loop_rotation_control
P08-EXP-0004_python_open_loop_controller_node
```

troubleshooting 정리 여부:

```text
정식 troubleshooting 항목은 필수로 추가하지 않는다.

정지 명령을 --once로 한 번만 보냈을 때 바로 멈추지 않은 현상은 시스템 오류라기보다 제어 명령 발행 방식의 주의사항에 가깝다.
따라서 docs/phases/phase08_control_basics.md와 phase summary의 Notes에 기록하는 것으로 충분하다.
```

---

## 17. 현재 프로젝트 폴더 기준

README 기준으로 MissionBot-ROS2 프로젝트는 루트 바로 아래 `src/`를 ROS2 패키지 작성 위치로 사용한다.

주의:

```text
missionbot_ws/src 구조를 만들지 않는다.
```

현재 기준 구조:

```text
missionbot-ros2/
├── README.md
├── docs/
│   ├── phases/
│   │   ├── phase05_navigation2.md
│   │   ├── phase06_rosbag2_logging.md
│   │   ├── phase07_failure_analysis.md
│   │   └── phase08_control_basics.md
│   ├── concepts/
│   ├── templates/
│   └── handoffs/
│       ├── MBROS2_Phase8_Handoff.md
│       └── MBROS2_Phase8_prompt.md
│
├── src/
│   └── missionbot_basic/
│       ├── missionbot_basic/
│       │   ├── pose_subscriber.py
│       │   ├── velocity_publisher.py
│       │   └── open_loop_controller.py
│       └── setup.py
│
├── configs/
├── maps/
│   └── phase04_slam/
│       ├── tb3_world_slam_map_01.pgm
│       └── tb3_world_slam_map_01.yaml
│
├── rosbags/
│   ├── phase06_logging/
│   │   └── p06_nav2_goal_01/
│   └── failure_cases/
│       └── P07-FAIL-0001_unreachable_goal_test/
│
├── results/
│   └── failure_cases/
│       ├── failure_case_template.md
│       └── P07-FAIL-0001_unreachable_goal_test.md
│
└── notes/
    ├── experiment_log.md
    ├── troubleshooting.md
    ├── daily_logs/
    ├── phase_summaries/
    │   ├── phase06_rosbag2_logging_summary.md
    │   ├── phase07_failure_analysis_summary.md
    │   └── phase08_control_basics_summary.md
    └── handoff_notes/
```

현재 프로젝트 루트에서 확인되는 기본 폴더:

```text
build
configs
docs
install
log
maps
notes
README.md
results
rosbags
src
```

`build`, `install`, `log`는 `colcon build` 수행으로 생성된 ROS2 빌드 산출물이다.

---

## 18. 최종 확정 환경

```text
Development Client:
MacBook

Remote Network:
Tailscale

Remote GUI:
NoMachine

Code Editing:
Antigravity IDE
VS Code Remote SSH 가능

Host:
Windows Desktop

Virtualization:
VMware Workstation 17

Guest OS:
Ubuntu 22.04 LTS

ROS2:
Humble Hawksbill

Simulator:
Gazebo Classic 11.10.2

Robot:
TurtleBot3 Burger

Visualization:
RViz2

SLAM:
slam_toolbox

Navigation:
Navigation2

Logging:
rosbag2

Failure Analysis:
rosbag2 기반 topic 증거 분석

Control:
Python ROS2 node 기반 open-loop /cmd_vel 제어

Main TurtleBot3 Workspace:
~/turtlebot3_ws

MissionBot Project Location:
~/projects/missionbot-ros2
```

---

## 19. 현재 .bashrc 기준

새 터미널을 열면 `.bashrc`가 자동 실행되고, 아래 환경이 적용된다.

```text
ROS2 Humble
TurtleBot3 workspace
TURTLEBOT3_MODEL=burger
GAZEBO_MODEL_PATH
```

새 터미널을 열면 다음 문구가 자동으로 출력된다.

```text
ROS2 humble is activated!
```

이 문구는 사용자가 의도적으로 유지하는 환경 적용 확인 메시지다.

주의:

```text
source ~/.bashrc를 매번 다시 실행할 필요는 없다.
```

다만, MissionBot 프로젝트에서 직접 만든 패키지를 실행하려면 별도로 아래 명령이 필요하다.

```bash
cd ~/projects/missionbot-ros2
source install/setup.bash
```

이 둘의 역할은 다르다.

```text
source ~/.bashrc
→ ROS2 Humble, TurtleBot3 workspace, Gazebo model path 등 기본 환경 적용

source install/setup.bash
→ MissionBot 프로젝트에서 colcon build로 만든 패키지를 현재 터미널이 인식
```

TurtleBot3 Gazebo, RViz2, SLAM Toolbox, Navigation2, rosbag2 같은 외부 ROS2 패키지를 실행할 때는 `.bashrc`로 기본 ROS2/TurtleBot3 환경이 잡혀 있으면 충분한 경우가 많다.

직접 만든 `open_loop_controller`를 실행할 때는 반드시 프로젝트 루트에서 다음을 적용한다.

```bash
cd ~/projects/missionbot-ros2
source install/setup.bash
```

---

## 20. Phase 8 완료 판정

Phase 8은 다음 기준을 만족했으므로 완료로 판단한다.

```text
[x] /cmd_vel topic 확인
[x] /odom topic 확인
[x] /cmd_vel publisher/subscriber 구조 확인
[x] turtlebot3_diff_drive가 /cmd_vel을 subscribe하는 것 확인
[x] /odom이 publish되는 것 확인
[x] teleop_keyboard로 /cmd_vel 값 변화 확인
[x] 이동 후 /odom position/orientation 변화 확인
[x] open-loop 전진 명령 발행
[x] 전진 명령 후 /odom position 변화 확인
[x] open-loop 회전 명령 발행
[x] 회전 명령 후 /odom orientation 변화 확인
[x] 전진과 회전의 /odom 반응 비교
[x] open_loop_controller.py 작성
[x] setup.py entry point 등록
[x] colcon build 성공
[x] ros2 pkg executables에서 open_loop_controller 확인
[x] ros2 run missionbot_basic open_loop_controller 실행
[x] Gazebo에서 전진 → 정지 → 회전 → 정지 확인
[x] 마지막 정지 확인
[x] README Result 섹션 업데이트
[x] notes/phase_summaries/phase08_control_basics_summary.md 작성
[x] notes/experiment_log.md에 Phase 8 실험 기록 추가
[x] docs/phases/phase08_control_basics.md 작성
[x] handoff 문서 작성
```

완료 의미:

```text
MissionBot-ROS2는 Navigation2가 생성하던 /cmd_vel 속도 명령을 제어 기초 관점에서 직접 이해하고, Python ROS2 node로 open-loop 제어 명령을 발행할 수 있게 되었다.

이제 다음 Phase에서 MoveIt2와 로봇팔 조작 기초를 시작하기 전에, 모바일 베이스의 기본 속도 명령과 반응 구조를 이해한 상태가 되었다.
```

---

## 21. 다음 Phase 시작 목표

다음 Phase:

```text
Phase 9. MoveIt2 Basics
```

Phase 9의 핵심 목표:

```text
MoveIt2와 로봇팔 조작 기초를 이해하기 위한 환경과 기본 개념을 확인한다.
```

단, Phase 9 시작 시 처음부터 복잡한 모바일 매니퓰레이션 전체 구현으로 가지 않는다.

첫 단계에서는 다음을 확인한다.

```text
1. 기존 Gazebo / RViz2 / control node 정리
2. ROS2 Humble 환경 확인
3. MoveIt2 관련 패키지 설치 여부 확인
4. MoveIt2가 어떤 역할을 하는지 개념 정리
5. 현재 MissionBot 구조에서 MoveIt2가 어느 위치에 연결되는지 확인
```

Phase 9에서 중요하게 연결될 개념:

```text
MoveIt2
→ ROS2에서 로봇팔 motion planning을 다루는 대표 프레임워크

motion planning
→ 로봇팔이 충돌 없이 목표 자세까지 움직이는 경로를 계산하는 과정

planning scene
→ 로봇과 주변 환경, 장애물 정보를 포함한 계획 공간

robot model
→ URDF / SRDF 기반 로봇 구조 정보

joint
→ 로봇팔 관절

end-effector
→ 로봇팔 끝단 도구 또는 손

trajectory
→ 시간에 따른 관절 움직임 경로
```

주의:

```text
Phase 9에서는 LLM/VLM, VLA, 완전한 모바일 매니퓰레이션으로 앞서가지 않는다.
우선 MoveIt2가 무엇이고, ROS2 로봇팔 조작에서 어떤 역할을 하는지 확인하는 것부터 시작한다.
```

---

## 22. Phase 9 시작 전 확인 명령

새 터미널에서 확인:

```bash
cd ~/projects/missionbot-ros2
pwd

ros2 node list

echo $ROS_DISTRO
echo $TURTLEBOT3_MODEL

which ros2
which gazebo
which rviz2

ros2 pkg list | grep moveit
ros2 pkg list | grep moveit_ros
ros2 pkg list | grep moveit_configs
```

정상 기대값은 아직 확정하지 않는다.

이유:

```text
MoveIt2가 현재 설치되어 있는지 아직 확인하지 않았다.
```

따라서 다음 채팅의 첫 목표는 다음이다.

```text
Phase 9-1. MoveIt2 시작 전 환경 확인과 설치 여부 점검
```

첫 단계에서 할 일:

```text
1. 기존 노드 정리 확인
2. ROS2 Humble 환경 확인
3. MissionBot 프로젝트 루트 확인
4. MoveIt2 관련 패키지 인식 여부 확인
5. 설치되어 있지 않다면 설치 필요 여부 판단
```

---

## 23. Phase 9에서 주의할 점

```text
Phase 9에서는 MoveIt2 기초만 다룬다.
처음부터 모바일 매니퓰레이션 전체 구조, LLM/VLM 미션 이해, VLA, 실제 로봇팔 제어까지 앞서가지 않는다.
```

다만 한 문장 정도로 연결은 가능하다.

좋은 연결:

```text
MoveIt2는 나중에 모바일 매니퓰레이션에서 로봇팔이 물체를 잡거나 특정 위치로 이동하기 위한 motion planning 기반이 된다.
```

첫 단계에서는 다음 정도만 다룬다.

```text
MoveIt2가 무엇인지
ROS2에서 어디에 쓰이는지
설치되어 있는지
어떤 패키지와 예제가 있는지
다음 실습을 어떤 기준으로 잡을지
```

---

## 24. 다음 채팅 시작 지점

다음 채팅에서는 아래 상태에서 시작하면 된다.

```text
현재 MissionBot-ROS2는 Phase 8. Control Basics를 완료했다.

완료한 것:
- /cmd_vel과 /odom 관계 복습
- /cmd_vel publisher/subscriber 구조 확인
- turtlebot3_diff_drive가 /cmd_vel을 subscribe하는 것 확인
- /odom이 Gazebo TurtleBot3에서 publish되는 것 확인
- teleop_keyboard로 /cmd_vel 값 변화 확인
- ros2 topic pub으로 open-loop 전진 명령 발행
- linear.x = 0.10 명령에 따른 /odom position 변화 확인
- ros2 topic pub으로 open-loop 회전 명령 발행
- angular.z = 1.0 명령에 따른 /odom orientation 변화 확인
- 전진 명령과 회전 명령의 /odom 반응 비교
- open_loop_controller.py 작성
- setup.py entry_points에 open_loop_controller 등록
- colcon build 성공
- ros2 run missionbot_basic open_loop_controller 실행
- Gazebo에서 전진 → 정지 → 회전 → 정지 확인
- 마지막 정지 확인
- README Result 섹션 업데이트
- docs/phases/phase08_control_basics.md 작성
- notes/phase_summaries/phase08_control_basics_summary.md 작성
- notes/experiment_log.md에 Phase 8 실험 기록 추가

주요 결과물:
- src/missionbot_basic/missionbot_basic/open_loop_controller.py
- src/missionbot_basic/setup.py
- docs/phases/phase08_control_basics.md
- notes/phase_summaries/phase08_control_basics_summary.md
- notes/experiment_log.md의 P08-EXP-0001~0004
- docs/handoffs/MBROS2_Phase8_Handoff.md
- docs/handoffs/MBROS2_Phase8_prompt.md

다음 목표:
- Phase 9. MoveIt2 Basics 시작
- 첫 단계는 MoveIt2 시작 전 환경 확인과 패키지 설치 여부 점검
```

추천 시작점:

```text
Phase 9-1. MoveIt2 시작 전 환경 확인과 설치 여부 점검
```

첫 단계에서 할 일:

```text
1. 기존 Gazebo / RViz2 / control node가 남아 있지 않은지 확인
2. ROS2 Humble 환경 확인
3. MissionBot 프로젝트 위치 확인
4. MoveIt2 관련 패키지 인식 여부 확인
5. MoveIt2가 없으면 설치가 필요한지 판단
6. MoveIt2가 있으면 다음 실습 기준을 잡기
```
