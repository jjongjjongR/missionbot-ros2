# 2026-06-12 신규 : Semantic Validator 함수가 포함된 모듈을 불러옴.
from mission_parser.semantic_validator import validate_mission_command


# 2026-06-12 신규 : Validator의 정상 및 오류 탐지 기능을 확인할 테스트 데이터를 정의함.
TEST_CASES = [
    {
        "name": "valid_move_to",
        "command": {
            "intent": "move_to",
            "target": "desk",
            "object": None,
            "constraints": ["front"],
            "requires_navigation": True,
            "requires_vision": False,
            "requires_manipulation": False,
        },
        "expected_valid": True,
    },
    {
        "name": "invalid_move_to_without_target",
        "command": {
            "intent": "move_to",
            "target": None,
            "object": None,
            "constraints": [],
            "requires_navigation": True,
            "requires_vision": False,
            "requires_manipulation": False,
        },
        "expected_valid": False,
    },
    {
        "name": "invalid_direction_used_as_target",
        "command": {
            "intent": "inspect_object",
            "target": "left",
            "object": "cup",
            "constraints": [],
            "requires_navigation": False,
            "requires_vision": True,
            "requires_manipulation": False,
        },
        "expected_valid": False,
    },
    {
        "name": "invalid_stop_with_navigation",
        "command": {
            "intent": "stop",
            "target": None,
            "object": None,
            "constraints": [],
            "requires_navigation": True,
            "requires_vision": False,
            "requires_manipulation": False,
        },
        "expected_valid": False,
    },
    {
        "name": "valid_unknown_with_preserved_object",
        "command": {
            "intent": "unknown",
            "target": None,
            "object": "coffee",
            "constraints": [],
            "requires_navigation": False,
            "requires_vision": False,
            "requires_manipulation": False,
        },
        "expected_valid": True,
    },
    {
        "name": "invalid_unknown_with_manipulation",
        "command": {
            "intent": "unknown",
            "target": None,
            "object": "coffee",
            "constraints": [],
            "requires_navigation": False,
            "requires_vision": False,
            "requires_manipulation": True,
        },
        "expected_valid": False,
    },
]


# 2026-06-12 신규 : 여러 테스트 명령을 Validator에 전달하고 예상 결과와 비교하는 함수를 정의함.
def main() -> None:

    # 2026-06-12 신규 : 전체 테스트 개수를 계산함.
    total_count = len(TEST_CASES)

    # 2026-06-12 신규 : 예상 결과와 일치한 테스트 개수를 저장함.
    passed_count = 0

    # 2026-06-12 신규 : Semantic Validator 독립 테스트 시작 메시지를 출력함.
    print("MissionBot Semantic Validator 테스트 시작")
    print(f"전체 테스트 수: {total_count}")
    print("=" * 60)

    # 2026-06-12 신규 : 정의한 테스트 케이스를 순서대로 실행함.
    for index, test_case in enumerate(
        TEST_CASES,
        start=1,
    ):
        # 2026-06-12 신규 : 현재 테스트의 이름을 읽어옴.
        test_name = test_case["name"]

        # 2026-06-12 신규 : Validator에 전달할 Mission command를 읽어옴.
        command = test_case["command"]

        # 2026-06-12 신규 : 현재 테스트가 기대하는 유효성 값을 읽어옴.
        expected_valid = test_case["expected_valid"]

        # 2026-06-12 신규 : Mission command를 Semantic Validator로 검사함.
        validation_result = validate_mission_command(
            command
        )

        # 2026-06-12 신규 : 현재 테스트 이름과 진행 순서를 출력함.
        print(f"\n[{index}/{total_count}] {test_name}")

        # 2026-06-12 신규 : Validator가 반환한 실제 유효성 결과를 출력함.
        print(
            "실제 Validation 결과: "
            f"{validation_result.is_valid}"
        )

        # 2026-06-12 신규 : 테스트에서 기대한 유효성 결과를 출력함.
        print(
            "예상 Validation 결과: "
            f"{expected_valid}"
        )

        # 2026-06-12 신규 : 발견된 오류가 있으면 각 오류 메시지를 출력함.
        if validation_result.errors:
            print("Errors:")

            for error in validation_result.errors:
                print(f"- {error}")

        # 2026-06-12 신규 : 발견된 경고가 있으면 각 경고 메시지를 출력함.
        if validation_result.warnings:
            print("Warnings:")

            for warning in validation_result.warnings:
                print(f"- {warning}")

        # 2026-06-12 신규 : 실제 결과와 예상 결과가 같은지 확인함.
        is_test_passed = (
            validation_result.is_valid
            == expected_valid
        )

        # 2026-06-12 신규 : 예상한 Validation 결과와 일치하면 PASS로 기록함.
        if is_test_passed:
            passed_count += 1
            print("판정: PASS")

        # 2026-06-12 신규 : 예상한 Validation 결과와 다르면 FAIL로 기록함.
        else:
            print("판정: FAIL")

        # 2026-06-12 신규 : 각 테스트 결과를 구분하는 선을 출력함.
        print("-" * 60)

    # 2026-06-12 신규 : 전체 Validator 테스트 결과를 출력함.
    print("\n최종 Semantic Validator 테스트 결과")
    print(f"PASS: {passed_count}")
    print(f"FAIL: {total_count - passed_count}")
    print(f"TOTAL: {total_count}")

# 2026-06-12 신규 : 파일을 직접 실행했을 때 main 함수를 호출함.
if __name__ == "__main__":
    main()