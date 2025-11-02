# 市场建设大富翁 - 实现计划

## 📋 项目概述

**游戏名称：** 市场建设大富翁  
**游戏类型：** 单人棋盘冒险类  
**主题：** 构建全国统一大市场  
**平台：** Web 版 + 小程序版  
**开发周期：** 预计 5-7 天

---

## 🎯 游戏设计核心

### 游戏目标

玩家从"起点"出发，通过掷骰子前进，完成各类任务，最终到达"全国统一大市场建成"终点。

### 核心机制

- **棋盘系统：** 50 个格子，环形或线性路径
- **掷骰子：** 1-6 点随机数，控制前进步数
- **格子事件：** 踩到不同颜色格子触发不同事件
- **积分系统：** 完成任务获得积分，显示在界面上
- **问答题库：** 复用现有 `question.json` 数据
- **通关条件：** 到达终点格子即可通关

---

## 📐 游戏设计详细规划

### 1. 棋盘布局设计（50 格）

#### 格子类型分布

| 格子类型      | 颜色 | 数量 | 触发事件                 | 主题           |
| ------------- | ---- | ---- | ------------------------ | -------------- |
| 🟦 **制度格** | 蓝色 | 12   | 回答选择题（制度规则类） | 市场制度统一   |
| 🟩 **设施格** | 绿色 | 12   | 回答选择题（基础设施类） | 市场设施联通   |
| 🟨 **要素格** | 黄色 | 10   | 回答选择题（要素市场类） | 要素市场化配置 |
| 🟥 **监管格** | 红色 | 8    | 回答选择题（监管执法类） | 监管与服务统一 |
| ⭐ **机遇格** | 金色 | 5    | 随机事件（正面）         | 政策支持       |
| ⚠️ **挑战格** | 灰色 | 3    | 随机事件（负面）         | 遭遇阻力       |

#### 棋盘路径设计（50 格具体分布）

```
起点(0) → 1-5(蓝) → 6(⭐) → 7-11(绿) → 12(⚠️) → 13-17(黄)
→ 18(⭐) → 19-23(红) → 24(⚠️) → 25-29(蓝) → 30(⭐)
→ 31-35(绿) → 36(⚠️) → 37-40(黄) → 41(⭐) → 42-45(红)
→ 46(⭐) → 47-49(蓝) → 终点(50)
```

**特殊格子说明：**

- **格子 0（起点）：** "市场建设启动"，展示欢迎信息
- **格子 10、20、30、40：** "里程碑格"，展示阶段性成果
- **格子 50（终点）：** "全国统一大市场建成"，播放通关动画

---

### 2. 题目分类与映射

从 `question.json` 的 100 道题中，按主题分类到不同格子：

#### 题目标签设计（需预处理题库）

```javascript
// 为每道题添加 category 字段
{
  "id": 1,
  "category": "制度",  // 制度/设施/要素/监管
  "question": "全国统一大市场的核心特征是什么？",
  // ... 其他字段
}
```

**分类规则：**

- **制度类（蓝格）：** 包含"制度"、"规则"、"标准"、"政策"等关键词
- **设施类（绿格）：** 包含"设施"、"联通"、"物流"、"信息"等关键词
- **要素类（黄格）：** 包含"要素"、"劳动力"、"资本"、"土地"、"数据"等关键词
- **监管类（红格）：** 包含"监管"、"执法"、"竞争"、"垄断"等关键词

---

### 3. 随机事件库设计

#### 机遇格事件（⭐ 金色，5 种）

```javascript
const fortuneEvents = [
  {
    id: 1,
    title: "🎉 中央政策支持",
    description: "国务院发布《加快建设全国统一大市场的意见》，市场建设提速！",
    effect: "前进 3 步",
    points: 50,
  },
  {
    id: 2,
    title: "🏆 试点城市成功",
    description: "您负责的试点城市市场统一度提升 20%，获得表彰！",
    effect: "获得 100 积分",
    points: 100,
  },
  {
    id: 3,
    title: "💡 创新突破",
    description: "成功建立跨区域市场监管协同机制，经验全国推广！",
    effect: "前进 2 步 + 50 积分",
    points: 50,
  },
  {
    id: 4,
    title: "🤝 区域协作",
    description: "长三角、珠三角等区域率先实现市场一体化！",
    effect: "免答下一题",
    points: 30,
  },
  {
    id: 5,
    title: "📈 市场活力提升",
    description: "全国市场主体突破 1.5 亿户，营商环境持续优化！",
    effect: "前进 4 步",
    points: 80,
  },
];
```

