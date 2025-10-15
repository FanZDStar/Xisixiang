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
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #fff;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.message {
  max-width: 80%;
  padding: 10px 14px;
  border-radius: 18px;
  word-wrap: break-word;
}

.message.user {
  align-self: flex-end;
  background-color: #dcf8c6;
}

.message.bot {
  align-self: flex-start;
  background-color: #e5e5ea;
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
