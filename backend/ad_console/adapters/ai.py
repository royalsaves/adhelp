from __future__ import annotations

import json

import boto3

from ad_console.config import Settings
from ad_console.domain.models import ChatMessage


class DemoAIChatAdapter:
    def reply(self, history: list[ChatMessage], system_prompt: str) -> str:
        latest = history[-1].text.lower()
        if "password" in latest or "비밀번호" in latest:
            return "비밀번호 관련 요청은 '비밀번호 변경' 또는 '비밀번호 초기화' 메뉴에서 처리할 수 있습니다."
        if "vpn" in latest:
            return "VPN 이슈는 잠금 해제, QR 재발급, 가이드 문서 확인 순서로 안내하는 데모 응답입니다."
        # 데모 모드에서는 실제 모델 대신 고정 응답으로 흐름만 본다.
        return "로컬 데모 모드입니다. 실제 Bedrock 대신 예시 응답을 반환합니다."


class BedrockAIChatAdapter:
    def __init__(self, settings: Settings) -> None:
        self._model_id = settings.bedrock_model_id
        self._client = boto3.client("bedrock-runtime", region_name=settings.aws_region)

    def reply(self, history: list[ChatMessage], system_prompt: str) -> str:
        messages = []
        for item in history:
            role = "assistant" if item.role == "ai" else item.role
            if role not in {"user", "assistant"}:
                continue
            messages.append({"role": role, "content": [{"type": "text", "text": item.text}]})

        # 내부 메시지 포맷을 Bedrock 요청 포맷으로 바꿔서 넘긴다.
        response = self._client.invoke_model(
            modelId=self._model_id,
            contentType="application/json",
            accept="application/json",
            body=json.dumps(
                {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 2048,
                    "temperature": 0.5,
                    "system": system_prompt,
                    "messages": messages,
                }
            ),
        )

        body = json.loads(response["body"].read().decode("utf-8"))
        content = body.get("content", [])
        return content[0].get("text", "AI response is empty.") if content else "AI response is empty."
