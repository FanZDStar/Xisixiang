<!-- frontend/src/components/ChatWindow.vue -->
<script setup>
import { ref, defineProps, watch, nextTick } from "vue";
import MessageMarkdown from "./MessageMarkdown.vue";

const props = defineProps({
  messages: {
    type: Array,
    required: true,
  },
});

const chatContainer = ref(null);

// 当消息更新时滚动到底部
watch(
  () => props.messages,
  () => {
    nextTick(() => {
      if (chatContainer.value) {
        chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
      }
    });
  },
  { deep: true }
);
</script>

<template>
  <div ref="chatContainer" class="chat-window">
    <div
      v-for="(message, index) in messages"
      :key="index"
      :class="['message', message.sender]"
    >
      <div class="message-content">
        <!-- 用户消息使用纯文本 -->
        <div v-if="message.sender === 'user'" class="user-text">
          {{ message.text }}
        </div>
        <!-- AI 消息使用 Markdown 渲染 -->
        <MessageMarkdown v-else :content="message.text" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.chat-window {
  height: 400px;
  overflow-y: auto;
  padding: 16px;
  border: 1px solid rgba(244, 67, 54, 0.25);
  border-radius: 12px;
  background: linear-gradient(to bottom, #fff5f5, #ffffff);
  display: flex;
  flex-direction: column;
  gap: 12px;
  scroll-behavior: smooth;
}

/* 美化滚动条 */
.chat-window::-webkit-scrollbar {
  width: 8px;
}

.chat-window::-webkit-scrollbar-track {
  background: #ffebee;
  border-radius: 4px;
}

.chat-window::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, #ff7061, #f44336);
  border-radius: 4px;
}

.chat-window::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(135deg, #f44336, #cc0000);
}

.message {
  max-width: 80%;
  padding: 12px 16px;
  border-radius: 18px 18px 18px 4px;
  word-wrap: break-word;
  animation: messageSlideIn 0.3s ease-out;
}

@keyframes messageSlideIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message-content {
  line-height: 1.6;
  font-size: 0.95rem;
}

.user-text {
  white-space: pre-wrap;
  word-break: break-word;
}

.message.user {
  align-self: flex-end;
  background: linear-gradient(135deg, #ff7061, #f44336);
  color: #fff;
  border-radius: 18px 18px 4px 18px;
  box-shadow: 0 2px 8px rgba(244, 67, 54, 0.25);
}

.message.bot {
  align-self: flex-start;
  background-color: #ffffff;
  border: 1px solid rgba(244, 67, 54, 0.15);
  color: #333;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

/* 移动端适配 */
@media (max-width: 768px) {
  .chat-window {
    height: 300px;
    padding: 12px;
  }

  .message {
    max-width: 90%;
    padding: 10px 14px;
    font-size: 14px;
  }

  .message-content {
    font-size: 0.9rem;
  }
}
</style>
