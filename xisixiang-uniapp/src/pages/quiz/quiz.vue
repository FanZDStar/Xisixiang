<template>
  <view class="quiz-page">
    <!-- 自定义 TabBar -->
    <custom-tab-bar />

    <!-- 加载状态 -->
    <view v-if="loading" class="loading-container">
      <view class="loading-spinner"></view>
      <text class="loading-text">正在加载题目...</text>
    </view>

    <!-- 题目内容 -->
    <view v-else-if="questions.length > 0" class="quiz-content">
      <!-- 进度指示器 -->
      <view class="progress-bar">
        <view class="progress-fill" :style="{ width: progressWidth }"></view>
      </view>

      <!-- 题目卡片 -->
      <view class="question-card">
        <view class="question-header">
          <text class="question-number"
            >题目 {{ currentIndex + 1 }} / {{ questions.length }}</text
          >
          <text class="score-badge"
            >得分: {{ score }} / {{ currentIndex }}</text
          >
        </view>

        <view class="question-text">
          {{ currentQuestion.question }}
        </view>

        <!-- 选项列表 -->
        <view class="options">
          <view
            v-for="(option, idx) in currentQuestion.options"
            :key="idx"
            @click="selectOption(option)"
            :class="[
              'option',
              {
                selected: selectedOption === option && !submitted,
                correct: submitted && isCorrectOption(option),
                wrong:
                  submitted &&
                  selectedOption === option &&
                  !isCorrectOption(option),
                disabled: submitted,
              },
            ]"
          >
            <view class="option-marker">
              <text v-if="!submitted">{{ getOptionLetter(idx) }}</text>
              <text v-else-if="isCorrectOption(option)">✓</text>
              <text v-else-if="selectedOption === option">✗</text>
              <text v-else>{{ getOptionLetter(idx) }}</text>
            </view>
            <text class="option-text">{{ option }}</text>
          </view>
        </view>

        <!-- 解析区域 - 预留固定位置 -->
        <view 
          :class="[
            'explanation-card',
            { 'disabled-explanation': !submitted }
          ]"
        >
          <view class="explanation-header">
            <text class="icon">💡</text>
            <text class="title">答案解析</text>
          </view>
          <text v-if="submitted" class="explanation-text">{{
            currentQuestion.explanation
          }}</text>
          <text v-else class="explanation-placeholder">
            提交答案后查看解析
          </text>
        </view>

        <!-- 操作按钮 -->
        <view class="actions">
          <button
            v-if="!submitted"
            @click="submitAnswer"
            :disabled="!selectedOption"
            class="action-btn submit-btn"
            :class="{ disabled: !selectedOption }"
          >
            提交答案
          </button>
          <button v-else @click="nextQuestion" class="action-btn next-btn">
            {{ currentIndex < questions.length - 1 ? "下一题 →" : "查看结果" }}
          </button>
        </view>
      </view>
    </view>

    <!-- 空状态 -->
    <view v-else class="empty-state">
      <text class="empty-icon">📝</text>
      <text class="empty-text">暂无题目</text>
      <button @click="loadQuestions" class="retry-btn">重新加载</button>
    </view>
  </view>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { onShow } from "@dcloudio/uni-app";
import { getRandomQuiz } from "../utils/request.js";

// 页面显示时更新 TabBar 状态
onShow(() => {
  uni.$emit("updateTabBar");
});

const questions = ref([]);
const currentIndex = ref(0);
const selectedOption = ref("");
const submitted = ref(false);
const loading = ref(true);
const score = ref(0);

const currentQuestion = computed(
  () => questions.value[currentIndex.value] || {}
);

const progressWidth = computed(() => {
  if (questions.value.length === 0) return "0%";
  return ((currentIndex.value + 1) / questions.value.length) * 100 + "%";
});

onMounted(() => {
  loadQuestions();
});

const loadQuestions = async () => {
  loading.value = true;
  try {
    const data = await getRandomQuiz();
    questions.value = data;
  } catch (error) {
    console.error("Load questions error:", error);
    uni.showToast({
      title: "加载失败，请重试",
      icon: "none",
      duration: 2000,
    });
  } finally {
    loading.value = false;
  }
};

const selectOption = (option) => {
  if (!submitted.value) {
    selectedOption.value = option;
  }
};

const isCorrectOption = (option) => {
  return option.startsWith(currentQuestion.value.answer);
};

const getOptionLetter = (index) => {
  return String.fromCharCode(65 + index); // A, B, C, D
};

const submitAnswer = () => {
  if (!selectedOption.value) return;

  submitted.value = true;
  if (isCorrectOption(selectedOption.value)) {
    score.value++;
    uni.showToast({
      title: "回答正确！🎉",
      icon: "success",
      duration: 1500,
    });
  } else {
    uni.showToast({
      title: "回答错误",
      icon: "none",
      duration: 1500,
    });
  }
};

const nextQuestion = () => {
  if (currentIndex.value < questions.value.length - 1) {
    currentIndex.value++;
    selectedOption.value = "";
    submitted.value = false;
  } else {
    showResult();
  }
};

