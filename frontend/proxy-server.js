const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');

const app = express();
const PORT = 8000;  // 代理服务器的端口

// 设置代理中间件
app.use('/user', createProxyMiddleware({
    target: 'http://localhost:8001',  // 后端服务地址
    changeOrigin: true,
    onProxyReq: (proxyReq, req, res) => {
        // 复制请求中的 cookies（如果有）
        if (req.headers.cookie) {
            proxyReq.setHeader('Cookie', req.headers.cookie);
        }
    }
}));

app.use('/surveymanage', createProxyMiddleware({
    target: 'http://localhost:8002',  // 后端服务地址
    changeOrigin: true,
    onProxyReq: (proxyReq, req, res) => {
        // 复制请求中的 cookies（如果有）
        if (req.headers.cookie) {
            proxyReq.setHeader('Cookie', req.headers.cookie);
        }
    }
}));

app.use('/survey', createProxyMiddleware({
    target: 'http://localhost:8002',  // 后端服务地址
    changeOrigin: true,
    onProxyReq: (proxyReq, req, res) => {
        // 复制请求中的 cookies（如果有）
        if (req.headers.cookie) {
            proxyReq.setHeader('Cookie', req.headers.cookie);
        }
    }
}));

app.use('/question', createProxyMiddleware({
    target: 'http://localhost:8002',  // 后端服务地址
    changeOrigin: true,
    onProxyReq: (proxyReq, req, res) => {
        // 复制请求中的 cookies（如果有）
        if (req.headers.cookie) {
            proxyReq.setHeader('Cookie', req.headers.cookie);
        }
    }
}));

app.use('/submit', createProxyMiddleware({
    target: 'http://localhost:8003',  // 后端服务地址
    changeOrigin: true,
    onProxyReq: (proxyReq, req, res) => {
        // 复制请求中的 cookies（如果有）
        if (req.headers.cookie) {
            proxyReq.setHeader('Cookie', req.headers.cookie);
        }
    }
}));

app.listen(PORT, () => {
    console.log(`Proxy server is running on http://localhost:${PORT}`);
});
