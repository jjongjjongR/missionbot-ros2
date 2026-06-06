# MissionBot-ROS2 Phase 9 인수인계 문서

> 목적: 이 문서는 MissionBot-ROS2 프로젝트의 Phase 9. MoveIt2 Basics 완료 상태를 정리하고, 다른 채팅창에서 Phase 10. LLM/VLM Extension을 바로 이어가기 위한 인수인계 문서다.
> 이 문서와 아래의 이어가기 프롬프트만 있으면 Phase 9 완료 상태를 복원하고 Phase 10을 시작할 수 있다.

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

Phase 9까지의 의미는 다음과 같다.

```text
Mobile Robot Foundation
→ Manipulation Basics

위 흐름까지 완료했다.
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
[x] Phase 9. MoveIt2 Basics
[ ] Phase 10. LLM/VLM Extension
```

현재는 Phase 9 실습과 문서화를 완료한 상태다.

다음 Phase는 다음이다.

```text
Phase 10. LLM/VLM Extension
```

다만 Phase 10에서도 처음부터 복잡한 Agent 시스템, VLA, 실제 모바일 매니퓰레이션 전체 구현으로 앞서가지 않는다.

Phase 10의 첫 목표는 다음 정도로 제한한다.

```text
1. 지금까지 만든 이동로봇 / 로봇팔 기초 흐름을 정리한다.
2. LLM Mission Parser가 맡을 역할을 아주 작은 범위로 정의한다.
3. 자연어 명령을 구조화된 mission command 또는 task schema로 바꾸는 최소 예제를 만든다.
4. VLM 또는 Object Selector는 바로 구현하지 말고, Mission Parser 다음 단계로 둔다.
```

---

## 3. 최종 확정 환경

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

Manipulation:
MoveIt2
Panda demo robot arm
ros2_control

Main TurtleBot3 Workspace:
~/turtlebot3_ws

MissionBot Project Location:
~/projects/missionbot-ros2
```

---

## 4. 현재 프로젝트 폴더 기준

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
│   │   ├── phase08_control_basics.md
│   │   └── phase09_moveit2_basics.md
│   ├── concepts/
│   ├── templates/
│   ├── prompt/
│   │   └── MBROS2_Phase9_prompt.md
│   └── handoffs/
│       └── MBROS2_Phase9_Handoff.md
│
├── src/
│   └── missionbot_basic/
│       └── missionbot_basic/
│           └── open_loop_controller.py
│
├── configs/
│   └── moveit2/
│
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
│   ├── screenshots/
│   │   └── rviz/
│   └── failure_cases/
│       ├── failure_case_template.md
│       └── P07-FAIL-0001_unreachable_goal_test.md
│
└── notes/
    ├── experiment_log.md
    ├── troubleshooting.md
    ├── daily_logs/
    ├── phase_summaries/
    │   ├── phase07_failure_analysis_summary.md
    │   ├── phase08_control_basics_summary.md
    │   └── phase09_moveit2_basics_summary.md
    └── handoff_notes/
```

현재 프로젝트 루트에서 확인되는 기본 폴더는 다음과 같다.

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

`build`, `install`, `log`는 `colcon build`를 수행했기 때문에 생성된 ROS2 빌드 산출물이다.

---

## 5. 현재 .bashrc 기준

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

다만 MissionBot 프로젝트에서 직접 만든 패키지를 실행하려면 프로젝트 루트에서 아래 명령이 필요하다.

```bash
cd ~/projects/missionbot-ros2
source install/setup.bash
```

이 명령은 `.bashrc`를 다시 적용하는 것이 아니라, MissionBot workspace에서 빌드한 패키지를 현재 터미널이 인식하도록 만드는 것이다.

---

## 6. Phase 8 완료 요약

Phase 8에서는 TurtleBot3의 `/cmd_vel` 속도 명령과 `/odom` 반응을 기준으로 이동로봇 제어 기초를 확인했다.

완료한 주요 내용:

