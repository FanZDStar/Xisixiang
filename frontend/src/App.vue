<script setup>
// 不再需要导入 HelloWorld 组件
</script>

<template>
  <div class="app-container">
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
        <router-link to="/theory" class="nav-link">理论学习中心</router-link>
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