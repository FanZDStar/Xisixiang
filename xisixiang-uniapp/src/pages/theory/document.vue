<template>
  <view class="document-page">
    <view v-if="loading" class="loading-container">
      <view class="loading-spinner"></view>
      <text class="loading-text">正在加载文档...</text>
    </view>

    <view v-else-if="error" class="error-container">
      <text class="error-icon">◆</text>
      <text class="error-text">{{ error }}</text>
      <button @click="loadDocument" class="retry-btn">重新加载</button>
    </view>

    <scroll-view v-else scroll-y class="document-content">
      <view class="markdown-body">
        <mp-html :content="htmlContent" :selectable="true" :tag-style="tagStyle" />
      </view>
    </scroll-view>
  </view>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { marked } from "marked";

const loading = ref(true);
const error = ref("");
const markdownContent = ref(""); // 存储原始Markdown内容
const htmlContent = ref(""); // 存储转换后的HTML内容
const fileName = ref("");
const title = ref("");

// 定义Markdown标签样式
const tagStyle = {
  h1: "font-size: 42rpx; font-weight: bold; margin: 30rpx 0 20rpx; padding-bottom: 15rpx; border-bottom: 1rpx solid #eaecef; color: #f44336;",
  h2: "font-size: 36rpx; font-weight: bold; margin: 25rpx 0 15rpx; padding-bottom: 10rpx; border-bottom: 1rpx solid #eaecef;",
  h3: "font-size: 30rpx; font-weight: bold; margin: 20rpx 0 10rpx;",
  p: "font-size: 28rpx; line-height: 1.8; margin: 15rpx 0;",
  ul: "margin: 15rpx 0; padding-left: 40rpx;",
  ol: "margin: 15rpx 0; padding-left: 40rpx;",
  li: "margin: 10rpx 0;",
  blockquote: "margin: 20rpx 0; padding: 20rpx; background-color: #f9f9f9; border-left: 6rpx solid #ff4d4d; color: #666;",
  code: "font-family: monospace; background-color: #f6f8fa; padding: 4rpx 8rpx; border-radius: 6rpx; font-size: 24rpx;",
  pre: "background-color: #f6f8fa; padding: 20rpx; border-radius: 6rpx; overflow: auto; margin: 20rpx 0;",
  a: "color: #ff4d4d; text-decoration: underline;",
  img: "max-width: 100%; height: auto;",
  table: "width: 100%; border-collapse: collapse; margin: 20rpx 0;",
  th: "background-color: #f6f8fa; font-weight: bold; padding: 15rpx; border: 1rpx solid #dfe2e5;",
  td: "padding: 15rpx; border: 1rpx solid #dfe2e5;",
  hr: "border: none; height: 1rpx; background-color: #eaecef; margin: 30rpx 0;"
};

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
      // 保存原始Markdown内容
      markdownContent.value = res.data;
      
      // 将Markdown转换为HTML
      htmlContent.value = marked(res.data);
    } else {
      throw new Error("文档加载失败");
    }
  } catch (err) {
    console.error("Load document error:", err);
    error.value = "文档加载失败，请确保后端服务已启动";
    markdownContent.value = `# ${title.value}\n\n文档内容加载失败...\n\n请确保后端服务运行在 http://127.0.0.1:5122`;
    // 在错误情况下也转换Markdown到HTML
    htmlContent.value = marked(markdownContent.value);
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
  color: #ff4d4d;
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