```text
[x] /cmd_vel topic 확인
[x] /odom topic 확인
[x] /cmd_vel의 geometry_msgs/msg/Twist 타입 확인
[x] /odom의 nav_msgs/msg/Odometry 타입 확인
[x] /cmd_vel publisher/subscriber 구조 확인
[x] turtlebot3_diff_drive가 /cmd_vel을 subscribe하는 것 확인
[x] teleop_keyboard 입력에 따른 /cmd_vel 값 변화 확인
[x] TurtleBot3 이동 후 /odom position 및 orientation 변화 확인
[x] ros2 topic pub으로 open-loop 전진 명령 실습
[x] ros2 topic pub으로 open-loop 회전 명령 실습
[x] open_loop_controller.py 작성
[x] setup.py entry_points에 open_loop_controller 등록
[x] colcon build 성공
[x] ros2 run missionbot_basic open_loop_controller 실행
[x] Gazebo에서 전진 → 정지 → 회전 → 정지 동작 확인
```

Phase 8 완료 의미:

```text
MissionBot-ROS2는 Navigation2가 자동으로 생성하던 /cmd_vel 명령을 기초 제어 관점에서 직접 이해하고, 간단한 Python ROS2 node로 속도 명령을 발행할 수 있게 되었다.
```

---

## 7. Phase 9 완료 내용

Phase 9에서는 TurtleBot3 기반 이동로봇 실습 이후, 로봇팔 조작 기초를 이해하기 위해 MoveIt2 환경을 구성하고 Panda 로봇팔 데모를 실행했다.

이번 Phase의 핵심 목표는 실제 로봇팔 하드웨어 제어나 복잡한 manipulation task를 구현하는 것이 아니라, MoveIt2가 로봇팔 모델, planning scene, move_group, controller, RViz2 MotionPlanning display를 통해 motion planning과 trajectory execution을 수행하는 기본 흐름을 확인하는 것이었다.

완료한 작업은 다음과 같다.

```text
[x] 기존 Gazebo / TurtleBot3 노드 정리
[x] ROS2 Humble 환경 확인
[x] MoveIt2 패키지 설치 확인
[x] ros-humble-moveit 설치
[x] moveit_core, moveit_msgs, moveit_ros_move_group 패키지 확인
[x] moveit_setup_assistant 실행 파일 확인
[x] move_group 실행 파일 확인
[x] moveit_msgs 인터페이스 확인
[x] Panda MoveIt2 demo resource 패키지 미설치 상태 확인
[x] moveit_resources_panda_description 설치 확인
[x] moveit_resources_panda_moveit_config 설치 확인
[x] Panda MoveIt2 demo.launch.py 실행
[x] RViz2에서 Panda 로봇팔 모델 표시 확인
[x] MotionPlanning display 추가
[x] Planning Group을 hand에서 panda_arm으로 변경
[x] Goal State를 <random valid>로 설정
[x] Plan 실행
[x] OMPL planning pipeline 사용 확인
[x] RRTConnect planner 사용 확인
[x] Motion plan computed successfully 확인
[x] Execute 실행
[x] panda_arm_controller trajectory execution 성공 확인
[x] MoveIt2 관련 node, topic, controller 구조 확인
```

---

## 8. Phase 9 설치 및 패키지 확인

처음에는 MoveIt2 관련 패키지가 설치되어 있지 않았다.

확인 명령:

```bash
ros2 pkg list | grep moveit
ros2 pkg list | grep moveit_ros
ros2 pkg list | grep moveit_configs
```

MoveIt2 설치 명령:

```bash
sudo apt update
sudo apt install -y ros-humble-moveit
```

설치 후 확인한 주요 패키지는 다음과 같다.

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

---

## 9. MoveIt2 핵심 실행 파일 확인

확인 명령:

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
→ 로봇 모델을 MoveIt2에서 사용할 수 있도록 설정하는 도구

