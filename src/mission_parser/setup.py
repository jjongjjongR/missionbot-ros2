from setuptools import find_packages, setup

package_name = 'mission_parser'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='user',
    maintainer_email='sx0123@naver.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'openai_connection_test = mission_parser.openai_connection_test:main',
            'llm_mission_parser = mission_parser.llm_mission_parser:main',
            'semantic_validator_test = mission_parser.semantic_validator_test:main',
            'mission_parser_node = mission_parser.mission_parser_node:main'
        ],
    },
)
