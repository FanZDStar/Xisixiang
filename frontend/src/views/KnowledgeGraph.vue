<!-- frontend/src/views/KnowledgeGraph.vue -->
<script setup>
</script>

<template>
  <div class="knowledge-graph-container">
    <h1>知识图谱</h1>
    <p class="subtitle">全国统一大市场知识图谱展示</p>
    
    <div class="content-placeholder">
      <div class="placeholder-icon">📊</div>
      <p>知识图谱内容待完善</p>
    </div>
  </div>
</template>

<style scoped>
.knowledge-graph-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  text-align: center;
}

.knowledge-graph-container h1 {
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
</style>