# Phase 9. MoveIt2 Basics

## 1. Phase 목표

Phase 9의 목표는 MoveIt2를 이용해 로봇팔 조작 기초를 이해하는 것이다.

이 Phase에서는 실제 로봇팔 하드웨어 제어나 복잡한 manipulation task를 구현하지 않는다. 대신 Panda demo robot arm을 사용해 MoveIt2의 기본 실행 구조를 확인한다.

핵심 목표는 다음과 같다.

```text
MoveIt2 설치 및 패키지 확인
→ Panda robot description / moveit config 확인
→ RViz2에서 Panda 로봇팔 표시
→ MotionPlanning display 추가
→ Planning Group 이해
→ Goal State 설정
→ Plan 실행
→ Execute 실행
→ node / topic / controller 구조 확인
```

---

## 2. 이번 Phase에서 다루는 범위

포함하는 것:

```text
MoveIt2 설치
MoveIt2 핵심 패키지 확인
moveit_msgs 인터페이스 확인
Panda demo resource 확인
RViz2 MotionPlanning display 사용
Planning Group 개념 이해
Planning Scene 개념 이해
move_group 역할 이해
OMPL / RRTConnect planner 확인
ros2_control controller 상태 확인
Plan과 Execute 차이 이해
```

포함하지 않는 것:

```text
실제 로봇팔 하드웨어 제어
복잡한 grasping task 구현
모바일 매니퓰레이션 전체 구현
LLM/VLM 기반 manipulation 명령 생성
로봇팔 강화학습
저수준 controller 직접 설계
```

---

## 3. 시작 전 환경

현재 프로젝트 환경은 다음과 같다.

```text
Host: Windows Desktop
Virtualization: VMware Workstation 17
Guest OS: Ubuntu 22.04 LTS
ROS2: Humble Hawksbill
Simulator: Gazebo Classic 11.10.2
Visualization: RViz2
Robot: TurtleBot3 Burger
MoveIt2 demo robot: Panda robot arm
Project path: ~/projects/missionbot-ros2
TurtleBot3 workspace: ~/turtlebot3_ws
```

새 터미널을 열면 다음 문구가 출력된다.

```text
ROS2 humble is activated!
```

이 문구는 `.bashrc`가 정상 적용되었다는 확인 메시지다.

---

## 4. Phase 9-1. 시작 전 환경 확인

먼저 프로젝트 루트로 이동했다.

```bash
cd ~/projects/missionbot-ros2
pwd
```

확인 결과:

```text
/home/user/projects/missionbot-ros2
```

기존 ROS2 node 확인:

```bash
ros2 node list
```

처음에는 이전 Gazebo / TurtleBot3 관련 node가 남아 있었다.

```text
/gazebo
/robot_state_publisher
/turtlebot3_diff_drive
/turtlebot3_imu
/turtlebot3_joint_state
/turtlebot3_laserscan
```

MoveIt2 실습 전에는 기존 Gazebo node를 정리해야 하므로, 관련 터미널에서 Ctrl + C로 종료했다.

정리 후 확인:

```bash
ros2 node list
```

결과:

```text
출력 없음
```

의미:

```text
MoveIt2 demo 실행 전 기존 ROS2 node가 남아 있지 않은 상태가 되었다.
```

환경 확인:

```bash
echo $ROS_DISTRO
echo $TURTLEBOT3_MODEL

which ros2
which gazebo
which rviz2
```

확인 결과:

```text
humble
burger
/opt/ros/humble/bin/ros2
/usr/bin/gazebo
/opt/ros/humble/bin/rviz2
```

---

## 5. Phase 9-2. MoveIt2 설치 확인 및 설치

처음 MoveIt2 패키지 확인 명령을 실행했다.

```bash
ros2 pkg list | grep moveit
ros2 pkg list | grep moveit_ros
ros2 pkg list | grep moveit_configs
```

초기 상태에서는 MoveIt2 관련 패키지가 출력되지 않았다.

따라서 MoveIt2를 설치했다.

```bash
sudo apt update
sudo apt install -y ros-humble-moveit
```

