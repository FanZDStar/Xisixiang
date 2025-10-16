<!-- frontend/src/components/MessageMarkdown.vue -->
<!-- 专门用于聊天消息的轻量级 Markdown 渲染组件 -->
<script setup>
import { computed } from "vue";
import { marked } from "marked";
import DOMPurify from "dompurify";

const props = defineProps({
  content: {
    type: String,
    required: true,
  },
});

// 配置 marked 选项
marked.setOptions({
  breaks: true, // 支持 GFM 换行
  gfm: true, // 启用 GitHub Flavored Markdown
});

// 渲染并清理 HTML
const renderedContent = computed(() => {
  if (!props.content) return "";

  try {
    // 将 Markdown 转换为 HTML
    const rawHtml = marked.parse(props.content);
    // 使用 DOMPurify 清理 HTML，防止 XSS 攻击
    return DOMPurify.sanitize(rawHtml);
  } catch (error) {
    console.error("Markdown 渲染错误:", error);
    // 出错时返回纯文本
    return props.content;
  }
});
</script>

<template>
  <div class="message-markdown" v-html="renderedContent"></div>
</template>

<style scoped>
.message-markdown {
  line-height: 1.6;
  word-wrap: break-word;
}

/* 由于使用了 v-html，需要使用 :deep() 来应用样式 */
.message-markdown :deep(p) {
  margin: 0.5em 0;
}

.message-markdown :deep(p:first-child) {
  margin-top: 0;
}

.message-markdown :deep(p:last-child) {
  margin-bottom: 0;
}

.message-markdown :deep(strong) {
  color: #d32f2f;
  font-weight: 600;
}

.message-markdown :deep(em) {
  font-style: italic;
  color: #666;
}

.message-markdown :deep(ul),
.message-markdown :deep(ol) {
  margin: 0.5em 0;
  padding-left: 1.5em;
}

.message-markdown :deep(li) {
  margin: 0.3em 0;
}

.message-markdown :deep(ul) {
  list-style-type: disc;
}

.message-markdown :deep(ol) {
  list-style-type: decimal;
}

.message-markdown :deep(code) {
  background-color: #fff3e0;
  color: #e65100;
  padding: 2px 6px;
  border-radius: 3px;
  font-family: "Courier New", Consolas, Monaco, monospace;
  font-size: 0.9em;
}

.message-markdown :deep(pre) {
  background-color: #f5f5f5;
  padding: 12px;
  border-radius: 6px;
  overflow-x: auto;
  margin: 0.5em 0;
}

.message-markdown :deep(pre code) {
  background: none;
  padding: 0;
  color: inherit;
  font-size: 0.85em;
}

.message-markdown :deep(blockquote) {
  border-left: 3px solid #f44336;
  padding-left: 12px;
  margin: 0.5em 0;
  color: #666;
  font-style: italic;
}

.message-markdown :deep(h1),
.message-markdown :deep(h2),
.message-markdown :deep(h3),
.message-markdown :deep(h4),
.message-markdown :deep(h5),
.message-markdown :deep(h6) {
  color: #d32f2f;
  margin: 0.8em 0 0.4em;
  font-weight: 600;
  line-height: 1.3;
}

.message-markdown :deep(h1) {
  font-size: 1.4em;
}

.message-markdown :deep(h2) {
  font-size: 1.3em;
}

.message-markdown :deep(h3) {
  font-size: 1.2em;
}

.message-markdown :deep(h4) {
  font-size: 1.1em;
}

.message-markdown :deep(a) {
  color: #f44336;
  text-decoration: none;
  border-bottom: 1px solid #f44336;
  transition: all 0.2s ease;
}

.message-markdown :deep(a:hover) {
  color: #cc0000;
  border-bottom-color: #cc0000;
}

.message-markdown :deep(hr) {
  border: none;
  border-top: 1px solid rgba(244, 67, 54, 0.3);
  margin: 1em 0;
}

.message-markdown :deep(table) {
  border-collapse: collapse;
  width: 100%;
  margin: 0.5em 0;
  font-size: 0.9em;
}

.message-markdown :deep(th),
.message-markdown :deep(td) {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.message-markdown :deep(th) {
  background-color: #ffebee;
  color: #d32f2f;
  font-weight: 600;
}

.message-markdown :deep(tr:nth-child(even)) {
  background-color: #f9f9f9;
}

.message-markdown :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 4px;
  margin: 0.5em 0;
}
</style>
