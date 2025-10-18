// utils/request.js
//const BASE_URL = "http://127.0.0.1:5122"; // 开发环境
const BASE_URL = 'https://xisixiang.nuyoahming.xyz'; // 生产环境

export function request(options) {
  return new Promise((resolve, reject) => {
    // 是否显示加载提示（默认不显示，避免与页面自定义加载动画冲突）
    const showLoading = options.showLoading !== false;

    if (showLoading && !options.silent) {
      uni.showLoading({
        title: options.loadingText || "加载中...",
        mask: true,
      });
    }

    uni.request({
      url: BASE_URL + options.url,
      method: options.method || "GET",
      data: options.data || {},
      header: {
        "Content-Type": "application/json",
        ...options.header,
      },
      success: (res) => {
        if (showLoading && !options.silent) {
          uni.hideLoading();
        }
        if (res.statusCode === 200) {
          resolve(res.data);
        } else {
          reject(new Error(`请求失败: ${res.statusCode}`));
        }
      },
      fail: (err) => {
        if (showLoading && !options.silent) {
          uni.hideLoading();
        }
        if (!options.silent) {
          uni.showToast({
            title: "网络请求失败",
            icon: "none",
          });
        }
        reject(err);
      },
    });
  });
}

// 智能问答 API（禁用默认加载提示，使用页面自定义动画）
export function chatCompletion(messages) {
  return request({
    url: "/api/chat",
    method: "POST",
    data: { messages },
    showLoading: false, // 禁用默认加载圈，使用页面的加载动画
    silent: true, // 静默模式，不显示错误提示（由页面处理）
  });
}

// 获取题目列表
export function getQuestions() {
  return request({
    url: "/api/questions",
    method: "GET",
  });
}

// 获取随机题目
export function getRandomQuiz() {
  return request({
    url: "/api/quiz",
    method: "GET",
  });
}