설치 후 다시 확인했다.

```bash
ros2 pkg list | grep moveit
ros2 pkg list | grep moveit_ros
ros2 pkg list | grep moveit_configs
```

확인된 주요 패키지:

```text
moveit
moveit_common
moveit_configs_utils
moveit_core
moveit_kinematics
moveit_msgs
moveit_planners
moveit_planners_chomp
moveit_planners_ompl
moveit_plugins
moveit_ros
moveit_ros_benchmarks
moveit_ros_move_group
moveit_ros_occupancy_map_monitor
moveit_ros_planning
moveit_ros_planning_interface
moveit_ros_robot_interaction
moveit_ros_visualization
moveit_ros_warehouse
moveit_setup_app_plugins
moveit_setup_assistant
moveit_setup_controllers
moveit_setup_core_plugins
moveit_setup_framework
moveit_setup_srdf_plugins
moveit_simple_controller_manager
```

판정:

```text
MoveIt2 본체 설치 성공
```

---

## 6. Phase 9-3. MoveIt2 핵심 패키지 구조 확인

MoveIt2의 핵심 실행 파일을 확인했다.

```bash
ros2 pkg executables moveit_setup_assistant
ros2 pkg executables moveit_ros_move_group
ros2 pkg executables moveit_ros_visualization
ros2 pkg executables moveit_ros_planning_interface
```

확인 결과:

```text
moveit_setup_assistant collisions_updater
moveit_setup_assistant moveit_setup_assistant
moveit_ros_move_group list_move_group_capabilities
moveit_ros_move_group load_map
moveit_ros_move_group move_group
moveit_ros_move_group save_map
```

중요한 실행 파일:

```text
moveit_setup_assistant moveit_setup_assistant
moveit_ros_move_group move_group
```

의미:

```text
moveit_setup_assistant
→ 로봇 모델을 MoveIt2 설정 패키지로 구성하기 위한 도구

move_group
→ MoveIt2의 중심 노드
→ planning 요청을 받고 planning pipeline으로 전달
→ trajectory execution 흐름을 관리
```

---

## 7. Phase 9-4. moveit_msgs 인터페이스 확인

MoveIt2가 사용하는 ROS2 interface를 확인했다.

```bash
ros2 interface list | grep moveit_msgs | head -n 30
```

확인 결과:

```text
moveit_msgs/msg/AllowedCollisionEntry
moveit_msgs/msg/AllowedCollisionMatrix
moveit_msgs/msg/AttachedCollisionObject
moveit_msgs/msg/BoundingVolume
moveit_msgs/msg/CartesianPoint
moveit_msgs/msg/CartesianTrajectory
moveit_msgs/msg/CartesianTrajectoryPoint
moveit_msgs/msg/CollisionObject
moveit_msgs/msg/ConstraintEvalResult
moveit_msgs/msg/Constraints
moveit_msgs/msg/ContactInformation
moveit_msgs/msg/CostSource
moveit_msgs/msg/DisplayRobotState
moveit_msgs/msg/DisplayTrajectory
moveit_msgs/msg/GenericTrajectory
moveit_msgs/msg/Grasp
moveit_msgs/msg/GripperTranslation
moveit_msgs/msg/JointConstraint
moveit_msgs/msg/JointLimits
moveit_msgs/msg/KinematicSolverInfo
moveit_msgs/msg/LinkPadding
moveit_msgs/msg/LinkScale
moveit_msgs/msg/MotionPlanDetailedResponse
moveit_msgs/msg/MotionPlanRequest
moveit_msgs/msg/MotionPlanResponse
moveit_msgs/msg/MotionSequenceItem
moveit_msgs/msg/MotionSequenceRequest
moveit_msgs/msg/MotionSequenceResponse
moveit_msgs/msg/MoveItErrorCodes
moveit_msgs/msg/ObjectColor
```

주요 의미:

```text
MotionPlanRequest
→ motion planning 요청

MotionPlanResponse
→ motion planning 결과 응답

DisplayTrajectory
→ RViz2에서 trajectory를 시각화하기 위한 메시지

CollisionObject
→ planning scene에 추가되는 충돌 객체

JointConstraint
→ 관절 제약 조건

JointLimits
→ 관절 제한 정보
```

