# 2026-05-25 신규: /turtle1/cmd_vel topic으로 속도 명령을 publish하는 기본 publisher 노드 파일

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist # 속도 명령 메세지 타입

class VelocityPublisher(Node): # Node 상속
    def __init__(self):
        super().__init__("velocity_publisher") # 노드 이름 지정
    
        self.publisher = self.create_publisher(
            Twist, # 라는 메세지 타입의 메세지를 보낸다.
            '/turtle1/cmd_vel', # 라는 토픽으로
            10
        )

        self.timer = self.create_timer(
            0.5, # 초 마다
            self.publish_velocity #함수 실행
        )

    def publish_velocity(self):
        msg = Twist()

        msg.linear.x = 1.0
        msg.angular.z = 0.5

        self.publisher.publish(msg)

        self.get_logger().info(
            f'Published velocity: linear.x={msg.linear.x:.2f}, angular.z={msg.angular.z:.2f}'
        )

def main(args = None):
    rclpy.init(args = args)
    
    node = VelocityPublisher()
    
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()