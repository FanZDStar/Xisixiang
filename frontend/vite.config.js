import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  base: '/',
  build: {
    assetsInlineLimit: 0,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['vue', 'vue-router'],
          markdown: ['marked', 'dompurify']
        }
      }
    }
  },
  server: {
    host: '0.0.0.0',
    port: 3000
  }
})