move_group
→ MoveIt2의 중심 노드
→ motion planning 요청을 받고 planning pipeline으로 전달
→ trajectory execution 흐름을 관리
```

---

## 10. moveit_msgs 인터페이스 확인

확인 명령:

```bash
ros2 interface list | grep moveit_msgs | head -n 30
```

확인한 주요 interface:

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

중요하게 확인한 interface:

```text
MotionPlanRequest
MotionPlanResponse
DisplayTrajectory
CollisionObject
JointConstraint
JointLimits
MoveItErrorCodes
```

---

## 11. Panda MoveIt2 demo resource 확인

처음에는 Panda demo resource 패키지가 없었다.

확인 명령:

```bash
ros2 pkg list | grep moveit_resources
ros2 pkg list | grep panda
ros2 pkg list | grep moveit2_tutorials
```

Panda demo 실행 시도:

```bash
ros2 launch moveit_resources_panda_moveit_config demo.launch.py
```

오류:

```text
Package 'moveit_resources_panda_moveit_config' not found
```

판단:

```text
MoveIt2 본체는 설치되었지만 Panda demo resource 패키지가 아직 없는 상태였다.
```

이후 설치 후 확인된 패키지는 다음과 같다.

```text
moveit_resources_panda_description
moveit_resources_panda_moveit_config
```

의미:

```text
moveit_resources_panda_description
→ Panda 로봇팔의 link, joint, mesh 등 로봇 모델 정보

moveit_resources_panda_moveit_config
→ Panda 로봇팔을 MoveIt2에서 planning하기 위한 설정 묶음
→ planning group, kinematics, collision, controller, RViz 설정 등을 포함
```

---

## 12. Panda MoveIt2 demo 실행

실행 명령:

```bash
ros2 launch moveit_resources_panda_moveit_config demo.launch.py
```

확인한 결과:

```text
[x] RViz2 창 실행
[x] Panda 로봇팔 모델 표시
[x] Global Status: Ok
[x] PlanningScene display 표시
[x] Trajectory display 표시
[x] robot model 'panda' 로딩 확인
[x] planning scene monitor 시작 확인
[x] panda_hand_controller configured and activated 확인
```

확인한 주요 로그:

```text
Loading robot model 'panda'
Starting planning scene monitor
Loaded panda_hand_controller
Configured and activated panda_hand_controller
```

---

## 13. MotionPlanning display 추가

처음에는 RViz2의 `Panels` 메뉴에서 MotionPlanning을 찾으려고 했다.

하지만 실제 추가 위치는 다음이었다.

```text
Displays
→ Add
→ By display type
→ MotionPlanning
```

확인한 것:

```text
[x] MotionPlanning display가 Displays에 추가됨
[x] 아래쪽 MotionPlanning panel 표시
[x] Planning 탭 표시
[x] Plan / Execute / Plan & Execute 버튼 표시
[x] Planning Group 선택창 표시
```

---

## 14. Planning Group 설정

처음 Planning Group은 다음 값이었다.

```text
hand
```

`hand`는 Panda gripper에 해당한다.

로봇팔 본체의 motion planning을 확인하기 위해 다음으로 변경했다.

```text
panda_arm
```

의미:

```text
hand
→ gripper / 집게 부분

