# 2026-06-12 신규 : 환경변수와 프로젝트 경로를 다루기 위한 기본 모듈을 불러옴.
import os
from pathlib import Path

# 2026-06-12 수정 : JSON 출력, 프롬프트 정리, 타입 제한, 테스트 타입 정의에 필요한 모듈을 추가함.
import json
from textwrap import dedent
from typing import Any, Literal

# 2026-06-12 신규 : .env 파일과 OpenAI API를 사용하기 위한 외부 라이브러리를 불러옴.
from dotenv import load_dotenv
from openai import OpenAI

# 2026-06-12 수정 : Structured Outputs의 schema와 필드 설명을 정의하기 위해 Pydantic을 추가함.
from pydantic import BaseModel, Field

# 2026-06-12 수정 : Mission command의 의미 검증과 실행 허용 여부를 판단하는 함수를 불러옴.
from mission_parser.semantic_validator import (
    is_execution_allowed,
    validate_mission_command,
)

# 2026-06-12 수정 : Mission Parser에서 사용할 OpenAI 모델을 gpt-4o-mini로 고정함.
MODEL_NAME = "gpt-4o-mini"


# 2026-06-12 수정 : LLM 응답의 필드와 자료형을 고정하기 위한 Pydantic schema를 정의함.
class MissionCommand(BaseModel):

    # 2026-06-12 수정 : MissionBot이 현재 허용하는 네 가지 명령 의도만 선택할 수 있도록 제한함.
    intent: Literal[
        "move_to",
        "inspect_object",
        "stop",
        "unknown",
    ] = Field(
        description="The primary intent of the user's command."
    )

    # 2026-06-12 수정 : 이동 목적지나 장소 landmark를 영어 표준 표현으로 저장함.
    target: str | None = Field(
        description=(
            "A navigation destination or spatial landmark. "
            "Use a simple canonical noun such as desk or shelf. "
            "Do not include spatial relations such as front_of_desk."
        )
    )

    # 2026-06-12 수정 : 사용자가 확인하거나 조작 대상으로 언급한 물체를 저장함.
    object: str | None = Field(
        description=(
            "An entity that the user explicitly mentions as an inspection, "
            "manipulation, or unsupported-action subject. "
            "Use null when a place or landmark is only a navigation destination."
        )
    )

    # 2026-06-12 수정 : 사용자가 명시한 방향이나 행동 조건을 문자열 배열로 저장함.
    constraints: list[str] = Field(
        description=(
            "Only explicitly stated spatial or behavioral constraints. "
            "Examples: front, left, right, stop_after_arrival. "
            "Never infer constraints that the user did not state."
        )
    )

    # 2026-06-12 수정 : 이동로봇의 base 이동이 필요한지를 나타냄.
    requires_navigation: bool = Field(
        description="True only when robot base movement is required."
    )

    # 2026-06-12 수정 : 카메라 영상이나 객체 인식이 필요한지를 나타냄.
    requires_vision: bool = Field(
        description="True only when visual scene or object recognition is required."
    )

    # 2026-06-12 수정 : 로봇팔을 이용한 집기, 놓기 등의 조작이 필요한지를 나타냄.
    requires_manipulation: bool = Field(
        description="True only when robot arm manipulation is required."
    )


# 2026-06-12 신규 : 프로젝트 루트의 .env 파일에서 OpenAI API key를 읽어오는 함수를 정의함.
def load_api_key() -> str | None:

    # 2026-06-12 신규 : 현재 터미널의 작업 위치를 MissionBot 프로젝트 루트로 사용함.
    project_root = Path.cwd()

    # 2026-06-12 신규 : 프로젝트 루트에 있는 .env 파일의 전체 경로를 생성함.
    env_path = project_root / ".env"

    # 2026-06-12 신규 : .env 파일에 저장된 환경변수를 현재 Python 프로세스로 불러옴.
    load_dotenv(dotenv_path=env_path)

    # 2026-06-12 신규 : OPENAI_API_KEY 환경변수 값을 읽어옴.
    api_key = os.environ.get("OPENAI_API_KEY")

    # 2026-06-12 신규 : API key가 없으면 확인한 경로를 출력하고 함수 실행을 종료함.
    if not api_key:
        print("OPENAI_API_KEY를 찾지 못했습니다.")
        print(f"현재 작업 위치: {project_root}")
        print(f"확인한 .env 경로: {env_path}")
        print(
            ".env 파일에 "
            "OPENAI_API_KEY=본인_API_KEY 형식으로 작성했는지 확인하세요."
        )
        return None

    # 2026-06-12 신규 : 정상적으로 읽은 API key를 호출한 코드에 반환함.
    return api_key


