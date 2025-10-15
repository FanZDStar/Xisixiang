# Flask 后端开发指南

##  创建虚拟环境
```bash
cd server
python -m venv venv
venv\Scripts\activate

#安装依赖
pip install -r requirements.txt

#运行应用
python app.py

#退出虚拟环境
deactivate

#更新依赖列表
pip freeze > requirements.txt
```