panda_arm
→ Panda 로봇팔 본체 관절 그룹
```

---

## 15. Plan 실행 결과

RViz2 MotionPlanning panel에서 수행한 작업:

```text
Planning Group: panda_arm
Goal State: <random valid>
Plan 클릭
```

확인한 주요 로그:

```text
Planning request received for MoveGroup action.
Using planning pipeline 'ompl'
Planner configuration 'panda_arm' will use planner 'geometric::RRTConnect'
Motion plan was computed successfully.
Planning request complete!
time taken to generate plan: 0.0191608 seconds
```

해석:

```text
RViz2 MotionPlanning panel
→ move_group
→ OMPL planning pipeline
→ RRTConnect planner
→ motion plan 생성
→ RViz2에서 trajectory 시각화
```

`Plan`은 실제 controller를 움직이는 것이 아니라, 목표 상태까지 갈 수 있는 경로를 계산하고 RViz2에서 미리 보여주는 단계다.

---

## 16. Execute 실행 결과

Plan 성공 후 `Execute`를 실행했다.

확인한 주요 로그:

```text
Goal request accepted!
Goal reached, success!
Controller 'panda_arm_controller' successfully finished
Completed trajectory execution with status SUCCEEDED
Execution completed: SUCCEEDED
Execute request success!
```

해석:

```text
move_group
→ panda_arm_controller
→ trajectory goal 전달
→ Panda 팔 목표 상태 도달
→ trajectory execution 성공
```

즉, 단순히 경로 계산만 성공한 것이 아니라, 계산된 trajectory가 controller에 전달되어 Panda 로봇팔 상태에 실제로 적용되는 흐름까지 확인했다.

마지막에 다음 warning이 있었지만 치명적인 문제로 보지 않았다.

```text
Maybe failed to update robot state, time diff: 0.052s
```

이유:

```text
직전에 Execution completed: SUCCEEDED, Execute request success 로그가 확인되었기 때문에 trajectory execution 자체는 성공으로 판단했다.
```

---

## 17. 실행 중 확인한 node 구조

확인 명령:

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
/rviz2_private_126897426011232
/rviz2_private_126897560647792
/static_transform_publisher
/transform_listener_impl_6062f162e510
/transform_listener_impl_6062f2bc8720
/transform_listener_impl_6288493c6b10
/transform_listener_impl_73699c032940
```

중요한 node:

```text
/rviz2
/move_group
/robot_state_publisher
/controller_manager
/joint_state_broadcaster
/panda_arm_controller
/panda_hand_controller
/moveit_simple_controller_manager
```

해석:

```text
/rviz2
→ 사용자가 목표 자세를 지정하고 Plan / Execute 요청

/move_group
→ MoveIt2의 중심 노드
→ motion planning 요청 처리

/robot_state_publisher
→ Panda 로봇 모델의 TF 구조 발행

/controller_manager
→ ros2_control controller들을 관리

/joint_state_broadcaster
→ 현재 joint 상태 발행

/panda_arm_controller
→ Panda 팔 관절 trajectory 실행

/panda_hand_controller
→ Panda gripper 실행

/moveit_simple_controller_manager
→ MoveIt2와 controller 사이의 연결 관리
```

---

## 18. 실행 중 확인한 topic 구조

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

중요한 topic:

```text
/joint_states
/dynamic_joint_states
/robot_description
/planning_scene
/monitored_planning_scene
/planning_scene_world
/panda_arm_controller/joint_trajectory
/panda_arm_controller/state
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
→ move_group과 RViz2가 공유하는 planning scene 상태

/planning_scene_world
→ planning scene 안의 world 정보

/panda_arm_controller/joint_trajectory
→ 팔 controller가 받을 joint trajectory 명령

/panda_arm_controller/state
→ 팔 controller의 현재 상태

/tf, /tf_static
→ Panda link들의 좌표계 관계

/trajectory_execution_event
→ trajectory 실행 이벤트
```

---

## 19. controller 상태 확인

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
→ 현재 joint 상태를 발행하는 broadcaster

panda_arm_controller
→ Panda 팔 joint trajectory 실행 controller

panda_hand_controller
→ Panda hand / gripper controller
```

세 controller가 모두 active 상태였기 때문에 Execute가 정상적으로 성공할 수 있었다.

---

## 20. Phase 9에서 배운 핵심 개념

## 20.1 MoveIt2

```text
MoveIt2는 ROS2에서 로봇팔 motion planning을 수행하기 위한 프레임워크다.
```

역할:

```text
로봇팔 모델 로딩
관절 상태 관리
planning scene 관리
충돌 검사
motion planning
trajectory execution
RViz2 연동
controller 연결
```

---

## 20.2 Robot Description

```text
로봇의 link, joint, mesh, 관절 제한 등 로봇 모델 정보를 담는 설명이다.
```

Panda demo에서는 `moveit_resources_panda_description` 패키지가 이 역할을 했다.

---

## 20.3 Link와 Joint

```text
link
→ 로봇을 구성하는 몸체 조각