---

## 8. Phase 9-5. Panda demo resource 확인

MoveIt2 본체 설치 후 Panda demo resource가 있는지 확인했다.

```bash
ros2 pkg list | grep moveit_resources
ros2 pkg list | grep panda
ros2 pkg list | grep moveit2_tutorials
```

초기에는 출력이 없었다.

Panda demo 실행을 시도했다.

```bash
ros2 launch moveit_resources_panda_moveit_config demo.launch.py
```

오류:

```text
Package 'moveit_resources_panda_moveit_config' not found
```

판단:

```text
MoveIt2 본체는 설치되었지만 Panda demo resource 패키지는 아직 없는 상태였다.
```

이후 Panda resource 설치 후 다음 패키지를 확인했다.

```bash
ros2 pkg list | grep moveit_resources
ros2 pkg list | grep panda
```

확인 결과:

```text
moveit_resources_panda_description
moveit_resources_panda_moveit_config
moveit_resources_panda_description
moveit_resources_panda_moveit_config
```

의미:

```text
moveit_resources_panda_description
→ Panda 로봇팔의 로봇 모델 정보

moveit_resources_panda_moveit_config
→ Panda 로봇팔을 MoveIt2에서 사용하기 위한 설정 패키지
```

---

## 9. Phase 9-6. Panda MoveIt2 demo 실행

Panda MoveIt2 demo를 실행했다.

```bash
ros2 launch moveit_resources_panda_moveit_config demo.launch.py
```

확인한 것:

```text
[x] RViz2 실행
[x] Panda 로봇팔 모델 표시
[x] Global Status: Ok
[x] PlanningScene display 표시
[x] Trajectory display 표시
[x] move_group 관련 로그 확인
[x] controller 관련 로그 확인
```

주요 로그:

```text
Loading robot model 'panda'
Starting planning scene monitor
Loaded panda_hand_controller
Configured and activated panda_hand_controller
```

판정:

```text
Panda MoveIt2 demo 실행 성공
```

---

## 10. Phase 9-7. MotionPlanning display 추가

처음에는 RViz2의 `Panels` 메뉴에서 MotionPlanning을 찾으려고 했다.

확인한 메뉴:

```text
Panels
→ Delete Panel
```

여기에는 다음 항목만 보였다.

```text
Displays
Selection
Tool Properties
Views
```

판단:

```text
Panels 메뉴에는 이미 열려 있는 패널만 표시된다.
MotionPlanning은 Panels에서 찾는 것이 아니라 Displays에서 Add해야 한다.
```

해결 방법:

```text
Displays
→ Add
→ By display type
→ MotionPlanning
```

추가 후 확인한 것:

```text
[x] MotionPlanning display가 Displays에 추가됨
[x] 아래쪽 MotionPlanning panel 표시
[x] Planning 탭 표시
[x] Plan / Execute / Plan & Execute 버튼 표시
[x] Planning Group 선택창 표시
```

---

## 11. Phase 9-8. Planning Group 설정

MotionPlanning display를 추가한 뒤 Planning Group을 확인했다.

초기 상태:

```text
Planning Group: hand
```

`hand`는 Panda gripper에 해당한다.

로봇팔 본체 motion planning을 확인하기 위해 다음으로 변경했다.

```text
Planning Group: panda_arm
```

의미:

```text
hand
→ gripper / 집게 부분

panda_arm
→ Panda 로봇팔 본체 관절 그룹
```

확인한 것:

```text
[x] Planning Group 드롭다운 확인
[x] hand와 panda_arm 구분
[x] panda_arm 선택
[x] Panda 팔 부분이 선택 대상으로 표시
[x] Plan 버튼 활성화 확인
```

---

## 12. Phase 9-9. Goal State 설정 후 Plan 실행

Goal State를 다음으로 변경했다.

```text
Goal State: <random valid>
```

그 다음 `Plan` 버튼을 클릭했다.

주요 로그:

```text
Planning request received for MoveGroup action. Forwarding to planning pipeline.
Using planning pipeline 'ompl'
Planner configuration 'panda_arm' will use planner 'geometric::RRTConnect'.
Motion plan was computed successfully.
Planning request complete!
time taken to generate plan: 0.0191608 seconds
```

해석:

```text
RViz2 MotionPlanning panel에서 planning 요청
→ move_group이 요청 수신
→ OMPL planning pipeline 사용
→ RRTConnect planner 사용
→ motion plan 생성 성공
→ RViz2에서 trajectory 시각화
```

Plan과 Execute의 차이:

```text
Plan
→ 경로 계산 및 RViz2 시각화

Execute
→ 계산된 trajectory를 controller에 전달해 로봇 상태 변경

Plan & Execute
→ Plan과 Execute를 한 번에 수행
```

이번 단계에서는 Plan만 먼저 실행했다.

---

## 13. Phase 9-10. Execute 실행

Plan 성공 후 `Execute` 버튼을 클릭했다.

주요 로그:

```text
Goal request accepted!
Goal reached, success!
Controller 'panda_arm_controller' successfully finished
Completed trajectory execution with status SUCCEEDED ...
Execution completed: SUCCEEDED
Execute request success!
```

해석:

```text
move_group
→ panda_arm_controller에 trajectory goal 전달
→ panda_arm_controller가 목표 상태까지 실행
→ trajectory execution 성공
```

판정:

```text
Panda arm trajectory execution 성공
```

마지막 warning:

```text
Maybe failed to update robot state, time diff: 0.052s
```

판단:

```text
실행 직전에 Execution completed: SUCCEEDED와 Execute request success가 확인되었으므로 치명적인 문제로 보지 않았다.
```

---

## 14. Phase 9-11. MoveIt2 실행 구조 확인

MoveIt2 demo 실행 중 node 구조를 확인했다.

```bash
ros2 node list
```

확인한 주요 node:

```text
/controller_manager
/interactive_marker_display_105978135401712
/joint_state_broadcaster
/move_group
/move_group_private_108337483829584
/moveit_simple_controller_manager
/panda_arm_controller
/panda_hand_controller
/robot_state_publisher
/rviz2
/static_transform_publisher
```

해석:

```text
/rviz2
→ 사용자가 목표 상태를 지정하고 Plan / Execute 요청

/move_group
→ MoveIt2의 중심 node

/robot_state_publisher
→ Panda robot description을 바탕으로 TF 발행

/controller_manager
→ controller 관리

/joint_state_broadcaster
→ 현재 joint 상태 발행

/panda_arm_controller
→ Panda 팔 trajectory 실행

/panda_hand_controller
→ Panda hand / gripper 제어

/moveit_simple_controller_manager
→ MoveIt2와 controller 연결 관리
```

---

## 15. Phase 9-12. MoveIt2 topic 구조 확인

확인 명령:

```bash
ros2 topic list | grep -E "joint|trajectory|planning|robot|controller|tf"
```

확인한 주요 topic:

```text
/dynamic_joint_states
/joint_state_broadcaster/transition_event
/joint_states
/monitored_planning_scene
/panda_arm_controller/controller_state
/panda_arm_controller/joint_trajectory
/panda_arm_controller/state
/panda_arm_controller/transition_event
/panda_hand_controller/transition_event
/planning_scene
/planning_scene_world
/robot_description
/rviz_moveit_motion_planning_display/robot_interaction_interactive_marker_topic/feedback
/rviz_moveit_motion_planning_display/robot_interaction_interactive_marker_topic/update
/tf
/tf_static
/trajectory_execution_event
```

해석:

```text
/joint_states
→ 현재 로봇팔 관절 상태

/dynamic_joint_states
→ 동적인 joint 상태 정보

/robot_description
→ Panda 로봇 모델 설명

/planning_scene
→ MoveIt2가 인식하는 planning 환경

/monitored_planning_scene
→ RViz2와 move_group이 공유하는 planning scene 상태

/planning_scene_world
→ planning scene 안의 world 정보

/panda_arm_controller/joint_trajectory
→ 팔 controller가 받을 trajectory 명령

/panda_arm_controller/state
→ 팔 controller 상태

/tf, /tf_static
→ Panda link 좌표계 관계

/trajectory_execution_event
→ trajectory execution 이벤트
```

