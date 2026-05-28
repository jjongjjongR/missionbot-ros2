from setuptools import find_packages, setup

# 2026-05-25 신규: launch 파일을 설치 경로에 포함하기 위한 표준 라이브러리
import os
from glob import glob

package_name = 'missionbot_basic'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),

        # 2026-05-25 신규: ros2 launch가 launch 파일을 찾을 수 있도록 설치 경로에 포함
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='user',
    maintainer_email='user@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            # 2026-05-25 신규: ros2 run으로 pose_subscriber 노드를 실행하기 위한 진입점 등록
            'pose_subscriber = missionbot_basic.pose_subscriber:main',

            # 2026-05-25 신규: ros2 run으로 velocity_publisher 노드를 실행하기 위한 진입점 등록
            'velocity_publisher = missionbot_basic.velocity_publisher:main',
        ],
    },
)
