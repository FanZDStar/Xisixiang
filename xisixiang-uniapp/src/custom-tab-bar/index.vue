<template>
  <view class="custom-tab-bar">
    <view
      v-for="(item, index) in tabList"
      :key="index"
      class="tab-item"
      :class="{ active: currentIndex === index }"
      @click="switchTab(index)"
    >
      <view class="tab-item-bg" :class="{ active: currentIndex === index }">
        <text class="tab-emoji">{{ item.emoji }}</text>
        <text class="tab-text">{{ item.text }}</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from "vue";

const currentIndex = ref(0);

const tabList = [
  {
    pagePath: "/pages/chat/chat",
    emoji: "💬",
    text: "智能问答",
  },
  {
    pagePath: "/pages/quiz/quiz",
    emoji: "📝",
    text: "习题训练",
  },
  {
    pagePath: "/pages/theory/theory",
    emoji: "📚",
    text: "理论学习",
  },
];

// 更新当前选中的 tab (可以被外部调用)
const updateCurrentIndex = () => {
  const pages = getCurrentPages();
  if (pages.length === 0) return;

  const currentPage = pages[pages.length - 1];
  const route = "/" + currentPage.route;

  // 设置当前选中的 tab
  tabList.forEach((item, index) => {
    if (route === item.pagePath) {
      currentIndex.value = index;
    }
  });
};

onMounted(() => {
  updateCurrentIndex();

  // 监听自定义事件,用于页面切换时更新状态
  uni.$on("updateTabBar", updateCurrentIndex);
});

const switchTab = (index) => {
  if (currentIndex.value === index) return;

  // 先跳转页面
  uni.switchTab({
    url: tabList[index].pagePath,
    success: () => {
      // 跳转成功后触发更新事件
      uni.$emit("updateTabBar");
    },
  });
};
</script>

<style scoped>
.custom-tab-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 120rpx;
  background-color: #ffffff;
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding: 10rpx 20rpx;
  box-shadow: 0 -2rpx 10rpx rgba(0, 0, 0, 0.05);
  z-index: 9999;
}

.tab-item {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 5rpx;
}

.tab-item-bg {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 15rpx 25rpx;
  border-radius: 20rpx;
  background-color: #f5f5f5;
  transition: all 0.3s ease;
  min-width: 160rpx;
}

.tab-item-bg.active {
  background: linear-gradient(135deg, #ff4d4d, #cc0000);
  transform: scale(1.05);
  box-shadow: 0 4rpx 15rpx rgba(255, 77, 77, 0.3);
}

.tab-emoji {
  font-size: 44rpx;
  margin-bottom: 5rpx;
  display: block;
}

.tab-text {
  font-size: 26rpx;
  font-weight: 500;
  color: #666666;
  transition: color 0.3s ease;
}

.tab-item-bg.active .tab-text {
  color: #ffffff;
  font-weight: bold;
}
</style>
