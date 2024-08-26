const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    // port: 8080,
    // host: '192.168.43.86',
    proxy: {
      "/proxy_url": {
        target: 'http://localhost:8000',
        changeOrigin: true,
        pathRewrite: {
          '^/proxy_url': '/'
        }
      }
    }
  }
})