#### 挑战格事件（⚠️ 灰色，3 种）

```javascript
const challengeEvents = [
  {
    id: 1,
    title: "⚠️ 地方保护主义",
    description: "某省份设置不合理的市场准入限制，需要协调处理...",
    effect: "后退 2 步",
    points: -30,
  },
  {
    id: 2,
    title: "🚧 市场壁垒",
    description: "发现部分地区存在行政垄断行为，市场分割严重。",
    effect: "暂停一回合",
    points: -20,
  },
  {
    id: 3,
    title: "📉 执行不力",
    description: "部分政策执行打折扣，统一大市场建设进度放缓。",
    effect: "扣除 50 积分",
    points: -50,
  },
];
```

---

### 4. 界面布局设计

#### Web 版布局（`frontend/src/views/GameView.vue`）

```
┌─────────────────────────────────────────┐
│          市场建设大富翁                    │
├─────────────────────────────────────────┤
│  当前位置: 15/50  |  积分: 230  |  🎲 掷骰子  │
├─────────────────────────────────────────┤
│                                         │
│         [棋盘区域 - Canvas 绘制]           │
│                                         │
│   🟦→🟦→🟦→⭐→🟩→🟩→⚠️→🟨                │
│   ↓                              ↑      │
│   🟦                            🟨      │
│   ↓                              ↑      │
│   🟥←🟥←⭐←🟩←🟩←🟩←⚠️←🟨              │
│                                         │
│         [玩家棋子 🎯 在格子上移动]           │
│                                         │
├─────────────────────────────────────────┤
│         [事件/题目弹窗区域]                 │
│                                         │
│    当前格子: 🟦 制度规则统一                 │
│    题目: 全国统一大市场的核心特征是？         │
│    A. xxx    B. xxx                     │
│    C. xxx    D. xxx                     │
│              [提交答案]                   │
└─────────────────────────────────────────┘
```

#### 小程序版布局（`xisixiang-uniapp/src/pages/game/game.vue`）

```
┌─────────────────────────────────────────┐
│  <custom-tab-bar />                     │
├─────────────────────────────────────────┤
│  位置: 15/50  积分: 230  [🎲 掷骰子]       │
├─────────────────────────────────────────┤
│                                         │
│      [棋盘 - scroll-view 滚动显示]         │
│                                         │
│      🟦🟦🟦⭐🟩🟩⚠️🟨                      │
│                                         │
│      当前位置: 格子 15 (🟩)               │
│                                         │
├─────────────────────────────────────────┤
│  [题目卡片 - 占据下半屏]                    │
│  问题: xxxxx                             │
│  [选项按钮组]                             │
└─────────────────────────────────────────┘
```

---

## 🛠️ 技术实现步骤

### 阶段一：数据准备（1 天）

#### ✅ Task 1.1: 创建游戏数据文件

**文件：** `frontend/public/game/board-config.json`

```json
{
  "boardSize": 50,
  "cells": [
    { "id": 0, "type": "start", "name": "起点", "color": "#ff4d4d" },
    { "id": 1, "type": "blue", "name": "制度统一", "color": "#4a90e2" },
    { "id": 2, "type": "blue", "name": "规则完善", "color": "#4a90e2" },
    // ... 48 个格子配置
    { "id": 50, "type": "end", "name": "终点", "color": "#ffd700" }
  ],
  "fortuneEvents": [
    {
      "id": 1,
      "title": "中央政策支持",
      "description": "...",
      "effect": "forward",
      "value": 3,
      "points": 50
    }
    // ... 5 个机遇事件
  ],
  "challengeEvents": [
    {
      "id": 1,
      "title": "地方保护主义",
      "description": "...",
      "effect": "backward",
      "value": 2,
      "points": -30
    }
    // ... 3 个挑战事件
  ]
}
```

#### ✅ Task 1.2: 预处理题库数据

**文件：** `server/process_questions.py`（临时脚本）

```python
# 读取 question.json，为每道题添加 category 字段
# 根据问题内容中的关键词自动分类
# 输出到 frontend/public/game/questions-categorized.json
```

**分类规则示例：**

```python
def categorize_question(question_text):
    if any(kw in question_text for kw in ['制度', '规则', '标准', '政策']):
        return 'blue'
    elif any(kw in question_text for kw in ['设施', '联通', '物流', '基础']):
        return 'green'
    elif any(kw in question_text for kw in ['要素', '劳动力', '资本', '土地', '数据']):
        return 'yellow'
    elif any(kw in question_text for kw in ['监管', '执法', '竞争', '垄断']):
        return 'red'
    else:
        return 'blue'  # 默认分类
```

