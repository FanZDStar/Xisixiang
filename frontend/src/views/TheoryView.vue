<script setup>
import { ref, computed } from "vue";
import { useRoute } from "vue-router";
import MarkdownRenderer from "../components/MarkdownRenderer.vue";
import KnowledgeGraph from "./KnowledgeGraph.vue";
import BackToTop from "../components/BackToTop.vue";

const route = useRoute();

// 添加控制目录折叠状态的响应式变量
const isSidebarCollapsed = ref(false);

// 理论文章列表
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
]);

const selectedArticle = ref(theoryArticles.value[0]);

// 判断当前是否在知识图谱页面
const isKnowledgeGraph = computed(() => {
  return route.path === "/theory/knowledge-graph";
});

// 切换侧边栏折叠状态
const toggleSidebar = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value;
};

// 添加截取标题的函数，最多显示12个字
const truncateTitle = (title, maxLength = 12) => {
  if (!title) return '';
  return title.length > maxLength ? title.substring(0, maxLength) + '...' : title;
};
</script>

<template>
  <div class="theory-container">
    <!-- 知识图谱页面内容 -->
    <div v-if="isKnowledgeGraph">
      <KnowledgeGraph />
    </div>

    <!-- 理论学习页面内容 -->
    <div v-else>
      <div class="content-layout">
        <!-- 侧边栏 - 文章列表 -->
        <aside class="sidebar" :class="{ collapsed: isSidebarCollapsed }">
          <h2 @click="toggleSidebar">
            {{ isSidebarCollapsed ? '▶' : '▼' }} 学习目录
          </h2>
          <ul class="article-list" v-show="!isSidebarCollapsed">
            <li
              v-for="article in theoryArticles"
              :key="article.id"
              :class="{ active: selectedArticle.id === article.id }"
              @click="selectedArticle = article"
            >
              {{ truncateTitle(article.title) }}
            </li>
          </ul>
        </aside>

        <!-- 主内容区 - Markdown渲染 -->
        <main class="main-content">
          <MarkdownRenderer :file-path="selectedArticle.path" />
          <!-- 返回顶部组件 -->
          <BackToTop />
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
  transition: all 0.3s ease;
}

/* 折叠状态样式 */
.sidebar.collapsed {
  flex: 0 0 50px;
}

.sidebar h2 {
  margin-top: 0;
  color: #f44336;
  border-bottom: 2px solid #f44336;
  padding-bottom: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  user-select: none;
}

.sidebar.collapsed h2 {
  justify-content: center;
  border-bottom: none;
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
  /* 添加单行显示和省略号效果 */
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
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
  max-height: 60vh;
  overflow-y: auto;
  position: relative; /* 为返回顶部组件提供定位上下文 */
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
    max-height: 55vh;
  }
  
  /* 在移动端保持折叠功能 */
  .sidebar.collapsed {
    flex: none;
    height: 50px;
    padding: 10px 20px;
  }
}
</style>