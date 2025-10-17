<template>
  <view class="document-page">
    <view v-if="loading" class="loading-container">
      <view class="loading-spinner"></view>
      <text class="loading-text">正在加载文档...</text>
    </view>

    <view v-else-if="error" class="error-container">
      <text class="error-icon">❌</text>
      <text class="error-text">{{ error }}</text>
      <button @click="loadDocument" class="retry-btn">重新加载</button>
    </view>

    <scroll-view v-else scroll-y class="document-content">
      <view class="markdown-body">
        <mp-html :content="markdownContent" :selectable="true" />
      </view>
    </scroll-view>
  </view>
</template>

<script setup>
import { ref, onMounted } from "vue";

const loading = ref(true);
const error = ref("");
const markdownContent = ref("");
const fileName = ref("");
const title = ref("");

onMounted(() => {
  // 获取 URL 参数
  const pages = getCurrentPages();
  const currentPage = pages[pages.length - 1];
  const options = currentPage.options;

  title.value = decodeURIComponent(options.title || "");
  fileName.value = decodeURIComponent(options.file || "");

  uni.setNavigationBarTitle({
    title: title.value,
  });

  loadDocument();
});

const loadDocument = async () => {
  loading.value = true;
  error.value = "";

  try {
    // 从后端加载文档（小程序无法直接访问本地 static 文件）
    const baseUrl = "http://127.0.0.1:5122/static/theory/";

    const res = await new Promise((resolve, reject) => {
      uni.request({
        url: baseUrl + fileName.value,
        method: "GET",
        success: resolve,
        fail: reject,
      });
    });

    if (res.statusCode === 200) {
      // mp-html 可以直接渲染 Markdown
      markdownContent.value = res.data;
    } else {
      throw new Error("文档加载失败");
    }
  } catch (err) {
    console.error("Load document error:", err);
    error.value = "文档加载失败，请确保后端服务已启动";
    markdownContent.value = `# ${title.value}\n\n文档内容加载失败...\n\n请确保后端服务运行在 http://127.0.0.1:5122`;
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.document-page {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.loading-container,
.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
}

.loading-spinner {
  width: 80rpx;
  height: 80rpx;
  border: 6rpx solid #ffcccc;
  border-top-color: #ff4d4d;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.loading-text {
  margin-top: 30rpx;
  color: #999;
  font-size: 28rpx;
}

.error-icon {
  font-size: 100rpx;
  margin-bottom: 30rpx;
}

.error-text {
  color: #666;
  font-size: 28rpx;
  margin-bottom: 40rpx;
}

.retry-btn {
  background: linear-gradient(135deg, #ff4d4d, #cc0000);
  color: white;
  border: none;
  padding: 20rpx 60rpx;
  border-radius: 40rpx;
}

.document-content {
  height: 100vh;
}

.markdown-body {
  padding: 40rpx;
  background-color: white;
  line-height: 1.8;
  font-size: 28rpx;
  color: #333;
}
</style>