#### ✅ Task 1.3: 复制数据到小程序

将生成的 JSON 文件复制到小程序目录：

- `xisixiang-uniapp/src/static/game/board-config.json`
- `xisixiang-uniapp/src/static/game/questions-categorized.json`

---

### 阶段二：Web 版实现（3 天）

#### ✅ Task 2.1: 创建游戏页面路由

**文件：** `frontend/src/router/index.js`

```javascript
// 添加新路由
{
  path: '/game',
  name: 'Game',
  component: () => import('../views/GameView.vue')
}
```

**文件：** `frontend/src/App.vue`

```vue
<!-- 在导航栏添加"实践闯关"链接 -->
<router-link to="/game">🎮 实践闯关</router-link>
```

#### ✅ Task 2.2: 创建游戏主组件

**文件：** `frontend/src/views/GameView.vue`

**组件结构：**

```vue
<template>
  <div class="game-container">
    <!-- 1. 顶部状态栏 -->
    <div class="status-bar">
      <span>位置: {{ playerPosition }}/50</span>
      <span>积分: {{ totalPoints }}</span>
      <button @click="rollDice" :disabled="isMoving">🎲 掷骰子</button>
    </div>

    <!-- 2. 棋盘区域 -->
    <div class="board-wrapper">
      <canvas ref="boardCanvas" width="800" height="600"></canvas>
    </div>

    <!-- 3. 事件弹窗 -->
    <GameEventModal
      v-if="showModal"
      :event="currentEvent"
      @close="closeModal"
    />

    <!-- 4. 题目弹窗 -->
    <QuestionModal
      v-if="showQuestion"
      :question="currentQuestion"
      @answer="handleAnswer"
    />

    <!-- 5. 通关弹窗 -->
    <WinModal v-if="gameWon" :score="totalPoints" @restart="restartGame" />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
// ... 游戏逻辑
</script>
```

**核心状态管理：**

```javascript
const playerPosition = ref(0); // 玩家当前位置 (0-50)
const totalPoints = ref(0); // 总积分
const diceValue = ref(0); // 骰子点数
const isMoving = ref(false); // 是否正在移动
const showModal = ref(false); // 是否显示事件弹窗
const showQuestion = ref(false); // 是否显示题目弹窗
const currentEvent = ref(null); // 当前事件
const currentQuestion = ref(null); // 当前题目
const gameWon = ref(false); // 是否通关
const boardData = ref(null); // 棋盘数据
const questionsData = ref(null); // 题目数据
```

#### ✅ Task 2.3: 实现棋盘绘制逻辑

**文件：** `frontend/src/utils/boardRenderer.js`