joint
→ link와 link를 연결하고 움직임을 정의하는 관절
```

로봇팔은 여러 link와 joint가 이어진 구조다.

MoveIt2는 이 구조를 바탕으로 현재 자세, 목표 자세, 가능한 움직임, 충돌 여부를 계산한다.

---

## 20.4 Planning Group

```text
Planning Group은 MoveIt2에서 어느 부분을 움직일지 정하는 단위다.
```

이번 Phase에서는 다음 차이를 확인했다.

```text
hand
→ gripper planning group

panda_arm
→ 로봇팔 본체 planning group
```

---

## 20.5 Planning Scene

```text
Planning Scene은 MoveIt2가 motion planning을 할 때 참고하는 가상 환경이다.
```

포함할 수 있는 정보:

```text
로봇 현재 상태
로봇 주변 환경
충돌 객체
허용 충돌 정보
attached object
```

이번 Phase에서는 복잡한 collision object를 추가하지는 않았지만, `/planning_scene`, `/monitored_planning_scene`, `/planning_scene_world` topic을 통해 planning scene 관련 구조가 실행되는 것을 확인했다.

---

## 20.6 move_group

```text
move_group은 MoveIt2의 중심 노드다.
```

역할:

```text
RViz2나 외부 코드에서 planning 요청을 받음
planning pipeline으로 요청 전달
planner를 통해 trajectory 계산
controller와 연결해 trajectory execution 수행
```

이번 Phase에서는 RViz2 MotionPlanning display에서 누른 Plan / Execute 요청이 move_group을 통해 처리되는 것을 확인했다.

---

## 20.7 OMPL

```text
OMPL은 motion planning 알고리즘 라이브러리다.
```

이번 Phase에서는 MoveIt2가 `ompl` planning pipeline을 사용했다.

---

## 20.8 RRTConnect

```text
RRTConnect는 시작 상태와 목표 상태를 연결하는 sampling-based motion planner 중 하나다.
```

이번 Phase에서는 `panda_arm` planning group에 대해 `geometric::RRTConnect` planner가 사용되었다.

---

## 20.9 Plan과 Execute의 차이

```text
Plan
→ 목표 상태까지 갈 경로를 계산하고 RViz2에서 미리 보여줌

Execute
→ 계산된 trajectory를 controller에 전달해 로봇 상태를 실제로 변경

Plan & Execute
→ Plan과 Execute를 한 번에 수행
```

이번 Phase에서는 개념을 분리해서 이해하기 위해 Plan과 Execute를 따로 실행했다.

---

## 20.10 ros2_control

```text
ros2_control은 ROS2에서 controller를 관리하고 로봇 상태와 명령을 연결하는 제어 프레임워크다.
```

이번 Phase에서는 다음 controller가 active 상태임을 확인했다.

```text
joint_state_broadcaster
panda_arm_controller
panda_hand_controller
```

---

## 21. Phase 9에서 확인한 전체 흐름

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

이 흐름을 통해 MoveIt2 기반 로봇팔 motion planning과 trajectory execution의 기본 구조를 확인했다.

---

## 22. Phase 9 발생 이슈와 판단

## 22.1 Panda demo resource package not found

증상:

```text
Package 'moveit_resources_panda_moveit_config' not found
```

원인:

```text
MoveIt2 본체는 설치되었지만 Panda demo resource 패키지가 아직 설치되지 않은 상태였다.
```

해결:

```text
moveit_resources_panda_description
moveit_resources_panda_moveit_config
```

패키지가 인식되는 것을 확인했다.

---

## 22.2 MotionPlanning panel을 Panels 메뉴에서 찾을 수 없음

증상:

```text
Panels → Delete Panel에는 Displays, Selection, Tool Properties, Views만 보였다.
MotionPlanning이 보이지 않았다.
```

원인:

```text
Panels 메뉴는 이미 떠 있는 패널을 관리하는 메뉴이고, MotionPlanning display는 Displays의 Add에서 추가해야 했다.
```

해결:

```text
Displays
→ Add
→ By display type
→ MotionPlanning
```

---

## 22.3 robot state update warning

증상:

```text
Maybe failed to update robot state, time diff: 0.052s
```

판단:

```text
직전에 trajectory execution 성공 로그가 있었기 때문에 치명적인 문제로 보지 않았다.
```

성공 로그:

```text
Execution completed: SUCCEEDED
Execute request success!
```

---

## 23. Phase 9 기록 파일

Phase 9 관련 정리 파일:

```text
README.md
notes/experiment_log.md
docs/phases/phase09_moveit2_basics.md
notes/phase_summaries/phase09_moveit2_basics_summary.md
docs/handoffs/MBROS2_Phase9_Handoff.md
docs/prompt/MBROS2_Phase9_prompt.md
```

Phase 9에서 추가 설치 또는 확인한 주요 패키지:

```text
ros-humble-moveit
moveit_resources_panda_description
moveit_resources_panda_moveit_config
```

experiment_log 업데이트 내용:

```text
P09-EXP-0001_moveit2_install_check
P09-EXP-0002_moveit2_package_structure_check
P09-EXP-0003_panda_moveit_demo_resource_check
P09-EXP-0004_panda_moveit2_rviz_motion_planning
P09-EXP-0005_panda_moveit2_trajectory_execute
```

troubleshooting 정리 여부:

```text
정식 troubleshooting 항목은 필수로 추가하지 않는다.

