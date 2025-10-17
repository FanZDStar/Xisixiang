<template>
  <view class="theory-page">
    <!-- 自定义 TabBar -->
    <custom-tab-bar />

    <!-- 顶部标题 -->
    <view class="page-header">
      <text class="header-title">📚 理论学习中心</text>
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
        <view class="card-icon">📄</view>
        <view class="card-content">
          <text class="card-title">{{ doc.title }}</text>
          <text class="card-description">{{ doc.description }}</text>
        </view>
        <view class="card-arrow">→</view>
      </view>
    </view>

    <!-- 知识图谱入口 -->
    <view class="knowledge-graph-entry" @click="goToKnowledgeGraph">
      <view class="entry-icon">🗺️</view>
      <view class="entry-content">
        <text class="entry-title">知识图谱</text>
        <text class="entry-subtitle">可视化理论关系</text>
      </view>
      <view class="entry-arrow">→</view>
    </view>
  </view>
</template>

<script setup>
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

.knowledge-graph-entry {
  display: flex;
  align-items: center;
  background: linear-gradient(135deg, #ff4d4d, #cc0000);
  border-radius: 20rpx;
  padding: 35rpx;
  box-shadow: 0 8rpx 25rpx rgba(255, 77, 77, 0.3);
}

.knowledge-graph-entry:active {
  transform: scale(0.98);
}

.entry-icon {
  font-size: 60rpx;
  margin-right: 25rpx;
}

.entry-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.entry-title {
  font-size: 34rpx;
  font-weight: bold;
  color: white;
  margin-bottom: 8rpx;
}

.entry-subtitle {
  font-size: 24rpx;
  color: rgba(255, 255, 255, 0.9);
}

.entry-arrow {
  font-size: 40rpx;
  color: white;
  margin-left: 20rpx;
}
</style>