```javascript
export class BoardRenderer {
  constructor(canvas, boardData) {
    this.canvas = canvas;
    this.ctx = canvas.getContext("2d");
    this.boardData = boardData;
    this.cellSize = 80;
    this.gap = 10;
  }

  // 绘制整个棋盘
  drawBoard() {
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    this.boardData.cells.forEach((cell, index) => {
      this.drawCell(cell, index);
    });
  }

  // 绘制单个格子
  drawCell(cell, index) {
    const position = this.calculatePosition(index);

    // 绘制格子背景
    this.ctx.fillStyle = cell.color;
    this.ctx.fillRect(position.x, position.y, this.cellSize, this.cellSize);

    // 绘制格子边框
    this.ctx.strokeStyle = "#333";
    this.ctx.lineWidth = 2;
    this.ctx.strokeRect(position.x, position.y, this.cellSize, this.cellSize);

    // 绘制格子编号
    this.ctx.fillStyle = "#fff";
    this.ctx.font = "bold 14px Arial";
    this.ctx.textAlign = "center";
    this.ctx.fillText(cell.id, position.x + this.cellSize / 2, position.y + 20);

    // 绘制格子名称
    this.ctx.font = "12px Arial";
    this.ctx.fillText(
      cell.name,
      position.x + this.cellSize / 2,
      position.y + 40
    );
  }

  // 计算格子在画布上的位置（回字形排列）
  calculatePosition(index) {
    // 设计一个 10x5 的回字形棋盘
    // 路径: 顶部从左到右 → 右侧从上到下 → 底部从右到左 → 左侧从下到上

    const topRowCount = 10; // 顶部 10 格
    const rightColCount = 5; // 右侧 5 格
    const bottomRowCount = 10; // 底部 10 格
    const leftColCount = 5; // 左侧 5 格

    let x, y;

    if (index < topRowCount) {
      // 顶部行
      x = index * (this.cellSize + this.gap);
      y = 0;
    } else if (index < topRowCount + rightColCount) {
      // 右侧列
      x = (topRowCount - 1) * (this.cellSize + this.gap);
      y = (index - topRowCount + 1) * (this.cellSize + this.gap);
    } else if (index < topRowCount + rightColCount + bottomRowCount) {
      // 底部行（从右到左）
      x =
        (topRowCount - 1 - (index - topRowCount - rightColCount)) *
        (this.cellSize + this.gap);
      y = rightColCount * (this.cellSize + this.gap);
    } else {
      // 左侧列（从下到上）
      x = 0;
      y =
        (rightColCount -
          (index - topRowCount - rightColCount - bottomRowCount)) *
        (this.cellSize + this.gap);
    }

    return { x: x + 50, y: y + 50 }; // 留出边距
  }

  // 绘制玩家棋子
  drawPlayer(position) {
    const pos = this.calculatePosition(position);
    const centerX = pos.x + this.cellSize / 2;
    const centerY = pos.y + this.cellSize / 2;

    // 绘制圆形棋子
    this.ctx.beginPath();
    this.ctx.arc(centerX, centerY, 15, 0, Math.PI * 2);
    this.ctx.fillStyle = "#ff4d4d";
    this.ctx.fill();
    this.ctx.strokeStyle = "#fff";
    this.ctx.lineWidth = 3;
    this.ctx.stroke();

    // 绘制棋子图标
    this.ctx.fillStyle = "#fff";
    this.ctx.font = "bold 20px Arial";
    this.ctx.textAlign = "center";
    this.ctx.textBaseline = "middle";
    this.ctx.fillText("🎯", centerX, centerY);
  }

  // 动画：棋子移动
  async animateMove(fromPos, toPos, diceValue) {
    const steps = toPos - fromPos;
    const duration = 300; // 每步 300ms

    for (let i = 1; i <= steps; i++) {
      await new Promise((resolve) => setTimeout(resolve, duration));
      this.drawBoard();
      this.drawPlayer(fromPos + i);
    }
  }
}
```

#### ✅ Task 2.4: 实现游戏核心逻辑

**文件：** `frontend/src/composables/useGameLogic.js`

```javascript
import { ref } from "vue";

export function useGameLogic(boardData, questionsData) {
  const playerPosition = ref(0);
  const totalPoints = ref(0);
  const diceValue = ref(0);
  const isMoving = ref(false);

  // 掷骰子
  function rollDice() {
    if (isMoving.value) return;

    isMoving.value = true;
    diceValue.value = Math.floor(Math.random() * 6) + 1;

    // 动画效果：骰子旋转
    // ... 实现骰子旋转动画

    setTimeout(() => {
      movePlayer(diceValue.value);
    }, 1000);
  }

  // 移动玩家
  async function movePlayer(steps) {
    const newPosition = Math.min(playerPosition.value + steps, 50);

    // 播放移动动画
    await animatePlayerMove(playerPosition.value, newPosition);

    playerPosition.value = newPosition;

    // 检查是否到达终点
    if (playerPosition.value === 50) {
      handleWin();
      return;
    }

    // 触发格子事件
    handleCellEvent(playerPosition.value);

    isMoving.value = false;
  }

  // 处理格子事件
  function handleCellEvent(position) {
    const cell = boardData.value.cells[position];

    switch (cell.type) {
      case "blue":
      case "green":
      case "yellow":
      case "red":
        // 问答题
        showQuestion(cell.type);
        break;
      case "fortune":
        // 机遇格
        showFortuneEvent();
        break;
      case "challenge":
        // 挑战格
        showChallengeEvent();
        break;
      default:
        isMoving.value = false;
    }
  }

  // 显示问答题
  function showQuestion(category) {
    // 从题库中随机选择对应类别的题目
    const categoryQuestions = questionsData.value.filter(
      (q) => q.category === category
    );
    const randomQuestion =
      categoryQuestions[Math.floor(Math.random() * categoryQuestions.length)];

    currentQuestion.value = randomQuestion;
    showQuestionModal.value = true;
  }

  // 处理答题结果
  function handleAnswer(selectedOption, isCorrect) {
    if (isCorrect) {
      totalPoints.value += 50;
      showToast("✅ 回答正确！+50 分");
    } else {
      totalPoints.value = Math.max(0, totalPoints.value - 20);
      showToast("❌ 回答错误！-20 分");
    }

    showQuestionModal.value = false;
    isMoving.value = false;
  }

  // 显示机遇事件
  function showFortuneEvent() {
    const events = boardData.value.fortuneEvents;
    const randomEvent = events[Math.floor(Math.random() * events.length)];

    currentEvent.value = randomEvent;
    showEventModal.value = true;

    // 应用事件效果
    applyEventEffect(randomEvent);
  }

  // 显示挑战事件
  function showChallengeEvent() {
    const events = boardData.value.challengeEvents;
    const randomEvent = events[Math.floor(Math.random() * events.length)];

    currentEvent.value = randomEvent;
    showEventModal.value = true;

    // 应用事件效果
    applyEventEffect(randomEvent);
  }

  // 应用事件效果
  function applyEventEffect(event) {
    totalPoints.value += event.points;

    if (event.effect === "forward") {
      // 前进
      setTimeout(() => {
        movePlayer(event.value);
      }, 2000);
    } else if (event.effect === "backward") {
      // 后退
      playerPosition.value = Math.max(0, playerPosition.value - event.value);
    }
    // 其他效果...
  }

  // 处理通关
  function handleWin() {
    gameWon.value = true;
    // 播放通关动画
    // 显示最终得分
  }

  // 重新开始
  function restartGame() {
    playerPosition.value = 0;
    totalPoints.value = 0;
    diceValue.value = 0;
    gameWon.value = false;
    isMoving.value = false;
  }

  return {
    playerPosition,
    totalPoints,
    diceValue,
    isMoving,
    rollDice,
    handleAnswer,
    restartGame,
  };
}
```

