import json
import random
import os

# 加载题目数据
def load_questions():
    with open(os.path.join(os.path.dirname(__file__), 'question.json'), 'r', encoding='utf-8') as f:
        return json.load(f)

# 获取所有题目（包含答案和解析）
def get_all_questions():
    try:
        questions = load_questions()
        return questions, 200
    except Exception as e:
        return {"error": str(e)}, 500

# 随机获取10道题目（包含答案和解析）
def get_random_quiz():
    try:
        questions = load_questions()
        # 随机选择10道题目
        selected_questions = random.sample(questions, min(10, len(questions)))
        return selected_questions, 200
    except Exception as e:
        return {"error": str(e)}, 500

# 获取题目详情
def get_question_detail(question_id):
    try:
        questions = load_questions()
        for q in questions:
            if q["id"] == question_id:
                return q, 200
        return {"error": "Question not found"}, 404
    except Exception as e:
        return {"error": str(e)}, 500