<!-- frontend/src/components/MarkdownRenderer.vue -->
<script setup>
import { ref, onMounted, watch, shallowRef } from 'vue'
import { marked } from 'marked'
import DOMPurify from 'dompurify'

const props = defineProps({
  filePath: {
    type: String,
    required: true
  }
})

const renderedContent = shallowRef('') // 使用 shallowRef 提高性能
const loading = ref(false)
const error = ref(null)

// 创建内容缓存
const cache = new Map()

// 防抖函数，避免频繁切换时重复加载
let debounceTimer = null
const debounceDelay = 300

const renderMarkdown = async () => {
  if (!props.filePath) return
  
  // 清除之前的防抖定时器
  if (debounceTimer) {
    clearTimeout(debounceTimer)
  }
  
  // 设置新的防抖定时器
  debounceTimer = setTimeout(async () => {
    // 检查缓存
    if (cache.has(props.filePath)) {
      console.log('从缓存加载:', props.filePath)
      renderedContent.value = cache.get(props.filePath)
      return
    }
    
    loading.value = true
    error.value = null
    
    try {
      console.log('网络加载:', props.filePath)
      // 获取Markdown文件内容
      const response = await fetch(props.filePath)
      if (!response.ok) {
        throw new Error(`无法加载文件: ${response.status}`)
      }
      
      const markdownText = await response.text()
      
      // 解析Markdown为HTML
      const rawHtml = marked(markdownText)
      
      // 使用DOMPurify净化HTML防止XSS攻击
      const cleanHtml = DOMPurify.sanitize(rawHtml)
      
      // 存入缓存
      cache.set(props.filePath, cleanHtml)
      
      // 限制缓存大小，防止内存泄漏
      if (cache.size > 10) {
        const firstKey = cache.keys().next().value
        cache.delete(firstKey)
        console.log('缓存已满，删除最旧的缓存项:', firstKey)
      }
      
      renderedContent.value = cleanHtml
    } catch (err) {
      error.value = `加载失败: ${err.message}`
      console.error('Markdown渲染错误:', err)
    } finally {
      loading.value = false
    }
  }, debounceDelay)
}

// 监听文件路径变化
watch(() => props.filePath, renderMarkdown)

// 组件挂载时渲染
onMounted(renderMarkdown)
</script>

<template>
  <div class="markdown-container">
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <div class="markdown-content" v-html="renderedContent"></div>
    </div>
  </div>
</template>

<style scoped>
.markdown-container {
  text-align: left;
}

.loading, .error {
  padding: 20px;
  text-align: center;
}

.error {
  color: #f44336;
}

.markdown-content {
  line-height: 1.6;
  font-size: 16px;
}

.markdown-content h1,
.markdown-content h2,
.markdown-content h3 {
  margin-top: 24px;
  margin-bottom: 16px;
  font-weight: 600;
  line-height: 1.25;
}

.markdown-content h1 {
  font-size: 2em;
  border-bottom: 1px solid #eaecef;
  padding-bottom: 0.3em;
}

.markdown-content h2 {
  font-size: 1.5em;
  border-bottom: 1px solid #eaecef;
  padding-bottom: 0.3em;
}

.markdown-content h3 {
  font-size: 1.25em;
}

.markdown-content p {
  margin-top: 0;
  margin-bottom: 16px;
}

.markdown-content ul,
.markdown-content ol {
  padding-left: 2em;
  margin-top: 0;
  margin-bottom: 16px;
}

.markdown-content li {
  margin-bottom: 8px;
}

.markdown-content pre {
  background-color: #f6f8fa;
  border-radius: 6px;
  padding: 16px;
  overflow: auto;
  margin-top: 0;
  margin-bottom: 16px;
}

.markdown-content code {
  background-color: rgba(27, 31, 35, 0.05);
  border-radius: 6px;
  padding: 0.2em 0.4em;
  font-family: monospace;
}

.markdown-content pre code {
  background-color: transparent;
  padding: 0;
}

.markdown-content blockquote {
  margin: 0;
  padding: 0 1em;
  color: #6a737d;
  border-left: 0.25em solid #dfe2e5;
  margin-bottom: 16px;
}

.markdown-content table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 16px;
}

.markdown-content th,
.markdown-content td {
  padding: 6px 13px;
  border: 1px solid #dfe2e5;
}

.markdown-content th {
  background-color: #f6f8fa;
  font-weight: 600;
}

/* 响应式适配 */
@media (max-width: 768px) {
  .markdown-content {
    font-size: 14px;
    padding: 0 10px;
  }
  
  .markdown-content h1 {
    font-size: 1.5em;
  }
  
  .markdown-content h2 {
    font-size: 1.3em;
  }
  
  .markdown-content h3 {
    font-size: 1.1em;
  }
  
  .markdown-content pre {
    padding: 12px;
  }
}
</style>