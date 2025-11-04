<template>
  <view class="video-page">
    <!-- 顶部标题区 -->
    <view class="header">
      <text class="title">AI视频作品</text>
      <text class="subtitle">人工智能生成视频展示</text>
    </view>

    <!-- 待开发提示 -->
    <view class="coming-soon">
      <view class="icon-wrapper">
        <text class="icon">🎬</text>
      </view>
      <text class="coming-text">功能开发中</text>
      <text class="desc-text">AI视频生成功能即将上线</text>
      <text class="desc-text">敬请期待...</text>
    </view>
  </view>
</template>

<script setup>
// 待开发页面，暂无逻辑
</script>

<style scoped>
.video-page { min-height:100vh; background: linear-gradient(135deg,#ff4d4d 0%,#cc0000 100%); padding-bottom:40rpx; display:flex; flex-direction:column }
.header{ padding:40rpx 30rpx 20rpx; text-align:center }
.title{ display:block; font-size:48rpx; font-weight:bold; color:white; margin-bottom:15rpx }
.subtitle{ display:block; font-size:26rpx; color:rgba(255,255,255,0.9) }
.coming-soon{ flex:1; display:flex; flex-direction:column; justify-content:center; align-items:center; padding:100rpx 60rpx }
.icon-wrapper{ width:200rpx; height:200rpx; background:rgba(255,255,255,0.2); border-radius:50%; display:flex; align-items:center; justify-content:center; margin-bottom:40rpx }
.icon{ font-size:100rpx }
.coming-text{ font-size:40rpx; font-weight:bold; color:white; margin-bottom:20rpx }
.desc-text{ font-size:28rpx; color:rgba(255,255,255,0.8); margin-bottom:10rpx; text-align:center }
</style>
