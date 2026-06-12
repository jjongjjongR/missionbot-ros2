# 2026-06-12 신규 : 검증된 Mission command를 JSON 문자열로 변환하기 위해 json 모듈을 불러옴.
import json

# 2026-06-12 신규 : ROS2 Python client library를 사용하기 위해 rclpy를 불러옴.
import rclpy

# 2026-06-12 신규 : ROS2 Node 클래스를 상속받기 위해 Node를 불러옴.
from rclpy.node import Node

# 2026-06-12 신규 : 자연어 명령과 JSON 결과를 ROS2 topic으로 전달하기 위해 String message를 불러옴.
from std_msgs.msg import String

# 2026-06-12 신규 : 자연어 명령을 Structured MissionCommand로 변환하는 LLM Parser 함수를 불러옴.
from mission_parser.llm_mission_parser import parse_mission_command

# 2026-06-12 신규 : Mission command의 의미 검증과 실행 허용 여부를 판단하는 함수를 불러옴.
from mission_parser.semantic_validator import (
    is_execution_allowed,
    validate_mission_command,
)


# 2026-06-12 신규 : 자연어 ROS2 topic을 받아 LLM Parser와 Validator를 실행하는 Node를 정의함.
class MissionParserNode(Node):

    # 2026-06-12 신규 : Mission Parser Node의 topic publisher와 subscriber를 초기화함.
    def __init__(self) -> None:

        # 2026-06-12 신규 : ROS2 graph에서 사용할 Node 이름을 mission_parser_node로 설정함.
        super().__init__("mission_parser_node")

        # 2026-06-12 신규 : 사용자의 자연어 명령을 받을 topic 이름을 정의함.
        self.user_command_topic = (
            "/missionbot/user_command"
        )

        # 2026-06-12 신규 : 검증된 Mission command를 발행할 topic 이름을 정의함.
        self.mission_command_topic = (
            "/missionbot/mission_command"
        )

        # 2026-06-12 신규 : 자연어 String message를 수신하는 subscriber를 생성함.
        self.command_subscription = (
            self.create_subscription(
                String,
                self.user_command_topic,
                self.command_callback,
                10,
            )
        )

        # 2026-06-12 신규 : 검증된 Mission command JSON을 발행하는 publisher를 생성함.
        self.mission_publisher = (
            self.create_publisher(
                String,
                self.mission_command_topic,
                10,
            )
        )

        # 2026-06-12 신규 : Node가 정상적으로 시작되었음을 터미널에 출력함.
        self.get_logger().info(
            "Mission Parser Node가 시작되었습니다."
        )

        # 2026-06-12 신규 : 자연어 명령을 수신할 topic 이름을 터미널에 출력함.
        self.get_logger().info(
            "명령 수신 topic: "
            f"{self.user_command_topic}"
        )

        # 2026-06-12 신규 : 검증된 Mission command를 발행할 topic 이름을 터미널에 출력함.
        self.get_logger().info(
            "결과 발행 topic: "
            f"{self.mission_command_topic}"
        )

    # 2026-06-12 신규 : 자연어 String message가 도착했을 때 실행되는 callback 함수를 정의함.
    def command_callback(
        self,
        message: String,
    ) -> None:

        # 2026-06-12 신규 : ROS2 String message에서 자연어 명령을 읽고 앞뒤 공백을 제거함.
        user_command = message.data.strip()

        # 2026-06-12 신규 : 빈 문자열이 들어오면 LLM API를 호출하지 않고 처리를 종료함.
        if not user_command:
            self.get_logger().warning(
                "빈 사용자 명령을 수신하여 처리하지 않았습니다."
            )
            return

        # 2026-06-12 신규 : 수신한 자연어 명령을 터미널에 출력함.
        self.get_logger().info(
            f"사용자 명령 수신: {user_command}"
        )

        try:
            # 2026-06-12 신규 : 자연어 명령을 OpenAI 기반 LLM Mission Parser에 전달함.
            mission_command = parse_mission_command(
                user_command
            )

        # 2026-06-12 신규 : OpenAI API 호출 또는 Structured Outputs 처리 중 발생한 예외를 확인함.
        except Exception as error:
            self.get_logger().error(
                "LLM Mission Parser 실행 중 "
                f"오류가 발생했습니다: {error}"
            )
            return

        # 2026-06-12 신규 : LLM이 Mission command를 생성하지 못하면 topic을 발행하지 않음.
        if mission_command is None:
            self.get_logger().error(
                "Mission command가 생성되지 않았습니다."
            )
            return

        # 2026-06-12 신규 : Pydantic MissionCommand 객체를 일반 Python dictionary로 변환함.
        command_dictionary = (
            mission_command.model_dump()
        )

        # 2026-06-12 신규 : LLM이 생성한 Mission command를 Semantic Validator로 검사함.
        validation_result = (
            validate_mission_command(
                command_dictionary
            )
        )

        # 2026-06-12 신규 : Validator가 반환한 경고 메시지를 ROS2 logger로 출력함.
        for warning in validation_result.warnings:
            self.get_logger().warning(warning)

        # 2026-06-12 신규 : Semantic Validation에 실패하면 모든 오류를 출력하고 topic 발행을 차단함.
        if not validation_result.is_valid:

            # 2026-06-12 신규 : Validator가 발견한 오류를 순서대로 ROS2 logger에 출력함.
            for error in validation_result.errors:
                self.get_logger().error(error)

            # 2026-06-12 신규 : 유효하지 않은 Mission command가 실행 계층으로 전달되지 않도록 callback을 종료함.
            self.get_logger().error(
                "Semantic Validation에 실패하여 "
                "Mission command 발행을 차단했습니다."
            )
            return

        # 2026-06-12 신규 : Validation 결과와 intent를 사용해 실제 실행 허용 여부를 판단함.
        execution_allowed = (
            is_execution_allowed(
                command_dictionary,
                validation_result.is_valid,
            )
        )

        # 2026-06-12 신규 : unknown과 같이 지원 범위 밖인 명령은 유효해도 topic 발행을 차단함.
        if not execution_allowed:
            self.get_logger().warning(
                "Mission command는 의미적으로 유효하지만 "
                "MissionBot의 실행 지원 범위 밖이므로 "
                "발행하지 않았습니다."
            )
            return

        # 2026-06-12 신규 : 검증된 Mission command를 전달할 ROS2 String message를 생성함.
        output_message = String()

        # 2026-06-12 신규 : Mission command dictionary를 한 줄 JSON 문자열로 변환해 message에 저장함.
        output_message.data = json.dumps(
            command_dictionary,
            ensure_ascii=False,
        )

        # 2026-06-12 신규 : 검증되고 실행 가능한 Mission command를 ROS2 topic으로 발행함.
        self.mission_publisher.publish(
            output_message
        )

        # 2026-06-12 신규 : 실제로 발행한 Mission command JSON을 터미널에 출력함.
        self.get_logger().info(
            "검증된 Mission command 발행: "
            f"{output_message.data}"
        )


# 2026-06-12 신규 : ROS2 Mission Parser Node를 초기화하고 반복 실행하는 main 함수를 정의함.
def main(args=None) -> None:

    # 2026-06-12 신규 : ROS2 Python 통신 기능을 초기화함.
    rclpy.init(args=args)

    # 2026-06-12 신규 : MissionParserNode 객체를 생성함.
    mission_parser_node = (
        MissionParserNode()
    )

    try:
        # 2026-06-12 신규 : topic message가 들어올 때마다 callback을 실행하도록 Node를 반복 실행함.
        rclpy.spin(
            mission_parser_node
        )

    # 2026-06-12 신규 : Ctrl+C가 입력되면 오류 없이 Node 반복 실행을 종료함.
    except KeyboardInterrupt:
        pass

    finally:
        # 2026-06-12 신규 : 종료 전에 Mission Parser Node가 사용한 ROS2 자원을 해제함.
        mission_parser_node.destroy_node()

        # 2026-06-12 신규 : ROS2 Python 통신 기능을 종료함.
        rclpy.shutdown()


# 2026-06-12 신규 : 파일을 직접 실행했을 때 ROS2 Mission Parser Node를 시작함.
if __name__ == "__main__":
    main()