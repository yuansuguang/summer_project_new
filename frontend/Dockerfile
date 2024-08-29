FROM node:18
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 8080
CMD ["npm", "run", "serve"]


# # 使用官方 Node.js 作为基础镜像
# FROM node:16 AS build

# # 设置工作目录
# WORKDIR /app

# # 复制 package.json 和 package-lock.json
# COPY package*.json ./

# # 安装依赖
# RUN npm install

# # 复制应用源码
# COPY . .

# # 构建应用
# RUN npm run build

# # 将构建后的代码复制到 nginx 镜像中
# FROM nginx:latest
# COPY --from=0 /app/dist /usr/share/nginx/html

# # 暴露容器的 8080 端口，此处其实只是一个声明作用，不写的话也可以，后面运行容器的
# # docker run --name container_name -p <host_port>:<container_port>命令中container_port可以覆盖此处的声明，不写就默认80端口
# EXPOSE 8080

# # 启动 nginx 服务
# CMD ["nginx", "-g", "daemon off;"]