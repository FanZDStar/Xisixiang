<!-- frontend/src/views/ChatView.vue -->
<script setup>
import { ref } from "vue";
import apiClient from "../api/client.js";
import ChatWindow from "../components/ChatWindows.vue";
import MessageInput from "../components/MessageInput.vue";

const messages = ref([
  {
    sender: "bot",
    text: "👋 **您好！我是全国统一大市场政策智能助手。**\n\n我可以帮您解答关于构建全国统一大市场的各类问题，包括：\n\n• **政策背景与意义** - 为什么要建设统一大市场\n• **实施路径与措施** - 如何推进市场建设\n• **相关理论与实践** - 理论基础和实践案例\n\n💡 **提示**：您可以点击下方的快捷问题快速开始，或直接输入您的问题。",
  },
]);

const loading = ref(false);
const error = ref(null);

// 快捷问题建议
const quickQuestions = ref([
  "什么是全国统一大市场？",
  "为什么要构建全国统一大市场？",
  "统一大市场建设的主要内容是什么？",
  "如何纵深推进统一大市场建设？",
]);

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
        reply && reply.length > 0
          ? reply
          : "抱歉，我暂时无法理解您的问题。\n\n**建议**：\n• 尝试换个方式提问\n• 点击上方的快捷问题\n• 提供更多具体信息",
    });
  } catch (err) {
    error.value = err.message || "网络连接失败，请检查后端服务是否正常运行";
    messages.value.push({
      sender: "bot",
      text: "⚠️ **服务暂时不可用**\n\n可能的原因：\n• 后端服务未启动\n• API 密钥配置错误\n• 网络连接问题\n\n请稍后再试或联系管理员。",
    });
  } finally {
    loading.value = false;
  }
};

// 处理快捷问题点击
const handleQuickQuestion = (question) => {
  sendMessage(question);
};
</script>

<template>
  <div class="view-container">
    <div class="chat-header">
      <h1>智能问答中心</h1>
      <p class="description">
        专业解读"构建全国统一大市场"政策，为您提供权威、详实的答疑服务
      </p>
    </div>

    <div class="chat-card">
      <!-- 快捷问题区域 -->
      <div v-if="messages.length === 1" class="quick-questions">
        <div class="quick-title">💡 您可能想问：</div>
        <div class="question-chips">
          <button
            v-for="(question, index) in quickQuestions"
            :key="index"
            @click="handleQuickQuestion(question)"
            :disabled="loading"
            class="chip-button"
          >
            {{ question }}
          </button>
        </div>
      </div>

      <ChatWindow :messages="messages" />

      <div v-if="error" class="error-banner">⚠️ {{ error }}</div>

      <div v-if="loading" class="loading-banner">
        <span class="loading-dots">
          <span class="dot"></span>
          <span class="dot"></span>
          <span class="dot"></span>
        </span>
        AI 正在思考中，请稍候...
      </div>

      <MessageInput
        placeholder="💭 请输入您想了解的问题，例如：统一大市场的建设意义是什么？"
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
  margin-bottom: 24px;
  color: #f44336;
}



@keyframes float {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

.chat-header h1 {
  margin-bottom: 8px;
  font-size: 2rem;
  font-weight: 700;
  background: linear-gradient(135deg, #ff4d4d, #cc0000);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.description {
  margin: 0;
  color: #666;
  font-size: 1rem;
  line-height: 1.6;
}

.chat-card {
  background-color: #ffffff;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(244, 67, 54, 0.12);
  border: 1px solid rgba(244, 67, 54, 0.15);
  display: flex;
  flex-direction: column;
  min-height: 580px;
  overflow: hidden;
}

/* 快捷问题样式 */
.quick-questions {
  padding: 16px;
  background: linear-gradient(135deg, #fff5f5, #ffebee);
  border-bottom: 1px solid rgba(244, 67, 54, 0.15);
}

.quick-title {
  font-size: 0.9rem;
  color: #d32f2f;
  font-weight: 600;
  margin-bottom: 12px;
}

.question-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.chip-button {
  padding: 8px 16px;
  border: 1px solid rgba(244, 67, 54, 0.3);
  border-radius: 20px;
  background-color: #ffffff;
  color: #f44336;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.chip-button:hover:not(:disabled) {
  background: linear-gradient(135deg, #ff4d4d, #f44336);
  color: #ffffff;
  border-color: #f44336;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(244, 67, 54, 0.3);
}

.chip-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.error-banner,
.loading-banner {
  padding: 12px 16px;
  font-size: 0.95rem;
  margin: 0 16px 12px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.error-banner {
  background-color: #ffebee;
  color: #c62828;
  border: 1px solid #ef5350;
}

.loading-banner {
  background: linear-gradient(135deg, #fff3e0, #ffe0b2);
  color: #e65100;
  border: 1px solid #ffb74d;
}

/* 加载动画 */
.loading-dots {
  display: inline-flex;
  gap: 4px;
  margin-right: 8px;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #ff6f00;
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

/* 移动端适配 */
@media (max-width: 768px) {
  .view-container {
    padding: 15px;
  }


  .chat-header h1 {
    font-size: 1.6rem;
  }

  .description {
    font-size: 0.9rem;
  }

  .chat-card {
    min-height: 500px;
    border-radius: 12px;
  }

  .quick-questions {
    padding: 12px;
  }

  .quick-title {
    font-size: 0.85rem;
  }

  .chip-button {
    padding: 6px 12px;
    font-size: 0.8rem;
  }
}

@media (max-width: 480px) {
  .chat-header h1 {
    font-size: 1.4rem;
  }

  .description {
    font-size: 0.85rem;
  }

  .question-chips {
    flex-direction: column;
  }

  .chip-button {
    width: 100%;
    text-align: center;
  }
}
</style>