Panda demo resource package not found 문제와 MotionPlanning display 위치 혼동은 Phase 9 문서와 summary의 Notes / Issue에 기록하는 것으로 충분하다.

robot state update warning도 execution success가 확인되었기 때문에 치명적 오류로 분류하지 않는다.
```

---

## 24. Phase 9 완료 판정

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
[x] README Result 섹션 업데이트
[x] notes/experiment_log.md에 Phase 9 실험 기록 추가
[x] docs/phases/phase09_moveit2_basics.md 작성
[x] notes/phase_summaries/phase09_moveit2_basics_summary.md 작성
```

완료 의미:

```text
MissionBot-ROS2는 MoveIt2를 통해 로봇팔 모델을 RViz2에서 시각화하고, planning group을 선택한 뒤, move_group을 통해 motion plan을 생성하고 controller를 통해 trajectory를 실행하는 기본 흐름을 확인했다.
```

---

## 25. Phase 10 시작 목표

다음 Phase:

```text
Phase 10. LLM/VLM Extension
```

Phase 10의 핵심 목표:

```text
MissionBot-ROS2의 하위 로봇 시스템 기초를 바탕으로, 자연어 명령을 로봇이 이해할 수 있는 구조화된 mission command로 바꾸는 LLM Mission Parser 기초를 설계한다.
```

단, Phase 10 시작 시 처음부터 다음으로 앞서가지 않는다.

```text
복잡한 LangGraph Agent
VLA 모델
실제 VLM object detection 전체 구현
실제 모바일 매니퓰레이션 통합
OpenAI API 기반 자동 실행 로봇 시스템
실제 로봇팔 task execution
```

첫 단계에서는 다음만 확인한다.

```text
1. Phase 9까지 완료된 로봇 시스템 흐름 정리
2. Mission Parser가 받을 자연어 명령 예시 정의
3. 자연어 명령을 단순 JSON schema로 변환하는 목표 설정
4. schema 필드 정의
5. Python 파일을 만들기 전, 입력/출력 형식부터 확정
```

좋은 시작점:

```text
Phase 10-1. Mission Parser 입력/출력 schema 설계
```

---

## 26. Phase 10 시작 전 확인해야 할 것

Phase 10은 ROS2 실행보다 먼저 설계 기준을 잡는 것이 중요하다.

먼저 확인할 것:

```text
1. MissionBot에서 자연어 명령이 어디에 연결될지
2. LLM이 직접 로봇을 움직이는 것이 아니라, 구조화된 명령을 만드는 역할이라는 점
3. 출력 schema가 너무 복잡하지 않은지
4. 현재는 이동 명령과 조작 명령을 모두 완성하려 하지 않는지
5. 먼저 pick/place 같은 복잡한 명령보다 move_to, inspect, stop 같은 단순 명령부터 시작할지
```

추천 첫 입력 예시:

