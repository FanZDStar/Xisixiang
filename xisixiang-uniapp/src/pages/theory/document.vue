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
        <rich-text :nodes="htmlContent"></rich-text>
      </view>
    </scroll-view>
  </view>
</template>

<script setup>
import { ref, onMounted } from "vue";

const loading = ref(true);
const error = ref("");
const htmlContent = ref("");
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
    // 注意：小程序中需要从网络加载文档
    // 你需要将 Markdown 文件放到服务器上，或者使用云存储
    const baseUrl = "http://127.0.0.1:5122/static/theory/"; // 需要配置后端静态文件服务

    const res = await new Promise((resolve, reject) => {
      uni.request({
        url: baseUrl + fileName.value,
        method: "GET",
        success: resolve,
        fail: reject,
      });
    });

    if (res.statusCode === 200) {
      htmlContent.value = formatMarkdown(res.data);
    } else {
      throw new Error("文档加载失败");
    }
  } catch (err) {
    console.error("Load document error:", err);
    error.value = "文档加载失败，请检查网络连接";

    // 临时方案：显示占位内容
    htmlContent.value = `
      <h1>${title.value}</h1>
      <p style="color: #999;">文档内容加载中...</p>
      <p style="color: #999;">提示：请确保后端已配置静态文件服务</p>
    `;
  } finally {
    loading.value = false;
  }
};

// 简化的 Markdown 转 HTML（小程序版）
const formatMarkdown = (text) => {
  if (!text) return "";

  let html = text
    // 标题
    .replace(
      /^### (.+)$/gm,
      '<h3 style="color: #ff4d4d; font-size: 32rpx; margin: 20rpx 0; font-weight: bold;">$1</h3>'
    )
    .replace(
      /^## (.+)$/gm,
      '<h2 style="color: #ff4d4d; font-size: 36rpx; margin: 25rpx 0; font-weight: bold;">$1</h2>'
    )
    .replace(
      /^# (.+)$/gm,
      '<h1 style="color: #ff4d4d; font-size: 40rpx; margin: 30rpx 0; font-weight: bold;">$1</h1>'
    )
    // 加粗
    .replace(
      /\*\*(.+?)\*\*/g,
      '<strong style="color: #ff4d4d; font-weight: bold;">$1</strong>'
    )
    // 列表
    .replace(
      /^[\-\*] (.+)$/gm,
      '<p style="margin: 10rpx 0; padding-left: 20rpx;">• $1</p>'
    )
    // 段落
    .replace(/\n\n/g, "<br/><br/>")
    .replace(/\n/g, "<br/>");

  return html;
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