# 2026-06-12 수정 : LLM이 따라야 할 Mission Parser 역할과 의미 규칙을 별도 함수로 분리함.
def build_system_prompt() -> str:

    # 2026-06-12 수정 : Python 코드 들여쓰기가 실제 prompt에 포함되지 않도록 dedent를 적용함.
    return dedent(
        """
        너는 MissionBot-ROS2 프로젝트의 Mission Parser다.

        역할:
        - 사용자의 한국어 또는 영어 자연어 명령을 구조화된 mission command로 변환한다.
        - 로봇을 직접 실행하지 않는다.
        - Navigation2, MoveIt2, VLM 실행 코드를 생성하지 않는다.
        - 사용자의 명령에 없는 사실을 임의로 추가하지 않는다.

        출력 규칙:
        - 모든 문자열 값은 영어로 작성한다.
        - 모든 문자열 값은 가능한 한 lowercase snake_case 형식을 사용한다.
        - 한국어 장소, 물체, 방향 표현은 영어 표준 표현으로 정규화한다.

        의도 판단:
        - 특정 장소로 이동하는 명령은 move_to다.
        - 물체를 찾거나 확인하는 명령은 inspect_object다.
        - 현재 동작을 멈추라는 명령은 stop이다.
        - 현재 범위에서 해석할 수 없거나 지원하지 않는 명령은 unknown이다.

        unknown 처리 정책:
        - intent가 unknown이면 어떤 실행 모듈도 활성화하지 않는다.
        - requires_navigation, requires_vision, requires_manipulation은 모두 false다.
        - 명령에서 명확하게 추출할 수 있는 대상은 object에 보존할 수 있다.
        - 예를 들어 "커피를 만들어줘"는 intent=unknown, object=coffee로 표현한다.
        - unknown이라는 이유만으로 사용자가 명시한 모든 정보를 지우지 않는다.

        필요 모듈 판단:
        - 이동이 필요하면 requires_navigation은 true다.
        - 카메라나 물체 인식이 필요하면 requires_vision은 true다.
        - 잡기, 집기, 놓기 등 로봇팔 조작이 필요하면
          requires_manipulation은 true다.
        - 단, 현재 지원하지 않는 전체 작업이면 intent는 unknown이며
          모든 requires 필드는 false다.

        표준 표현:
        - 책상: desk
        - 선반: shelf
        - 컵: cup
        - 빨간 컵: red_cup
        - 커피: coffee
        - 왼쪽: left
        - 오른쪽: right
        - 앞: front
        - 뒤: behind
        - 도착 후 정지: stop_after_arrival

        공간 관계 해석 규칙:
        - front, behind, left, right, near는 장소나 물체 자체가 아니라 공간 관계다.
        - 공간 관계는 target에 넣지 않고 constraints 배열에 넣는다.
        - target에는 desk, shelf, table, door와 같은 장소 또는 landmark만 넣는다.
        - target에 front_of_desk, left, right 같은 값을 넣지 않는다.

        한국어 표현 변환 규칙:
        - "X 앞", "X 앞에", "X 앞으로", "X 앞까지"는
          target="X의 영어 표준명", constraints에 "front"를 추가한다.
        - "X 뒤", "X 뒤에", "X 뒤쪽"은
          target 또는 object는 그대로 유지하고 constraints에 "behind"를 추가한다.
        - "왼쪽에 있는 X"는
          object="X의 영어 표준명", target=null, constraints에 "left"를 추가한다.
        - "오른쪽에 있는 X"는
          object="X의 영어 표준명", target=null, constraints에 "right"를 추가한다.
        - 방향 표현만으로 target을 생성하지 않는다.

        명령 유형별 target 규칙:
        - move_to 명령에서 target은 이동할 장소 또는 landmark다.
        - inspect_object 명령에서 단순 방향은 target이 아니다.
        - inspect_object 명령에 명시적인 장소가 없다면 target은 null이다.
        - inspect_object의 방향 정보는 constraints에 넣는다.

        제약조건 보존 규칙:
        - 사용자가 명시한 공간 관계는 반드시 constraints에 보존한다.
        - "앞까지"에서 front를 생략하지 않는다.
        - "가서 멈춰"는 stop_after_arrival을 추가한다.
        - 사용자가 말하지 않은 공간 관계나 행동 조건은 추가하지 않는다.

        공간 관계 예시 1:
        입력: 선반 앞까지 가서 멈춰

        올바른 출력:
        {
          "intent": "move_to",
          "target": "shelf",
          "object": null,
          "constraints": ["front", "stop_after_arrival"],
          "requires_navigation": true,
          "requires_vision": false,
          "requires_manipulation": false
        }

        공간 관계 예시 2:
        입력: 왼쪽에 있는 컵을 확인해줘

        올바른 출력:
        {
          "intent": "inspect_object",
          "target": null,
          "object": "cup",
          "constraints": ["left"],
          "requires_navigation": false,
          "requires_vision": true,
          "requires_manipulation": false
        }

        unknown 예시:
        입력: 커피를 만들어줘

        올바른 출력:
        {
          "intent": "unknown",
          "target": null,
          "object": "coffee",
          "constraints": [],
          "requires_navigation": false,
          "requires_vision": false,
          "requires_manipulation": false
        }

        잘못된 공간 관계 출력:
        {
          "target": "left",
          "object": "cup",
          "constraints": []
        }

        잘못된 이유:
        - left는 목적지나 landmark가 아니다.
        - left는 cup의 공간 관계이므로 constraints에 들어가야 한다.
        """
    ).strip()


