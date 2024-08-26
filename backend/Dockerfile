# 使用官方 Python 镜像作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制项目的依赖文件到容器中
COPY requirements.txt .

# 安装项目依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目的所有文件到容器中
COPY . .

# 设置环境变量，防止 Python 写入 .pyc 文件
ENV PYTHONUNBUFFERED=1

# 运行数据库迁移并启动应用
CMD ["sh", "-c", "python manage.py migrate && gunicorn --bind 0.0.0.0:8000 survey_planet.wsgi:application","python manage.py test"]

# 暴露应用端口
EXPOSE 8000