```text
"책상 앞으로 이동해줘"
"빨간 컵을 찾아줘"
"선반 앞까지 가서 멈춰"
"왼쪽에 있는 물체를 확인해줘"
```

단, 첫 구현에서는 VLM 기반 물체 인식까지 바로 연결하지 않는다.

첫 출력 schema 예시:

```json
{
  "intent": "move_to",
  "target": "desk",
  "object": null,
  "constraints": [],
  "requires_vision": false,
  "requires_navigation": true,
  "requires_manipulation": false
}
```

이 schema는 Phase 10에서 다시 조정할 수 있다.

---

## 27. Phase 10에서 주의할 점

```text
Phase 10에서는 LLM/VLM Extension을 시작하지만, 바로 거대한 AI Agent 프로젝트로 확장하지 않는다.
```

중요한 기준:

```text
LLM은 로봇을 직접 움직이는 존재가 아니다.
LLM은 사용자의 자연어 명령을 구조화된 mission command로 변환하는 상위 해석 모듈이다.
ROS2 / Navigation2 / MoveIt2는 실제 실행 계층이다.
VLM 또는 Object Selector는 이후 단계에서 object 관련 명령을 해석하기 위해 연결한다.
```

Phase 10 첫 단계에서는 다음 정도만 다룬다.

```text
Mission Parser가 무엇인지
왜 필요한지
MissionBot-ROS2에서 어디에 연결되는지
입력 자연어와 출력 JSON schema가 무엇인지
어떤 명령은 navigation이 필요하고, 어떤 명령은 vision이나 manipulation이 필요한지
```

---

## 28. 다음 채팅 시작 지점

다음 채팅에서는 아래 상태에서 시작하면 된다.

```text
현재 MissionBot-ROS2는 Phase 9. MoveIt2 Basics를 완료했다.

완료한 것:
- MoveIt2 설치
- moveit_core, moveit_msgs, moveit_ros_move_group 확인
- move_group 실행 파일 확인
- moveit_msgs interface 확인
- Panda demo resource 설치
- moveit_resources_panda_description 확인
- moveit_resources_panda_moveit_config 확인
- Panda MoveIt2 demo.launch.py 실행
- RViz2에서 Panda 로봇팔 모델 표시
- MotionPlanning display 추가
- Planning Group을 hand에서 panda_arm으로 변경
- Goal State를 <random valid>로 설정
- Plan 실행 성공
- OMPL planning pipeline 확인
- RRTConnect planner 확인
- Execute 실행 성공
- panda_arm_controller trajectory execution 성공
- MoveIt2 node/topic/controller 구조 확인
- README Result 섹션 업데이트
- docs/phases/phase09_moveit2_basics.md 작성
- notes/phase_summaries/phase09_moveit2_basics_summary.md 작성
- notes/experiment_log.md에 Phase 9 실험 기록 추가

주요 결과물:
- docs/phases/phase09_moveit2_basics.md
- notes/phase_summaries/phase09_moveit2_basics_summary.md
- notes/experiment_log.md의 P09-EXP-0001~0005
- docs/handoffs/MBROS2_Phase9_Handoff.md
- docs/prompt/MBROS2_Phase9_prompt.md

다음 목표:
- Phase 10. LLM/VLM Extension 시작
- 첫 단계는 Mission Parser 입력/출력 schema 설계
```

추천 시작점:

```text
Phase 10-1. Mission Parser 입력/출력 schema 설계
```

첫 단계에서 할 일:

```text
1. 지금까지 만든 하위 로봇 시스템 흐름 정리
2. LLM Mission Parser의 역할 정의
3. 자연어 명령 예시 3~5개 선정
4. 출력 JSON schema 초안 작성
5. navigation / vision / manipulation 필요 여부를 필드로 분리
6. 아직 ROS2 node나 OpenAI API 코드는 만들지 않고 schema부터 확정
```

먼저 Phase 10-1로, Mission Parser가 무엇이고 MissionBot-ROS2에서 어디에 연결되는지 설명한 뒤, 입력/출력 schema 설계부터 안내해줘.
