<template>
  <view class="game-page">
    <!-- 状态栏 -->
    <view class="status-bar">
      <view class="status-item">
        <text class="status-label">位置</text>
        <text class="status-value">{{ playerPosition }}/50</text>
      </view>
      <view class="status-item">
        <text class="status-label">积分</text>
        <text class="status-value">{{ totalPoints }}</text>
      </view>
      <button
        @click="rollDice"
        :disabled="isMoving || !boardData"
        class="dice-btn"
        :class="{ disabled: isMoving || !boardData }"
      >
        🎲 掷骰子
      </button>
    </view>

    <!-- 棋盘区域 -->
    <view v-if="boardData && boardData.cells" class="board-wrapper">
      <view class="board-grid">
        <view
          v-for="(cell, index) in boardData.cells"
          :key="index"
          :class="[
            'cell',
            getCellClass(cell.type),
            { current: playerPosition === index },
          ]"
          :style="getCellPosition(index)"
          :id="'cell-' + index"
        >
          <!-- 格子内容 -->
          <text class="cell-number">{{ cell.id }}</text>
          <text class="cell-name">{{ cell.name }}</text>

          <!-- 玩家棋子 -->
          <view v-if="playerPosition === index" class="player-piece">🎯</view>
        </view>
      </view>
    </view>

    <!-- 加载提示 -->
    <view v-else class="loading-container">
      <text class="loading-text">{{
        boardData ? "数据格式错误" : "加载游戏数据中..."
      }}</text>
    </view>

    <!-- 骰子动画区 -->
    <view v-if="showDice" class="dice-animation">
      <text class="dice">🎲</text>
      <text class="dice-value">{{ diceValue }}</text>
    </view>

    <!-- 事件弹窗 -->
    <view v-if="showEventModal" class="modal" @click="closeEventModal">
      <view class="event-card" @click.stop>
        <text class="event-title">{{ currentEvent.title }}</text>
        <text class="event-desc">{{ currentEvent.description }}</text>
        <text class="event-effect">
          {{ getEffectText(currentEvent) }}
        </text>
        <view
          class="event-points"
          :class="{
            positive: currentEvent.points > 0,
            negative: currentEvent.points < 0,
          }"
        >
          {{ currentEvent.points > 0 ? "+" : "" }}{{ currentEvent.points }} 分
        </view>
        <button class="confirm-btn" @click="closeEventModal">确定</button>
      </view>
    </view>

    <!-- 题目弹窗 -->
    <view v-if="showQuestionModal" class="modal">
      <view class="question-card">
        <text class="question-text">{{ currentQuestion.question }}</text>
        <view class="options">
          <button
            v-for="(option, idx) in currentQuestion.options"
            :key="idx"
            @click="selectAnswer(option)"
            :class="['option-btn', { selected: selectedOption === option }]"
          >
            {{ option }}
          </button>
        </view>
        <button
          class="submit-btn"
          @click="submitAnswer"
          :disabled="!selectedOption"
        >
          提交答案
        </button>
      </view>
    </view>

    <!-- 通关弹窗 -->
    <view v-if="gameWon" class="modal">
      <view class="win-card">
        <text class="win-title">🎉 恭喜通关！</text>
        <text class="win-desc">全国统一大市场建设完成！</text>
        <view class="final-score">
          <text class="score-label">最终得分</text>
          <text class="score-value">{{ totalPoints }}</text>
        </view>
        <button class="restart-btn" @click="restartGame">再玩一次</button>
      </view>
    </view>

    <!-- 自定义 Toast -->
    <CustomToast ref="toastRef" />
  </view>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { onShow } from "@dcloudio/uni-app";
import CustomToast from "@/components/CustomToast.vue";

// 页面显示时更新 TabBar
onShow(() => {
  uni.$emit("updateTabBar");
});

// 游戏状态
const playerPosition = ref(0);
const totalPoints = ref(0);
const diceValue = ref(0);
const isMoving = ref(false);
const showDice = ref(false);
const showEventModal = ref(false);
const showQuestionModal = ref(false);
const gameWon = ref(false);

const boardData = ref(null);
const questionsData = ref(null);
const currentEvent = ref(null);
const currentQuestion = ref(null);
const selectedOption = ref("");
const skipNext = ref(false); // 是否跳过下一题

// 自定义 Toast 引用
const toastRef = ref(null);

