<template>
  <div class="knowledge-graph-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>习近平新时代中国特色社会主义思想知识图谱</h1>
      <p class="subtitle">深入学习习近平新时代中国特色社会主义思想的核心要义与实践指导</p>
    </div>

    <!-- 主要内容布局 -->
    <div class="content-layout">
      <!-- 侧边栏导航 -->
      <div class="sidebar">
        <div class="sidebar-header">
          <h2>知识体系</h2>
          <div class="sidebar-divider"></div>
        </div>
        
        <ul class="category-list">
          <li class="category-item">
            <div class="category-header">
              <h3>🏛️ 制度建设</h3>
            </div>
            <ul class="subcategory-list">
              <li class="subcategory-item">
                <span>党的制度建设</span>
              </li>
              <li class="subcategory-item">
                <span>国家制度体系</span>
              </li>
              <li class="subcategory-item">
                <span>治理体系现代化</span>
              </li>
            </ul>
          </li>
          
          <li class="category-item">
            <div class="category-header">
              <h3>🏆 竞争优势</h3>
            </div>
            <ul class="subcategory-list">
              <li class="subcategory-item">
                <span>制度优势</span>
              </li>
              <li class="subcategory-item">
                <span>发展优势</span>
              </li>
              <li class="subcategory-item">
                <span>文化优势</span>
              </li>
            </ul>
          </li>
          
          <li class="category-item">
            <div class="category-header">
              <h3>⚡ 实践指导</h3>
            </div>
            <ul class="subcategory-list">
              <li class="subcategory-item">
                <span>经济建设</span>
              </li>
              <li class="subcategory-item">
                <span>社会发展</span>
              </li>
              <li class="subcategory-item">
                <span>生态文明</span>
              </li>
            </ul>
          </li>
        </ul>
      </div>

      <!-- 主内容区域 -->
      <div class="main-content">
        <!-- 移动端提示 -->
        <div class="mobile-warning">
          <div class="warning-content">
            <h3>移动端提示</h3>
            <p>此模块移动端待开发，请使用PC端访问获得最佳体验</p>
          </div>
        </div>

        <!-- PC端知识图谱 -->
        <div class="desktop-only">
          <!-- 知识图谱区域 -->
          <div class="graph-container">
            <div class="graph-wrapper">
              <!-- 装饰轨道 -->
              <div class="orbit orbit-1"></div>
              <div class="orbit orbit-2"></div>
              <div class="orbit orbit-3"></div>
              
              <!-- 连接线 -->
              <div class="connection-line institution-line"></div>
              <div class="connection-line competition-line"></div>
              <div class="connection-line implementation-line"></div>
              
              <!-- 核心节点 -->
              <div class="node core-node" @click="showNodeDetail('core')">
                <span>习近平新时代<br>中国特色社会主义思想</span>
              </div>
              
              <!-- 分类节点 -->
              <div class="node category-node institution-node" @click="showNodeDetail('institution')">
                <span>制度建设</span>
              </div>
              
              <div class="node category-node competition-node" @click="showNodeDetail('competition')">
                <span>竞争优势</span>
              </div>
              
              <div class="node category-node implementation-node" @click="showNodeDetail('implementation')">
                <span>实践指导</span>
              </div>
            </div>
          </div>

          <!-- 时间轴区域 -->
          <div class="timeline-section">
            <div class="timeline-header">
              <h3>📚 重要文献时间轴</h3>
              <p>按时间顺序展示重要理论文献和政策文件</p>
            </div>
            
            <div class="timeline">
              <div class="timeline-line"></div>
              <div class="timeline-items">
                <div v-for="item in timelineItems" :key="item.id" class="timeline-item">
                  <div class="dot"></div>
                  <div class="meta">
                    <span class="date">{{ item.date }}</span>
                    <a @click="navigateToArticle(item.articleId)" class="title">{{ item.title }}</a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 节点详情面板 -->
        <div v-if="selectedNode" class="node-detail-panel">
          <div class="detail-header">
            <h3>{{ nodeDetails[selectedNode].title }}</h3>
            <button class="close-btn" @click="selectedNode = null">×</button>
          </div>
          <div class="detail-content">
            <p>{{ nodeDetails[selectedNode].description }}</p>
            <div class="related-articles">
              <h4>相关文章</h4>
              <ul>
                <li v-for="article in nodeDetails[selectedNode].articles" :key="article.id">
                  <a @click="navigateToArticle(article.articleId)">{{ article.title }}</a>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const selectedNode = ref(null)

