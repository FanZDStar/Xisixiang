<template>
  <view class="chat-page">
    <!-- 快捷问题 -->
    <view v-if="messages.length === 1" class="quick-questions">
      <view
        v-for="(q, idx) in quickQuestions"
        :key="idx"
        class="quick-question-chip"
        @click="askQuestion(q)"
      >
        <text>{{ q }}</text>
      </view>
    </view>

    <!-- 聊天窗口 -->
    <scroll-view
      scroll-y
      class="chat-window"
      :scroll-into-view="scrollIntoView"
      scroll-with-animation
      :enhanced="true"
      :show-scrollbar="false"
    >
      <view
        v-for="(msg, index) in messages"
        :key="index"
        :id="'msg-' + index"
        class="message-wrapper"
      >
        <view :class="['message', msg.sender]">
          <view v-if="msg.sender === 'bot'" class="bot-avatar">🤖</view>
          <view class="message-content">
            <text v-if="msg.sender === 'user'">{{ msg.text }}</text>
            <rich-text v-else :nodes="formatMarkdown(msg.text)"></rich-text>
          </view>
          <view v-if="msg.sender === 'user'" class="user-avatar">👤</view>
        </view>
      </view>

      <!-- 加载动画 -->
      <view v-if="loading" class="loading-wrapper">
        <view class="loading-dots">
          <view class="dot"></view>
          <view class="dot"></view>
          <view class="dot"></view>
        </view>
      </view>
    </scroll-view>

    <!-- 输入框 -->
    <view class="input-box">
      <input
        v-model="inputText"
        placeholder="💬 例如：什么是全国统一大市场？"
        placeholder-class="input-placeholder"
        confirm-type="send"
        @confirm="sendMessage"
        :disabled="loading"
      />
      <button
        @click="sendMessage"
        :disabled="loading || !inputText.trim()"
        class="send-btn"
        :class="{ disabled: loading || !inputText.trim() }"
      >
        <text>{{ loading ? "⏳" : "📤" }}</text>
      </button>
    </view>
  </view>
</template>

<script setup>
import { ref, nextTick } from "vue";
import { chatCompletion } from "../utils/request.js";

const messages = ref([
  {
    sender: "bot",
    text: "您好！👋 我是**习思想智能助手**\n\n我可以帮您：\n• 📖 解读全国统一大市场政策\n• 💡 解答理论学习问题\n• 🎯 分析重点难点\n\n请随时向我提问！",
  },
]);

const quickQuestions = [
  "什么是全国统一大市场？",
  "建设统一大市场的意义？",
  "如何推进市场制度规则统一？",
  "统一大市场的主要特征？",
];

const inputText = ref("");
const loading = ref(false);
const scrollIntoView = ref("");

const sendMessage = async () => {
  if (!inputText.value.trim() || loading.value) return;

  const text = inputText.value.trim();
  messages.value.push({ sender: "user", text });
  inputText.value = "";
  loading.value = true;

  await nextTick();
  scrollToBottom();

  try {
    const payload = messages.value.map((m) => ({
      role: m.sender === "bot" ? "assistant" : "user",
      content: m.text,
    }));

    const res = await chatCompletion(payload);
    messages.value.push({
      sender: "bot",
      text: res.reply || "抱歉，我暂时无法回答这个问题。",
    });
  } catch (error) {
    console.error("Chat error:", error);
    messages.value.push({
      sender: "bot",
      text: "❌ **服务暂时不可用**\n\n请检查：\n• 网络连接是否正常\n• 后端服务是否启动\n\n请稍后再试。",
    });
  } finally {
    loading.value = false;
    await nextTick();
    scrollToBottom();
  }
};

const askQuestion = (question) => {
  inputText.value = question;
  sendMessage();
};

const scrollToBottom = () => {
  scrollIntoView.value = "msg-" + (messages.value.length - 1);
};