// 加载游戏数据
onMounted(async () => {
  try {
    uni.showLoading({
      title: "加载中...",
      mask: true,
    });

    // 加载棋盘配置
    const boardRes = await new Promise((resolve, reject) => {
      uni.request({
        url: "https://xisixiang.nuyoahming.xyz/static/game/board-config.json",
        method: "GET",
        success: (res) => {
          console.log("棋盘数据加载结果:", res);
          if (res.statusCode === 200) {
            resolve(res.data);
          } else {
            reject(new Error("Failed to load board config"));
          }
        },
        fail: (err) => {
          console.error("棋盘数据加载失败:", err);
          reject(err);
        },
      });
    });
    boardData.value = boardRes;
    console.log("棋盘数据:", boardData.value);

    // 加载题目数据
    const questionsRes = await new Promise((resolve, reject) => {
      uni.request({
        url: "https://xisixiang.nuyoahming.xyz/static/game/questions-categorized.json",
        method: "GET",
        success: (res) => {
          console.log("题目数据加载结果:", res);
          if (res.statusCode === 200) {
            resolve(res.data);
          } else {
            reject(new Error("Failed to load questions"));
          }
        },
        fail: (err) => {
          console.error("题目数据加载失败:", err);
          reject(err);
        },
      });
    });
    questionsData.value = questionsRes;
    console.log("题目数据条数:", questionsData.value?.length);

    uni.hideLoading();

    toastRef.value?.show("游戏加载成功", "success", 1500);
  } catch (error) {
    uni.hideLoading();
    console.error("加载游戏数据失败:", error);
    uni.showModal({
      title: "加载失败",
      content: "游戏数据加载失败，请检查网络后重试",
      showCancel: false,
    });
  }
});

// 掷骰子
function rollDice() {
  if (isMoving.value || !boardData.value) return;

  isMoving.value = true;
  showDice.value = true;

  // 震动反馈
  uni.vibrateShort({ type: "medium" });

  // 最终点数
  const finalValue = Math.floor(Math.random() * 6) + 1;

  // 数字快速跳动效果（模拟骰子滚动）
  let count = 0;
  const rollInterval = setInterval(() => {
    diceValue.value = Math.floor(Math.random() * 6) + 1;
    count++;

    // 跳动15次后停止
    if (count >= 15) {
      clearInterval(rollInterval);
      diceValue.value = finalValue;

      // 最终结果震动反馈
      setTimeout(() => {
        uni.vibrateShort({ type: "heavy" });
      }, 100);

      // 1.5秒后开始移动
      setTimeout(() => {
        showDice.value = false;
        movePlayer(finalValue);
      }, 1500);
    }
  }, 80); // 每80ms变化一次数字
}

// 移动玩家
function movePlayer(steps) {
  // 逐步移动动画
  let currentStep = 0;
  const interval = setInterval(() => {
    if (currentStep < steps && playerPosition.value < 50) {
      playerPosition.value++;
      currentStep++;

      // 播放移动音效（可选）
      // uni.vibrateShort({ type: "light" });
    } else {
      clearInterval(interval);

      // 检查是否通关
      if (playerPosition.value === 50) {
        setTimeout(() => {
          handleWin();
        }, 500);
        return;
      }

      // 触发格子事件
      setTimeout(() => {
        handleCellEvent();
      }, 500);
    }
  }, 400); // 每400ms移动一格
}

// 处理格子事件
function handleCellEvent() {
  const cell = boardData.value.cells[playerPosition.value];

  if (["blue", "green", "yellow", "red"].includes(cell.type)) {
    // 检查是否跳过
    if (skipNext.value) {
      skipNext.value = false;
      toastRef.value?.show("✨ 免答一题", "info", 2000);
      isMoving.value = false;
    } else {
      // 问答题
      showQuestion(cell.type);
    }
  } else if (cell.type === "fortune") {
    // 机遇格
    showFortuneEvent();
  } else if (cell.type === "challenge") {
    // 挑战格
    showChallengeEvent();
  } else {
    isMoving.value = false;
  }
}

// 显示问答题
function showQuestion(category) {
  const categoryQuestions = questionsData.value.filter(
    (q) => q.category === category
  );

  if (categoryQuestions.length === 0) {
    // 如果没有对应分类的题目，从所有题目中随机选择
    const allQuestions = questionsData.value;
    const randomQuestion =
      allQuestions[Math.floor(Math.random() * allQuestions.length)];
    currentQuestion.value = randomQuestion;
  } else {
    const randomQuestion =
      categoryQuestions[Math.floor(Math.random() * categoryQuestions.length)];
    currentQuestion.value = randomQuestion;
  }

  showQuestionModal.value = true;
}

