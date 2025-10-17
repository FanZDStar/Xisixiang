# 📚 文档目录说明

## 目录结构

```
document/
└── theory/                    # 理论学习文档
    ├── 中共中央国务院关于加快建设全国统一大市场的意见.md
    ├── 全国统一大市场建设指引（试行）.md
    ├── 全国统一大市场的那些事.md
    ├── 将制定《妨碍统一市场和公平竞争行为防范事项清单》.md
    ├── 怎么理解纵深推进全国统一大市场建设.md
    ├── 构建全国统一大市场.md
    ├── 深化构建全国统一大市场的逻辑认识与思考.md
    └── 纵深推进全国统一大市场建设.md
```

## 访问方式

### API 路由

```
GET /static/theory/<filename>
```

**示例：**

```
http://127.0.0.1:5122/static/theory/构建全国统一大市场.md
```

### 代码实现

在 `app.py` 中：

```python
@app.route('/static/theory/<path:filename>', methods=['GET'])
def serve_theory_file(filename):
    """提供 Markdown 文档静态文件服务"""
    # 使用相对路径，相对于 app.py 所在目录
    theory_dir = os.path.join(os.path.dirname(__file__), 'document', 'theory')
    return send_from_directory(theory_dir, filename, mimetype='text/markdown; charset=utf-8')
```

## 部署说明

### 本地开发

文档存储在 `server/document/theory/` 目录下，使用相对路径访问，无需配置。

### 服务器部署

1. **上传整个 server 目录**

   ```bash
   server/
   ├── app.py
   ├── chat_api.py
   ├── quiz_api.py
   ├── question.json
   ├── document/
   │   └── theory/
   │       └── *.md
   └── requirements.txt
   ```

2. **文档会自动随代码一起部署**

   - 无需额外配置路径
   - 无需修改代码
   - 相对路径自动适配部署环境

3. **验证部署**
   ```bash
   curl http://your-server.com:5122/static/theory/构建全国统一大市场.md
   ```

## 添加新文档

1. 将 Markdown 文件放入 `server/document/theory/` 目录
2. 无需修改代码，自动可访问
3. 在前端 `theory.vue` 中添加文档信息：

```javascript
const documents = [
  {
    title: "新文档标题",
    description: "文档描述",
    fileName: "新文档.md", // 必须与实际文件名一致
  },
  // ... 其他文档
];
```

## 文件编码

所有 Markdown 文件使用 **UTF-8** 编码，确保中文正确显示。

## 注意事项

1. **文件名大小写敏感**（Linux 服务器）
2. **避免特殊字符**：建议文件名只使用中文、英文、数字、下划线
3. **URL 编码**：前端传递文件名时会自动进行 URL 编码
4. **CORS 已配置**：跨域请求已支持

---

**更新时间：** 2025 年 10 月 17 日  
**存储位置：** `server/document/theory/`  
**访问方式：** 相对路径（便于部署）
