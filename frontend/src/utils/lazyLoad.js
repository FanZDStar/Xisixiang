// 懒加载工具函数
import { defineAsyncComponent } from 'vue'

/**
 * 创建组件懒加载函数
 * @param {Function} importFn - 动态导入函数
 * @param {Object} options - 配置选项
 */
export const createLazyComponent = (importFn, options = {}) => {
  const {
    loadingComponent = null,
    errorComponent = null,
    delay = 200,
    timeout = 3000
  } = options

  return defineAsyncComponent({
    loader: importFn,
    loadingComponent,
    errorComponent,
    delay,
    timeout
  })
}

/**
 * 防抖函数
 * @param {Function} fn - 要防抖的函数
 * @param {number} delay - 延迟时间（毫秒）
 */
export const debounce = (fn, delay = 300) => {
  let timer = null
  return function (...args) {
    if (timer) clearTimeout(timer)
    timer = setTimeout(() => fn.apply(this, args), delay)
  }
}

/**
 * 节流函数
 * @param {Function} fn - 要节流的函数
 * @param {number} delay - 延迟时间（毫秒）
 */
export const throttle = (fn, delay = 100) => {
  let timer = null
  return function (...args) {
    if (timer) return
    timer = setTimeout(() => {
      fn.apply(this, args)
      timer = null
    }, delay)
  }
}

/**
 * 创建内容缓存管理器
 * @param {number} maxSize - 最大缓存大小
 */
export const createCache = (maxSize = 10) => {
  const cache = new Map()

  return {
    get(key) {
      return cache.get(key)
    },
    
    set(key, value) {
      // 如果缓存已满，删除最旧的项
      if (cache.size >= maxSize) {
        const firstKey = cache.keys().next().value
        cache.delete(firstKey)
        console.log('缓存已满，删除最旧的缓存项:', firstKey)
      }
      cache.set(key, value)
    },
    
    has(key) {
      return cache.has(key)
    },
    
    delete(key) {
      cache.delete(key)
    },
    
    clear() {
      cache.clear()
    },
    
    size() {
      return cache.size
    }
  }
}

/**
 * 预加载资源
 * @param {Array} urls - 要预加载的URL数组
 */
export const preloadResources = (urls) => {
  urls.forEach(url => {
    const link = document.createElement('link')
    link.rel = 'prefetch'
    link.href = url
    document.head.appendChild(link)
  })
}

/**
 * 图片懒加载
 * @param {HTMLElement} container - 容器元素
 * @param {Object} options - 配置选项
 */
export const createImageLazyLoader = (container, options = {}) => {
  const {
    rootMargin = '50px',
    threshold = 0.1
  } = options

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target
        const src = img.dataset.src
        if (src) {
          img.src = src
          img.removeAttribute('data-src')
          observer.unobserve(img)
        }
      }
    })
  }, {
    root: container,
    rootMargin,
    threshold
  })

  return {
    observe(img) {
      observer.observe(img)
    },
    
    disconnect() {
      observer.disconnect()
    }
  }
}