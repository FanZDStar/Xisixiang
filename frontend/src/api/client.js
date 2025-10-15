// frontend/src/api/client.js
export class ApiClient {
  constructor(baseURL) {
    this.baseURL = baseURL;
  }

  async get(endpoint) {
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (!response.ok) {
      const payload = await response.json().catch(() => ({}));
      const message = payload.error || `请求失败：${response.status}`;
      throw new Error(message);
    }
    return response.json();
  }

  async post(endpoint, data) {
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      const payload = await response.json().catch(() => ({}));
      const message = payload.error || `请求失败：${response.status}`;
      throw new Error(message);
    }
    return response.json();
  }
}

export default new ApiClient("http://localhost:5000"); // 替换为你的后端地址
