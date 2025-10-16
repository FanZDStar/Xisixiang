from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

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

if __name__ == '__main__':
    app.run(debug=True)
