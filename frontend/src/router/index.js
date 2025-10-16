// frontend/src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';

// 懒加载路由组件
const ChatView = () => import('../views/ChatView.vue');
const QuizView = () => import('../views/QuizView.vue');
const TheoryView = () => import('../views/TheoryView.vue');
const KnowledgeGraph = () => import('../views/KnowledgeGraph.vue');

const routes = [
  {
    path: '/',
    redirect: '/chat'
  },
  {
    path: '/chat',
    name: 'Chat',
    component: ChatView
  },
  {
    path: '/quiz',
    name: 'Quiz',
    component: QuizView
  },
  {
    path: '/theory',
    name: 'Theory',
    component: TheoryView,
    children: [
      {
        path: '',
        redirect: 'learning'
      },
      {
        path: 'learning',
        name: 'TheoryLearning',
        component: TheoryView
      },
      {
        path: 'knowledge-graph',
        name: 'KnowledgeGraph',
        component: KnowledgeGraph
      }
    ]
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;