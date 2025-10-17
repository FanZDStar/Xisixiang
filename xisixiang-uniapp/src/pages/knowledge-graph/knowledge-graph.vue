<template>
  <view class="knowledge-graph-page">
    <view class="header">
      <text class="header-title">知识图谱</text>
      <text class="header-subtitle">全国统一大市场理论体系</text>
    </view>

    <view class="content-container">
      <!-- 知识图谱可视化区域 -->
      <view class="graph-section">
        <view class="graph-container">
          <!-- 连接线 -->
          <view class="connection-line institution-line"></view>
          <view class="connection-line competition-line"></view>
          <view class="connection-line implementation-line"></view>
          
          <!-- 核心节点 -->
          <view class="node core-node" @click="showNodeDetail('core')">
            <text class="node-text">构建全国\n统一大市场</text>
          </view>
          
          <!-- 分类节点 -->
          <view class="node category-node institution-node" @click="showNodeDetail('institution')">
            <text class="node-text">制度创新</text>
          </view>
          
          <view class="node category-node competition-node" @click="showNodeDetail('competition')">
            <text class="node-text">公平竞争</text>
          </view>
          
          <view class="node category-node implementation-node" @click="showNodeDetail('implementation')">
            <text class="node-text">统一治理</text>
          </view>
        </view>
      </view>

      <!-- 知识体系导航 -->
      <view class="navigation-section">
        <view class="section-title">知识体系</view>
        
        <view class="category-list">
          <view 
            v-for="(category, index) in categories" 
            :key="index" 
            class="category-item"
          >
            <view class="category-header" @click="selectCategory(index)">
              <text class="category-name">{{ category.name }}</text>
              <text class="arrow">{{ openCategoryIndex === index ? '▲' : '▼' }}</text>
            </view>
            
            <view v-show="openCategoryIndex === index" class="subcategory-list">
              <view 
                v-for="(subcategory, subIndex) in category.subcategories" 
                :key="subIndex" 
                class="subcategory-item"
                @click="showNodeDetail(subcategory.nodeType)"
              >
                <text class="subcategory-text">● {{ subcategory.name }}</text>
              </view>
            </view>
          </view>
        </view>
      </view>

      <!-- 时间轴 -->
      <view class="timeline-section">
        <view class="section-title">政策时间轴</view>
        
        <scroll-view class="timeline-scroll" scroll-x>
          <view class="timeline-container">
            <view 
              v-for="(item, index) in timelineItems" 
              :key="index" 
              class="timeline-item"
              @click="navigateToArticle(item.articleId)"
            >
              <view class="timeline-dot"></view>
              <view class="timeline-content">
                <text class="timeline-date">{{ item.date }}</text>
                <text class="timeline-title">{{ item.title }}</text>
              </view>
            </view>
          </view>
        </scroll-view>
      </view>
    </view>

    <!-- 节点详情弹窗 -->
    <view v-if="selectedNode" class="detail-modal" @click="closeDetail">
      <view class="detail-content" @click.stop>
        <view class="detail-header">
          <text class="detail-title">{{ nodeDetails[selectedNode].title }}</text>
          <view class="close-btn" @click="closeDetail">×</view>
        </view>
        
        <scroll-view class="detail-scroll" scroll-y>
          <view class="detail-description">
            <text>{{ nodeDetails[selectedNode].description }}</text>
          </view>
          
          <view class="related-articles">
            <text class="related-title">相关文章</text>
            <view 
              v-for="(article, index) in nodeDetails[selectedNode].articles" 
              :key="index" 
              class="article-item"
              @click="navigateToArticle(article.articleId)"
            >
              <text class="article-title">▶ {{ article.title }}</text>
            </view>
          </view>
        </scroll-view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref } from "vue";

const openCategoryIndex = ref(null);
const selectedNode = ref(null);