const showResult = () => {
  const percentage = Math.round((score.value / questions.value.length) * 100);
  let message = "";
  
  // 根据正确率显示不同鼓励语句
  if (percentage === 100) {
    message = "太棒了！全部答对了，你真是个学霸！";
  } else if (percentage >= 80) {
    message = "做得很好！继续保持，你正在进步的路上！";
  } else if (percentage >= 60) {
    message = "不错哦！再努力一点就能取得更好的成绩！";
  } else if (percentage >= 40) {
    message = "还有提升空间，继续加油！";
  } else {
    message = "不要气馁，多练习几次一定会更好！";
  }

  uni.showModal({
    title: "测试完成",
    content: `您的得分：${score.value} / ${questions.value.length}\n正确率：${percentage}%\n\n${message}`,
    showCancel: true,
    cancelText: "结束",
    confirmText: "再来一次",
    success: (res) => {
      if (res.confirm) {
        // 重新开始
        currentIndex.value = 0;
        selectedOption.value = "";
        submitted.value = false;
        score.value = 0;
        loadQuestions();
      } else {
        // 返回首页
        uni.switchTab({
          url: "/pages/chat/chat",
        });
      }
    },
  });
};
</script>

<style scoped>
.quiz-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #fff5f5, #f5f5f5);
  padding-bottom: 120rpx; /* 为自定义 TabBar 预留空间 */
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
}

.loading-spinner {
  width: 80rpx;
  height: 80rpx;
  border: 6rpx solid #ffcccc;
  border-top-color: #ff4d4d;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.loading-text {
  margin-top: 30rpx;
  color: #999;
  font-size: 28rpx;
}

.quiz-content {
  padding: 20rpx;
}

.progress-bar {
  height: 8rpx;
  background-color: #ffcccc;
  border-radius: 10rpx;
  overflow: hidden;
  margin-bottom: 30rpx;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #ff4d4d, #cc0000);
  transition: width 0.3s ease;
}

.question-card {
  background-color: white;
  border-radius: 30rpx;
  padding: 40rpx;
  box-shadow: 0 8rpx 30rpx rgba(255, 77, 77, 0.1);
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40rpx;
}

.question-number {
  color: #ff4d4d;
  font-weight: bold;
  font-size: 28rpx;
}

.score-badge {
  background: linear-gradient(135deg, #ff4d4d, #cc0000);
  color: white;
  padding: 10rpx 20rpx;
  border-radius: 20rpx;
  font-size: 24rpx;
}

.question-text {
  font-size: 32rpx;
  line-height: 1.8;
  margin-bottom: 40rpx;
  color: #333;
  font-weight: 500;
}

.options {
  margin-bottom: 30rpx;
}

.option {
  display: flex;
  align-items: center;
  padding: 25rpx;
  margin-bottom: 20rpx;
  border: 3rpx solid #eee;
  border-radius: 20rpx;
  background-color: #fff;
  transition: all 0.3s;
}

.option:active {
  transform: scale(0.98);
}

.option.selected {
  border-color: #ff4d4d;
  background-color: #fff5f5;
}

.option.correct {
  border-color: #4caf50;
  background-color: #e8f5e9;
}

.option.wrong {
  border-color: #f44336;
  background-color: #ffebee;
}

.option.disabled {
  cursor: not-allowed;
}

.option-marker {
  width: 50rpx;
  height: 50rpx;
  margin-right: 20rpx;
  border-radius: 50%;
  background-color: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 28rpx;
  flex-shrink: 0;
}

.option.selected .option-marker {
  background: linear-gradient(135deg, #ff4d4d, #cc0000);
  color: white;
}

.option.correct .option-marker {
  background-color: #4caf50;
  color: white;
}

.option.wrong .option-marker {
  background-color: #f44336;
  color: white;
}

.option-text {
  flex: 1;
  font-size: 28rpx;
  line-height: 1.6;
  color: #333;
}

.explanation-card {
  min-height: 180rpx; /* 预留固定高度避免页面跳动 */
  padding: 30rpx;
  background: linear-gradient(135deg, #fff3e0, #ffe8cc);
  border-radius: 20rpx;
  margin-bottom: 30rpx;
  transition: all 0.3s ease;
}

.explanation-card.disabled-explanation {
  background: #f5f5f5;
  opacity: 0.7;
}

.explanation-header {
  display: flex;
  align-items: center;
  margin-bottom: 15rpx;
}

.explanation-header .icon {
  font-size: 32rpx;
  margin-right: 10rpx;
}

.explanation-header .title {
  color: #ff6f00;
  font-weight: bold;
  font-size: 28rpx;
}

.explanation-text {
  color: #666;
  line-height: 1.8;
  font-size: 26rpx;
}

.explanation-placeholder {
  color: #999;
  line-height: 1.8;
  font-size: 26rpx;
  font-style: italic;
}

.actions {
  margin-top: 20rpx;
}

.action-btn {
  width: 100%;
  height: 90rpx;
  border-radius: 45rpx;
  font-size: 32rpx;
  font-weight: bold;
  border: none;
}

.action-btn::after {
  border: none;
}

.submit-btn {
  background: linear-gradient(135deg, #ff4d4d, #cc0000);
  color: white;
}

.submit-btn.disabled {
  background: #ccc;
  opacity: 0.6;
}

.next-btn {
  background: linear-gradient(135deg, #4caf50, #388e3c);
  color: white;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
}

.empty-icon {
  font-size: 120rpx;
  margin-bottom: 30rpx;
}

.empty-text {
  color: #999;
  font-size: 32rpx;
  margin-bottom: 40rpx;
}

.retry-btn {
  background: linear-gradient(135deg, #ff4d4d, #cc0000);
  color: white;
  border: none;
  padding: 20rpx 60rpx;
  border-radius: 40rpx;
}
</style>