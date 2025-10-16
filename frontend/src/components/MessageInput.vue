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
  padding: 16px;
  border-top: 1px solid rgba(244, 67, 54, 0.2);
  background: linear-gradient(to top, #fff5f5, #ffffff);
  align-items: flex-end;
}

.input-field {
  flex: 1;
  resize: none;
  min-height: 44px;
  max-height: 120px;
  padding: 12px 16px;
  border: 2px solid rgba(244, 67, 54, 0.2);
  border-radius: 22px;
  font-family: inherit;
  font-size: 14px;
  outline: none;
  transition: all 0.3s ease;
  background-color: #ffffff;
}

.input-field:focus {
  border-color: #f44336;
  box-shadow: 0 0 0 3px rgba(244, 67, 54, 0.1);
}

.input-field::placeholder {
  color: #999;
}

.send-button {
  height: 44px;
  padding: 0 24px;
  border: none;
  border-radius: 22px;
  background: linear-gradient(135deg, #ff7061, #f44336);
  color: #ffffff;
  font-weight: 600;
  font-size: 15px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(244, 67, 54, 0.25);
}

.send-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(244, 67, 54, 0.35);
  background: linear-gradient(135deg, #f44336, #cc0000);
}

.send-button:active:not(:disabled) {
  transform: translateY(0);
  box-shadow: 0 2px 8px rgba(244, 67, 54, 0.25);
}

.send-button:disabled {
  background: linear-gradient(135deg, #ffcdd2, #ef9a9a);
  cursor: not-allowed;
  opacity: 0.6;
  transform: none;
  box-shadow: none;
}

/* 移动端适配 */
@media (max-width: 768px) {
  .message-input {
    padding: 12px;
  }

  .input-field {
    min-height: 40px;
    padding: 10px 14px;
    font-size: 14px;
  }

  .send-button {
    height: 40px;
    padding: 0 20px;
    font-size: 14px;
  }
}
</style>