// 知识体系分类
const categories = [
  {
    name: "制度创新",
    subcategories: [
      { name: "统一制度规则", nodeType: "institution" },
      { name: "市场准入制度", nodeType: "institution" },
      { name: "要素配置机制", nodeType: "institution" }
    ]
  },
  {
    name: "公平竞争",
    subcategories: [
      { name: "反垄断治理", nodeType: "competition" },
      { name: "公平竞争审查", nodeType: "competition" },
      { name: "市场监管体系", nodeType: "competition" }
    ]
  },
  {
    name: "统一治理",
    subcategories: [
      { name: "标准统一", nodeType: "implementation" },
      { name: "执法协调", nodeType: "implementation" },
      { name: "信息共享", nodeType: "implementation" }
    ]
  }
];

// 时间轴数据
const timelineItems = [
  { date: "2022-04-10", title: "加快建设全国统一大市场的意见", articleId: 1 },
  { date: "2023-03-15", title: "纵深推进全国统一大市场建设", articleId: 2 },
  { date: "2023-07-20", title: "怎么理解纵深推进", articleId: 3 },
  { date: "2024-02-28", title: "构建全国统一大市场", articleId: 4 },
  { date: "2024-06-18", title: "全国统一大市场的那些事", articleId: 5 },
  { date: "2024-09-12", title: "逻辑认识与思考", articleId: 6 },
  { date: "2025-01-30", title: "防范事项清单", articleId: 7 },
  { date: "2025-05-15", title: "建设指引（试行）", articleId: 8 }
];

// 节点详情数据
const nodeDetails = {
  core: {
    title: "构建全国统一大市场",
    description: "加快建设高效规范、公平竞争、充分开放的全国统一大市场，全面推动我国市场由大到强转变，为建设高标准市场体系、构建高水平社会主义市场经济体制提供坚强支撑。",
    articles: [
      { title: "中共中央国务院关于加快建设全国统一大市场的意见", articleId: 1 },
      { title: "纵深推进全国统一大市场建设", articleId: 2 },
      { title: "怎么理解纵深推进全国统一大市场建设", articleId: 3 }
    ]
  },
  institution: {
    title: "制度创新",
    description: "通过统一的制度规则、破除地方保护和市场分割、打通制约经济循环的关键堵点，促进商品要素资源在更大范围内畅通流动。",
    articles: [
      { title: "中共中央国务院关于加快建设全国统一大市场的意见", articleId: 1 },
      { title: "张国清：构建全国统一大市场", articleId: 4 },
      { title: "全国统一大市场建设指引（试行）", articleId: 8 }
    ]
  },
  competition: {
    title: "公平竞争",
    description: "坚持公平竞争政策基础地位，健全公平竞争制度框架和政策实施机制，建立全方位、多层次、立体化监管体系，规范不当市场竞争和市场干预行为。",
    articles: [
      { title: "理响中国丨全国统一大市场的'那些事'", articleId: 5 },
      { title: "深化构建全国统一大市场的逻辑认识与思考", articleId: 6 },
      { title: "将制定《妨碍统一市场和公平竞争行为防范事项清单》", articleId: 7 }
    ]
  },
  implementation: {
    title: "统一治理",
    description: "推进市场监管公平统一，健全统一规范的涉企优惠政策制度，完善产权保护制度，推进统一的市场监管，加强统一的社会信用体系建设。",
    articles: [
      { title: "纵深推进全国统一大市场建设", articleId: 2 },
      { title: "怎么理解纵深推进全国统一大市场建设", articleId: 3 },
      { title: "深化构建全国统一大市场的逻辑认识与思考", articleId: 6 }
    ]
  }
};

// 选择分类（修复折叠功能）
const selectCategory = (index) => {
  if (openCategoryIndex.value === index) {
    openCategoryIndex.value = null; // 关闭当前打开的分类
  } else {
    openCategoryIndex.value = index; // 打开点击的分类
  }
};

// 显示节点详情
const showNodeDetail = (nodeType) => {
  selectedNode.value = nodeType;
};

// 关闭详情弹窗
const closeDetail = () => {
  selectedNode.value = null;
};

