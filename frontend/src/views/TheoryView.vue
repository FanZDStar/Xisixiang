<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import MarkdownRenderer from '../components/MarkdownRenderer.vue'

const route = useRoute()

// 理论文章列表
const theoryArticles = ref([
  { id: 1, title: '关于加快建设全国统一大市场的指导意见', path: '/theory/中共中央国务院关于加快建设全国统一大市场的意见.md' },
])

const selectedArticle = ref(theoryArticles.value[0])

// 判断当前是否在知识图谱页面
const isKnowledgeGraph = computed(() => {
  return route.path === '/theory/knowledge-graph'
})
</script>

<template>
  <div class="theory-container">
    <!-- 知识图谱页面内容 -->
    <div v-if="isKnowledgeGraph">
      <div class="knowledge-graph-placeholder">
        <h1>知识图谱</h1>
        <p class="subtitle">全国统一大市场知识图谱展示</p>
        
        <div class="content-placeholder">
          <div class="placeholder-icon">📊</div>
          <p>知识图谱内容待完善</p>
        </div>
      </div>
    </div>
    
    <!-- 理论学习页面内容 -->
    <div v-else>
      <div class="content-layout">
        <!-- 侧边栏 - 文章列表 -->
        <aside class="sidebar">
          <h2>学习目录</h2>
          <ul class="article-list">
            <li 
              v-for="article in theoryArticles" 
              :key="article.id"
              :class="{ active: selectedArticle.id === article.id }"
              @click="selectedArticle = article"
            >
              {{ article.title }}
            </li>
          </ul>
        </aside>
        
        <!-- 主内容区 - Markdown渲染 -->
        <main class="main-content">
          <MarkdownRenderer :file-path="selectedArticle.path" />
        </main>
      </div>
    </div>
  </div>
</template>

<style scoped>
.theory-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.theory-container h1 {
  color: #f44336;
  text-align: center;
  margin-bottom: 30px;
}

.content-layout {
  display: flex;
  gap: 20px;
}

.sidebar {
  flex: 0 0 250px;
  background-color: #f5f5f5;
  border-radius: 8px;
  padding: 20px;
  height: fit-content;
}

.sidebar h2 {
  margin-top: 0;
  color: #f44336;
  border-bottom: 2px solid #f44336;
  padding-bottom: 10px;
}

.article-list {
  list-style: none;
  padding: 0;
}

.article-list li {
  padding: 12px 15px;
  margin: 8px 0;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.article-list li:hover {
  background-color: #e0e0e0;
}

.article-list li.active {
  background-color: #f44336;
  color: white;
}

.main-content {
  flex: 1;
  background-color: white;
  border-radius: 8px;
  padding: 25px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.article-header h2 {
  margin-top: 0;
  color: #333;
  border-bottom: 1px solid #eee;
  padding-bottom: 15px;
}

/* 知识图谱页面样式 */
.knowledge-graph-placeholder {
  text-align: center;
}

.knowledge-graph-placeholder h1 {
  color: #f44336;
  margin-bottom: 10px;
}

.subtitle {
  color: #666;
  margin-bottom: 40px;
}

.content-placeholder {
  background-color: #f5f5f5;
  border-radius: 8px;
  padding: 60px 20px;
  margin: 40px auto;
  max-width: 500px;
}

.placeholder-icon {
  font-size: 4rem;
  margin-bottom: 20px;
}

.content-placeholder p {
  font-size: 1.2rem;
  color: #666;
  margin: 0;
}

/* 响应式适配 */
@media (max-width: 768px) {
  .content-layout {
    flex-direction: column;
  }
  
  .sidebar {
    flex: none;
  }
  
  .theory-container {
    padding: 15px;
  }
  
  .main-content {
    padding: 15px;
  }
}
</style>