#### ✅ Task 2.5: 创建子组件

**文件：** `frontend/src/components/game/GameEventModal.vue`

```vue
<!-- 显示机遇/挑战事件的弹窗 -->
<template>
  <div class="modal-overlay">
    <div class="event-card">
      <h2>{{ event.title }}</h2>
      <p>{{ event.description }}</p>
      <div class="effect">效果: {{ event.effect }}</div>
      <div class="points">
        {{ event.points > 0 ? "+" : "" }}{{ event.points }} 分
      </div>
      <button @click="$emit('close')">确定</button>
    </div>
  </div>
</template>
```

**文件：** `frontend/src/components/game/QuestionModal.vue`

```vue
<!-- 显示问答题的弹窗，复用 QuizQuestion 组件逻辑 -->
<template>
  <div class="modal-overlay">
    <div class="question-card">
      <h3>{{ question.question }}</h3>
      <div class="options">
        <button
          v-for="(option, index) in question.options"
          :key="index"
          @click="selectAnswer(option)"
          :class="{ selected: selectedOption === option }"
        >
          {{ option }}
        </button>
      </div>
      <button
        class="submit-btn"
        @click="submitAnswer"
        :disabled="!selectedOption"
      >
        提交答案
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const props = defineProps(["question"]);
const emit = defineEmits(["answer"]);

const selectedOption = ref("");

function selectAnswer(option) {
  selectedOption.value = option;
}

function submitAnswer() {
  const isCorrect = selectedOption.value.startsWith(props.question.answer);
  emit("answer", selectedOption.value, isCorrect);
  selectedOption.value = "";
}
</script>
```

**文件：** `frontend/src/components/game/WinModal.vue`

```vue
<!-- 通关弹窗 -->
<template>
  <div class="modal-overlay">
    <div class="win-card">
      <h1>🎉 恭喜通关！</h1>
      <p>全国统一大市场建设完成！</p>
      <div class="final-score">
        <span>最终得分</span>
        <span class="score">{{ score }}</span>
      </div>
      <button @click="$emit('restart')">再玩一次</button>
    </div>
  </div>
</template>
```

#### ✅ Task 2.6: 样式设计

**文件：** `frontend/src/views/GameView.vue` (style 部分)

```css
.game-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 20px;
}

.status-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.status-bar button {
  padding: 10px 30px;
  background: linear-gradient(135deg, #ff4d4d, #cc0000);
  color: white;
  border: none;
  border-radius: 25px;
  font-size: 18px;
  cursor: pointer;
  transition: transform 0.3s;
}

.status-bar button:hover:not(:disabled) {
  transform: scale(1.05);
}

.status-bar button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.board-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  background: white;
  border-radius: 15px;
  padding: 30px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.event-card,
.question-card,
.win-card {
  background: white;
  border-radius: 20px;
  padding: 40px;
  max-width: 500px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    transform: translateY(-50px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}
```

