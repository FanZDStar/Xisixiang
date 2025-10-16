<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'

const showButton = ref(false)
let scrollContainer = null
const buttonPosition = ref({ bottom: '20px', right: '20px' })

// 检查滚动位置
const checkScroll = () => {
  if (scrollContainer) {
    showButton.value = scrollContainer.scrollTop > 100 // 降低阈值便于测试
    console.log('ScrollTop:', scrollContainer.scrollTop, 'ShowButton:', showButton.value)
  }
}

// 计算按钮位置（相对于.main-content容器的右下角）
const updateButtonPosition = () => {
  if (scrollContainer) {
    const rect = scrollContainer.getBoundingClientRect()
    buttonPosition.value = {
      bottom: `${window.innerHeight - rect.bottom + 20}px`,
      right: `${window.innerWidth - rect.right + 20}px`
    }
    console.log('Button position updated:', buttonPosition.value)
  }
}

// 滚动到顶部
const scrollToTop = () => {
  if (scrollContainer) {
    scrollContainer.scrollTo({
      top: 0,
      behavior: 'smooth'
    })
  }
}

// 查找滚动容器
const findScrollContainer = () => {
  // 查找具有滚动条的父元素，只取第一个
  const containers = document.querySelectorAll('.main-content')
  console.log('Found containers:', containers.length)
  
  if (containers.length > 0) {
    // 取最后一个容器（最可能是当前页面的）
    const container = containers[containers.length - 1]
    console.log('Container scrollHeight:', container.scrollHeight, 'clientHeight:', container.clientHeight)
    
    scrollContainer = container
    scrollContainer.addEventListener('scroll', checkScroll)
    
    // 计算初始按钮位置
    updateButtonPosition()
    
    // 监听窗口大小变化和滚动容器位置变化
    window.addEventListener('resize', updateButtonPosition)
    window.addEventListener('scroll', updateButtonPosition)
    
    // 检查是否有滚动内容，如果有就显示按钮
    if (container.scrollHeight > container.clientHeight) {
      console.log('Container has scrollable content')
      checkScroll() // 检查当前滚动位置
    } else {
      console.log('Container has no scrollable content, but button will be available when content loads')
      // 即使现在没有滚动内容，也要监听，因为内容可能会动态加载
    }
    
    return true
  }
  return false
}

onMounted(async () => {
  // 等待DOM更新
  await nextTick()
  
  // 延迟查找容器
  setTimeout(() => {
    if (findScrollContainer()) {
      console.log('ScrollContainer found and initialized')
      
      // 使用 MutationObserver 监听内容变化
      if (scrollContainer) {
        const observer = new MutationObserver(() => {
          console.log('Content changed, rechecking scroll')
          checkScroll()
        })
        
        observer.observe(scrollContainer, {
          childList: true,
          subtree: true,
          characterData: true
        })
        
        // 定期检查滚动状态（为了处理异步内容加载）
        const interval = setInterval(() => {
          checkScroll()
        }, 1000)
        
        // 5秒后停止定期检查
        setTimeout(() => {
          clearInterval(interval)
        }, 5000)
      }
    } else {
      console.log('Failed to find scroll container')
    }
  }, 500)
})

onUnmounted(() => {
  if (scrollContainer) {
    scrollContainer.removeEventListener('scroll', checkScroll)
  }
  window.removeEventListener('resize', updateButtonPosition)
  window.removeEventListener('scroll', updateButtonPosition)
})
</script>

<template>
  <div class="back-to-top-container">
    <!-- 临时强制显示按钮用于测试位置 -->
    <div 
      class="back-to-top test-button" 
      @click="scrollToTop"
      :style="{ bottom: buttonPosition.bottom, right: buttonPosition.right }"
    >
      <span>测试</span>
    </div>
    <!-- 正常的返回顶部按钮 -->
    <div 
      class="back-to-top" 
      v-show="showButton" 
      @click="scrollToTop"
      :style="{ bottom: buttonPosition.bottom, right: buttonPosition.right }"
    >
      <span>↑</span>
    </div>
  </div>
</template>

<style scoped>
.back-to-top-container {
  position: relative;
  pointer-events: none;
  z-index: 999;
}

.back-to-top {
  position: fixed;
  width: 50px;
  height: 50px;
  background-color: #f44336;
  color: white;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  box-shadow: 0 4px 20px rgba(244, 67, 54, 0.4);
  transition: all 0.3s ease;
  pointer-events: all;
  border: 2px solid white;
}

.back-to-top:hover {
  background-color: #d32f2f;
  transform: translateY(-3px) scale(1.1);
  box-shadow: 0 6px 25px rgba(244, 67, 54, 0.6);
}

.back-to-top span {
  font-size: 22px;
  font-weight: bold;
  line-height: 1;
}

.test-button {
  background-color: #2196F3 !important;
  width: 60px !important;
  height: 30px !important;
  border-radius: 15px !important;
  transform: translateY(-40px); /* 在正常按钮上方 */
}

.test-button span {
  font-size: 12px !important;
}
</style>