// 理论文章列表 - 与TheoryView.vue保持一致
const theoryArticles = ref([
  {
    id: 1,
    title: "中共中央国务院关于加快建设全国统一大市场的意见",
    path: "/theory/中共中央国务院关于加快建设全国统一大市场的意见.md",
  },
  {
    id: 2,
    title: "纵深推进全国统一大市场建设",
    path: "/theory/纵深推进全国统一大市场建设.md",
  },
  {
    id: 3,
    title: "怎么理解纵深推进全国统一大市场建设",
    path: "/theory/怎么理解纵深推进全国统一大市场建设.md",
  },
  {
    id: 4,
    title: "张国清：构建全国统一大市场",
    path: "/theory/构建全国统一大市场.md",
  },
  {
    id: 5,
    title: "理响中国丨全国统一大市场的'那些事'",
    path: "/theory/全国统一大市场的那些事.md",
  },
  {
    id: 6,
    title: "深化构建全国统一大市场的逻辑认识与思考",
    path: "/theory/深化构建全国统一大市场的逻辑认识与思考.md",
  },
  {
    id: 7,
    title: "中国发布丨国家发展改革委：将制定《妨碍统一市场和公平竞争行为防范事项清单》",
    path: "/theory/将制定《妨碍统一市场和公平竞争行为防范事项清单》.md",
  },
  {
    id: 8,
    title: "全国统一大市场建设指引（试行）",
    path: "/theory/全国统一大市场建设指引（试行）.md",
  },
]);

// 时间轴数据 - 使用真实文章数据
const timelineItems = computed(() => [
  {
    id: 1,
    date: '2022-04-10',
    title: '中共中央国务院关于加快建设全国统一大市场的意见',
    articleId: 1
  },
  {
    id: 2,
    date: '2023-03-15',
    title: '纵深推进全国统一大市场建设',
    articleId: 2
  },
  {
    id: 3,
    date: '2023-07-20',
    title: '怎么理解纵深推进全国统一大市场建设',
    articleId: 3
  },
  {
    id: 4,
    date: '2024-02-28',
    title: '张国清：构建全国统一大市场',
    articleId: 4
  },
  {
    id: 5,
    date: '2024-06-18',
    title: '理响中国丨全国统一大市场的"那些事"',
    articleId: 5
  },
  {
    id: 6,
    date: '2024-09-12',
    title: '深化构建全国统一大市场的逻辑认识与思考',
    articleId: 6
  },
  {
    id: 7,
    date: '2025-01-30',
    title: '将制定《妨碍统一市场和公平竞争行为防范事项清单》',
    articleId: 7
  },
  {
    id: 8,
    date: '2025-05-15',
    title: '全国统一大市场建设指引（试行）',
    articleId: 8
  }
].sort((a, b) => new Date(a.date) - new Date(b.date)))

// 跳转到理论学习页面的具体文章
const navigateToArticle = (articleId) => {
  router.push({
    path: '/theory',
    query: { article: articleId }
  })
}

