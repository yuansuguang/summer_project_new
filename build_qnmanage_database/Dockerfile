# 使用官方 MySQL 镜像作为基础镜像
FROM mysql:8.0

# 将初始化脚本复制到 Docker 镜像中的 /docker-entrypoint-initdb.d 目录
COPY init.sql /docker-entrypoint-initdb.d/

# 设置环境变量（可以根据需要调整）
ENV MYSQL_ROOT_PASSWORD=350305Glj
ENV MYSQL_DATABASE=qnmanage_database
# ENV MYSQL_USER=myuser
# ENV MYSQL_PASSWORD=mypassword

# 暴露 MySQL 默认端口
EXPOSE 3306