# 2026-06-12 수정 : 자연어 명령을 OpenAI Structured Outputs로 MissionCommand 객체로 변환함.
def parse_mission_command(user_command: str) -> MissionCommand | None:

    # 2026-06-12 신규 : .env 파일에서 OpenAI API key를 읽어옴.
    api_key = load_api_key()

    # 2026-06-12 신규 : API key를 읽지 못하면 OpenAI API 호출을 수행하지 않음.
    if not api_key:
        return None

    # 2026-06-12 신규 : OpenAI API 요청을 전송할 클라이언트를 생성함.
    client = OpenAI(api_key=api_key)

    # 2026-06-12 수정 : 별도 함수에서 Mission Parser system prompt를 불러옴.
    system_prompt = build_system_prompt()

    # 2026-06-12 수정 : Pydantic schema를 적용한 Structured Outputs 방식으로 LLM을 호출함.
    response = client.responses.parse(
        model=MODEL_NAME,
        input=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_command,
            },
        ],
        text_format=MissionCommand,
    )

    # 2026-06-12 수정 : schema 검증이 완료된 MissionCommand 객체를 반환함.
    return response.output_parsed


# 2026-06-12 수정 : Mission Parser의 여러 명령 유형을 검증하기 위한 테스트 데이터를 추가함.
TEST_CASES: list[dict[str, Any]] = [
    {
        "input": "책상 앞으로 이동해줘",
        "expected": {
            "intent": "move_to",
            "target": "desk",
            "object": None,
            "constraints": ["front"],
            "requires_navigation": True,
            "requires_vision": False,
            "requires_manipulation": False,
        },
    },
    {
        "input": "빨간 컵을 찾아줘",
        "expected": {
            "intent": "inspect_object",
            "target": None,
            "object": "red_cup",
            "constraints": [],
            "requires_navigation": False,
            "requires_vision": True,
            "requires_manipulation": False,
        },
    },
    {
        "input": "선반 앞까지 가서 멈춰",
        "expected": {
            "intent": "move_to",
            "target": "shelf",
            "object": None,
            "constraints": ["front", "stop_after_arrival"],
            "requires_navigation": True,
            "requires_vision": False,
            "requires_manipulation": False,
        },
    },
    {
        "input": "왼쪽에 있는 컵을 확인해줘",
        "expected": {
            "intent": "inspect_object",
            "target": None,
            "object": "cup",
            "constraints": ["left"],
            "requires_navigation": False,
            "requires_vision": True,
            "requires_manipulation": False,
        },
    },
    {
        "input": "멈춰",
        "expected": {
            "intent": "stop",
            "target": None,
            "object": None,
            "constraints": [],
            "requires_navigation": False,
            "requires_vision": False,
            "requires_manipulation": False,
        },
    },
        {
        "input": "커피를 만들어줘",
        "expected": {
            "intent": "unknown",
            "target": None,
            "object": "coffee",
            "constraints": [],
            "requires_navigation": False,
            "requires_vision": False,
            "requires_manipulation": False,
        },
    },
]


