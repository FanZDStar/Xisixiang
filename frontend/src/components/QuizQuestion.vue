<!-- frontend/src/components/QuizQuestion.vue -->
<script setup>
import { ref } from 'vue'

const props = defineProps({
  question: {
    type: Object,
    required: true
  },
  index: {
    type: Number,
    required: true
  },
  showAnswer: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['select-answer'])

const selectedOption = ref('')

const handleOptionSelect = (option) => {
  selectedOption.value = option
  emit('select-answer', {
    questionId: props.question.id,
    selectedOption: option
  })
}

// 判断选项状态的函数
const getOptionStatus = (option) => {
  if (!props.showAnswer) {
    // 未提交答案时，只显示选中状态
    return selectedOption.value === option ? 'selected' : 'unselected'
  } else {
    // 提交答案后，显示正确/错误状态
    const isCorrectOption = option.startsWith(props.question.answer)
    const isSelectedOption = selectedOption.value === option
    
    if (isCorrectOption && isSelectedOption) {
      // 正确且选中
      return 'correct-selected'
    } else if (isCorrectOption) {
      // 正确但未选中（这种情况在错误选择时也会显示正确答案）
      return 'correct-unselected'
    } else if (isSelectedOption) {
      // 错误且选中
      return 'incorrect'
    } else {
      // 其他情况
      return 'unselected'
    }
  }
}
</script>

<template>
  <div class="question-container">
    <h3 class="question-title">第{{ index + 1 }}题：{{ question.question }}</h3>
    <div class="options-container">
      <div 
        v-for="(option, idx) in question.options" 
        :key="idx"
        class="option-item"
        :class="getOptionStatus(option)"
        @click="handleOptionSelect(option)"
      >
        <div class="option-circle"></div>
        <div class="option-text">{{ option }}</div>
      </div>
    </div>
    <!-- 预留解析位置，避免屏幕伸缩 -->
    <div class="explanation-placeholder" :class="{ 'show': showAnswer, 'disabled': !showAnswer }">
      <div v-if="showAnswer" class="explanation-content">
        <p><strong>解析：</strong>{{ question.explanation }}</p>
      </div>
      <div v-else class="explanation-disabled">
        <p><strong>解析：</strong>提交答案后查看解析</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.question-container {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.question-title {
  margin-top: 0;
  color: #333;
  font-size: 1.1rem;
}

.options-container {
  margin: 15px 0;
}

.option-item {
  display: flex;
  align-items: center;
  padding: 12px 15px;
  margin: 8px 0;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.option-item:hover {
  background-color: #f5f5f5;
}

.option-circle {
  width: 20px;
  height: 20px;
  border: 2px solid #757575;
  border-radius: 50%;
  margin-right: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.option-text {
  flex-grow: 1;
}

/* 未选中状态 */
.option-item.unselected .option-circle {
  border-color: #757575;
}

/* 选中状态 - 蓝色中心 */
.option-item.selected .option-circle {
  border-color: #2196f3;
}

.option-item.selected .option-circle::after {
  content: '';
  width: 10px;
  height: 10px;
  background-color: #2196f3;
  border-radius: 50%;
}

/* 正确且选中 - 绿色中心 */
.option-item.correct-selected .option-circle {
  border-color: #4caf50;
}

.option-item.correct-selected .option-circle::after {
  content: '';
  width: 10px;
  height: 10px;
  background-color: #4caf50;
  border-radius: 50%;
}

/* 正确但未选中 - 绿色边框和绿色中心 */
.option-item.correct-unselected .option-circle {
  border-color: #4caf50;
}

.option-item.correct-unselected .option-circle::after {
  content: '';
  width: 10px;
  height: 10px;
  background-color: #4caf50;
  border-radius: 50%;
}

/* 错误且选中 - 红色中心 */
.option-item.incorrect .option-circle {
  border-color: #f44336;
}

.option-item.incorrect .option-circle::after {
  content: '';
  width: 10px;
  height: 10px;
  background-color: #f44336;
  border-radius: 50%;
}

/* 预留解析位置 */
.explanation-placeholder {
  min-height: 60px;
  margin-top: 15px;
  padding: 10px;
  background-color: #fafafa;
  border-left: 4px solid #f44336;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.explanation-placeholder.show {
  background-color: #ffebee;
}

.explanation-placeholder.disabled {
  background-color: #f5f5f5;
  border-left-color: #9e9e9e;
  color: #9e9e9e;
}

.explanation-content {
  opacity: 0;
  transition: opacity 0.3s ease;
}

.explanation-placeholder.show .explanation-content {
  opacity: 1;
}

.explanation-disabled {
  opacity: 1;
}


/* 移动端适配 */
@media (max-width: 768px) {
  .question-container {
    padding: 15px;
  }
  
  .question-title {
    font-size: 1rem;
  }
  
  .option-item {
    padding: 10px 12px;
    font-size: 0.9rem;
  }
  
  .option-circle {
    width: 18px;
    height: 18px;
  }
  
  .option-item.selected .option-circle::after,
  .option-item.correct-selected .option-circle::after,
  .option-item.correct-unselected .option-circle::after,
  .option-item.incorrect .option-circle::after {
    width: 8px;
    height: 8px;
  }
}
</style>