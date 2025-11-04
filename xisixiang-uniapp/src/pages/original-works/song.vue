<template>
  <view class="music-page">
    <!-- 顶部标题区 -->
    <view class="header">
      <text class="title">《破壁前行》——统一大市场</text>
      <text class="subtitle">全国统一大市场主题原创歌曲</text>
    </view>

    <!-- 音乐封面 -->
    <view class="cover-container">
      <view 
        class="cover-wrapper" 
        :class="{ rotating: isMusicPlaying }"
        @click="togglePlay"
      >
        <image 
          class="cover-image" 
          src="/static/music.png" 
          mode="aspectFill"
        />
        <!-- 播放/暂停图标叠加层 -->
        <view class="play-overlay" v-if="!isMusicPlaying">
          <image 
            src="/static/启动.png" 
            class="play-icon"
            mode="aspectFit"
          />
        </view>
      </view>
    </view>

    <!-- 歌词显示区 -->
    <view class="lyrics-container">
      <view class="lyrics-wrapper">
        <!-- 上一句歌词 -->
        <view 
          v-if="currentLyricIndex > 0"
          class="lyric-line prev-lyric"
          :key="'prev-' + currentLyricIndex"
        >
          {{ lyrics[currentLyricIndex - 1].text }}
        </view>
        
        <!-- 当前歌词 -->
        <view 
          v-if="currentLyricIndex >= 0 && currentLyricIndex < lyrics.length"
          class="lyric-line current-lyric"
          :key="'current-' + currentLyricIndex"
        >
          {{ lyrics[currentLyricIndex].text }}
        </view>
        
        <!-- 下一句歌词 -->
        <view 
          v-if="currentLyricIndex >= 0 && currentLyricIndex < lyrics.length - 1"
          class="lyric-line next-lyric"
          :key="'next-' + currentLyricIndex"
        >
          {{ lyrics[currentLyricIndex + 1].text }}
        </view>
        
        <!-- 默认提示（音乐未开始时） -->
        <view v-if="currentLyricIndex < 0" class="lyric-line current-lyric">
          点击封面开始播放
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";

// 音频相关状态
const isMusicPlaying = ref(false);
const currentLyricIndex = ref(-1);
let innerAudio = null;
let lyricTimer = null;

// 歌词数据（时间格式：秒）- 改为普通常量数组
const lyrics = [
  { time: 14, text: "曾有无形的墙，阻隔山海相望" },
  { time: 21, text: "货车滞留关卡，雄心困于街巷" },
  { time: 27, text: "市场的血脉，被壁垒阻挡" },
  { time: 34, text: "创新的火种，在阴影中迷茫" },
  { time: 40, text: "听，号角已吹响，要破壁前行" },
  { time: 47, text: "用巨锤砸碎，那旧日的屏障" },
  { time: 53, text: "让规则统一，如江河汇入海洋" },
  { time: 59, text: "让要素流动，从西江到北疆" },
  { time: 78, text: "天平需归位，公平是灵魂微光" },
  { time: 85, text: "巨兽的垄断，不能遮蔽暖阳" },
  { time: 92, text: "清理那藩篱，无论以何名状" },
  { time: 98, text: "同一起跑线，奔向同一前方" },
  { time: 104, text: "看，巨龙正腾飞，要破壁前行" },
  { time: 111, text: "用制度创新，重塑游戏主场" },
  { time: 117, text: "让循环畅通，为发展注入力量" },
  { time: 124, text: "亿万的创造，汇成未来的万丈光芒" },
  { time: 131, text: "畅通未来中国" },
  { time: 137, text: "我们身在其中" },
];

// 初始化音频
const initAudio = () => {
  try {
    innerAudio = uni.createInnerAudioContext();
    innerAudio.src = "/static/music.mp3";
    innerAudio.loop = false;

    innerAudio.onPlay(() => {
      isMusicPlaying.value = true;
      startLyricSync();
    });

    innerAudio.onPause(() => {
      isMusicPlaying.value = false;
      stopLyricSync();
    });

    innerAudio.onStop(() => {
      isMusicPlaying.value = false;
      stopLyricSync();
    });

    innerAudio.onEnded(() => {
      isMusicPlaying.value = false;
      currentLyricIndex.value = -1;
      stopLyricSync();
    });

    innerAudio.onError((err) => {
      console.error("音频播放错误:", err);
      isMusicPlaying.value = false;
      uni.showToast({
        title: "音频加载失败",
        icon: "none"
      });
    });
  } catch (e) {
    console.error("初始化音频失败:", e);
  }
};

