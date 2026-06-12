# 2026-06-12 신규 : 문자열 형식 검사를 위해 정규표현식 모듈을 불러옴.
import re

# 2026-06-12 신규 : Mission command dictionary의 여러 값 형식을 표현하기 위해 Any를 불러옴.
from typing import Any

# 2026-06-12 신규 : Semantic Validation 결과를 구조화된 객체로 표현하기 위해 BaseModel을 불러옴.
from pydantic import BaseModel


# 2026-06-12 신규 : Mission Parser가 사용할 수 있는 공간 관계 표현을 정의함.
SPATIAL_RELATIONS = {
    "front",
    "behind",
    "left",
    "right",
    "near",
}


# 2026-06-12 신규 : Mission Parser의 constraints 필드에서 허용할 값을 정의함.
ALLOWED_CONSTRAINTS = SPATIAL_RELATIONS | {
    "stop_after_arrival",
}


# 2026-06-12 신규 : 영어 lowercase_snake_case 문자열인지 검사할 정규표현식을 정의함.
LOWERCASE_SNAKE_CASE_PATTERN = re.compile(
    r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)*$"
)


# 2026-06-12 신규 : Semantic Validator의 검사 결과 구조를 정의함.
class SemanticValidationResult(BaseModel):

    # 2026-06-12 신규 : Mission command가 의미 규칙을 통과했는지 저장함.
    is_valid: bool

    # 2026-06-12 신규 : 실행을 차단해야 하는 오류 메시지 목록을 저장함.
    errors: list[str]

    # 2026-06-12 신규 : 실행을 차단하지 않는 참고 메시지 목록을 저장함.
    warnings: list[str]


# 2026-06-12 신규 : 문자열이 lowercase_snake_case 형식인지 검사하는 함수를 정의함.
def is_lowercase_snake_case(value: str) -> bool:

    # 2026-06-12 신규 : 문자열 전체가 정의한 정규표현식과 일치하는지 확인함.
    return bool(
        LOWERCASE_SNAKE_CASE_PATTERN.fullmatch(value)
    )


# 2026-06-12 신규 : target 값이 공간 관계를 목적지처럼 잘못 표현했는지 검사함.
def is_invalid_spatial_target(value: str) -> bool:

    # 2026-06-12 신규 : left, right, front 같은 공간 관계 자체가 target이면 잘못된 값으로 판단함.
    if value in SPATIAL_RELATIONS:
        return True

    # 2026-06-12 신규 : front_of_desk처럼 공간 관계와 landmark를 합친 target을 검사함.
    for relation in SPATIAL_RELATIONS:
        combined_prefix = f"{relation}_of_"

        # 2026-06-12 신규 : target이 공간 관계 결합 표현으로 시작하면 잘못된 값으로 판단함.
        if value.startswith(combined_prefix):
            return True

    # 2026-06-12 신규 : 공간 관계 target 문제가 없으면 False를 반환함.
    return False


