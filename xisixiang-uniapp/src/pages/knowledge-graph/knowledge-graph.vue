<template>
  <view class="knowledge-graph-page">
    <view class="placeholder-container">
      <text class="placeholder-icon">🗺️</text>
      <text class="placeholder-title">知识图谱</text>
      <text class="placeholder-text">知识图谱功能开发中...</text>
      <text class="placeholder-hint"
        >将展示全国统一大市场理论的知识关系网络</text
      >

      <view class="features-list">
        <view class="feature-item">
          <text class="feature-icon">🔗</text>
          <text class="feature-text">概念关系可视化</text>
        </view>
        <view class="feature-item">
          <text class="feature-icon">🎯</text>
          <text class="feature-text">核心知识点标注</text>
        </view>
        <view class="feature-item">
          <text class="feature-icon">🔍</text>
          <text class="feature-text">交互式知识探索</text>
        </view>
      </view>

      <button @click="goBack" class="back-btn">返回理论学习</button>
    </view>
  </view>
</template>

<script setup>
const goBack = () => {
  uni.navigateBack();
};
</script>

<style scoped>
.knowledge-graph-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #fff5f5, #f5f5f5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.placeholder-container {
  text-align: center;
  padding: 60rpx 40rpx;
}

.placeholder-icon {
  font-size: 120rpx;
  display: block;
  margin-bottom: 30rpx;
}

.placeholder-title {
  display: block;
  font-size: 40rpx;
  font-weight: bold;
  color: #ff4d4d;
  margin-bottom: 20rpx;
}

.placeholder-text {
  display: block;
  font-size: 28rpx;
  color: #666;
  margin-bottom: 15rpx;
}

.placeholder-hint {
  display: block;
  font-size: 24rpx;
  color: #999;
  margin-bottom: 50rpx;
}

.features-list {
  margin: 40rpx 0;
}

.feature-item {
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 20rpx 0;
  padding: 20rpx;
  background-color: white;
  border-radius: 15rpx;
  box-shadow: 0 4rpx 15rpx rgba(0, 0, 0, 0.05);
}

.feature-icon {
  font-size: 35rpx;
  margin-right: 15rpx;
}

.feature-text {
  font-size: 28rpx;
  color: #333;
}

.back-btn {
  background: linear-gradient(135deg, #ff4d4d, #cc0000);
  color: white;
  border: none;
  padding: 25rpx 80rpx;
  border-radius: 40rpx;
  font-size: 30rpx;
  margin-top: 40rpx;
}
</style>
