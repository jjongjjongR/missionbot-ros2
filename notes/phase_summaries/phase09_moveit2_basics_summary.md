# Phase 9 Summary - MoveIt2 Basics

## 1. Phase 개요

Phase 9에서는 TurtleBot3 기반 이동로봇 실습 이후, 로봇팔 조작 기초를 이해하기 위해 MoveIt2 환경을 구성하고 Panda 로봇팔 데모를 실행했다.

이번 Phase의 핵심 목표는 실제 로봇팔 하드웨어 제어나 복잡한 manipulation task를 구현하는 것이 아니라, MoveIt2가 로봇팔 모델, planning scene, move_group, controller, RViz2 MotionPlanning display를 통해 motion planning과 trajectory execution을 수행하는 기본 흐름을 확인하는 것이었다.

---

## 2. 진행 환경

```text
Host: Windows Desktop
Virtualization: VMware Workstation 17
Guest OS: Ubuntu 22.04 LTS
ROS2: Humble Hawksbill
Simulator: Gazebo Classic 11.10.2
Visualization: RViz2
MoveIt2: ros-humble-moveit
Robot model: Panda demo robot arm
Project path: ~/projects/missionbot-ros2
TurtleBot3 workspace: ~/turtlebot3_ws
```

---

## 3. 완료한 작업

```text
[x] 기존 Gazebo / TurtleBot3 노드 정리
[x] ROS2 Humble 환경 확인
[x] TURTLEBOT3_MODEL=burger 확인
[x] ros2 / gazebo / rviz2 실행 경로 확인
[x] MoveIt2 관련 패키지 미설치 상태 확인
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

## 4. 설치 및 패키지 확인

처음에는 MoveIt2 관련 패키지가 설치되어 있지 않은 상태였다.

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

설치 후 확인된 주요 패키지는 다음과 같다.

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
moveit_setup_assistant
moveit_simple_controller_manager
```

---

## 5. MoveIt2 핵심 실행 파일 확인

확인 명령:

```bash
ros2 pkg executables moveit_setup_assistant
ros2 pkg executables moveit_ros_move_group
ros2 pkg executables moveit_ros_visualization
ros2 pkg executables moveit_ros_planning_interface
```

확인된 주요 실행 파일:

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

## 6. moveit_msgs 인터페이스 확인

확인 명령:

```bash
ros2 interface list | grep moveit_msgs | head -n 30
```

확인한 주요 interface:

```text
moveit_msgs/msg/MotionPlanRequest
moveit_msgs/msg/MotionPlanResponse
moveit_msgs/msg/DisplayTrajectory
moveit_msgs/msg/CollisionObject
moveit_msgs/msg/JointConstraint
moveit_msgs/msg/JointLimits
moveit_msgs/msg/MoveItErrorCodes
```

의미:

```text
MotionPlanRequest / MotionPlanResponse
→ motion planning 요청과 응답

DisplayTrajectory
→ RViz2에서 planning 결과 trajectory를 보여주기 위한 메시지

CollisionObject
→ planning scene에 포함되는 충돌 객체

JointConstraint / JointLimits
→ 관절 제약과 관절 제한 정보

MoveItErrorCodes
→ planning 또는 execution 결과 상태 코드
```

---

## 7. Panda MoveIt2 demo resource 확인

처음에는 Panda demo resource 패키지가 없었다.

확인 명령:

```bash
ros2 pkg list | grep moveit_resources
ros2 pkg list | grep panda
ros2 pkg list | grep moveit2_tutorials
```

demo 실행 시도:

```bash
ros2 launch moveit_resources_panda_moveit_config demo.launch.py
```

오류:

```text
Package 'moveit_resources_panda_moveit_config' not found
```

이 오류는 MoveIt2 본체는 설치되어 있지만 Panda demo resource 패키지가 아직 없는 상태라는 의미였다.

이후 확인된 Panda 관련 패키지는 다음과 같다.

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

## 8. Panda MoveIt2 demo 실행

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

## 9. MotionPlanning display 추가

처음에는 RViz2의 `Panels` 메뉴에서 MotionPlanning을 찾으려고 했지만, `Panels`에는 기존에 떠 있는 패널만 표시되었다.

실제 추가 위치는 다음이었다.

```text
Displays
→ Add
→ By display type
→ MotionPlanning
```

추가 후 확인한 것:

```text
[x] MotionPlanning display가 Displays에 추가됨
[x] 아래쪽 MotionPlanning 패널이 열림
[x] Planning 탭 표시
[x] Plan / Execute / Plan & Execute 버튼 표시
[x] Planning Group 선택창 표시
```

---

## 10. Planning Group 설정

처음 Planning Group은 다음 값으로 설정되어 있었다.

```text
hand
```

