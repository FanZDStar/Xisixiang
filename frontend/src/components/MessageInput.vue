<!-- frontend/src/components/MessageInput.vue -->
<script setup>
import { ref, defineProps, defineEmits } from "vue";

const props = defineProps({
  placeholder: {
    type: String,
    default: "请输入消息...",
  },
  disabled: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["send"]);

const inputText = ref("");

function handleSend() {
  if (inputText.value.trim() !== "") {
    emit("send", inputText.value.trim());
    inputText.value = "";
  }
}

function handleKeydown(event) {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    handleSend();
  }
}
</script>

<template>
  <div class="message-input">
    <textarea
      v-model="inputText"
      :placeholder="placeholder"
      :disabled="disabled"
      @keydown="handleKeydown"
      class="input-field"
    />
    <button
      @click="handleSend"
      :disabled="disabled || inputText.trim() === ''"
      class="send-button"
    >
      发送
    </button>
  </div>
</template>

<style scoped>
.message-input {
  display: flex;
  gap: 10px;
  padding: 12px;
  border-top: 1px solid rgba(244, 67, 54, 0.2);
  background-color: #fff5f5;
  align-items: flex-end;
}

.input-field {
  flex: 1;
  resize: none;
  min-height: 40px;
  max-height: 120px;
  padding: 10px 14px;
  border: 1px solid rgba(244, 67, 54, 0.2);
  border-radius: 20px;
  font-family: inherit;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
}

.input-field:focus {
  border-color: #f44336;
}

.send-button {
  height: 40px;
  padding: 0 20px;
  border: none;
  border-radius: 20px;
  background: linear-gradient(135deg, #ff7061, #f44336);
  color: #ffffff;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.send-button:hover:not(:disabled) {
  filter: brightness(0.95);
}

.send-button:disabled {
  background: #ffcdd2;
  cursor: not-allowed;
}

/* 移动端适配 */
@media (max-width: 768px) {
  .message-input {
    padding: 10px;
  }

  .input-field {
    min-height: 36px;
    padding: 8px 12px;
    font-size: 14px;
  }

  .send-button {
    height: 36px;
    padding: 0 16px;
    font-size: 14px;
  }
}
</style>
