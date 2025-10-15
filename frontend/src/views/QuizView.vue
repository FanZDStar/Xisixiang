<!-- frontend/src/views/QuizView.vue -->
<script setup>
import { ref, onMounted } from 'vue'
import apiClient from '../api/client.js'
import QuizQuestion from '../components/QuizQuestion.vue'

const questions = ref([])
const userAnswers = ref({})
const showResults = ref(false)
const loading = ref(false)
const error = ref(null)

// 获取随机题目
const fetchQuizQuestions = async () => {
  loading.value = true
  error.value = null
  try {
    const data = await apiClient.get('/api/quiz')
    questions.value = data
  } catch (err) {
    error.value = '获取题目失败，请稍后重试'
    console.error('获取题目失败:', err)
  } finally {
    loading.value = false
  }
}

// 处理用户选择答案
const handleSelectAnswer = ({ questionId, selectedOption }) => {
  userAnswers.value[questionId] = selectedOption
}

// 提交答案
const submitAnswers = () => {
  showResults.value = true
}

// 重新开始
const restartQuiz = () => {
  questions.value = []
  userAnswers.value = {}
  showResults.value = false
  fetchQuizQuestions()
}

// 计算正确答案数
const calculateCorrectAnswers = () => {
  if (!showResults.value) return 0
  let correct = 0
  questions.value.forEach(question => {
    if (userAnswers.value[question.id] && userAnswers.value[question.id].startsWith(question.answer)) {
      correct++
    }
  })
  return correct
}

// 获取鼓励语句
const getEncouragementMessage = () => {
  const correctCount = calculateCorrectAnswers()
  const totalCount = questions.value.length
  const percentage = totalCount > 0 ? (correctCount / totalCount) * 100 : 0
  
  if (percentage === 100) {
    return "太棒了！全部答对了，你真是个学霸！"
  } else if (percentage >= 80) {
    return "做得很好！继续保持，你正在进步的路上！"
  } else if (percentage >= 60) {
    return "不错哦！再努力一点就能取得更好的成绩！"
  } else if (percentage >= 40) {
    return "还有提升空间，继续加油！"
  } else {
    return "不要气馁，多练习几次一定会更好！"
  }
}

// 组件挂载时获取题目
onMounted(() => {
  fetchQuizQuestions()
})
</script>

<template>
  <div class="view-container">
    
    <!-- 加载状态 -->
    <div v-if="loading" class="loading">
      正在加载题目...
    </div>
    
    <!-- 错误信息 -->
    <div v-else-if="error" class="error">
      {{ error }}
      <button @click="fetchQuizQuestions" class="retry-btn">重新加载</button>
    </div>
    
    <!-- 题目内容 -->
    <div v-else-if="questions.length > 0">
      <div class="quiz-header">
        <h2>请选择正确答案</h2>
      </div>
      
      <!-- 固定在右上角的提交按钮 -->
      <div v-if="!showResults" class="submit-btn-container">
        <button 
          @click="submitAnswers" 
          class="submit-btn"
          :disabled="Object.keys(userAnswers).length !== questions.length"
        >
          提交答案
        </button>
      </div>
      
      <div class="progress-info">
        <p>已回答：{{ Object.keys(userAnswers).length }} / {{ questions.length }}</p>
      </div>
      
      <div class="questions-list">
        <QuizQuestion
          v-for="(question, index) in questions"
          :key="question.id"
          :question="question"
          :index="index"
          :show-answer="showResults"
          @select-answer="handleSelectAnswer"
        />
      </div>
      
      <!-- 提交后显示重新开始按钮 -->
      <div v-if="showResults" class="restart-btn-container">
        <button 
          @click="restartQuiz" 
          class="restart-btn"
        >
          重新开始
        </button>
      </div>
      
      <div v-if="showResults" class="results-summary">
        <h3>答题结果</h3>
        <p>正确率：{{ calculateCorrectAnswers() }} / {{ questions.length }}</p>
        <p>得分：{{ Math.round((calculateCorrectAnswers() / questions.length) * 100) }}分</p>
        <p class="encouragement-message">{{ getEncouragementMessage() }}</p>
      </div>
    </div>
    
    <!-- 无题目 -->
    <div v-else class="no-questions">
      暂无题目
    </div>
  </div>
</template>

<style scoped>
.view-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.view-container h1 {
  color: #f44336;
  text-align: center;
}

.quiz-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 10px;
  padding-bottom: 10px;
  border-bottom: 2px solid #f44336;
}

.quiz-header h2 {
  margin: 0;
  color: #f44336;
}

.submit-btn-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1000;
}

.submit-btn, .restart-btn, .retry-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s;
}

.submit-btn {
  background-color: #f44336;
  color: white;
}

.submit-btn:hover:not(:disabled) {
  background-color: #d32f2f;
}

.submit-btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.restart-btn, .retry-btn {
  background-color: #f44336;
  color: white;
}

.restart-btn:hover, .retry-btn:hover {
  background-color: #d32f2f;
}

.loading, .error, .no-questions {
  text-align: center;
  padding: 40px 20px;
  font-size: 1.1rem;
}

.error {
  color: #f44336;
}

.retry-btn {
  margin-top: 10px;
}

.questions-list {
  margin: 20px 0;
}

.results-summary {
  background-color: #ffebee;
  padding: 15px;
  border-radius: 8px;
  text-align: center;
  margin-top: 20px;
  border: 1px solid #f44336;
}

.results-summary h3 {
  margin-top: 0;
  color: #f44336;
}

.restart-btn-container {
  display: flex;
  justify-content: center;
  margin: 20px 0;
}

.encouragement-message {
  font-weight: bold;
  margin-top: 10px;
  color: #f44336;
}

/* 移动端适配 */
@media (max-width: 768px) {
  .view-container {
    padding: 15px;
  }
  
  .quiz-header {
    flex-direction: column;
    align-items: stretch;
  }
  
  .submit-btn, .restart-btn, .retry-btn {
    padding: 12px;
    width: 100%;
  }
  
  .progress-info {
    padding: 8px 12px;
    font-size: 0.9rem;
  }
  
  .submit-btn-container {
    position: fixed;
    top: 15px;
    right: 15px;
  }
}
</style>