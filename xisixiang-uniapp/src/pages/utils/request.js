// utils/request.js
const BASE_URL = "http://127.0.0.1:5122"; // 开发环境
// const BASE_URL = 'https://your-domain.com'; // 生产环境

export function request(options) {
  return new Promise((resolve, reject) => {
    uni.showLoading({
      title: "加载中...",
      mask: true,
    });

    uni.request({
      url: BASE_URL + options.url,
      method: options.method || "GET",
      data: options.data || {},
      header: {
        "Content-Type": "application/json",
        ...options.header,
      },
      success: (res) => {
        uni.hideLoading();
        if (res.statusCode === 200) {
          resolve(res.data);
        } else {
          reject(new Error(`请求失败: ${res.statusCode}`));
        }
      },
      fail: (err) => {
        uni.hideLoading();
        uni.showToast({
          title: "网络请求失败",
          icon: "none",
        });
        reject(err);
      },
    });
  });
}

// 智能问答 API
export function chatCompletion(messages) {
  return request({
    url: "/api/chat",
    method: "POST",
    data: { messages },
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
