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
          <!-- 去除emoji，仅保留文字 -->
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
    text: "智能问答",
  },
  {
    pagePath: "/pages/quiz/quiz",
    text: "习题训练",
  },
  {
    pagePath: "/pages/theory/theory",
    text: "理论学习",
  },
  {
    pagePath: "/pages/game/game",
    text: "实践闯关",
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
  width: 100%;
  height: 100rpx;
  background-color: #ffffff;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8rpx 16rpx;
  box-shadow: 0 -2rpx 10rpx rgba(0, 0, 0, 0.05);
  z-index: 9999;
  box-sizing: border-box;
}

.tab-item {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0 4rpx;
  max-width: 25%;
}

.tab-item-bg {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 8rpx 6rpx;
  border-radius: 16rpx;
  transition: all 0.2s ease;
  width: 100%;
  max-width: 140rpx;
  min-width: 80rpx;
}

.tab-item-bg.active {
  background: linear-gradient(90deg, #ff4d4d 0%, #fff5f5 100%);
  box-shadow: 0 2rpx 8rpx rgba(255,77,77,0.15);
}

.tab-text {
  font-size: 22rpx;
  font-weight: 500;
  color: #666666;
  transition: color 0.2s ease;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
}

.tab-item-bg.active .tab-text {
  color: #d32f2f;
  font-weight: 600;
}
</style>