# 2026-06-12 수정 : constraints 배열 순서 차이를 제거하기 위한 정규화 함수를 추가함.
def normalize_mission_command(
    command: dict[str, Any],
) -> dict[str, Any]:

    # 2026-06-12 수정 : 원본 dictionary를 변경하지 않도록 복사본을 생성함.
    normalized = command.copy()

    # 2026-06-12 수정 : constraints의 순서가 달라도 같은 의미로 비교되도록 정렬함.
    normalized["constraints"] = sorted(normalized["constraints"])

    # 2026-06-12 수정 : 정규화가 완료된 Mission command를 반환함.
    return normalized


# 2026-06-12 수정 : 실제 LLM 결과와 예상 결과를 exact-match 방식으로 비교함.
def compare_mission_commands(
    actual: dict[str, Any],
    expected: dict[str, Any],
) -> bool:

    # 2026-06-12 수정 : 실제 결과의 constraints 배열 순서를 정규화함.
    normalized_actual = normalize_mission_command(actual)

    # 2026-06-12 수정 : 예상 결과의 constraints 배열 순서를 정규화함.
    normalized_expected = normalize_mission_command(expected)

    # 2026-06-12 수정 : 모든 필드가 동일한 경우에만 True를 반환함.
    return normalized_actual == normalized_expected