// 节点详情数据 - 包含真实文章链接
const nodeDetails = {
  core: {
    title: '习近平新时代中国特色社会主义思想',
    description: '习近平新时代中国特色社会主义思想是马克思主义中国化时代化的最新成果，是当代中国马克思主义、二十一世纪马克思主义，是中华文化和中国精神的时代精华，实现了马克思主义中国化新的飞跃。',
    articles: [
      { id: 1, title: '中共中央国务院关于加快建设全国统一大市场的意见', articleId: 1 },
      { id: 2, title: '纵深推进全国统一大市场建设', articleId: 2 },
      { id: 3, title: '怎么理解纵深推进全国统一大市场建设', articleId: 3 }
    ]
  },
  institution: {
    title: '制度建设',
    description: '坚持和完善中国特色社会主义制度，推进国家治理体系和治理能力现代化，这是全党的一项重大战略任务。',
    articles: [
      { id: 1, title: '中共中央国务院关于加快建设全国统一大市场的意见', articleId: 1 },
      { id: 4, title: '张国清：构建全国统一大市场', articleId: 4 },
      { id: 8, title: '全国统一大市场建设指引（试行）', articleId: 8 }
    ]
  },
  competition: {
    title: '竞争优势',
    description: '中国特色社会主义制度具有显著优势，这些优势是我们坚定中国特色社会主义道路自信、理论自信、制度自信、文化自信的基本依据。',
    articles: [
      { id: 5, title: '理响中国丨全国统一大市场的"那些事"', articleId: 5 },
      { id: 6, title: '深化构建全国统一大市场的逻辑认识与思考', articleId: 6 },
      { id: 7, title: '将制定《妨碍统一市场和公平竞争行为防范事项清单》', articleId: 7 }
    ]
  },
  implementation: {
    title: '实践指导',
    description: '习近平新时代中国特色社会主义思想不仅有鲜明的理论品格，更有强烈的实践品格，为新时代坚持和发展中国特色社会主义提供了科学指南。',
    articles: [
      { id: 2, title: '纵深推进全国统一大市场建设', articleId: 2 },
      { id: 3, title: '怎么理解纵深推进全国统一大市场建设', articleId: 3 },
      { id: 6, title: '深化构建全国统一大市场的逻辑认识与思考', articleId: 6 }
    ]
  }
}

// 显示节点详情
const showNodeDetail = (nodeType) => {
  selectedNode.value = nodeType
}
</script>

<style scoped>
/* 全局样式重置 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* 容器样式 */
.knowledge-graph-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  padding: 20px;
  font-family: 'Microsoft YaHei', 'PingFang SC', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* 页面标题 */
.page-header {
  text-align: center;
  margin-bottom: 32px;
  padding: 32px 20px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  backdrop-filter: blur(20px);
  border: 2px solid #f44336;
  box-shadow: 0 8px 32px rgba(244, 67, 54, 0.15);
}