---

## 16. Phase 9-13. controller 구조 확인

확인 명령:

```bash
ros2 control list_controllers
```

확인 결과:

```text
joint_state_broadcaster joint_state_broadcaster/JointStateBroadcaster          active
panda_arm_controller    joint_trajectory_controller/JointTrajectoryController  active
panda_hand_controller   position_controllers/GripperActionController           active
```

해석:

```text
joint_state_broadcaster
→ 현재 joint 상태를 /joint_states로 발행

panda_arm_controller
→ Panda 팔 관절 trajectory 실행

panda_hand_controller
→ Panda hand / gripper 제어
```

세 controller가 모두 active였기 때문에 Execute가 정상적으로 성공했다.

---

## 17. 전체 MoveIt2 실행 흐름

이번 Phase에서 확인한 전체 흐름은 다음과 같다.

```text
Panda robot description
→ robot_state_publisher
→ RViz2 MotionPlanning display
→ move_group
→ OMPL planning pipeline
→ RRTConnect planner
→ trajectory 생성
→ panda_arm_controller
→ Execute 성공
→ /joint_states 갱신
```

좀 더 풀어서 쓰면 다음과 같다.

```text
1. Panda description이 로봇팔 모델을 제공한다.
2. robot_state_publisher가 로봇 link와 joint의 TF 구조를 발행한다.
3. RViz2 MotionPlanning display에서 목표 상태를 지정한다.
4. move_group이 planning 요청을 받는다.
5. OMPL planning pipeline이 motion planning을 수행한다.
6. RRTConnect planner가 시작 상태와 목표 상태를 연결하는 경로를 계산한다.
7. 계산된 trajectory가 RViz2에 표시된다.
8. Execute 요청 시 panda_arm_controller가 trajectory를 실행한다.
9. joint_state_broadcaster가 변경된 joint 상태를 발행한다.
```

---

## 18. 이번 Phase에서 배운 핵심 개념

## 18.1 MoveIt2

```text
MoveIt2는 ROS2에서 로봇팔 motion planning을 수행하기 위한 프레임워크다.
```

주요 역할:

```text
로봇 모델 로딩
관절 상태 관리
planning scene 관리
충돌 검사
motion planning
trajectory execution
RViz2 연동
controller 연결
```

---

## 18.2 Robot Description

```text
로봇의 link, joint, mesh, 관절 제한 등 로봇 모델 정보를 담는 설명이다.
```

MoveIt2는 robot description을 바탕으로 로봇팔의 구조를 이해한다.

---

## 18.3 Link

```text
link는 로봇을 구성하는 몸체 조각이다.
```

예를 들어 로봇팔에서 각 팔 마디, 손목, gripper 등이 link로 표현된다.

---

## 18.4 Joint

```text
joint는 link와 link를 연결하고 움직임을 정의하는 관절이다.
```

MoveIt2는 joint의 현재 값과 제한 범위를 바탕으로 가능한 자세를 계산한다.

---

## 18.5 Planning Group

```text
Planning Group은 MoveIt2에서 어느 부분을 움직일지 정하는 단위다.
```

이번 Phase에서는 다음을 확인했다.

```text
hand
→ gripper 부분

panda_arm
→ 로봇팔 본체
```

---

## 18.6 Planning Scene

```text
Planning Scene은 MoveIt2가 motion planning을 수행할 때 참고하는 가상 환경이다.
```

포함할 수 있는 정보:

```text
로봇 현재 상태
주변 환경
충돌 객체
허용 충돌 정보
attached object
```

이번 Phase에서는 복잡한 collision object를 직접 추가하지는 않았지만, planning scene 관련 topic이 실행되는 것을 확인했다.

---

## 18.7 move_group

```text
move_group은 MoveIt2의 중심 노드다.
```

역할:

