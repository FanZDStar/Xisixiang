<!-- frontend/src/views/ChatView.vue -->
<script setup>
import { ref } from "vue";
import apiClient from "../api/client.js";
import ChatWindow from "../components/ChatWindows.vue";
import MessageInput from "../components/MessageInput.vue";

const messages = ref([
  {
    sender: "bot",
    text: "您好！我是智能问答助手，可为您解读“构建全国统一大市场”的政策与背景，有任何问题欢迎提问。",
  },
]);

const loading = ref(false);
const error = ref(null);

const buildPayload = () => {
  return messages.value
    .filter((message) => message.sender === "user" || message.sender === "bot")
    .map((message) => ({
      role: message.sender === "bot" ? "assistant" : "user",
      content: message.text,
    }));
};

const sendMessage = async (text) => {
  if (!text || loading.value) return;

  error.value = null;
  messages.value.push({ sender: "user", text });
  loading.value = true;

  try {
    const response = await apiClient.post("/api/chat", {
      messages: buildPayload(),
    });
    const reply = response.reply?.trim();

    messages.value.push({
      sender: "bot",
      text:
        reply && reply.length > 0 ? reply : "抱歉，我暂时无法回答这个问题。",
    });
  } catch (err) {
    error.value = err.message || "请求失败，请稍后重试";
    messages.value.push({
      sender: "bot",
      text: "抱歉，服务出现了一些问题，请稍后再试。",
    });
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="view-container">
    <div class="chat-header">
      <h1>智能问答系统</h1>
      <p class="description">
        围绕“构建全国统一大市场”答疑解惑，输入问题即可获取权威解答。
      </p>
    </div>

    <div class="chat-card">
      <ChatWindow :messages="messages" />

      <div v-if="error" class="error-banner">
        {{ error }}
      </div>

      <div v-if="loading" class="loading-banner">正在思考，请稍候…</div>

      <MessageInput
        placeholder="请描述你想了解的政策、背景或具体问题…"
        :disabled="loading"
        @send="sendMessage"
      />
    </div>
  </div>
</template>

<style scoped>
.view-container {
  padding: 20px;
  max-width: 900px;
  margin: 0 auto;
}

.chat-header {
  text-align: center;
  margin-bottom: 20px;
  color: #f44336;
}

.chat-header h1 {
  margin-bottom: 8px;
  font-size: 1.8rem;
}

.description {
  margin: 0;
  color: #555;
  font-size: 1rem;
}

.chat-card {
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 6px 18px rgba(244, 67, 54, 0.08);
  border: 1px solid rgba(244, 67, 54, 0.2);
  display: flex;
  flex-direction: column;
  min-height: 520px;
}

.error-banner,
.loading-banner {
  padding: 10px 16px;
  font-size: 0.95rem;
  margin: 0 16px 12px;
  border-radius: 8px;
}

.error-banner {
  background-color: #ffebee;
  color: #c62828;
  border: 1px solid #ef5350;
}

.loading-banner {
  background-color: #fff3e0;
  color: #ef6c00;
  border: 1px solid #ffb74d;
}

@media (max-width: 768px) {
  .view-container {
    padding: 15px;
  }

  .chat-card {
    min-height: 460px;
  }

  .chat-header h1 {
    font-size: 1.5rem;
  }
}
</style>
