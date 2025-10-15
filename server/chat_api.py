import os
from typing import List, Dict, Tuple, Union, Optional

from openai import OpenAI

ClientMessage = Dict[str, str]
ChatResult = Tuple[Union[str, Dict[str, str]], int]

_client: Optional[OpenAI] = None


def _get_client() -> OpenAI:
    """Create and cache the OpenAI-compatible client for Aliyun DashScope."""
    global _client
    if _client is not None:
        return _client

    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise RuntimeError("缺少 DASHSCOPE_API_KEY 环境变量，请在 server/.env 中配置")

    base_url = os.getenv(
        "DASHSCOPE_BASE_URL",
        "https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    _client = OpenAI(api_key=api_key, base_url=base_url)
    return _client


def _normalise_messages(messages: List[ClientMessage]) -> List[ClientMessage]:
    """Validate message payload before sending it to the model."""
    cleaned: List[ClientMessage] = []

    for message in messages:
        role = message.get("role")
        content = message.get("content", "").strip()

        if role not in {"user", "assistant"}:
            raise ValueError("messages 中的 role 仅支持 'user' 或 'assistant'")
        if not content:
            raise ValueError("messages 中存在空内容，请检查输入")

        cleaned.append({"role": role, "content": content})

    if not any(msg["role"] == "user" for msg in cleaned):
        raise ValueError("messages 至少包含一条用户消息")

    return cleaned


def create_chat_completion(messages: List[ClientMessage]) -> ChatResult:
    """Send chat completion request to DashScope and return model reply."""
    try:
        formatted_messages = _normalise_messages(messages)
        system_prompt = os.getenv(
            "CHAT_SYSTEM_PROMPT",
            "You are a knowledgeable assistant helping students understand China's "
            "national unified market policies, provide concise and accurate answers.",
        )
        dashscope_messages = [
            {"role": "system", "content": system_prompt},
            *formatted_messages,
        ]

        client = _get_client()
        response = client.chat.completions.create(
            model=os.getenv("DASHSCOPE_MODEL", "qwen-plus"),
            messages=dashscope_messages,
        )

        content = response.choices[0].message.content
        return content, 200
    except ValueError as validation_error:
        return {"error": str(validation_error)}, 400
    except Exception as exc:  # noqa: BLE001 - surface vendor error to client
        return {
            "error": str(exc),
            "help": "https://help.aliyun.com/zh/model-studio/developer-reference/error-code",
        }, 500