// 跳转到文章
const navigateToArticle = (articleId) => {
  uni.navigateTo({
    url: `/pages/theory/document?title=${encodeURIComponent(
      getArticleTitle(articleId)
    )}&file=${encodeURIComponent(getArticleFileName(articleId))}`
  });
};

// 获取文章标题
const getArticleTitle = (articleId) => {
  const articles = [
    "中共中央国务院关于加快建设全国统一大市场的意见",
    "纵深推进全国统一大市场建设",
    "怎么理解纵深推进全国统一大市场建设",
    "构建全国统一大市场",
    "全国统一大市场的那些事",
    "深化构建全国统一大市场的逻辑认识与思考",
    "将制定《妨碍统一市场和公平竞争行为防范事项清单》",
    "全国统一大市场建设指引（试行）"
  ];
  return articles[articleId - 1] || "";
};

// 获取文章文件名
const getArticleFileName = (articleId) => {
  const fileNames = [
    "中共中央国务院关于加快建设全国统一大市场的意见.md",
    "纵深推进全国统一大市场建设.md",
    "怎么理解纵深推进全国统一大市场建设.md",
    "构建全国统一大市场.md",
    "全国统一大市场的那些事.md",
    "深化构建全国统一大市场的逻辑认识与思考.md",
    "将制定《妨碍统一市场和公平竞争行为防范事项清单》.md",
    "全国统一大市场建设指引（试行）.md"
  ];
  return fileNames[articleId - 1] || "";
};
</script>

<style scoped>
.knowledge-graph-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #fff5f5, #f5f5f5);
  padding: 20rpx;
}

.header {
  text-align: center;
  padding: 30rpx 20rpx;
  margin-bottom: 30rpx;
}

.header-title {
  display: block;
  font-size: 42rpx;
  font-weight: bold;
  color: #f44336;
  margin-bottom: 15rpx;
}

.header-subtitle {
  display: block;
  font-size: 26rpx;
  color: #666;
}

.content-container {
  display: flex;
  flex-direction: column;
  gap: 30rpx;
}

/* 知识图谱可视化区域 */
.graph-section {
  background: white;
  border-radius: 20rpx;
  padding: 40rpx 20rpx;
  box-shadow: 0 4rpx 20rpx rgba(244, 67, 54, 0.1);
}

.graph-container {
  position: relative;
  width: 100%;
  height: 500rpx;
}

/* 连接线 */
.connection-line {
  position: absolute;
  background: rgba(244, 67, 54, 0.8);
  border-radius: 2rpx;
  transform-origin: 0 0;
}

.institution-line {
  width: 180rpx;
  height: 4rpx;
  top: 42%;
  left: 28%;
  transform: rotate(-20deg);
}

.competition-line {
  width: 180rpx;
  height: 4rpx;
  top: 42%;
  right: 28%;
  transform: rotate(20deg);
}

.implementation-line {
  width: 4rpx;
  height: 160rpx;
  bottom: 25%;
  left: 50%;
  transform: translateX(-50%);
}

/* 节点样式 */
.node {
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  text-align: center;
  font-weight: bold;
  color: #2c3e50;
  border: 4rpx solid #f44336;
  box-shadow: 0 8rpx 25rpx rgba(244, 67, 54, 0.2);
  transition: all 0.3s ease;
}

.node-text {
  font-size: 24rpx;
  line-height: 1.4;
}

