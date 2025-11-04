<template>
  <view class="works-page">
    <!-- 自定义 TabBar -->
    <custom-tab-bar />

    <!-- 顶部标题区 -->
    <view class="header">
      <text class="title">原创作品</text>
      <text class="subtitle">全国统一大市场主题原创内容</text>
    </view>

    <!-- 三个模块入口 -->
    <view class="modules-container">
      <view 
        v-for="(module, index) in modules" 
        :key="index"
        class="module-card"
        @click="navigateTo(module.path)"
      >
        <view class="module-icon-wrapper">
          <image 
            :src="module.iconImage" 
            class="module-icon-image"
            mode="aspectFit"
          />
        </view>
        <view class="module-info">
          <text class="module-name">{{ module.name }}</text>
          <text class="module-desc">{{ module.desc }}</text>
        </view>
        <view class="module-arrow">
          <text class="arrow-icon">›</text>
        </view>
      </view>
    </view>

    <!-- 底部致谢 -->
    <view class="footer-thanks">
      <view class="thanks-title">特别致谢</view>
      <view class="thanks-content">
        <text class="thanks-text">感谢所有团队成员的辛勤付出与创作：</text>
        <view class="team-members">
          <text class="member-name">张三</text>
          <text class="separator">•</text>
          <text class="member-name">李四</text>
          <text class="separator">•</text>
          <text class="member-name">王五</text>
          <text class="separator">•</text>
          <text class="member-name">赵六</text>
        </view>
        <text class="thanks-footer">携手共创，致敬每一份努力</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { onShow } from "@dcloudio/uni-app";

// 页面显示时更新 TabBar
onShow(() => {
  uni.$emit("updateTabBar");
});

// 三个模块配置
const modules = [
  {
    name: "原创歌曲",
    desc: "《破壁前行》——统一大市场主题歌曲",
    iconImage: "/static/icon-song.png",
    path: "/pages/original-works-sub/song"
  },
  {
    name: "AI视频",
    desc: "人工智能生成视频作品",
    iconImage: "/static/icon-video.png",
    path: "/pages/original-works-sub/video"
  },
  {
    name: "传统相声",
    desc: "传统艺术与时代主题结合",
    iconImage: "/static/icon-xiangsheng.png",
    path: "/pages/original-works-sub/xiangsheng"
  }
];

// 导航到子页面
const navigateTo = (path) => {
  uni.navigateTo({
    url: path
  });
};
</script>

<style scoped>
.works-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #ff4d4d 0%, #cc0000 100%);
  padding-bottom: 120rpx;
}

/* 顶部标题 */
.header {
  padding: 40rpx 30rpx 30rpx;
  text-align: center;
}

.title {
  display: block;
  font-size: 48rpx;
  font-weight: bold;
  color: white;
  margin-bottom: 15rpx;
  text-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.2);
}

.subtitle {
  display: block;
  font-size: 26rpx;
  color: rgba(255, 255, 255, 0.9);
}

/* 模块容器 */
.modules-container {
  padding: 20rpx 30rpx;
}

.module-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20rpx;
  padding: 30rpx;
  margin-bottom: 20rpx;
  display: flex;
  align-items: center;
  box-shadow: 0 8rpx 20rpx rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.module-card:active {
  transform: scale(0.98);
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.15);
}

.module-icon-wrapper {
  width: 100rpx;
  height: 100rpx;
  background: linear-gradient(135deg, #ff4d4d 0%, #cc0000 100%);
  border-radius: 20rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 25rpx;
  box-shadow: 0 4rpx 12rpx rgba(255, 77, 77, 0.3);
}

.module-icon-image {
  width: 60rpx;
  height: 60rpx;
}

.module-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.module-name {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 8rpx;
}

.module-desc {
  font-size: 24rpx;
  color: #666;
  line-height: 1.4;
}

.module-arrow {
  width: 40rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.arrow-icon {
  font-size: 48rpx;
  color: #ff4d4d;
  font-weight: bold;
}

/* 底部致谢 */
.footer-thanks {
  margin: 40rpx 30rpx 20rpx;
  padding: 30rpx;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  border-radius: 20rpx;
}

.thanks-title {
  font-size: 32rpx;
  font-weight: bold;
  color: white;
  text-align: center;
  margin-bottom: 20rpx;
  text-shadow: 0 2rpx 6rpx rgba(0, 0, 0, 0.2);
}

.thanks-content {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.thanks-text {
  font-size: 26rpx;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 15rpx;
  text-align: center;
}

.team-members {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  margin: 10rpx 0 15rpx;
}

.member-name {
  font-size: 28rpx;
  color: white;
  font-weight: 500;
  padding: 0 8rpx;
}

.separator {
  font-size: 24rpx;
  color: rgba(255, 255, 255, 0.6);
  padding: 0 4rpx;
}

.thanks-footer {
  font-size: 24rpx;
  color: rgba(255, 255, 255, 0.8);
  text-align: center;
  font-style: italic;
  margin-top: 10rpx;
}
</style>