---

### 阶段三：小程序版实现（2 天）

#### ✅ Task 3.1: 更新 pages.json

**文件：** `xisixiang-uniapp/src/pages.json`

```json
{
  "pages": [
    // ... 现有页面
    {
      "path": "pages/game/game",
      "style": {
        "navigationBarTitleText": "市场建设大富翁",
        "navigationBarBackgroundColor": "#ff4d4d",
        "navigationBarTextStyle": "white"
      }
    }
  ],
  "tabBar": {
    "list": [
      // ... 现有 tab
      {
        "pagePath": "pages/game/game",
        "text": "实践闯关",
        "iconPath": "static/images/game.png",
        "selectedIconPath": "static/images/game-active.png"
      }
    ]
  }
}
```

#### ✅ Task 3.2: 创建小程序游戏页面

**文件：** `xisixiang-uniapp/src/pages/game/game.vue`

**结构简化：**

- 不使用 Canvas（小程序 Canvas 性能问题）
- 使用 scroll-view + 格子列表呈现棋盘
- 使用绝对定位的棋子图标表示当前位置

```vue
<template>
  <view class="game-page">
    <custom-tab-bar />

    <!-- 状态栏 -->
    <view class="status-bar">
      <text>位置: {{ playerPosition }}/50</text>
      <text>积分: {{ totalPoints }}</text>
      <button @click="rollDice" :disabled="isMoving">🎲 掷骰子</button>
    </view>

    <!-- 棋盘区域 -->
    <scroll-view
      scroll-x
      class="board-container"
      :scroll-left="scrollLeft"
      scroll-with-animation
    >
      <view class="board-track">
        <view
          v-for="(cell, index) in boardData.cells"
          :key="index"
          :class="['cell', getCellClass(cell.type)]"
          :id="'cell-' + index"
        >
          <!-- 格子内容 -->
          <text class="cell-number">{{ cell.id }}</text>
          <text class="cell-name">{{ cell.name }}</text>

          <!-- 玩家棋子 -->
          <view v-if="playerPosition === index" class="player-piece"> 🎯 </view>
        </view>
      </view>
    </scroll-view>

    <!-- 骰子动画区 -->
    <view v-if="showDice" class="dice-animation">
      <text class="dice">🎲</text>
      <text class="dice-value">{{ diceValue }}</text>
    </view>

    <!-- 事件弹窗 -->
    <view v-if="showEventModal" class="modal">
      <view class="event-card">
        <text class="event-title">{{ currentEvent.title }}</text>
        <text class="event-desc">{{ currentEvent.description }}</text>
        <text class="event-effect">效果: {{ currentEvent.effect }}</text>
        <button @click="closeEventModal">确定</button>
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
        <text class="final-score">最终得分: {{ totalPoints }}</text>
        <button @click="restartGame">再玩一次</button>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { onShow } from "@dcloudio/uni-app";

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
const scrollLeft = ref(0);

const boardData = ref(null);
const questionsData = ref(null);
const currentEvent = ref(null);
const currentQuestion = ref(null);
const selectedOption = ref("");

// 加载游戏数据
onMounted(async () => {
  try {
    // 加载棋盘配置
    const boardRes = await fetch("/static/game/board-config.json");
    boardData.value = await boardRes.json();

    // 加载题目数据
    const questionsRes = await fetch("/static/game/questions-categorized.json");
    questionsData.value = await questionsRes.json();
  } catch (error) {
    console.error("加载游戏数据失败:", error);
    uni.showToast({
      title: "数据加载失败",
      icon: "none",
    });
  }
});

// 掷骰子
function rollDice() {
  if (isMoving.value) return;

  isMoving.value = true;
  showDice.value = true;

  // 随机生成点数（1-6）
  diceValue.value = Math.floor(Math.random() * 6) + 1;

  // 1秒后开始移动
  setTimeout(() => {
    showDice.value = false;
    movePlayer(diceValue.value);
  }, 1000);
}

// 移动玩家
function movePlayer(steps) {
  const newPosition = Math.min(playerPosition.value + steps, 50);

  // 逐步移动动画
  let currentStep = 0;
  const interval = setInterval(() => {
    if (currentStep < steps && playerPosition.value < 50) {
      playerPosition.value++;
      currentStep++;

      // 滚动到当前位置
      scrollLeft.value = playerPosition.value * 120;
    } else {
      clearInterval(interval);

      // 检查是否通关
      if (playerPosition.value === 50) {
        handleWin();
        return;
      }

      // 触发格子事件
      handleCellEvent();
    }
  }, 300);
}

// 处理格子事件
function handleCellEvent() {
  const cell = boardData.value.cells[playerPosition.value];

  if (["blue", "green", "yellow", "red"].includes(cell.type)) {
    // 问答题
    showQuestion(cell.type);
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
  const randomQuestion =
    categoryQuestions[Math.floor(Math.random() * categoryQuestions.length)];

  currentQuestion.value = randomQuestion;
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
    uni.showToast({
      title: "✅ 回答正确！+50分",
      icon: "success",
    });
  } else {
    totalPoints.value = Math.max(0, totalPoints.value - 20);
    uni.showToast({
      title: "❌ 回答错误！-20分",
      icon: "none",
    });
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

  setTimeout(() => {
    if (randomEvent.effect === "forward") {
      movePlayer(randomEvent.value);
    } else {
      isMoving.value = false;
    }
  }, 2000);
}

// 显示挑战事件
function showChallengeEvent() {
  const events = boardData.value.challengeEvents;
  const randomEvent = events[Math.floor(Math.random() * events.length)];

  currentEvent.value = randomEvent;
  showEventModal.value = true;

  totalPoints.value += randomEvent.points;

  if (randomEvent.effect === "backward") {
    playerPosition.value = Math.max(
      0,
      playerPosition.value - randomEvent.value
    );
  }

  setTimeout(() => {
    isMoving.value = false;
  }, 2000);
}

// 关闭事件弹窗
function closeEventModal() {
  showEventModal.value = false;
}

// 处理通关
function handleWin() {
  gameWon.value = true;
  uni.showToast({
    title: "🎉 恭喜通关！",
    icon: "success",
    duration: 2000,
  });
}

// 重新开始
function restartGame() {
  playerPosition.value = 0;
  totalPoints.value = 0;
  diceValue.value = 0;
  gameWon.value = false;
  isMoving.value = false;
  scrollLeft.value = 0;
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
</script>

<style scoped>
.game-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
  padding-bottom: 120rpx;
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

.status-bar text {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
}

.status-bar button {
  padding: 15rpx 30rpx;
  background: linear-gradient(135deg, #ff4d4d, #cc0000);
  color: white;
  border: none;
  border-radius: 30rpx;
  font-size: 28rpx;
}

.board-container {
  margin: 20rpx;
  background: white;
  border-radius: 20rpx;
  padding: 30rpx 0;
  box-shadow: 0 4rpx 15rpx rgba(0, 0, 0, 0.1);
  white-space: nowrap;
}

.board-track {
  display: inline-flex;
  gap: 20rpx;
  padding: 0 30rpx;
}

.cell {
  width: 100rpx;
  height: 120rpx;
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-radius: 15rpx;
  border: 3rpx solid #ddd;
  position: relative;
  flex-shrink: 0;
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
  font-size: 24rpx;
  font-weight: bold;
}

.cell-name {
  font-size: 20rpx;
  text-align: center;
  margin-top: 5rpx;
}

.player-piece {
  position: absolute;
  top: -20rpx;
  font-size: 50rpx;
  animation: bounce 0.5s infinite;
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
  animation: diceRoll 0.5s ease-in-out;
}

.dice {
  font-size: 120rpx;
}

.dice-value {
  font-size: 80rpx;
  font-weight: bold;
  color: #ff4d4d;
  margin-top: 20rpx;
}

@keyframes diceRoll {
  0%,
  100% {
    transform: translate(-50%, -50%) rotate(0deg);
  }
  25% {
    transform: translate(-50%, -50%) rotate(90deg);
  }
  50% {
    transform: translate(-50%, -50%) rotate(180deg);
  }
  75% {
    transform: translate(-50%, -50%) rotate(270deg);
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
}

/* ... 其他弹窗样式 */
</style>
```