// 选择答案
function selectAnswer(option) {
  selectedOption.value = option;
}

// 提交答案
function submitAnswer() {
  const isCorrect = selectedOption.value.startsWith(
    currentQuestion.value.answer
  );

  if (isCorrect) {
    totalPoints.value += 50;
    toastRef.value?.show("回答正确！+50分", "success", 2000);
  } else {
    totalPoints.value = Math.max(0, totalPoints.value - 20);
    toastRef.value?.show("回答错误！-20分", "error", 2000);

    // 显示正确答案
    setTimeout(() => {
      uni.showModal({
        title: "正确答案",
        content: `${currentQuestion.value.answer}\n\n${currentQuestion.value.explanation}`,
        showCancel: false,
      });
    }, 1500);
  }

  showQuestionModal.value = false;
  selectedOption.value = "";
  isMoving.value = false;
}

// 显示机遇事件
function showFortuneEvent() {
  const events = boardData.value.fortuneEvents;
  const randomEvent = events[Math.floor(Math.random() * events.length)];

  currentEvent.value = randomEvent;
  showEventModal.value = true;

  totalPoints.value += randomEvent.points;
}

// 显示挑战事件
function showChallengeEvent() {
  const events = boardData.value.challengeEvents;
  const randomEvent = events[Math.floor(Math.random() * events.length)];

  currentEvent.value = randomEvent;
  showEventModal.value = true;

  totalPoints.value = Math.max(0, totalPoints.value + randomEvent.points);
}

// 关闭事件弹窗
function closeEventModal() {
  showEventModal.value = false;

  // 根据事件效果执行操作
  const event = currentEvent.value;

  if (event.effect === "forward") {
    // 前进
    setTimeout(() => {
      movePlayer(event.value);
    }, 500);
  } else if (event.effect === "backward") {
    // 后退（逐格后退动画）
    const backSteps = event.value;
    let currentStep = 0;
    const interval = setInterval(() => {
      if (currentStep < backSteps && playerPosition.value > 0) {
        playerPosition.value--;
        currentStep++;
      } else {
        clearInterval(interval);
        isMoving.value = false;
      }
    }, 400);
  } else if (event.effect === "skip") {
    // 免答下一题
    skipNext.value = true;
    isMoving.value = false;
  } else {
    // 其他效果（如仅加减分）
    isMoving.value = false;
  }
}

// 处理通关
function handleWin() {
  gameWon.value = true;
  isMoving.value = false;

  toastRef.value?.show("🎉 恭喜通关！", "success", 2000);

  // 震动反馈
  uni.vibrateShort({
    type: "heavy",
  });
}

// 重新开始
function restartGame() {
  playerPosition.value = 0;
  totalPoints.value = 0;
  diceValue.value = 0;
  gameWon.value = false;
  isMoving.value = false;
  skipNext.value = false;
}

// 获取格子样式类
function getCellClass(type) {
  const classMap = {
    start: "cell-start",
    end: "cell-end",
    blue: "cell-blue",
    green: "cell-green",
    yellow: "cell-yellow",
    red: "cell-red",
    fortune: "cell-fortune",
    challenge: "cell-challenge",
  };
  return classMap[type] || "";
}

// 计算格子位置（回字形布局）
function getCellPosition(index) {
  const cellSize = 65; // 格子大小 (rpx)
  const gap = 5; // 格子间距 (rpx)
  const step = cellSize + gap;

  // 回字形布局（根据实际路径）
  // 外圈：0-30 (31个格子)
  // 内圈：31-50 (20个格子)

  let left = 0;
  let top = 0;

  // 外圈路径
  if (index === 0) {
    // 起点：左下角
    left = 0;
    top = 7 * step;
  } else if (index >= 1 && index <= 9) {
    // 底边：1-9 (从左到右)
    left = index * step;
    top = 7 * step;
  } else if (index >= 10 && index <= 16) {
    // 右边：10-16 (从下到上)
    left = 9 * step;
    top = (7 - (index - 9)) * step;
  } else if (index >= 17 && index <= 25) {
    // 顶边：17-25 (从右到左)
    left = (9 - (index - 16)) * step;
    top = 0;
  } else if (index >= 26 && index <= 31) {
    // 左边：26-31 (从上到下，但不包括最底部，因为0已经占据)
    left = 0;
    top = (index - 25) * step;
  }
  // 内圈路径
  else if (index >= 32 && index <= 39) {
    // 内圈底边：32-39 (从左到右，第1-8列)
    left = (index - 31) * step;
    top = 6 * step;
  } else if (index === 40) {
    // 特殊处理40号：内圈底边转角
    left = 8 * step;
    top = 6 * step;
  } else if (index >= 41 && index <= 45) {
    // 内圈右边：41-45 (从下到上)
    left = 8 * step;
    top = (6 - (index - 40)) * step;
  } else if (index >= 46 && index <= 49) {
    // 内圈顶边：46-49 (从右到左)
    left = (8 - (index - 45)) * step;
    top = step;
  } else if (index === 50) {
    // 终点：中心位置
    left = 4.5 * step;
    top = 3.5 * step;
  }

  return {
    left: `${left}rpx`,
    top: `${top}rpx`,
  };
} // 获取效果文本
function getEffectText(event) {
  const effectMap = {
    forward: `前进 ${event.value} 步`,
    backward: `后退 ${event.value} 步`,
    skip: `免答下一题`,
    pause: `暂停一回合`,
    points: event.points > 0 ? "获得积分" : "扣除积分",
  };
  return effectMap[event.effect] || "";
}
</script>