// 改进的 Markdown 渲染（小程序版）
const formatMarkdown = (text) => {
  if (!text) return "";

  // 转义 HTML 特殊字符（除了我们要保留的标签）
  let html = text
    // 先处理代码块（保护其中的特殊字符）
    .replace(/```(\w+)?\n([\s\S]+?)```/g, (match, lang, code) => {
      const escapedCode = code.replace(/</g, "&lt;").replace(/>/g, "&gt;");
      return `<div style="background: #f5f5f5; padding: 10px; border-radius: 8px; margin: 10px 0; font-family: monospace; font-size: 24rpx; overflow-x: auto;">${escapedCode}</div>`;
    })
    // 行内代码
    .replace(
      /`([^`]+)`/g,
      '<code style="background: #f5f5f5; padding: 2px 6px; border-radius: 4px; font-family: monospace; color: #e83e8c;">$1</code>'
    )
    // 标题（h3, h2, h1）
    .replace(
      /^### (.+)$/gm,
      '<div style="font-size: 32rpx; font-weight: bold; color: #ff4d4d; margin: 15px 0;">$1</div>'
    )
    .replace(
      /^## (.+)$/gm,
      '<div style="font-size: 36rpx; font-weight: bold; color: #ff4d4d; margin: 18px 0;">$1</div>'
    )
    .replace(
      /^# (.+)$/gm,
      '<div style="font-size: 40rpx; font-weight: bold; color: #ff4d4d; margin: 20px 0;">$1</div>'
    )
    // 加粗（支持中英文）
    .replace(
      /\*\*(.+?)\*\*/g,
      '<span style="color: #ff4d4d; font-weight: bold;">$1</span>'
    )
    // 斜体
    .replace(/\*(.+?)\*/g, '<i style="font-style: italic;">$1</i>')
    // 有序列表（数字开头）
    .replace(
      /^\d+\.\s+(.+)$/gm,
      '<div style="padding-left: 20px; margin: 8px 0; line-height: 1.6;">• $1</div>'
    )
    // 无序列表（•、-、* 开头）
    .replace(
      /^[•\-\*]\s+(.+)$/gm,
      '<div style="padding-left: 20px; margin: 8px 0; line-height: 1.6;">• $1</div>'
    )
    // 引用块
    .replace(
      /^>\s+(.+)$/gm,
      '<div style="border-left: 4px solid #ff4d4d; padding-left: 15px; margin: 10px 0; color: #666; font-style: italic;">$1</div>'
    )
    // 链接（显示为文本）
    .replace(
      /\[([^\]]+)\]\(([^)]+)\)/g,
      '<span style="color: #ff4d4d; text-decoration: underline;">$1</span>'
    )
    // 分割线
    .replace(
      /^---$/gm,
      '<div style="border-bottom: 2px solid #eee; margin: 15px 0;"></div>'
    )
    // 段落（双换行）
    .replace(/\n\n/g, '</div><div style="margin: 12px 0;">')
    // 单换行
    .replace(/\n/g, "<br/>");

  // 包装在一个容器中
  return `<div style="line-height: 1.8; word-wrap: break-word;">${html}</div>`;
};
</script>

<style scoped>
.chat-page {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #f5f5f5;
}

.quick-questions {
  padding: 20rpx;
  background-color: white;
  border-bottom: 1rpx solid #eee;
}

.quick-question-chip {
  display: inline-block;
  padding: 15rpx 25rpx;
  margin: 10rpx;
  background: linear-gradient(135deg, #fff5f5, #ffe8e8);
  border: 2rpx solid #ffcccc;
  border-radius: 30rpx;
  color: #ff4d4d;
  font-size: 26rpx;
  transition: all 0.3s;
}

.quick-question-chip:active {
  background: linear-gradient(135deg, #ff4d4d, #cc0000);
  color: white;
  transform: scale(0.95);
}

.chat-window {
  flex: 1;
  padding: 20rpx;
}

.message-wrapper {
  margin-bottom: 30rpx;
}

.message {
  display: flex;
  align-items: flex-start;
  gap: 15rpx;
}

.bot-avatar,
.user-avatar {
  width: 60rpx;
  height: 60rpx;
  line-height: 60rpx;
  text-align: center;
  font-size: 35rpx;
  flex-shrink: 0;
}

.message-content {
  max-width: 70%;
  padding: 25rpx;
  border-radius: 20rpx;
  word-wrap: break-word;
  line-height: 1.6;
  font-size: 28rpx;
}

.message.user {
  justify-content: flex-end;
}

.message.user .message-content {
  background: linear-gradient(135deg, #ff7061, #f44336);
  color: white;
}

.message.bot .message-content {
  background-color: white;
  color: #333;
  box-shadow: 0 4rpx 15rpx rgba(0, 0, 0, 0.05);
}

.loading-wrapper {
  display: flex;
  justify-content: flex-start;
  padding: 0 20rpx;
}

.loading-dots {
  display: flex;
  align-items: center;
  gap: 10rpx;
  padding: 25rpx;
  background-color: white;
  border-radius: 20rpx;
  box-shadow: 0 4rpx 15rpx rgba(0, 0, 0, 0.05);
}

.dot {
  width: 15rpx;
  height: 15rpx;
  background: linear-gradient(135deg, #ff4d4d, #cc0000);
  border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out both;
}

.dot:nth-child(1) {
  animation-delay: -0.32s;
}

.dot:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes bounce {
  0%,
  80%,
  100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1);
  }
}

.input-box {
  display: flex;
  padding: 20rpx;
  background-color: white;
  border-top: 1rpx solid #eee;
  gap: 20rpx;
  box-shadow: 0 -2rpx 10rpx rgba(0, 0, 0, 0.05);
}

.input-box input {
  flex: 1;
  padding: 20rpx 25rpx;
  border: 2rpx solid #ddd;
  border-radius: 30rpx;
  font-size: 28rpx;
  background-color: #f9f9f9;
}

.input-placeholder {
  color: #999;
}

.send-btn {
  width: 100rpx;
  height: 80rpx;
  padding: 0;
  background: linear-gradient(135deg, #ff4d4d, #cc0000);
  color: white;
  border: none;
  border-radius: 30rpx;
  font-size: 35rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.send-btn.disabled {
  background: #ccc;
  opacity: 0.6;
}

.send-btn::after {
  border: none;
}
</style>
