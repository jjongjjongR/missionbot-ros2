# 2026-05-25 신규: /turtle1/pose topic을 구독하는 기본 subscriber 노드 파일

import rclpy # Python으로 node를 만들고, topic을 구독하고, 로그를 출력하고, spin을 돌릴 때 필요하다.
from rclpy.node import Node # Node 클래스 가져옴
from turtlesim.msg import Pose # 터틀심의 Pose 메시지 타입을 가져옴

class PoseSubscriber(Node): # Node를 상속 받음
    def __init__(self):
        super().__init__('pose_subscriber') # 부모 클래스인 Node를 초기화하면서 ROS2 node 이름을 pose_subscriber로 정한다.
        
        self.subscription = self.create_subscription( # 생성 -> 생성한 subscriber 객체를 내부 변수로 저장
            Pose, # 토픽 메세지 타입 지정
            '/turtle1/pose', # 구독할 토픽 이름
            self.pose_callback, # 메시지 오면 보낼 콜백 함수 지정
            10 # 메시지 처리 동안 대기할 수 있는 대기열 크기
        )
        
    def pose_callback(self, msg):
        self.get_logger().info(
            f'x={msg.x:.2f}, y={msg.y:.2f}, theta={msg.theta:.2f}'
        )
        # print가 아닌 get_logger로 하는 이유:
        # 1. 어떤 node에서 출력한 로그인지 구분하기 좋다.
        # 2. ROS2 로그 시스템과 연결된다.
        # 3. 나중에 launch, debugging, log level 관리에 유리하다.

def main(args = None):
    rclpy.init(args=args) # 이 파이썬 파일을 ROS2 노드로 실행할 준비

    node = PoseSubscriber() # 노드 생성

    rclpy.spin(node) # 계속 실행 상태

    node.destroy_node() # 노드 정리 Ctrl+C를 위함
    rclpy.shutdown() # init으로 시작하고 shutdown으로 정리

if __name__ == '__main__':
    main()