module.exports = {
  apps: [{
    name: 'xisixiang-server',
    script: 'app.py',
    interpreter: './venv/bin/python3',  // 使用虚拟环境中的 Python 解释器
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G',
    env: {
      NODE_ENV: 'production',
      FLASK_ENV: 'production',
      FLASK_APP: 'app.py'
    },
    error_file: './logs/err.log',
    out_file: './logs/out.log',
    log_file: './logs/combined.log',
    time: true
  }]
}