```text
planning 요청 수신
planning pipeline 호출
trajectory 계산 결과 관리
controller에 trajectory execution 요청
RViz2 또는 외부 코드와 MoveIt2 내부 기능 연결
```

---

## 18.8 OMPL

```text
OMPL은 motion planning 알고리즘 라이브러리다.
```

이번 Phase에서는 MoveIt2가 `ompl` planning pipeline을 사용했다.

---

## 18.9 RRTConnect

```text
RRTConnect는 시작 상태와 목표 상태를 연결하는 sampling-based planner 중 하나다.
```

이번 Phase에서는 `panda_arm` planning group의 motion plan을 계산할 때 `geometric::RRTConnect` planner가 사용되었다.

---

## 18.10 ros2_control

```text
ros2_control은 ROS2에서 controller를 관리하고 로봇 상태와 명령을 연결하는 제어 프레임워크다.
```

이번 Phase에서는 다음 controller를 확인했다.

```text
joint_state_broadcaster
panda_arm_controller
panda_hand_controller
```

---

## 19. Plan, Execute, Plan & Execute 차이

```text
Plan
→ 경로를 계산하고 RViz2에서 미리 보여준다.
→ controller에 실제 실행 명령을 보내지는 않는다.

Execute
→ 이미 계산된 trajectory를 controller에 전달한다.
→ 로봇 모델의 현재 상태가 실제로 목표 상태로 변경된다.

Plan & Execute
→ planning과 execution을 한 번에 수행한다.
```

이번 Phase에서는 개념을 분리해서 이해하기 위해 Plan과 Execute를 따로 실행했다.

---

## 20. Phase 8과 Phase 9의 연결

Phase 8에서는 `/cmd_vel`을 직접 발행해 TurtleBot3 이동 명령을 이해했다.

```text
Python node
→ /cmd_vel
→ TurtleBot3 diff drive
→ /odom 변화
```

Phase 9에서는 로봇팔 trajectory execution 흐름을 확인했다.

```text
RViz2 MotionPlanning
→ move_group
→ planner
→ trajectory
→ panda_arm_controller
→ /joint_states 변화
```

연결 의미:

```text
Phase 8은 이동로봇의 속도 명령과 제어 흐름을 이해한 단계다.
Phase 9는 로봇팔의 planning과 trajectory execution 흐름을 이해한 단계다.
```

즉, MissionBot-ROS2는 이동로봇 기반에서 로봇팔 조작 기초로 확장되었다.

---

## 21. Phase 9 완료 판정

Phase 9는 다음 기준을 만족했으므로 완료로 판단한다.

```text
[x] MoveIt2 설치 확인
[x] MoveIt2 핵심 패키지 확인
[x] move_group 실행 파일 확인
[x] moveit_msgs interface 확인
[x] Panda demo resource 설치 확인
[x] Panda MoveIt2 demo 실행
[x] RViz2에서 Panda 로봇팔 표시
[x] MotionPlanning display 추가
[x] Planning Group을 panda_arm으로 설정
[x] Goal State를 <random valid>로 설정
[x] Plan 성공
[x] Execute 성공
[x] node 구조 확인
[x] topic 구조 확인
[x] controller active 상태 확인
```

완료 의미:

```text
MissionBot-ROS2는 MoveIt2를 통해 로봇팔 모델을 RViz2에서 시각화하고, planning group을 선택한 뒤, move_group을 통해 motion plan을 생성하고 controller를 통해 trajectory를 실행하는 기본 흐름을 확인했다.
```

---

## 22. 다음 단계

Phase 9 실습 자체는 완료되었다.

남은 작업은 문서화 마무리다.

```text
[x] README Result 추가
[x] notes/experiment_log.md 추가
[x] notes/phase_summaries/phase09_moveit2_basics_summary.md 작성
[x] docs/phases/phase09_moveit2_basics.md 작성
[ ] docs/handoffs/MBROS2_Phase9_Handoff.md 작성
[ ] docs/prompt/MBROS2_Phase9_prompt.md 작성
[ ] git add / commit
```

Phase 10은 LLM/VLM Extension이지만, 아직은 Phase 9 handoff와 prompt 정리가 먼저다.
