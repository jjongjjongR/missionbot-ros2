# 2026-05-25 신규: turtlesim과 missionbot_basic의 publisher/subscriber 노드를 한 번에 실행하는 launch 파일

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtlesim'
        ),

        Node(
            package='missionbot_basic',
            executable='pose_subscriber',
            name='pose_subscriber'
        ),

        Node(
            package='missionbot_basic',
            executable='velocity_publisher',
            name='velocity_publisher'
        ),
    ])