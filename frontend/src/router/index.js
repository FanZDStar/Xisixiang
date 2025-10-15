// frontend/src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import ChatView from '../views/ChatView.vue';
import QuizView from '../views/QuizView.vue';
import TheoryView from '../views/TheoryView.vue';

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
    component: TheoryView
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;