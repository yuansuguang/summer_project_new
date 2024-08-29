const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    // port: 8080,
    // host: '192.168.57.231',
    proxy: {
      "/proxy_url": {
        target: 'http://localhost:8000',
        // target: 'http://172.17.0.3:8000',
        changeOrigin: true,
        pathRewrite: {
          '^/proxy_url': '/'
        }
      }
    }
  },
  // configureWebpack: {
  //   optimization: {
  //     minimize: false,  // 禁用代码压缩（混淆）
  //   },
  // },
})
