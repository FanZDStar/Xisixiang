#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
题库分类脚本
将 question.json 中的题目按主题分类，生成游戏所需的分类题库
"""

import json
import os


def categorize_question(question_text, explanation=""):
    """
    根据问题内容和解析中的关键词自动分类
    返回分类：blue(制度)、green(设施)、yellow(要素)、red(监管)
    """
    # 合并问题和解析文本进行关键词匹配
    full_text = question_text + " " + explanation
    
    # 制度类关键词
    blue_keywords = [
        '制度', '规则', '标准', '政策', '法律', '法规', '条例',
        '意见', '准入', '产权', '知识产权', '信用', '负面清单',
        '体系', '机制', '规范', '统一标准', '制度创新'
    ]
    
    # 设施类关键词
    green_keywords = [
        '设施', '联通', '物流', '基础', '网络', '交通', '信息化',
        '数字', '平台', '互联互通', '流通', '配送', '仓储',
        '高标准联通', '市场设施'
    ]
    
    # 要素类关键词
    yellow_keywords = [
        '要素', '劳动力', '资本', '土地', '技术', '数据',
        '人才', '资金', '市场化配置', '自由流动', '资源配置',
        '生产要素', '要素市场'
    ]
    
    # 监管类关键词
    red_keywords = [
        '监管', '执法', '竞争', '垄断', '反垄断', '公平竞争',
        '市场监管', '行政执法', '协同监管', '不正当竞争',
        '地方保护', '市场壁垒', '市场分割', '行政垄断'
    ]
    
    # 计算每个分类的关键词匹配数量
    scores = {
        'blue': sum(1 for kw in blue_keywords if kw in full_text),
        'green': sum(1 for kw in green_keywords if kw in full_text),
        'yellow': sum(1 for kw in yellow_keywords if kw in full_text),
        'red': sum(1 for kw in red_keywords if kw in full_text)
    }
    
    # 返回得分最高的分类，如果都为0则默认为制度类
    if max(scores.values()) == 0:
        return 'blue'
    
    return max(scores, key=scores.get)


def process_questions():
    """处理题库，为每道题添加分类标签"""
    
    # 读取原始题库
    input_file = os.path.join(os.path.dirname(__file__), 'question.json')
    
    with open(input_file, 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    print(f"📚 读取题库成功，共 {len(questions)} 道题目")
    
    # 为每道题添加分类
    categorized_questions = []
    category_count = {'blue': 0, 'green': 0, 'yellow': 0, 'red': 0}
    
    for question in questions:
        # 分类
        category = categorize_question(
            question['question'],
            question.get('explanation', '')
        )
        
        # 添加分类字段
        categorized_question = {
            **question,
            'category': category
        }
        
        categorized_questions.append(categorized_question)
        category_count[category] += 1
    
    # 输出统计信息
    print("\n📊 分类统计：")
    print(f"  🟦 制度类 (blue):  {category_count['blue']} 题")
    print(f"  🟩 设施类 (green): {category_count['green']} 题")
    print(f"  🟨 要素类 (yellow): {category_count['yellow']} 题")
    print(f"  🟥 监管类 (red):   {category_count['red']} 题")
    
    # 保存到多个位置
    output_files = [
        'frontend/public/game/questions-categorized.json',
        'xisixiang-uniapp/src/static/game/questions-categorized.json'
    ]
    
    for output_file in output_files:
        output_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            output_file
        )
        
        # 确保目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # 写入文件
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(categorized_questions, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 已保存到: {output_path}")
    
    print("\n🎉 题库分类完成！")
    return categorized_questions


if __name__ == '__main__':
    process_questions()
