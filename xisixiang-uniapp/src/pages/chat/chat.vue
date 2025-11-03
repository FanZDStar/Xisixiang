<template>
  <view class="chat-page">
    <!-- 自定义 TabBar -->
    <custom-tab-bar />

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

    <!-- 聊天消息区域 -->
    <view class="messages-container">
      <view
        v-for="(msg, index) in messages"
        :key="index"
        :id="'msg-' + index"
        class="message-wrapper"
      >
        <view :class="['message', msg.sender]">
          <view v-if="msg.sender === 'bot'" class="bot-avatar">AI</view>
          <view class="message-content">
            <text v-if="msg.sender === 'user'">{{ msg.text }}</text>
            <mp-html v-else :content="msg.text" :selectable="true" />
          </view>
          <view v-if="msg.sender === 'user'" class="user-avatar">我</view>
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
    </view>

    <!-- 输入框 - 固定在底部 -->
    <view class="input-box">
      <input
        v-model="inputText"
        placeholder="例如：什么是全国统一大市场？"
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
        <text>{{ loading ? "发送中" : "发送" }}</text>
      </button>
    </view>
  </view>
</template>

<script setup>
import { ref, nextTick } from "vue";
import { onShow, onLoad, onShareAppMessage, onShareTimeline } from "@dcloudio/uni-app";
import { chatCompletion } from "../utils/request.js";
import { marked } from "marked";

// 配置 marked
marked.setOptions({
  breaks: true, // 支持换行符转换为 <br>
  gfm: true, // 启用 GitHub 风格的 Markdown
});

// 页面显示时更新 TabBar 状态
onShow(() => {
  uni.$emit("updateTabBar");
});

// 分享配置（可根据页面状态动态调整）
const shareTitle = "智能助手 | 理论问答";
const sharePath = "/pages/chat/chat?from=share";

onLoad(() => {
  // 打开右上角分享与朋友圈
  uni.showShareMenu({
    withShareTicket: true,
    menus: ["shareAppMessage", "shareTimeline"],
  });
});

onShareAppMessage(() => {
  return {
    title: shareTitle,
    path: sharePath,
  };
});

onShareTimeline(() => {
  return {
    title: shareTitle,
    query: "from=timeline",
  };
});

const messages = ref([
  {
    sender: "bot",
    text: marked(
      "您好！我是**习思想智能助手**\n\n我可以帮您：\n- 解读全国统一大市场政策\n- 解答理论学习问题\n- 分析重点难点\n\n请随时向我提问！"
    ),
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
      text: marked(res.reply || "抱歉，我暂时无法回答这个问题。"),
    });
  } catch (error) {
    console.error("Chat error:", error);
    messages.value.push({
      sender: "bot",
      text: marked(
        "服务暂时不可用\n\n请检查：\n- 网络连接是否正常\n- 后端服务是否启动\n\n请稍后再试。"
      ),
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
  // 移除滚动到底部的功能，因为现在使用原生滚动
  uni.pageScrollTo({
    scrollTop: 999999,
    duration: 300
  });
};
</script>

<style scoped>
.chat-page {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #f5f5f5;
  padding-bottom: 120rpx; /* 为自定义 TabBar 预留空间 */
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

.messages-container {
  flex: 1;
  padding: 20rpx;
  padding-bottom: 140rpx; /* 为输入框预留空间 */
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
  font-size: 24rpx;
  flex-shrink: 0;
  background-color: #ff4d4d;
  color: white;
  border-radius: 50%;
  font-weight: bold;
}

.user-avatar {
  background-color: #666;
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
  position: fixed;
  bottom: 120rpx; /* 在TabBar上方 */
  left: 0;
  right: 0;
  display: flex;
  padding: 20rpx;
  background-color: white;
  border-top: 1rpx solid #eee;
  gap: 20rpx;
  box-shadow: 0 -2rpx 10rpx rgba(0, 0, 0, 0.05);
  z-index: 100;
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
  width: 120rpx;
  height: 80rpx;
  padding: 0;
  background: linear-gradient(135deg, #ff4d4d, #cc0000);
  color: white;
  border: none;
  border-radius: 30rpx;
  font-size: 24rpx;
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