.core-node {
  width: 180rpx;
  height: 180rpx;
  background: linear-gradient(135deg, #f44336, #d32f2f);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  font-size: 26rpx;
}

.category-node {
  width: 140rpx;
  height: 140rpx;
  background: white;
}

.institution-node {
  top: 20%;
  left: 20%;
}

.competition-node {
  top: 20%;
  right: 20%;
}

.implementation-node {
  bottom: 20%;
  left: 50%;
  transform: translateX(-50%);
}

.node:active {
  transform: scale(1.1);
  box-shadow: 0 12rpx 35rpx rgba(244, 67, 54, 0.4);
}

.core-node:active {
  transform: translate(-50%, -50%) scale(1.1);
}

.implementation-node:active {
  transform: translateX(-50%) scale(1.1);
}

/* 知识体系导航 */
.navigation-section {
  background: white;
  border-radius: 20rpx;
  padding: 30rpx;
  box-shadow: 0 4rpx 20rpx rgba(244, 67, 54, 0.1);
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #f44336;
  margin-bottom: 30rpx;
  padding-bottom: 15rpx;
  border-bottom: 2rpx solid #f44336;
}

.category-list {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.category-item {
  background: linear-gradient(135deg, rgba(244, 67, 54, 0.1), rgba(211, 47, 47, 0.1));
  border-radius: 16rpx;
  padding: 20rpx;
  border: 1rpx solid rgba(244, 67, 54, 0.2);
}

.category-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10rpx 0;
}

.category-name {
  font-size: 28rpx;
  font-weight: bold;
  color: #2c3e50;
}

.arrow {
  font-size: 24rpx;
  color: #f44336;
}

.subcategory-list {
  margin-top: 20rpx;
  display: flex;
  flex-direction: column;
  gap: 15rpx;
}

.subcategory-item {
  padding: 15rpx 20rpx;
  background: rgba(255, 255, 255, 0.7);
  border-radius: 12rpx;
  transition: all 0.3s ease;
}

.subcategory-item:active {
  background: #f44336;
  color: white;
}

.subcategory-text {
  font-size: 24rpx;
  color: #34495e;
}

/* 时间轴 */
.timeline-section {
  background: white;
  border-radius: 20rpx;
  padding: 30rpx;
  box-shadow: 0 4rpx 20rpx rgba(244, 67, 54, 0.1);
}

.timeline-scroll {
  width: 100%;
  height: 200rpx;
  white-space: nowrap;
}

.timeline-container {
  display: inline-flex;
  padding: 20rpx 0;
}

.timeline-item {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  margin-right: 40rpx;
  min-width: 180rpx;
}

.timeline-dot {
  width: 20rpx;
  height: 20rpx;
  border-radius: 50%;
  background: #f44336;
  border: 4rpx solid white;
  box-shadow: 0 0 0 2rpx #f44336;
  margin-bottom: 15rpx;
}

.timeline-content {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.timeline-date {
  font-size: 20rpx;
  color: #666;
  margin-bottom: 10rpx;
}

.timeline-title {
  font-size: 22rpx;
  color: #f44336;
  text-align: center;
}

.timeline-item:active .timeline-dot {
  transform: scale(1.3);
}

/* 详情弹窗 */
.detail-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}

.detail-content {
  width: 90%;
  max-height: 80%;
  background: white;
  border-radius: 20rpx;
  overflow: hidden;
  box-shadow: 0 20rpx 50rpx rgba(0, 0, 0, 0.3);
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 30rpx;
  background: linear-gradient(135deg, #f44336, #d32f2f);
  color: white;
}

.detail-title {
  font-size: 32rpx;
  font-weight: bold;
  flex: 1;
  margin-right: 20rpx;
}

.close-btn {
  font-size: 36rpx;
  font-weight: bold;
  width: 50rpx;
  height: 50rpx;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.detail-scroll {
  height: 500rpx;
  padding: 30rpx;
  box-sizing: border-box;
}

.detail-description {
  font-size: 26rpx;
  color: #333;
  line-height: 1.6;
  margin-bottom: 30rpx;
  text-align: justify;
}

.related-title {
  font-size: 28rpx;
  font-weight: bold;
  color: #f44336;
  margin-bottom: 20rpx;
  display: block;
}

.article-item {
  padding: 20rpx;
  background: linear-gradient(135deg, rgba(244, 67, 54, 0.1), rgba(211, 47, 47, 0.1));
  border-radius: 12rpx;
  margin-bottom: 15rpx;
  border-left: 6rpx solid #f44336;
}

.article-title {
  font-size: 24rpx;
  color: #2c3e50;
  word-break: break-all;
}

.article-item:active {
  background: linear-gradient(135deg, rgba(244, 67, 54, 0.2), rgba(211, 47, 47, 0.2));
}
</style>