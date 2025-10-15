<!-- frontend/src/components/ChatWindow.vue -->
<script setup>
import { ref, defineProps, watch, nextTick } from "vue";

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
        {{ message.text }}
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
  background-color: #fff5f5;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.message {
  max-width: 80%;
  padding: 10px 14px;
  border-radius: 18px 18px 18px 4px;
  word-wrap: break-word;
}

.message-content {
  white-space: pre-wrap;
  line-height: 1.5;
}

.message.user {
  align-self: flex-end;
  background: linear-gradient(135deg, #ff7061, #f44336);
  color: #fff;
  border-radius: 18px 18px 4px 18px;
}

.message.bot {
  align-self: flex-start;
  background-color: #ffffff;
  border: 1px solid rgba(244, 67, 54, 0.15);
}

/* 移动端适配 */
@media (max-width: 768px) {
  .chat-window {
    height: 300px;
    padding: 12px;
  }

  .message {
    max-width: 90%;
    padding: 8px 12px;
    font-size: 14px;
  }
}
</style>