#### ✅ Task 3.3: 准备图标资源

**文件：**

- `xisixiang-uniapp/src/static/images/game.png`（未选中图标）
- `xisixiang-uniapp/src/static/images/game-active.png`（选中图标）

可以使用 🎮 或 🎯 emoji 转换为图片，或设计简单的游戏手柄图标。

---

### 阶段四：测试与优化（1 天）

#### ✅ Task 4.1: 功能测试清单

- [ ] 掷骰子功能正常（1-6 随机数）
- [ ] 棋子移动动画流畅
- [ ] 蓝/绿/黄/红格触发问答题
- [ ] 问答题答对加分、答错扣分
- [ ] 机遇格随机触发 5 种事件
- [ ] 挑战格随机触发 3 种事件
- [ ] 到达终点触发通关
- [ ] 重新开始功能正常
- [ ] 小程序 TabBar 切换正常

#### ✅ Task 4.2: 边界情况处理

- [ ] 积分不能为负数（最低 0 分）
- [ ] 位置不能超过 50 格（终点）
- [ ] 后退不能小于 0 格（起点）
- [ ] 移动过程中禁用掷骰子按钮
- [ ] 题库数据加载失败的提示
- [ ] 没有选择答案时禁用提交按钮

#### ✅ Task 4.3: 性能优化