// 播放/暂停切换
const togglePlay = () => {
  if (!innerAudio) {
    initAudio();
    setTimeout(() => {
      innerAudio.play();
    }, 100);
    return;
  }

  if (isMusicPlaying.value) {
    innerAudio.pause();
  } else {
    innerAudio.play();
  }
};

// 开始歌词同步
const startLyricSync = () => {
  stopLyricSync();
  lyricTimer = setInterval(() => {
    if (innerAudio) {
      const time = innerAudio.currentTime;
      
      // 查找当前应该显示的歌词
      for (let i = lyrics.length - 1; i >= 0; i--) {
        if (time >= lyrics[i].time) {
          if (currentLyricIndex.value !== i) {
            currentLyricIndex.value = i;
          }
          break;
        }
      }
    }
  }, 100);
};

// 停止歌词同步
const stopLyricSync = () => {
  if (lyricTimer) {
    clearInterval(lyricTimer);
    lyricTimer = null;
  }
};

// 页面加载时初始化
onMounted(() => {
  initAudio();
});

// 页面卸载时清理
onUnmounted(() => {
  stopLyricSync();
  if (innerAudio) {
    try {
      innerAudio.stop();
      innerAudio.destroy();
    } catch (e) {
      console.warn("清理音频失败:", e);
    }
    innerAudio = null;
  }
});
</script>

<style scoped>
.music-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #ff4d4d 0%, #cc0000 100%);
  padding-bottom: 40rpx;
  display: flex;
  flex-direction: column;
}

/* 顶部标题 */
.header {
  padding: 40rpx 30rpx 20rpx;
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

/* 封面区域 */
.cover-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40rpx 0;
}

.cover-wrapper {
  width: 500rpx;
  height: 500rpx;
  border-radius: 50%;
  overflow: hidden;
  box-shadow: 0 10rpx 40rpx rgba(0, 0, 0, 0.3);
  border: 8rpx solid rgba(255, 255, 255, 0.3);
  transition: transform 0.3s;
  position: relative;
  cursor: pointer;
}

.cover-wrapper:active {
  transform: scale(0.98);
}

.cover-wrapper.rotating {
  animation: rotate 20s linear infinite;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.cover-image {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #fff 0%, #f5f5f5 100%);
}

/* 播放图标叠加层 */
.play-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
}

.play-icon {
  width: 120rpx;
  height: 120rpx;
  filter: drop-shadow(0 4rpx 8rpx rgba(0, 0, 0, 0.3));
}

/* 歌词区域 */
.lyrics-container {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40rpx 30rpx;
  overflow: hidden;
}

.lyrics-wrapper {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 30rpx;
}

.lyric-line {
  text-align: center;
  line-height: 1.8;
  white-space: pre-wrap;
  word-break: break-all;
  width: 100%;
  transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  transform-origin: center;
}

/* 上一句歌词 */
.prev-lyric {
  color: rgba(255, 255, 255, 0.4);
  font-size: 28rpx;
  opacity: 0;
  animation: fadeInUp 0.6s ease-out forwards;
}

/* 当前歌词 - 突出显示 */
.current-lyric {
  color: #ffffff;
  font-size: 40rpx;
  font-weight: bold;
  text-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.4);
  opacity: 0;
  animation: scaleIn 0.6s ease-out forwards;
  letter-spacing: 2rpx;
}

/* 下一句歌词 */
.next-lyric {
  color: rgba(255, 255, 255, 0.4);
  font-size: 28rpx;
  opacity: 0;
  animation: fadeInDown 0.6s ease-out forwards;
}

/* 上一句淡入向上动画 */
@keyframes fadeInUp {
  0% {
    opacity: 0;
    transform: translateY(20rpx);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 当前歌词缩放淡入动画 */
@keyframes scaleIn {
  0% {
    opacity: 0;
    transform: scale(0.9);
  }
  50% {
    transform: scale(1.05);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

/* 下一句淡入向下动画 */
@keyframes fadeInDown {
  0% {
    opacity: 0;
    transform: translateY(-20rpx);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
