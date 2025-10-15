<script setup>
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const showTheoryDropdown = ref(false)

// 切换理论学习中心下拉菜单显示状态
const toggleTheoryDropdown = (event) => {
  event.stopPropagation()
  showTheoryDropdown.value = !showTheoryDropdown.value
}

// 点击其他地方关闭下拉菜单
const closeDropdown = () => {
  showTheoryDropdown.value = false
}

// 监听路由变化，关闭下拉菜单
watch(() => route.path, () => {
  showTheoryDropdown.value = false
})
</script>

<template>
  <div class="app-container" @click="closeDropdown">
    <div class="content-wrapper">
      <header class="header">
        <div class="header-content">
          <h1 class="title">习思想课程作业</h1>
          <p class="subtitle">构建全国统一大市场 —— 制度创新与公平竞争治理</p>
        </div>
      </header>
      
      <nav class="navigation">
        <router-link to="/chat" class="nav-link">智能问答</router-link>
        <router-link to="/quiz" class="nav-link">习题训练</router-link>
        <div class="nav-dropdown" :class="{ active: showTheoryDropdown }">
          <div 
            class="nav-link dropdown-trigger" 
            @click.stop="toggleTheoryDropdown"
            :class="{ active: route.path.startsWith('/theory') }"
          >
            理论学习中心
            <span class="arrow" :class="{ up: showTheoryDropdown }">▼</span>
          </div>
          <div v-if="showTheoryDropdown" class="dropdown-menu" @click.stop>
            <router-link 
              to="/theory/learning" 
              class="dropdown-item"
            >
              理论学习
            </router-link>
            <router-link 
              to="/theory/knowledge-graph" 
              class="dropdown-item"
            >
              知识图谱
            </router-link>
          </div>
        </div>
      </nav>
      
      <main class="main-content">
        <router-view></router-view>
      </main>
    </div>
  </div>
</template>

<style scoped>
.app-container {
  min-height: 100vh;
  background-color: #f5f5f5;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 20px;
}

.content-wrapper {
  width: 100%;
  max-width: 1200px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
}

.header {
  background: linear-gradient(135deg, #ff4d4d, #cc0000);
  color: white;
  padding: 1rem;
  border-radius: 10px 10px 0 0;
}

.header-content {
  text-align: center;
  padding: 1rem 0;
}

.title {
  margin: 0;
  font-size: 2rem;
  font-weight: 700;
}

.subtitle {
  margin: 0.5rem 0 0;
  font-size: 1.1rem;
  opacity: 0.9;
}

.navigation {
  display: flex;
  justify-content: center;
  gap: 1rem;
  padding: 1rem;
  background-color: #ffe6e6;
  border-bottom: 2px solid #ffcccc;
  flex-wrap: wrap;
  position: relative;
  z-index: 100;
}

.nav-link {
  font-weight: 600;
  color: #cc0000;
  text-decoration: none;
  padding: 0.75rem 1.5rem;
  border-radius: 30px;
  transition: all 0.3s ease;
  background-color: white;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 5px;
  cursor: pointer;
}

.nav-link:hover {
  background-color: #ff3333;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
}

.nav-link.router-link-active {
  background-color: #ff3333;
  color: white;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.nav-dropdown {
  position: relative;
}

.nav-dropdown.active .dropdown-trigger {
  background-color: #ff3333;
  color: white;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.dropdown-trigger {
  cursor: pointer;
  user-select: none;
}

.arrow {
  font-size: 0.8rem;
  transition: transform 0.3s ease;
  margin-left: 5px;
}

.arrow.up {
  transform: rotate(180deg);
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  min-width: 150px;
  margin-top: 5px;
}

.dropdown-item {
  display: block;
  padding: 12px 20px;
  color: #333;
  text-decoration: none;
  transition: background-color 0.2s;
  border-bottom: 1px solid #f0f0f0;
}

.dropdown-item:last-child {
  border-bottom: none;
  border-radius: 0 0 8px 8px;
}

.dropdown-item:hover {
  background-color: #ffe6e6;
}

.dropdown-item.router-link-active {
  background-color: #ffcccc;
  color: #cc0000;
  font-weight: 600;
}

.main-content {
  padding: 2rem 1rem;
}

/* 移动端适配 */
@media (max-width: 768px) {
  .app-container {
    padding: 10px;
  }
  
  .content-wrapper {
    border-radius: 8px;
  }
  
  .header {
    padding: 0.5rem;
    border-radius: 8px 8px 0 0;
  }
  
  .header-content {
    padding: 0.5rem 0;
  }
  
  .title {
    font-size: 1.5rem;
  }
  
  .subtitle {
    font-size: 0.9rem;
  }
  
  .navigation {
    gap: 0.5rem;
    padding: 0.5rem;
  }
  
  .nav-link {
    padding: 0.5rem 1rem;
    font-size: 0.9rem;
  }
  
  .main-content {
    padding: 1rem 0.5rem;
  }
  
  .dropdown-menu {
    min-width: 120px;
  }
  
  .dropdown-item {
    padding: 10px 15px;
    font-size: 0.9rem;
  }
}

/* 小屏幕移动端适配 */
@media (max-width: 480px) {
  .app-container {
    padding: 5px;
  }
  
  .title {
    font-size: 1.3rem;
  }
  
  .subtitle {
    font-size: 0.8rem;
  }
  
  .navigation {
    gap: 0.3rem;
  }
  
  .nav-link {
    padding: 0.4rem 0.8rem;
    font-size: 0.8rem;
  }
}
</style>