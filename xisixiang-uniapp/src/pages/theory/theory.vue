<template>
  <view class="theory-page">
    <!-- 自定义 TabBar -->
    <custom-tab-bar />

    <!-- 顶部标题 -->
    <view class="page-header">
      <text class="header-title">◆ 理论学习中心</text>
      <text class="header-subtitle">深入学习全国统一大市场理论</text>
    </view>

    <!-- 文档列表 -->
    <view class="document-list">
      <view
        v-for="(doc, index) in documents"
        :key="index"
        class="document-card"
        @click="openDocument(doc)"
      >
        <view class="card-icon">◆</view>
        <view class="card-content">
          <text class="card-title">{{ doc.title }}</text>
          <text class="card-description">{{ doc.description }}</text>
        </view>
        <view class="card-arrow">▶</view>
      </view>
    </view>

    <!-- 悬浮按钮 - 知识图谱入口 -->
    <view class="floating-button" @click="goToKnowledgeGraph">
      <image class="button-icon" src="/static/goto.png" mode="aspectFit"></image>
    </view>
  </view>
</template>

<script setup>
import { onShow } from "@dcloudio/uni-app";

// 页面显示时更新 TabBar 状态
onShow(() => {
  uni.$emit("updateTabBar");
});

const documents = [
  {
    title: "中共中央国务院关于加快建设全国统一大市场的意见",
    description: "官方政策文件，全面阐述统一大市场建设的总体要求",
    fileName: "中共中央国务院关于加快建设全国统一大市场的意见.md",
  },
  {
    title: "纵深推进全国统一大市场建设",
    description: "深入分析市场建设的路径和方法",
    fileName: "纵深推进全国统一大市场建设.md",
  },
  {
    title: "怎么理解纵深推进全国统一大市场建设",
    description: "解读纵深推进的内涵和要求",
    fileName: "怎么理解纵深推进全国统一大市场建设.md",
  },
  {
    title: "构建全国统一大市场",
    description: "全面论述统一大市场的构建过程",
    fileName: "构建全国统一大市场.md",
  },
  {
    title: "深化构建全国统一大市场的逻辑认识与思考",
    description: "从理论角度深度剖析逻辑体系",
    fileName: "深化构建全国统一大市场的逻辑认识与思考.md",
  },
  {
    title: "全国统一大市场的那些事",
    description: "通俗易懂解读统一大市场相关内容",
    fileName: "全国统一大市场的那些事.md",
  },
];

const openDocument = (doc) => {
  // 跳转到文档详情页（需要创建）
  uni.navigateTo({
    url: `/pages/theory/document?title=${encodeURIComponent(
      doc.title
    )}&file=${encodeURIComponent(doc.fileName)}`,
  });
};

const goToKnowledgeGraph = () => {
  uni.navigateTo({
    url: "/pages/knowledge-graph/knowledge-graph",
  });
};
</script>

<style scoped>
.theory-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #fff5f5, #f5f5f5);
  padding: 20rpx;
  padding-bottom: 140rpx; /* 为自定义 TabBar 预留更多空间 */
}

.page-header {
  text-align: center;
  padding: 40rpx 20rpx;
  margin-bottom: 30rpx;
}

.header-title {
  display: block;
  font-size: 40rpx;
  font-weight: bold;
  color: #ff4d4d;
  margin-bottom: 15rpx;
}

.header-subtitle {
  display: block;
  font-size: 26rpx;
  color: #999;
}

.document-list {
  margin-bottom: 30rpx;
}

.document-card {
  display: flex;
  align-items: center;
  background-color: white;
  border-radius: 20rpx;
  padding: 30rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 4rpx 20rpx rgba(255, 77, 77, 0.08);
  transition: all 0.3s;
}

.document-card:active {
  transform: scale(0.98);
  box-shadow: 0 2rpx 10rpx rgba(255, 77, 77, 0.15);
}

.card-icon {
  font-size: 50rpx;
  margin-right: 25rpx;
  color: #ff4d4d;
}

.card-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.card-title {
  font-size: 30rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 10rpx;
  line-height: 1.4;
}

.card-description {
  font-size: 24rpx;
  color: #999;
  line-height: 1.5;
}

.card-arrow {
  font-size: 35rpx;
  color: #ff4d4d;
  margin-left: 20rpx;
}

/* 悬浮按钮样式 */
.floating-button {
  position: fixed;
  right: 40rpx;
  bottom: 180rpx;
  width: 110rpx;
  height: 110rpx;
  background: linear-gradient(135deg, #ff4d4d, #cc0000);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 10rpx 30rpx rgba(255, 77, 77, 0.4);
  z-index: 999;
  transition: all 0.3s cubic-bezier(0.25, 0.1, 0.25, 1);
  border: 4rpx solid rgba(255, 255, 255, 0.3);
}

.floating-button:active {
  transform: scale(0.92);
  box-shadow: 0 4rpx 15rpx rgba(255, 77, 77, 0.6);
}

.button-icon {
  width: 50rpx;
  height: 50rpx;
  filter: drop-shadow(0 2rpx 4rpx rgba(0, 0, 0, 0.2));
}

/* 脉冲动画效果 */
.floating-button::before {
  content: '';
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: inherit;
  opacity: 0.3;
  z-index: -1;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 0.3;
  }
  50% {
    transform: scale(1.2);
    opacity: 0.1;
  }
  100% {
    transform: scale(1);
    opacity: 0.3;
  }
}
</style>