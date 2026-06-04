# src/missionbot_basic/missionbot_basic/open_loop_controller.py
# 2026-06-04 신규: Phase 8-5에서 사용할 간단한 open-loop 제어 노드


import rclpy

# 2026-06-04 신규: ROS2 Python Node 클래스, /cmd_vel로 보낼 Twist 메시지
from rclpy.node import Node
from geometry_msgs.msg import Twist


# 2026-06-04 신규: TurtleBot3에 속도 명령을 보내는 제어 노드입니다.
class OpenLoopController(Node):
    def __init__(self):
        # 2026-06-04 신규: 노드 이름을 open_loop_controller로 정합니다.
        super().__init__('open_loop_controller')

        # 2026-06-04 신규: /cmd_vel topic으로 Twist 메시지를 publish합니다.
        self.cmd_vel_publisher = self.create_publisher(Twist, '/cmd_vel', 10)

        # 2026-06-04 신규: 노드가 시작된 시간을 저장합니다.
        self.start_time = self.get_clock().now()

        # 2026-06-04 신규: 0.1초마다 control_loop 함수를 실행합니다.
        self.timer = self.create_timer(0.1, self.control_loop)

        # 2026-06-04 신규: 종료 처리를 한 번만 하기 위한 플래그입니다.
        self.is_finished = False

        # 2026-06-04 신규: 실습 시작 로그를 출력합니다.
        self.get_logger().info('Open-loop controller started.')

    def control_loop(self):
        # 2026-06-04 신규: 이미 종료 처리된 경우 더 이상 명령을 보내지 않습니다.
        if self.is_finished:
            return

        # 2026-06-04 신규: 노드 시작 후 몇 초가 지났는지 계산합니다.
        now = self.get_clock().now()
        elapsed_time = (now - self.start_time).nanoseconds / 1_000_000_000

        # 2026-06-04 신규: 매 주기마다 새 Twist 메시지를 만듭니다.
        cmd_msg = Twist()

        # 2026-06-04 신규: 0~2초 동안 전진 명령을 보냅니다.
        if elapsed_time < 2.0:
            cmd_msg.linear.x = 0.10
            cmd_msg.angular.z = 0.0
            self.get_logger().info('State: FORWARD')

        # 2026-06-04 신규: 2~3초 동안 정지 명령을 반복해서 보냅니다.
        elif elapsed_time < 3.0:
            cmd_msg.linear.x = 0.0
            cmd_msg.angular.z = 0.0
            self.get_logger().info('State: STOP_AFTER_FORWARD')

        # 2026-06-04 신규: 3~5초 동안 제자리 회전 명령을 보냅니다.
        elif elapsed_time < 5.0:
            cmd_msg.linear.x = 0.0
            cmd_msg.angular.z = 0.5
            self.get_logger().info('State: ROTATE')

        # 2026-06-04 신규: 5~6초 동안 마지막 정지 명령을 반복해서 보냅니다.
        elif elapsed_time < 6.0:
            cmd_msg.linear.x = 0.0
            cmd_msg.angular.z = 0.0
            self.get_logger().info('State: FINAL_STOP')

        # 2026-06-04 신규: 6초 이후에는 정지 명령을 보낸 뒤 노드를 종료합니다.
        else:
            self.publish_stop()
            self.is_finished = True
            self.get_logger().info('Open-loop control finished.')
            rclpy.shutdown()
            return

        # 2026-06-04 신규: 현재 상태에 맞는 속도 명령을 /cmd_vel로 보냅니다.
        self.cmd_vel_publisher.publish(cmd_msg)

    def publish_stop(self):
        # 2026-06-04 신규: 완전 정지 명령 메시지를 만듭니다.
        stop_msg = Twist()
        stop_msg.linear.x = 0.0
        stop_msg.angular.z = 0.0

        # 2026-06-04 신규: 마지막 정지 명령을 한 번 더 publish합니다.
        self.cmd_vel_publisher.publish(stop_msg)


# 2026-06-04 신규: ROS2 노드를 실행하는 main 함수입니다.
def main(args=None):
    # 2026-06-04 신규: rclpy를 초기화합니다.
    rclpy.init(args=args)

    # 2026-06-04 신규: OpenLoopController 노드를 생성합니다.
    node = OpenLoopController()

    # 2026-06-04 신규: 노드를 계속 실행합니다.
    rclpy.spin(node)

    # 2026-06-04 신규: 노드 자원을 정리합니다.
    node.destroy_node()


# 2026-06-04 신규: 이 파일을 직접 실행할 때 main 함수를 실행합니다.
if __name__ == '__main__':
    main()