<style scoped>
.game-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
  padding-bottom: 200rpx; /* 增加底部内边距，避免被 TabBar 遮挡 */
}

.status-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 30rpx;
  background: white;
  margin: 20rpx;
  border-radius: 20rpx;
  box-shadow: 0 4rpx 15rpx rgba(0, 0, 0, 0.1);
}

.status-item {
  padding-left: 90rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.status-label {
  font-size: 24rpx;
  color: #666;
  margin-bottom: 5rpx;
}

.status-value {
  font-size: 32rpx;
  font-weight: bold;
  color: #ff4d4d;
}

.dice-btn {
  padding: 15rpx 35rpx;
  background: linear-gradient(135deg, #ff4d4d, #cc0000);
  color: white;
  border: none;
  border-radius: 30rpx;
  font-size: 28rpx;
  box-shadow: 0 4rpx 10rpx rgba(255, 77, 77, 0.3);
}

.dice-btn.disabled {
  opacity: 0.5;
  box-shadow: none;
}

.dice-btn::after {
  border: none;
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 400rpx;
}

.loading-text {
  font-size: 28rpx;
  color: #999;
}

.board-wrapper {
  margin: 20rpx;
  padding: 20rpx;
  background: white;
  border-radius: 20rpx;
  box-shadow: 0 4rpx 15rpx rgba(0, 0, 0, 0.1);
  overflow-x: auto;
}

.board-grid {
  position: relative;
  width: 700rpx; /* 10 * (65 + 5) = 700 */
  height: 560rpx; /* 8 * (65 + 5) = 560 */
  margin: 0 auto;
}

.cell {
  width: 65rpx;
  height: 65rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-radius: 10rpx;
  border: 2rpx solid #ddd;
  position: absolute;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.cell.current {
  transform: scale(1.15);
  box-shadow: 0 8rpx 20rpx rgba(255, 77, 77, 0.4);
  z-index: 10;
}

.cell-blue {
  background: #4a90e2;
  color: white;
}
.cell-green {
  background: #50c878;
  color: white;
}
.cell-yellow {
  background: #ffd700;
  color: #333;
}
.cell-red {
  background: #ff4d4d;
  color: white;
}
.cell-fortune {
  background: linear-gradient(135deg, #ffd700, #ffed4e);
  color: #333;
}
.cell-challenge {
  background: #999;
  color: white;
}
.cell-start {
  background: linear-gradient(135deg, #ff4d4d, #cc0000);
  color: white;
}
.cell-end {
  background: linear-gradient(135deg, #ffd700, #ff8c00);
  color: white;
}

.cell-number {
  font-size: 18rpx;
  font-weight: bold;
}

.cell-name {
  font-size: 16rpx;
  text-align: center;
  margin-top: 2rpx;
  line-height: 1.1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 60rpx;
}

.player-piece {
  position: absolute;
  top: -22rpx;
  font-size: 40rpx;
  animation: bounce 0.5s infinite;
  filter: drop-shadow(0 4rpx 8rpx rgba(0, 0, 0, 0.3));
}

@keyframes bounce {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10rpx);
  }
}

.dice-animation {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  background: white;
  padding: 60rpx;
  border-radius: 30rpx;
  box-shadow: 0 10rpx 40rpx rgba(0, 0, 0, 0.3);
  z-index: 999;
  animation: dicePopIn 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.dice {
  font-size: 120rpx;
  animation: diceRotate 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55) infinite;
  display: inline-block;
}

.dice-value {
  font-size: 80rpx;
  font-weight: bold;
  color: #ff4d4d;
  margin-top: 20rpx;
  animation: numberPulse 0.3s ease-in-out;
  text-shadow: 0 2rpx 8rpx rgba(255, 77, 77, 0.3);
}

/* 骰子容器弹出动画 */
@keyframes dicePopIn {
  0% {
    transform: translate(-50%, -50%) scale(0.3);
    opacity: 0;
  }
  50% {
    transform: translate(-50%, -50%) scale(1.1);
  }
  100% {
    transform: translate(-50%, -50%) scale(1);
    opacity: 1;
  }
}

/* 骰子旋转翻滚动画 */
@keyframes diceRotate {
  0% {
    transform: rotate(0deg) rotateY(0deg);
  }
  25% {
    transform: rotate(90deg) rotateY(90deg);
  }
  50% {
    transform: rotate(180deg) rotateY(180deg);
  }
  75% {
    transform: rotate(270deg) rotateY(270deg);
  }
  100% {
    transform: rotate(360deg) rotateY(360deg);
  }
}

/* 数字脉冲动画 */
@keyframes numberPulse {
  0% {
    transform: scale(0.8);
    opacity: 0;
  }
  50% {
    transform: scale(1.2);
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.event-card,
.question-card,
.win-card {
  width: 600rpx;
  background: white;
  border-radius: 30rpx;
  padding: 50rpx;
  animation: slideIn 0.3s ease-out;
  max-height: 80vh;
  overflow-y: auto;
}

@keyframes slideIn {
  from {
    transform: translateY(-50rpx);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.event-title {
  display: block;
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 30rpx;
  text-align: center;
}

.event-desc {
  display: block;
  font-size: 28rpx;
  color: #666;
  line-height: 1.6;
  margin-bottom: 30rpx;
  text-align: center;
}

.event-effect {
  display: block;
  font-size: 26rpx;
  color: #999;
  margin-bottom: 20rpx;
  text-align: center;
}

.event-points {
  display: block;
  font-size: 48rpx;
  font-weight: bold;
  text-align: center;
  margin-bottom: 30rpx;
}

.event-points.positive {
  color: #50c878;
}

.event-points.negative {
  color: #ff4d4d;
}

.confirm-btn,
.restart-btn {
  width: 100%;
  padding: 25rpx;
  background: linear-gradient(135deg, #ff4d4d, #cc0000);
  color: white;
  border: none;
  border-radius: 30rpx;
  font-size: 30rpx;
  margin-top: 20rpx;
}

.confirm-btn::after,
.restart-btn::after {
  border: none;
}

.question-text {
  display: block;
  font-size: 30rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 30rpx;
  line-height: 1.6;
}

.options {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
  margin-bottom: 30rpx;
}

.option-btn {
  padding: 25rpx;
  background: #f5f5f5;
  border: 2rpx solid #ddd;
  border-radius: 15rpx;
  font-size: 26rpx;
  color: #333;
  text-align: left;
  transition: all 0.3s;
}

.option-btn::after {
  border: none;
}

.option-btn.selected {
  background: linear-gradient(135deg, #ff4d4d, #cc0000);
  color: white;
  border-color: #ff4d4d;
  transform: scale(1.02);
}

.submit-btn {
  width: 100%;
  padding: 25rpx;
  background: linear-gradient(135deg, #ff4d4d, #cc0000);
  color: white;
  border: none;
  border-radius: 30rpx;
  font-size: 30rpx;
}

.submit-btn[disabled] {
  opacity: 0.5;
}

.submit-btn::after {
  border: none;
}

.win-title {
  display: block;
  font-size: 48rpx;
  font-weight: bold;
  color: #ff4d4d;
  margin-bottom: 20rpx;
  text-align: center;
}

.win-desc {
  display: block;
  font-size: 28rpx;
  color: #666;
  margin-bottom: 40rpx;
  text-align: center;
}

.final-score {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40rpx;
  background: linear-gradient(135deg, #fff5f5, #ffe8e8);
  border-radius: 20rpx;
  margin-bottom: 30rpx;
}

.score-label {
  font-size: 26rpx;
  color: #999;
  margin-bottom: 10rpx;
}

.score-value {
  font-size: 64rpx;
  font-weight: bold;
  color: #ff4d4d;
}
</style>