# 2026-06-12 수정 : LLM 출력에 Exact-match 비교와 Semantic Validation을 함께 수행하도록 main 함수를 확장함.
def main() -> None:

    # 2026-06-12 수정 : 예상 Mission command와 완전히 일치한 테스트 개수를 저장함.
    exact_match_passed_count = 0

    # 2026-06-12 신규 : Semantic Validation을 통과한 테스트 개수를 저장함.
    validation_passed_count = 0

    # 2026-06-12 신규 : 실행 계층으로 전달 가능한 테스트 명령 개수를 저장함.
    execution_allowed_count = 0

    # 2026-06-12 수정 : 전체 테스트 개수를 계산함.
    total_count = len(TEST_CASES)

    # 2026-06-12 수정 : LLM Mission Parser 통합 테스트 시작 정보를 출력함.
    print("MissionBot LLM Mission Parser + Semantic Validator 테스트 시작")
    print(f"전체 테스트 수: {total_count}")
    print("=" * 60)

    # 2026-06-12 수정 : 정의한 자연어 테스트 명령을 순서대로 실행함.
    for index, test_case in enumerate(
        TEST_CASES,
        start=1,
    ):
        # 2026-06-12 수정 : 현재 테스트의 사용자 자연어 명령을 읽어옴.
        user_command = test_case["input"]

        # 2026-06-12 수정 : 현재 테스트에서 기대하는 Mission command를 읽어옴.
        expected = test_case["expected"]

        # 2026-06-12 수정 : 현재 테스트 순서와 사용자 명령을 출력함.
        print(f"\n[{index}/{total_count}] 입력 명령")
        print(user_command)

        try:
            # 2026-06-12 수정 : 자연어 명령을 OpenAI LLM Mission Parser에 전달함.
            mission_command = parse_mission_command(
                user_command
            )

        # 2026-06-12 신규 : API 호출이나 Structured Outputs 처리 중 발생한 예외를 확인함.
        except Exception as error:
            print("\n결과: ERROR")
            print(
                "API 호출 또는 Structured Outputs 처리 중 "
                f"오류가 발생했습니다: {error}"
            )
            print("-" * 60)
            continue

        # 2026-06-12 수정 : LLM이 Mission command를 반환하지 못하면 현재 테스트를 실패 처리함.
        if mission_command is None:
            print("\n결과: FAIL")
            print("Mission command가 생성되지 않았습니다.")
            print("-" * 60)
            continue

        # 2026-06-12 수정 : Pydantic MissionCommand 객체를 일반 Python dictionary로 변환함.
        actual = mission_command.model_dump()

        # 2026-06-12 수정 : LLM이 생성한 실제 Mission command를 JSON 형식으로 출력함.
        print("\n실제 결과:")
        print(
            json.dumps(
                actual,
                ensure_ascii=False,
                indent=2,
            )
        )

        # 2026-06-12 수정 : 테스트에서 기대하는 Mission command를 JSON 형식으로 출력함.
        print("\n예상 결과:")
        print(
            json.dumps(
                expected,
                ensure_ascii=False,
                indent=2,
            )
        )

        # 2026-06-12 신규 : LLM이 생성한 Mission command를 Semantic Validator로 검사함.
        validation_result = validate_mission_command(
            actual
        )

        # 2026-06-12 신규 : Semantic Validation 통과 여부를 출력함.
        print("\nSemantic Validation 결과:")
        print(f"is_valid: {validation_result.is_valid}")

        # 2026-06-12 신규 : Semantic Validator가 발견한 오류를 순서대로 출력함.
        if validation_result.errors:
            print("Errors:")

            for error in validation_result.errors:
                print(f"- {error}")

        # 2026-06-12 신규 : Semantic Validator가 발견한 경고를 순서대로 출력함.
        if validation_result.warnings:
            print("Warnings:")

            for warning in validation_result.warnings:
                print(f"- {warning}")

        # 2026-06-12 신규 : Semantic Validation을 통과한 테스트 개수를 증가시킴.
        if validation_result.is_valid:
            validation_passed_count += 1

        # 2026-06-12 신규 : 현재 Mission command가 실행 계층으로 전달 가능한지 판단함.
        execution_allowed = is_execution_allowed(
            actual,
            validation_result.is_valid,
        )

        # 2026-06-12 신규 : 현재 Mission command의 실행 허용 여부를 출력함.
        print(
            "Execution Allowed: "
            f"{execution_allowed}"
        )

        # 2026-06-12 신규 : 실행 가능한 테스트 명령 개수를 증가시킴.
        if execution_allowed:
            execution_allowed_count += 1

        # 2026-06-12 신규 : Semantic Validation에 실패한 명령은 Exact-match 여부와 관계없이 실패 처리함.
        if not validation_result.is_valid:
            print(
                "\n판정: FAIL "
                "(Semantic Validation 실패)"
            )
            print("-" * 60)
            continue

        # 2026-06-12 수정 : 실제 Mission command와 예상 Mission command를 비교함.
        is_exact_match = compare_mission_commands(
            actual,
            expected,
        )

        # 2026-06-12 수정 : 실제 결과와 예상 결과가 완전히 일치하면 PASS로 기록함.
        if is_exact_match:
            exact_match_passed_count += 1
            print("\n판정: PASS")

        # 2026-06-12 수정 : Semantic Validation은 통과했지만 예상 결과와 다르면 Exact-match 실패로 기록함.
        else:
            print(
                "\n판정: FAIL "
                "(Exact-match 불일치)"
            )

        # 2026-06-12 수정 : 각 테스트 결과를 구분하는 선을 출력함.
        print("-" * 60)

    # 2026-06-12 수정 : 전체 LLM Mission Parser 통합 테스트 결과를 출력함.
    print("\n최종 통합 테스트 결과")
    print(
        "Exact-match PASS: "
        f"{exact_match_passed_count}"
    )
    print(
        "Exact-match FAIL: "
        f"{total_count - exact_match_passed_count}"
    )
    print(f"TOTAL: {total_count}")

    # 2026-06-12 수정 : 명령 단위 Exact-match 비율을 계산함.
    exact_match_rate = (
        exact_match_passed_count
        / total_count
        * 100
    )

    # 2026-06-12 수정 : 명령 단위 Exact-match 비율을 출력함.
    print(
        "Exact-match pass rate: "
        f"{exact_match_rate:.1f}%"
    )

    # 2026-06-12 신규 : Semantic Validation 통과 개수를 출력함.
    print(
        "Semantic Validation PASS: "
        f"{validation_passed_count}/{total_count}"
    )

    # 2026-06-12 신규 : 실행 계층으로 전달 가능한 명령 개수를 출력함.
    print(
        "Execution Allowed: "
        f"{execution_allowed_count}/{total_count}"
    )


# 2026-06-12 수정 : ros2 run으로 이 파일이 실행되면 main 함수를 호출함.
if __name__ == "__main__":
    main()