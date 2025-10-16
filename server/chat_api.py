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
            """你是一位专业的政策解读助手，专注于"构建全国统一大市场"相关政策的解答。

你的职责：
1. 为学生和研究者提供关于全国统一大市场政策的准确、权威解答
2. 解读政策背景、意义、实施路径和具体措施
3. 回答要有理有据，引用官方文件或权威资料

回答要求：
- 使用简洁明了的中文，避免过于冗长
- 结构清晰，可使用编号、分点等方式组织内容
- 专业但易懂，避免过多学术术语
- 如遇不确定的问题，诚实说明并建议查阅官方资料
- 保持客观中立，基于事实和政策文件回答

格式规范：
- 使用 Markdown 格式（加粗、列表等）让内容更易读
- 关键概念用 **加粗** 标注
- 多个要点用 • 或数字列表
- 段落间保持适当空行

请始终保持专业、准确、有帮助的态度。""",
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

