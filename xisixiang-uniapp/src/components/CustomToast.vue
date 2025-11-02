<template>
  <view v-if="visible" class="custom-toast-wrapper">
    <view class="custom-toast" :class="[typeClass]">
      <view class="toast-icon">{{ iconText }}</view>
      <text class="toast-text">{{ message }}</text>
    </view>
  </view>
</template>

<script setup>
import { ref, computed } from "vue";

const visible = ref(false);
const message = ref("");
const type = ref("success"); // success, error, info, warning

const iconText = computed(() => {
  const iconMap = {
    success: "✅",
    error: "❌",
    info: "ℹ️",
    warning: "⚠️",
  };
  return iconMap[type.value] || "✅";
});

const typeClass = computed(() => {
  return `toast-${type.value}`;
});

// 显示 Toast
function show(msg, toastType = "success", duration = 2000) {
  message.value = msg;
  type.value = toastType;
  visible.value = true;

  setTimeout(() => {
    visible.value = false;
  }, duration);
}

// 暴露方法给父组件调用
defineExpose({
  show,
});
</script>

<style scoped>
.custom-toast-wrapper {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 9999;
  display: flex;
  justify-content: center;
  align-items: center;
  pointer-events: none;
}

.custom-toast {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-width: 200rpx;
  max-width: 500rpx;
  padding: 40rpx 50rpx;
  background: rgba(0, 0, 0, 0.85);
  border-radius: 20rpx;
  box-shadow: 0 8rpx 30rpx rgba(0, 0, 0, 0.3);
  animation: toastFadeIn 0.3s ease-out;
}

@keyframes toastFadeIn {
  from {
    opacity: 0;
    transform: scale(0.8);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.toast-icon {
  font-size: 60rpx;
  margin-bottom: 15rpx;
}

.toast-text {
  font-size: 28rpx;
  color: white;
  text-align: center;
  line-height: 1.5;
  word-wrap: break-word;
}

.toast-error {
  background: rgba(255, 77, 77, 0.9);
}

.toast-info {
  background: rgba(74, 144, 226, 0.9);
}

.toast-warning {
  background: rgba(255, 193, 7, 0.9);
}
</style>
