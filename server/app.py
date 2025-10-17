from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os

from chat_api import create_chat_completion
from quiz_api import get_all_questions, get_random_quiz, get_question_detail

load_dotenv()

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # 确保中文字符正常显示
CORS(app)  # 启用CORS支持

# 获取所有题目（包含答案和解析）
@app.route('/api/questions', methods=['GET'])
def api_get_all_questions():
    result, status_code = get_all_questions()
    return jsonify(result), status_code

# 随机获取10道题目（包含答案和解析）
@app.route('/api/quiz', methods=['GET'])
def api_get_random_quiz():
    result, status_code = get_random_quiz()
    return jsonify(result), status_code

# 获取题目详情
@app.route('/api/questions/<int:question_id>', methods=['GET'])
def api_get_question_detail(question_id):
    result, status_code = get_question_detail(question_id)
    return jsonify(result), status_code


@app.route('/api/chat', methods=['POST'])
def api_chat_completion():
    payload = request.get_json(silent=True) or {}
    messages = payload.get('messages')

    if not isinstance(messages, list):
        return jsonify({'error': "请求体需要包含 messages 数组"}), 400

    result, status_code = create_chat_completion(messages)

    if status_code == 200:
        print("ai 回复:", result)
        return jsonify({'reply': result}), 200
    return jsonify(result), status_code

# 静态文件服务 - 提供理论学习文档
@app.route('/static/theory/<path:filename>', methods=['GET'])
def serve_theory_file(filename):
    """提供 Markdown 文档静态文件服务"""
    try:
        # 获取 frontend/public/theory 目录的绝对路径
        theory_dir = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'public', 'theory')
        theory_dir = os.path.abspath(theory_dir)
        
        print(f"[静态文件] 请求文件: {filename}")
        print(f"[静态文件] 目录: {theory_dir}")
        
        return send_from_directory(theory_dir, filename, mimetype='text/markdown; charset=utf-8')
    except FileNotFoundError:
        print(f"[静态文件] 文件不存在: {filename}")
        return jsonify({'error': '文件不存在'}), 404
    except Exception as e:
        print(f"[静态文件] 错误: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5122)
