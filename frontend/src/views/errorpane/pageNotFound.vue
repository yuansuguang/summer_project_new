<template>
    <div>
      <!-- 错误页面内容 -->
      <div class="error-page">
        <h1>页面访问出错</h1>
        <p>抱歉，页面访问出错了。</p>
        <button @click="refreshPage">刷新页面</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    methods: {
      // 刷新页面
      refreshPage() {
        window.location.reload();
      }
    }
  }
  </script>
  
  <style>
  .error-page {
    text-align: center;
    margin-top: 100px;
  }
  
  .error-page h1 {
    font-size: 24px;
  }
  
  .error-page p {
    font-size: 18px;
    margin-bottom: 20px;
  }
  
  .error-page button {
    padding: 10px 20px;
    font-size: 16px;
    background-color: #007bff;
    color: #fff;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  
  .error-page button:hover {
    background-color: #0056b3;
  }
  </style>
  