- [ ] Web 版 Canvas 重绘优化（只重绘变化部分）
- [ ] 小程序长列表优化（虚拟滚动）
- [ ] 图片资源压缩（< 100KB）
- [ ] 动画帧率控制（60fps）
- [ ] 数据懒加载（按需加载事件）

#### ✅ Task 4.4: 用户体验优化

- [ ] 添加音效（可选）：掷骰子、移动、答对/答错
- [ ] 添加震动反馈（小程序）
- [ ] 答题时显示正确答案和解析
- [ ] 通关时展示统计数据（用时、正确率）
- [ ] 添加暂停/继续功能
- [ ] 添加游戏规则说明

---

## 📂 最终文件结构

### Web 版

```
frontend/
├── public/
│   └── game/
│       ├── board-config.json          # 棋盘配置
│       └── questions-categorized.json # 分类题库
├── src/
│   ├── views/
│   │   └── GameView.vue               # 游戏主页面
│   ├── components/
│   │   └── game/
│   │       ├── GameEventModal.vue     # 事件弹窗
│   │       ├── QuestionModal.vue      # 题目弹窗
│   │       └── WinModal.vue           # 通关弹窗
│   ├── composables/
│   │   └── useGameLogic.js            # 游戏逻辑
│   └── utils/
│       └── boardRenderer.js           # 棋盘渲染
```

### 小程序版

```
xisixiang-uniapp/
├── src/
│   ├── pages/
│   │   └── game/
│   │       └── game.vue               # 游戏页面
│   └── static/
│       ├── game/
│       │   ├── board-config.json
│       │   └── questions-categorized.json
│       └── images/
│           ├── game.png               # TabBar 图标
│           └── game-active.png
```

---

## 🎯 开发优先级建议

### 第一优先级（核心功能）

1. 数据准备（棋盘配置、题库分类）
2. 掷骰子和移动逻辑
3. 问答题触发和答题逻辑
4. 通关判定

### 第二优先级（增强体验）

5. 机遇/挑战事件
6. 动画效果
7. 积分系统

### 第三优先级（锦上添花）

8. 音效和震动
9. 统计数据
10. 规则说明

---

## 🚀 启动开发流程

1. **创建此文件：** `todo.md`
2. **数据准备：** 运行 `python server/process_questions.py`
3. **Web 版开发：** 按 Task 2.1 → 2.6 顺序
4. **小程序开发：** 按 Task 3.1 → 3.3 顺序
5. **测试优化：** 按 Task 4.1 → 4.4 检查

---

## ✅ 验收标准

- [ ] 单人游戏完整流程可玩
- [ ] 所有格子类型都能正确触发
- [ ] 题目来自现有题库，分类准确
- [ ] 通关后能重新开始
- [ ] Web 和小程序双端实现
- [ ] 无明显 Bug 和性能问题
- [ ] 游戏时长约 5-10 分钟

---

## 📝 后续扩展方向（可选）

1. **难度选择：** 简单（30 格）/ 普通（50 格）/ 困难（70 格）
2. **成就系统：** 首次通关、满分通关、连续答对等
3. **排行榜：** 本地存储历史最高分
4. **每日挑战：** 每天固定题目和事件
5. **皮肤系统：** 不同主题的棋盘和棋子
6. **多人模式：** WebSocket 实现联机对战

---

**预计完成时间：** 5-7 天  
**开发人数：** 1 人  
**技术难点：** Canvas 绘制、动画流畅度、小程序兼容性  
**建议：** 先完成 Web 版，再移植到小程序

---

**祝开发顺利！🎮**