.page-header h1 {
  color: #2c3e50;
  margin-bottom: 12px;
  font-size: 28px;
  font-weight: 700;
  background: linear-gradient(135deg, #f44336, #d32f2f);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  color: #2c3e50;
  margin: 0;
  font-size: 16px;
  font-weight: 400;
}

/* 主要内容布局 */
.content-layout {
  display: flex;
  gap: 24px;
  max-width: 1400px;
  margin: 0 auto;
  align-items: flex-start;
}

/* 侧边栏样式 */
.sidebar {
  flex: 0 0 320px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 24px;
  backdrop-filter: blur(20px);
  border: 2px solid #f44336;
  box-shadow: 0 8px 32px rgba(244, 67, 54, 0.15);
  height: fit-content;
  position: sticky;
  top: 20px;
}

.sidebar-header {
  text-align: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 2px solid #f44336;
}

.sidebar-header h2 {
  margin: 0;
  color: #2c3e50;
  font-size: 22px;
  font-weight: 700;
}

.sidebar-divider {
  height: 3px;
  background: linear-gradient(90deg, transparent, #f44336, transparent);
  border-radius: 2px;
  margin: 12px auto 0;
  width: 80%;
}

.category-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.category-item {
  margin-bottom: 20px;
  background: linear-gradient(135deg, rgba(244, 67, 54, 0.1), rgba(211, 47, 47, 0.1));
  border-radius: 16px;
  padding: 18px;
  border: 1px solid rgba(244, 67, 54, 0.2);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.category-item:hover {
  background: linear-gradient(135deg, rgba(244, 67, 54, 0.15), rgba(211, 47, 47, 0.15));
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(244, 67, 54, 0.3);
}

.category-header h3 {
  color: #2c3e50;
  margin: 0 0 16px 0;
  font-size: 18px;
  font-weight: 600;
}

.subcategory-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.subcategory-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  cursor: pointer;
  color: #34495e;
  border-radius: 12px;
  transition: all 0.3s ease;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 500;
}

.subcategory-item:hover {
  background: linear-gradient(135deg, #f44336, #d32f2f);
  color: white;
  transform: translateX(8px);
  box-shadow: 0 4px 15px rgba(244, 67, 54, 0.4);
}

/* 主内容区域 */
.main-content {
  flex: 1;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 32px;
  backdrop-filter: blur(20px);
  border: 2px solid #f44336;
  box-shadow: 0 8px 32px rgba(244, 67, 54, 0.15);
  min-height: 85vh;
  display: flex;
  flex-direction: column;
  gap: 24px;
  max-width: 100%;
  overflow: hidden;
}

/* 移动端提示 */
.mobile-warning {
  display: none;
  text-align: center;
  padding: 60px 24px;
}

.mobile-warning .warning-content {
  background: linear-gradient(135deg, #ffeaa7, #fab1a0);
  border: 2px solid #e17055;
  border-radius: 20px;
  padding: 32px;
  max-width: 400px;
  margin: 0 auto;
  box-shadow: 0 8px 25px rgba(225, 112, 85, 0.3);
}

.mobile-warning h3 {
  color: #2d3436;
  margin: 0 0 16px 0;
  font-size: 20px;
  font-weight: 700;
}

.mobile-warning p {
  color: #2d3436;
  margin: 0;
  font-size: 16px;
}

/* 知识图谱区域 */
.graph-container {
  background: linear-gradient(135deg, #ffffff, #f8f9fa);
  border-radius: 20px;
  padding: 32px;
  position: relative;
  overflow: hidden;
  min-height: 500px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: inset 0 2px 4px rgba(244, 67, 54, 0.1);
  border: 2px solid #f44336;
}

.graph-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 20% 20%, rgba(244, 67, 54, 0.05) 0%, transparent 40%),
    radial-gradient(circle at 80% 80%, rgba(244, 67, 54, 0.03) 0%, transparent 40%),
    radial-gradient(circle at 40% 60%, rgba(244, 67, 54, 0.02) 0%, transparent 30%);
  pointer-events: none;
}

.graph-wrapper {
  position: relative;
  width: 100%;
  max-width: 700px;
  height: 450px;
  z-index: 1;
}

/* 节点样式 */
.node {
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  text-align: center;
  font-weight: 700;
  color: #2c3e50;
  text-shadow: 0 2px 4px rgba(255,255,255,0.8);
  border: 4px solid rgba(244, 67, 54, 0.6);
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 25px rgba(244, 67, 54, 0.2);
}

.core-node {
  width: 160px;
  height: 160px;
  background: linear-gradient(135deg, #f44336, #d32f2f);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 18px;
  color: white;
  text-shadow: 0 2px 4px rgba(0,0,0,0.3);
  animation: coreGlow 4s ease-in-out infinite;
}

@keyframes coreGlow {
  0%, 100% { 
    transform: translate(-50%, -50%) scale(1);
    box-shadow: 0 8px 25px rgba(244, 67, 54, 0.4), 0 0 0 0 rgba(244, 67, 54, 0.7);
  }
  50% { 
    transform: translate(-50%, -50%) scale(1.05);
    box-shadow: 0 12px 35px rgba(244, 67, 54, 0.6), 0 0 0 10px rgba(244, 67, 54, 0);
  }
}

.category-node {
  width: 120px;
  height: 120px;
  font-size: 14px;
}

.institution-node {
  background: linear-gradient(135deg, #ffffff, #f5f5f5);
  top: 18%;
  left: 22%;
  color: #2c3e50;
  border: 4px solid #f44336;
}

.competition-node {
  background: linear-gradient(135deg, #ffffff, #f5f5f5);
  top: 18%;
  right: 22%;
  color: #2c3e50;
  border: 4px solid #f44336;
}

.implementation-node {
  background: linear-gradient(135deg, #ffffff, #f5f5f5);
  bottom: 18%;
  left: 50%;
  transform: translateX(-50%);
  color: #2c3e50;
  border: 4px solid #f44336;
}

.node:hover {
  transform: scale(1.15) !important;
  box-shadow: 0 15px 40px rgba(0,0,0,0.4) !important;
  z-index: 10;
}

.core-node:hover {
  transform: translate(-50%, -50%) scale(1.15) !important;
}

.implementation-node:hover {
  transform: translateX(-50%) scale(1.15) !important;
}

/* 连接线 */
.connection-line {
  position: absolute;
  background: rgba(244, 67, 54, 0.8);
  border-radius: 3px;
  transition: all 0.3s ease;
  z-index: 0;
  box-shadow: 0 2px 8px rgba(244, 67, 54, 0.3);
}

.connection-line:hover {
  background: rgba(244, 67, 54, 1);
  box-shadow: 0 4px 15px rgba(244, 67, 54, 0.6);
  transform: scaleY(1.5);
}

.institution-line {
  width: 200px;
  height: 4px;
  top: 40%;
  left: 30%;
  transform: rotate(-20deg);
  transform-origin: left center;
}

.competition-line {
  width: 200px;
  height: 4px;
  top: 40%;
  right: 30%;
  transform: rotate(20deg);
  transform-origin: right center;
}

.implementation-line {
  width: 4px;
  height: 140px;
  bottom: 32%;
  left: 50%;
  transform: translateX(-50%);
}

/* 装饰轨道 */
.orbit {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  border: 2px dashed rgba(244, 67, 54, 0.3);
  border-radius: 50%;
  pointer-events: none;
  animation: rotate 60s linear infinite;
}

@keyframes rotate {
  from { transform: translate(-50%, -50%) rotate(0deg); }
  to { transform: translate(-50%, -50%) rotate(360deg); }
}

.orbit-1 { width: 220px; height: 220px; animation-duration: 60s; }
.orbit-2 { width: 340px; height: 340px; animation-duration: 80s; }
.orbit-3 { width: 460px; height: 460px; animation-duration: 100s; }

/* 时间轴区域 */
.timeline-section {
  background: linear-gradient(135deg, rgba(244, 67, 54, 0.1), rgba(211, 47, 47, 0.1));
  border-radius: 16px;
  padding: 24px;
  border: 1px solid rgba(244, 67, 54, 0.3);
  backdrop-filter: blur(10px);
}

.timeline-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 2px solid #f44336;
}

.timeline-header h3 {
  margin: 0;
  font-size: 20px;
  color: #2c3e50;
  font-weight: 700;
}

.timeline-header p {
  margin: 0;
  color: #2c3e50;
  font-size: 14px;
}

.timeline {
  position: relative;
  overflow-x: auto;
  padding: 20px 12px;
  background: linear-gradient(135deg, #ffffff, #f8f9fa);
  border-radius: 12px;
  min-height: 120px;
  border: 2px solid #f44336;
}

.timeline::-webkit-scrollbar {
  height: 8px;
}

.timeline::-webkit-scrollbar-thumb {
  background: rgba(244, 67, 54, 0.5);
  border-radius: 4px;
}

.timeline::-webkit-scrollbar-track {
  background: rgba(244, 67, 54, 0.1);
  border-radius: 4px;
}

.timeline-line {
  position: absolute;
  left: 12px;
  right: 12px;
  top: 45px;
  height: 4px;
  background: linear-gradient(90deg, #f44336, #d32f2f, #f44336);
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(244, 67, 54, 0.5);
}

.timeline-items {
  position: relative;
  display: flex;
  gap: 30px;
  padding: 0 12px;
  z-index: 2;
}

.timeline-item {
  min-width: 200px;
  flex-shrink: 0;
}

.timeline-item .dot {
  display: block;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #f44336;
  border: 4px solid white;
  box-shadow: 0 0 0 3px #f44336, 0 4px 12px rgba(244, 67, 54, 0.5);
  cursor: pointer;
  transition: all 0.3s ease;
}

.timeline-item .dot:hover {
  background: #d32f2f;
  transform: scale(1.3);
  box-shadow: 0 0 0 3px #d32f2f, 0 6px 20px rgba(211, 47, 47, 0.7);
}

.timeline-item .meta {
  margin-top: 16px;
}

.timeline-item .date {
  display: block;
  font-size: 13px;
  color: #2c3e50;
  font-weight: 700;
  background: rgba(255,255,255,0.95);
  padding: 6px 12px;
  border-radius: 20px;
  margin-bottom: 8px;
  width: fit-content;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.timeline-item .title {
  display: block;
  font-size: 14px;
  color: white;
  text-decoration: none;
  background: rgba(244, 67, 54, 0.9);
  padding: 12px 16px;
  border-radius: 12px;
  line-height: 1.4;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 15px rgba(244, 67, 54, 0.3);
  cursor: pointer;
}

.timeline-item .title:hover {
  background: rgba(244, 67, 54, 1);
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(244, 67, 54, 0.5);
}

/* 详情面板 */
.node-detail-panel {
  position: absolute;
  top: 24px;
  right: 24px;
  width: 350px;
  background: rgba(255, 255, 255, 0.98);
  border-radius: 16px;
  box-shadow: 0 16px 50px rgba(0, 0, 0, 0.2);
  z-index: 100;
  max-height: 80%;
  overflow-y: auto;
  border: 1px solid rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(20px);
  animation: slideInPanel 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes slideInPanel {
  from { 
    opacity: 0;
    transform: translateX(30px);
  }
  to { 
    opacity: 1;
    transform: translateX(0);
  }
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 2px solid #ecf0f1;
  background: linear-gradient(135deg, #f44336, #d32f2f);
  color: white;
  border-radius: 16px 16px 0 0;
}

.detail-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 700;
}

.close-btn {
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  cursor: pointer;
  color: white;
  transition: all 0.3s ease;
  font-weight: bold;
}

.close-btn:hover {
  background: rgba(231, 76, 60, 0.8);
  transform: rotate(90deg);
}

.detail-content {
  padding: 24px;
}

.detail-content p {
  color: #2c3e50;
  line-height: 1.7;
  margin-bottom: 20px;
  font-size: 15px;
}

.related-articles h4 {
  color: #2c3e50;
  margin: 20px 0 16px;
  font-size: 16px;
  font-weight: 700;
}

.related-articles ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.related-articles li {
  margin-bottom: 12px;
  padding: 12px 16px;
  background: linear-gradient(135deg, rgba(244, 67, 54, 0.1), rgba(211, 47, 47, 0.1));
  border-radius: 10px;
  border-left: 4px solid #f44336;
  transition: all 0.3s ease;
}

.related-articles li:hover {
  background: linear-gradient(135deg, rgba(244, 67, 54, 0.15), rgba(211, 47, 47, 0.15));
  transform: translateX(6px);
  box-shadow: 0 4px 15px rgba(244, 67, 54, 0.2);
}

.related-articles a {
  color: #f44336;
  text-decoration: none;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
}

.related-articles a:hover {
  color: #d32f2f;
  text-decoration: underline;
}

/* PC端显示控制 */
.desktop-only {
  display: block;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .page-header { display: none; }
  
  .content-layout {
    flex-direction: column;
    padding: 12px;
  }
  
  .sidebar { display: none; }
  
  .knowledge-graph-container {
    padding: 12px;
  }
  
  .main-content {
    padding: 20px;
    min-height: auto;
  }
  
  .mobile-warning { display: block; }
  .desktop-only { display: none; }
}

@media (max-width: 1024px) {
  .content-layout {
    flex-direction: column;
  }
  
  .sidebar {
    flex: none;
    margin-bottom: 24px;
    position: static;
  }
  
  .node-detail-panel {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 90%;
    max-width: 400px;
    max-height: 80vh;
  }
}

@media (max-width: 480px) {
  .knowledge-graph-container {
    padding: 8px;
  }
}
</style>
