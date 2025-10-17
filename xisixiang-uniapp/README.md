# 习思想课程 - 小程序版

基于 uni-app 的微信小程序版本，包含智能问答、习题训练、理论学习等功能。

## 🚀 快速开始

### 1. 安装依赖

```powershell
npm install
```

### 2. 启动开发

#### 微信小程序

```powershell
npm run dev:mp-weixin
```

#### H5（浏览器调试）

```powershell
npm run dev:h5
```

### 3. 配置微信开发者工具

1. 打开微信开发者工具
2. 导入项目：选择 `dist/dev/mp-weixin` 目录
3. 填写 AppID（可以使用测试号）
4. 配置开发设置：
   - ✅ 不校验合法域名
   - ✅ 不校验 TLS 版本

### 4. 启动后端服务

```powershell
cd ../server
python app.py
```

后端服务将运行在 `http://localhost:5000`

## 📁 项目结构

```
xisixiang-uniapp/
├── src/
│   ├── pages/              # 页面目录
│   │   ├── chat/           # 智能问答
│   │   │   └── chat.vue
│   │   ├── quiz/           # 习题训练
│   │   │   └── quiz.vue
│   │   ├── theory/         # 理论学习
│   │   │   ├── theory.vue  # 文档列表
│   │   │   └── document.vue # 文档详情
│   │   └── knowledge-graph/ # 知识图谱
│   │       └── knowledge-graph.vue
│   │   └── utils/
│   │       └── request.js  # API 请求工具
│   ├── App.vue             # 应用入口
│   ├── main.js             # 主入口文件
│   ├── pages.json          # 页面配置
│   └── manifest.json       # 应用配置
├── package.json
└── vite.config.js
```

## ✨ 功能特性

### 智能问答

- ✅ 实时对话交互
- ✅ 快捷问题按钮
- ✅ Markdown 格式渲染
- ✅ 消息历史记录
- ✅ 加载动画效果

### 习题训练

- ✅ 随机抽取 10 道题目
- ✅ 单选题答题
- ✅ 实时答案检查
- ✅ 详细解析展示
- ✅ 进度条显示
- ✅ 成绩统计

### 理论学习

- ✅ 6 篇理论文档
- ✅ 文档列表展示
- ✅ Markdown 渲染
- ✅ 知识图谱入口

### 知识图谱

- 🚧 功能开发中

## 🎨 设计规范

### 主题色

- **主色**：`#ff4d4d`（红色）
- **辅助色**：`#cc0000`（深红）
- **背景色**：`#f5f5f5`（浅灰）
- **文字色**：`#333`（深灰）

### 单位规范

- 使用 `rpx` 响应式单位（750rpx = 屏幕宽度）
- 字体：26-40rpx
- 间距：20-40rpx
- 圆角：10-30rpx

### 动画效果

- 按钮按下：`transform: scale(0.98)`
- 页面切换：`transition: all 0.3s`
- 渐变背景：`linear-gradient(135deg, #ff4d4d, #cc0000)`

## 🔧 API 配置

### 开发环境

```javascript
// src/pages/utils/request.js
const BASE_URL = "http://localhost:5000";
```

### 生产环境

需要修改为 HTTPS 域名：

```javascript
const BASE_URL = "https://your-domain.com";
```

**注意**：微信小程序要求生产环境必须使用 HTTPS。

## 📡 API 接口

### 智能问答

- **POST** `/api/chat`
- 参数：`{ messages: [...] }`
- 返回：`{ reply: "回答内容" }`

### 习题训练

- **GET** `/api/quiz` - 获取随机 10 道题
- **GET** `/api/questions` - 获取所有题目
- **GET** `/api/questions/:id` - 获取单个题目

### 数据格式

```json
{
  "id": 1,
  "question": "题目内容",
  "options": ["A. 选项1", "B. 选项2", "C. 选项3", "D. 选项4"],
  "answer": "B",
  "explanation": "解析内容"
}
```

## 🐛 常见问题

### Q1: 网络请求失败？

**A**: 检查以下几点：

1. 后端服务是否启动
2. 微信开发者工具是否关闭了域名校验
3. 请求 URL 是否正确

### Q2: 页面样式异常？

**A**:

1. 确保使用 `rpx` 单位
2. 检查选择器是否正确
3. 小程序不支持某些 CSS 特性（如 `*` 选择器）

### Q3: 理论文档无法加载？

**A**:

1. 需要配置后端静态文件服务
2. 或将 Markdown 文件上传到云存储
3. 临时方案：使用占位内容

### Q4: Markdown 渲染不正确？

**A**:

- 小程序 `rich-text` 组件支持有限
- 建议使用 `towxml` 库实现完整 Markdown 支持
- 当前使用简化版渲染

## 📦 构建发布

### 构建微信小程序

```powershell
npm run build:mp-weixin
```

构建产物位于 `dist/build/mp-weixin/`

### 上传小程序

1. 使用微信开发者工具打开构建目录
2. 点击"上传"按钮
3. 填写版本号和描述
4. 提交审核

## 🔄 与 Web 版本的主要差异

| 特性     | Web 版             | 小程序版             |
| -------- | ------------------ | -------------------- |
| 路由     | Vue Router         | pages.json           |
| 请求     | fetch/axios        | uni.request          |
| 存储     | localStorage       | uni.setStorageSync   |
| 单位     | px                 | rpx                  |
| 组件     | HTML 标签          | uni-app 组件         |
| Markdown | marked + DOMPurify | rich-text + 简化渲染 |

## 📝 开发注意事项

1. **样式单位**：全部使用 `rpx`，不要使用 `px`
2. **API 请求**：必须通过 `uni.request`，不能使用 `fetch`
3. **路由跳转**：使用 `uni.navigateTo` / `uni.switchTab`
4. **弹窗提示**：使用 `uni.showToast` / `uni.showModal`
5. **生命周期**：使用 `onLoad` / `onShow` 等 uni-app 生命周期
6. **TabBar 页面**：只能使用 `uni.switchTab` 跳转

## 🎯 后续优化计划

- [ ] 集成 towxml 实现完整 Markdown 渲染
- [ ] 实现知识图谱可视化
- [ ] 添加用户学习进度记录
- [ ] 优化 Markdown 文档加载方式
- [ ] 添加分包加载优化性能
- [ ] 接入云函数替代传统后端
- [ ] 添加分享功能
- [ ] 实现离线缓存

## 📖 参考文档

- [uni-app 官方文档](https://uniapp.dcloud.net.cn/)
- [微信小程序文档](https://developers.weixin.qq.com/miniprogram/dev/framework/)
- [Vue 3 文档](https://cn.vuejs.org/)

## 👨‍💻 开发团队

习思想课程作业项目组

---

**创建时间**：2025 年 10 月 17 日  
**版本**：1.0.0  
**技术栈**：uni-app + Vue 3 + Flask