# 2026-06-12 신규 : Mission command의 의미적 일관성과 실행 안전 규칙을 검사하는 함수를 정의함.
def validate_mission_command(
    command: dict[str, Any],
) -> SemanticValidationResult:

    # 2026-06-12 신규 : 발견한 의미 오류를 저장할 빈 목록을 생성함.
    errors: list[str] = []

    # 2026-06-12 신규 : 실행을 막지는 않지만 확인이 필요한 내용을 저장할 빈 목록을 생성함.
    warnings: list[str] = []

    # 2026-06-12 신규 : Semantic Validation에 필요한 필수 필드 이름을 정의함.
    required_fields = {
        "intent",
        "target",
        "object",
        "constraints",
        "requires_navigation",
        "requires_vision",
        "requires_manipulation",
    }

    # 2026-06-12 신규 : Mission command에 존재하지 않는 필수 필드를 계산함.
    missing_fields = sorted(
        required_fields - set(command.keys())
    )

    # 2026-06-12 신규 : 필수 필드가 누락되면 더 이상 의미 검사를 수행할 수 없으므로 즉시 실패 결과를 반환함.
    if missing_fields:
        errors.append(
            "[REQUIRED_FIELDS_MISSING] "
            f"필수 필드가 누락되었습니다: {missing_fields}"
        )

        return SemanticValidationResult(
            is_valid=False,
            errors=errors,
            warnings=warnings,
        )

    # 2026-06-12 신규 : intent 필드 값을 읽어옴.
    intent = command["intent"]

    # 2026-06-12 신규 : target 필드 값을 읽어옴.
    target = command["target"]

    # 2026-06-12 신규 : object 필드 값을 읽어옴.
    object_name = command["object"]

    # 2026-06-12 신규 : constraints 필드 값을 읽어옴.
    constraints = command["constraints"]

    # 2026-06-12 신규 : Navigation2 실행 필요 여부를 읽어옴.
    requires_navigation = command["requires_navigation"]

    # 2026-06-12 신규 : Vision 실행 필요 여부를 읽어옴.
    requires_vision = command["requires_vision"]

    # 2026-06-12 신규 : MoveIt2 실행 필요 여부를 읽어옴.
    requires_manipulation = command["requires_manipulation"]

    # 2026-06-12 신규 : target이 문자열일 때 영어 lowercase_snake_case 형식인지 검사함.
    if isinstance(target, str):
        if not is_lowercase_snake_case(target):
            errors.append(
                "[TARGET_FORMAT_INVALID] "
                "target은 lowercase_snake_case 형식이어야 합니다."
            )

        # 2026-06-12 신규 : 방향이나 공간 관계가 target으로 잘못 사용되었는지 검사함.
        if is_invalid_spatial_target(target):
            errors.append(
                "[TARGET_SPATIAL_RELATION_INVALID] "
                "방향이나 공간 관계는 target이 아니라 "
                "constraints에 들어가야 합니다."
            )

    # 2026-06-12 신규 : object가 문자열일 때 영어 lowercase_snake_case 형식인지 검사함.
    if isinstance(object_name, str):
        if not is_lowercase_snake_case(object_name):
            errors.append(
                "[OBJECT_FORMAT_INVALID] "
                "object는 lowercase_snake_case 형식이어야 합니다."
            )

    # 2026-06-12 신규 : constraints가 배열이 아닐 경우 의미 검사를 중단할 수 있도록 오류를 추가함.
    if not isinstance(constraints, list):
        errors.append(
            "[CONSTRAINTS_TYPE_INVALID] "
            "constraints는 list 형식이어야 합니다."
        )

        # 2026-06-12 신규 : 이후 검사에서 오류가 발생하지 않도록 빈 배열로 대체함.
        constraints = []

    # 2026-06-12 신규 : 중복된 constraint가 존재하는지 검사함.
    if len(constraints) != len(set(constraints)):
        errors.append(
            "[CONSTRAINT_DUPLICATED] "
            "constraints에 중복된 값이 존재합니다."
        )

    # 2026-06-12 신규 : constraints 배열의 각 값을 순서대로 검사함.
    for constraint in constraints:

        # 2026-06-12 신규 : constraint가 문자열이 아니면 잘못된 값으로 판단함.
        if not isinstance(constraint, str):
            errors.append(
                "[CONSTRAINT_TYPE_INVALID] "
                "각 constraint는 문자열이어야 합니다."
            )
            continue

        # 2026-06-12 신규 : constraint 문자열이 lowercase_snake_case 형식인지 검사함.
        if not is_lowercase_snake_case(constraint):
            errors.append(
                "[CONSTRAINT_FORMAT_INVALID] "
                f"잘못된 constraint 형식입니다: {constraint}"
            )

        # 2026-06-12 신규 : 현재 MissionBot에서 허용한 constraint인지 검사함.
        if constraint not in ALLOWED_CONSTRAINTS:
            errors.append(
                "[CONSTRAINT_UNSUPPORTED] "
                f"지원하지 않는 constraint입니다: {constraint}"
            )

    # 2026-06-12 신규 : stop_after_arrival은 이동 명령에서만 사용할 수 있도록 검사함.
    if (
        "stop_after_arrival" in constraints
        and intent != "move_to"
    ):
        errors.append(
            "[STOP_AFTER_ARRIVAL_INTENT_INVALID] "
            "stop_after_arrival은 move_to 명령에서만 사용할 수 있습니다."
        )

    # 2026-06-12 신규 : move_to 명령에 필요한 의미 규칙을 검사함.
    if intent == "move_to":

        # 2026-06-12 신규 : 이동 명령에는 목적지 또는 landmark가 반드시 존재해야 함.
        if target is None:
            errors.append(
                "[MOVE_TO_TARGET_REQUIRED] "
                "move_to 명령에는 target이 필요합니다."
            )

        # 2026-06-12 신규 : 이동 목적지는 target으로 표현하므로 object는 null이어야 함.
        if object_name is not None:
            errors.append(
                "[MOVE_TO_OBJECT_MUST_BE_NULL] "
                "move_to 명령의 object는 null이어야 합니다."
            )

        # 2026-06-12 신규 : 이동 명령은 Navigation2 실행이 필요해야 함.
        if requires_navigation is not True:
            errors.append(
                "[MOVE_TO_NAVIGATION_REQUIRED] "
                "move_to 명령의 requires_navigation은 true여야 합니다."
            )

        # 2026-06-12 신규 : 현재 move_to 명령은 로봇팔 조작을 포함하지 않도록 검사함.
        if requires_manipulation is not False:
            errors.append(
                "[MOVE_TO_MANIPULATION_INVALID] "
                "move_to 명령의 requires_manipulation은 false여야 합니다."
            )

    # 2026-06-12 신규 : inspect_object 명령에 필요한 의미 규칙을 검사함.
    elif intent == "inspect_object":

        # 2026-06-12 신규 : 물체 탐색 또는 확인 명령에는 대상 object가 필요함.
        if object_name is None:
            errors.append(
                "[INSPECT_OBJECT_REQUIRED] "
                "inspect_object 명령에는 object가 필요합니다."
            )

        # 2026-06-12 신규 : 물체 탐색 또는 확인에는 Vision 처리가 필요해야 함.
        if requires_vision is not True:
            errors.append(
                "[INSPECT_VISION_REQUIRED] "
                "inspect_object 명령의 requires_vision은 true여야 합니다."
            )

        # 2026-06-12 신규 : 물체 확인 명령은 로봇팔 조작 명령이 아니므로 false여야 함.
        if requires_manipulation is not False:
            errors.append(
                "[INSPECT_MANIPULATION_INVALID] "
                "inspect_object 명령의 requires_manipulation은 false여야 합니다."
            )

    # 2026-06-12 신규 : stop 명령에 필요한 의미 규칙을 검사함.
    elif intent == "stop":

        # 2026-06-12 신규 : 즉시 정지 명령에는 이동 목적지가 없어야 함.
        if target is not None:
            errors.append(
                "[STOP_TARGET_MUST_BE_NULL] "
                "stop 명령의 target은 null이어야 합니다."
            )

        # 2026-06-12 신규 : 즉시 정지 명령에는 탐색 또는 조작 대상이 없어야 함.
        if object_name is not None:
            errors.append(
                "[STOP_OBJECT_MUST_BE_NULL] "
                "stop 명령의 object는 null이어야 합니다."
            )

        # 2026-06-12 신규 : 즉시 정지 명령에는 별도 constraint가 없어야 함.
        if constraints:
            errors.append(
                "[STOP_CONSTRAINTS_MUST_BE_EMPTY] "
                "stop 명령의 constraints는 비어 있어야 합니다."
            )

        # 2026-06-12 신규 : stop 명령이 새로운 Navigation 실행을 요청하지 않는지 검사함.
        if requires_navigation is not False:
            errors.append(
                "[STOP_NAVIGATION_MUST_BE_FALSE] "
                "stop 명령의 requires_navigation은 false여야 합니다."
            )

        # 2026-06-12 신규 : stop 명령이 Vision 실행을 요청하지 않는지 검사함.
        if requires_vision is not False:
            errors.append(
                "[STOP_VISION_MUST_BE_FALSE] "
                "stop 명령의 requires_vision은 false여야 합니다."
            )

        # 2026-06-12 신규 : stop 명령이 Manipulation 실행을 요청하지 않는지 검사함.
        if requires_manipulation is not False:
            errors.append(
                "[STOP_MANIPULATION_MUST_BE_FALSE] "
                "stop 명령의 requires_manipulation은 false여야 합니다."
            )

    # 2026-06-12 신규 : unknown 명령의 실행 차단 규칙을 검사함.
    elif intent == "unknown":

        # 2026-06-12 신규 : 지원 범위 밖 명령이 Navigation을 실행하지 않도록 검사함.
        if requires_navigation is not False:
            errors.append(
                "[UNKNOWN_NAVIGATION_MUST_BE_FALSE] "
                "unknown 명령의 requires_navigation은 false여야 합니다."
            )

        # 2026-06-12 신규 : 지원 범위 밖 명령이 Vision을 실행하지 않도록 검사함.
        if requires_vision is not False:
            errors.append(
                "[UNKNOWN_VISION_MUST_BE_FALSE] "
                "unknown 명령의 requires_vision은 false여야 합니다."
            )

        # 2026-06-12 신규 : 지원 범위 밖 명령이 Manipulation을 실행하지 않도록 검사함.
        if requires_manipulation is not False:
            errors.append(
                "[UNKNOWN_MANIPULATION_MUST_BE_FALSE] "
                "unknown 명령의 requires_manipulation은 false여야 합니다."
            )

                # 2026-06-12 수정 : unknown 명령에 target, object 또는 constraint가 남아 있는지 확인함.
        has_preserved_information = (
            target is not None
            or object_name is not None
            or bool(constraints)
        )

        # 2026-06-12 수정 : unknown 명령의 모든 실행 flag가 false인지 확인함.
        all_execution_flags_disabled = (
            requires_navigation is False
            and requires_vision is False
            and requires_manipulation is False
        )

        # 2026-06-12 수정 : 추출 정보는 남아 있지만 모든 실행이 차단된 안전한 unknown 명령에만 경고를 추가함.
        if (
            has_preserved_information
            and all_execution_flags_disabled
        ):
            warnings.append(
                "[UNKNOWN_ENTITY_PRESERVED] "
                "unknown 명령에 추출된 정보가 남아 있지만 "
                "모든 실행 flag가 false이므로 실행은 차단됩니다."
            )

    # 2026-06-12 신규 : 현재 Mission Parser가 지원하지 않는 intent를 오류로 처리함.
    else:
        errors.append(
            "[INTENT_UNSUPPORTED] "
            f"지원하지 않는 intent입니다: {intent}"
        )

    # 2026-06-12 신규 : 오류가 하나도 없을 때만 Semantic Validation을 통과시킴.
    is_valid = len(errors) == 0

    # 2026-06-12 신규 : 최종 검사 결과와 오류 및 경고 목록을 반환함.
    return SemanticValidationResult(
        is_valid=is_valid,
        errors=errors,
        warnings=warnings,
    )

# 2026-06-12 신규 : Semantic Validation 결과와 intent를 사용해 Mission command의 실행 허용 여부를 판단함.
def is_execution_allowed(
    command: dict[str, Any],
    validation_is_valid: bool,
) -> bool:

    # 2026-06-12 신규 : Semantic Validation을 통과하지 못한 명령은 실행 계층으로 전달하지 않음.
    if not validation_is_valid:
        return False

    # 2026-06-12 신규 : unknown 명령은 내부 구조가 유효해도 MissionBot의 지원 범위 밖이므로 실행하지 않음.
    if command["intent"] == "unknown":
        return False

    # 2026-06-12 신규 : Validation을 통과한 지원 intent는 실행 계층으로 전달할 수 있음.
    return True