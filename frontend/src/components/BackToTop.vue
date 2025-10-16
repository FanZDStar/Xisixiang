<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'

const showButton = ref(false)
let scrollContainer = null
const buttonPosition = ref({ bottom: '20px', right: '20px' })

// 检查滚动位置 - 使用节流优化性能
let throttleTimer = null
const checkScroll = () => {
  if (throttleTimer) return
  
  throttleTimer = setTimeout(() => {
    if (scrollContainer) {
      showButton.value = scrollContainer.scrollTop > 100
    }
    throttleTimer = null
  }, 100) // 100ms 节流
}

// 计算按钮位置（相对于.main-content容器的右下角） - 使用节流优化性能
let positionThrottleTimer = null
const updateButtonPosition = () => {
  if (positionThrottleTimer) return
  
  positionThrottleTimer = setTimeout(() => {
    if (scrollContainer) {
      const rect = scrollContainer.getBoundingClientRect()
      buttonPosition.value = {
        bottom: `${window.innerHeight - rect.bottom + 20}px`,
        right: `${window.innerWidth - rect.right + 20}px`
      }
    }
    positionThrottleTimer = null
  }, 100) // 100ms 节流
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
  
  if (containers.length > 0) {
    // 取最后一个容器（最可能是当前页面的）
    const container = containers[containers.length - 1]
    
    scrollContainer = container
    scrollContainer.addEventListener('scroll', checkScroll)
    
    // 计算初始按钮位置
    updateButtonPosition()
    
    // 监听窗口大小变化和滚动容器位置变化
    window.addEventListener('resize', updateButtonPosition)
    window.addEventListener('scroll', updateButtonPosition)
    
    // 检查是否有滚动内容，如果有就显示按钮
    if (container.scrollHeight > container.clientHeight) {
      checkScroll() // 检查当前滚动位置
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
      // 使用 MutationObserver 监听内容变化
      if (scrollContainer) {
        const observer = new MutationObserver(() => {
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
    <div 
      class="back-to-top" 
      v-show="showButton" 
      @click="scrollToTop"
      :style="{ bottom: buttonPosition.bottom, right: buttonPosition.right }"
    >
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
  background-image: url('/backToTop.png');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  pointer-events: all;
}

.back-to-top:hover {
  transform: translateY(-5px) scale(1.1);
}

.back-to-top:active {
  transform: translateY(-2px) scale(1.05);
  transition: all 0.1s ease;
}
</style>