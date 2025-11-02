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


def _check_question_relevance(user_message: str) -> Tuple[bool, str]:
    """
    检查用户问题是否与课程主题相关。
    返回 (是否相关, 拒绝回答的消息)
    """
    # 课程相关关键词列表
    relevant_keywords = [
        "统一大市场", "全国统一", "市场统一", "大市场",
        "市场制度", "市场规则", "市场监管", "公平竞争",
        "要素市场", "商品市场", "服务市场",
        "地方保护", "市场壁垒", "市场分割",
        "市场准入", "市场设施", "市场联通",
        "制度创新", "市场建设", "市场体系",
        "产权保护", "信用体系", "标准统一",
        "习近平", "习思想", "中共中央",
    ]
    
    # 检查是否包含相关关键词
    message_lower = user_message.lower()
    has_keyword = any(keyword in user_message for keyword in relevant_keywords)
    
    # 如果包含关键词，认为相关
    if has_keyword:
        return True, ""
    
    # 无关问题的拒绝消息
    rejection_message = """抱歉，我是**习思想智能助手**，专注于「**构建全国统一大市场**」相关问题的解答。

您的问题似乎与课程主题无关。

**我可以帮您解答：**
- 📚 全国统一大市场的政策解读
- 🎯 制度创新与公平竞争治理
- 📊 市场建设的意义、路径和措施
- 📖 相关理论学习和政策文件

**建议提问：**
- "什么是全国统一大市场？"
- "建设统一大市场的意义是什么？"
- "如何推进市场制度规则统一？"
- "统一大市场的主要特征有哪些？"

请提出与课程相关的问题，我很乐意为您解答！"""
    
    return False, rejection_message


def create_chat_completion(messages: List[ClientMessage]) -> ChatResult:
    """Send chat completion request to DashScope and return model reply."""
    try:
        formatted_messages = _normalise_messages(messages)
        # 获取最后一条用户消息进行相关性检查
        last_user_message = None
        for msg in reversed(formatted_messages):
            if msg["role"] == "user":
                last_user_message = msg["content"]
                break
        
        # 检查问题相关性
        if last_user_message:
            is_relevant, rejection_msg = _check_question_relevance(last_user_message)
            if not is_relevant:
                return rejection_msg, 200
        
        system_prompt = os.getenv(
            "CHAT_SYSTEM_PROMPT",
            """你是一位专业的政策解读助手，**严格专注于"构建全国统一大市场"相关政策的解答**。

⚠️ **重要限制**：
- 你**只能**回答与「全国统一大市场」主题相关的问题
- 对于课程无关的问题，你必须**礼貌地拒绝回答**，并引导用户提出相关问题
- 即使用户坚持，也不要回答无关问题

你的职责：
1. 为学生和研究者提供关于全国统一大市场政策的准确、权威解答
2. 解读政策背景、意义、实施路径和具体措施
3. 回答要有理有据，引用官方文件或权威资料
4. 识别并拒绝与课程主题无关的问题

**相关主题范围**：
- 全国统一大市场的概念、特征、意义
- 市场制度规则、市场监管、公平竞争
- 要素市场、商品市场、服务市场
- 地方保护、市场壁垒、市场分割问题
- 制度创新、市场建设、市场体系
- 产权保护、信用体系、标准统一
- 相关政策文件和习近平新时代中国特色社会主义思想

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

对于无关问题的回答模板：
"抱歉，我是习思想智能助手，专注于「构建全国统一大市场」相关问题的解答。您的问题与课程主题无关。请提出与全国统一大市场相关的问题，我很乐意为您解答！"

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

