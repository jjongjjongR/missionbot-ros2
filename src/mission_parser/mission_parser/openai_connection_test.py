# 2026-06-06 신규: OpenAI API 연결 테스트를 위한 기본 Python 파일입니다.
# API key는 코드에 직접 쓰지 않고, 프로젝트 루트의 .env 파일에서 읽어옵니다.

import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


def main():
    # 2026-06-06 수정: ros2 run 실행 시 __file__ 기준 경로는 install/ 쪽으로 잡힐 수 있습니다.
    # 따라서 이번 실습에서는 현재 터미널 위치를 프로젝트 루트로 보고 .env를 찾습니다.
    project_root = Path.cwd()

    # 2026-06-06 신규: 프로젝트 루트의 .env 파일을 로드합니다.
    env_path = project_root / ".env"
    load_dotenv(dotenv_path=env_path)

    # 2026-06-06 신규: .env에서 OpenAI API key를 읽어옵니다.
    api_key = os.environ.get("OPENAI_API_KEY")

    # 2026-06-06 신규: API key가 없으면 안내 메시지를 출력하고 종료합니다.
    if not api_key:
        print("OPENAI_API_KEY를 찾지 못했습니다.")
        print(f"현재 작업 위치: {project_root}")
        print(f"확인한 .env 경로: {env_path}")
        print(".env 파일에 OPENAI_API_KEY=본인_API_KEY 형식으로 작성했는지 확인하세요.")
        return

    # 2026-06-06 신규: OpenAI API 클라이언트를 생성합니다.
    client = OpenAI(api_key=api_key)

    # 2026-06-06 신규: MissionBot Phase 10 연결 테스트용 요청을 보냅니다.
    response = client.responses.create(
        model="gpt-4.1-mini",
        input="MissionBot-ROS2 Phase 10 연결 테스트입니다. 한 문장으로 응답해줘.",
    )

    # 2026-06-06 신규: LLM 응답 텍스트를 터미널에 출력합니다.
    print("LLM 응답:")
    print(response.output_text)


if __name__ == "__main__":
    main()