`hand`는 Panda의 gripper, 즉 집게 부분에 해당한다.

로봇팔 본체의 motion planning을 확인하기 위해 Planning Group을 다음으로 변경했다.

```text
panda_arm
```

의미:

```text
hand
→ 그리퍼 부분 planning group

panda_arm
→ Panda 로봇팔 본체 관절 planning group
```

---

## 11. Plan 실행 결과

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

## 12. Execute 실행 결과

Plan 성공 후 Execute를 실행했다.

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

마지막에 다음 warning이 있었지만 치명적인 문제로 보지는 않았다.

```text
Maybe failed to update robot state, time diff: 0.052s
```

이유:

```text
직전에 Execution completed: SUCCEEDED, Execute request success 로그가 확인되었기 때문에 trajectory execution 자체는 성공으로 판단했다.
```

---

## 13. 실행 중 확인한 node 구조

확인 명령:

```bash
ros2 node list
```

확인한 주요 node:

```text
/controller_manager
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

## 14. 실행 중 확인한 topic 구조

확인 명령:

```bash
ros2 topic list | grep -E "joint|trajectory|planning|robot|controller|tf"
```

확인한 주요 topic:

```text
/dynamic_joint_states
/joint_states
/monitored_planning_scene
/panda_arm_controller/controller_state
/panda_arm_controller/joint_trajectory
/panda_arm_controller/state
/panda_hand_controller/transition_event
/planning_scene
/planning_scene_world
/robot_description
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

## 15. controller 상태 확인

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
→ Panda hand/gripper controller
```

세 controller가 모두 active 상태였기 때문에 Execute가 정상적으로 성공할 수 있었다.

---

## 16. 이번 Phase에서 배운 핵심 개념

## 16.1 MoveIt2

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
```

---

## 16.2 Robot Description

```text
로봇의 link, joint, mesh, 관절 제한 등 로봇 모델 정보를 담는 설명이다.
```

Panda demo에서는 `moveit_resources_panda_description` 패키지가 이 역할을 했다.

---

## 16.3 Link와 Joint

```text
link
→ 로봇을 구성하는 몸체 조각

joint
→ link와 link를 연결하고 움직임을 정의하는 관절
```

로봇팔은 여러 link와 joint가 이어진 구조다.

MoveIt2는 이 구조를 바탕으로 현재 자세, 목표 자세, 가능한 움직임, 충돌 여부를 계산한다.

---

## 16.4 Planning Group

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

## 16.5 Planning Scene

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

## 16.6 move_group

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

## 16.7 OMPL

```text
OMPL은 motion planning 알고리즘 라이브러리다.
```

이번 Phase에서는 MoveIt2가 `ompl` planning pipeline을 사용했다.

---

## 16.8 RRTConnect

```text
RRTConnect는 시작 상태와 목표 상태를 연결하는 sampling-based motion planner 중 하나다.
```

이번 Phase에서는 `panda_arm` planning group에 대해 `geometric::RRTConnect` planner가 사용되었다.

---

## 16.9 Plan과 Execute의 차이

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

## 16.10 ros2_control

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

## 17. 이번 Phase에서 확인한 전체 흐름

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

## 18. 발생한 이슈와 판단

## 18.1 Panda demo resource package not found

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

## 18.2 MotionPlanning panel을 Panels 메뉴에서 찾을 수 없음

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

## 18.3 robot state update warning

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

## 19. Phase 9 완료 의미

Phase 9를 통해 MissionBot-ROS2는 이동로봇 중심의 SLAM, Navigation2, rosbag2, Failure Analysis, Control Basics 흐름에서 한 단계 확장하여, MoveIt2 기반 로봇팔 조작 기초를 처음으로 확인했다.

완료 의미:

```text
MissionBot-ROS2는 MoveIt2를 통해 로봇팔 모델을 RViz2에서 시각화하고, planning group을 선택한 뒤, move_group을 통해 motion plan을 생성하고 controller를 통해 trajectory를 실행하는 기본 흐름을 확인했다.
```

---

## 20. 다음 단계

다음 Phase는 Phase 10으로 넘어가기 전에, Phase 9 문서화와 handoff/prompt 정리가 필요하다.

남은 문서화 작업:

```text
[x] README Result 추가
[x] notes/experiment_log.md 추가
[x] notes/phase_summaries/phase09_moveit2_basics_summary.md 작성
[x] docs/phases/phase09_moveit2_basics.md 작성
[ ] docs/handoffs/MBROS2_Phase9_Handoff.md 작성
[ ] docs/prompt/MBROS2_Phase9_prompt.md 작성
[ ] git add / commit
```

Phase 10에서는 LLM/VLM 확장으로 넘어갈 수 있지만, 아직은 Phase 9 문서화가 먼저다.
