<template>
    <div class="container">
      <!-- <div class="header">
        <img src="@/assets/images/mylogo.png" alt="Logo" class="logo">
        <div class="buttons">
          <button class="nav-button" @click="navigate('personal')">个人首页</button>
          <button class="nav-button" @click="navigate('applications')">应用展示</button>
          <button class="nav-button" @click="navigate('samples')">样本服务</button>
          <button class="nav-button" id="surveyTemplateBtn" @click="navigate('surveys')">问卷模板</button>
          <button class="nav-button" @click="navigate('solutions')">解决方案</button>
        </div>
        <div class="auth">
            <button @click="gotoregister" class="register-button">注册</button>
            <button @click="gotologin" class="login-button">登录</button>
        </div>
      </div> -->
      <div class="content">
        <div class="scrolling-text">{{ scrollingText }}</div>
        <div class="statistics">问卷星球平台上累计发布问卷{{releaseNum}}份，回收答卷{{recycleNum}}份</div>
        <el-row><span>&emsp;</span></el-row>
        <el-row><span>&emsp;</span></el-row>
        <el-row><span>&emsp;</span></el-row>
        <el-row><span>&emsp;</span></el-row>
        <el-row><span>&emsp;</span></el-row>
        <el-row><span>&emsp;</span></el-row>
        <el-row><span>&emsp;</span></el-row>
        <el-row><span>&emsp;</span></el-row>
        <el-row><span>&emsp;</span></el-row>
        <div class="content-buttons">
          <button @click="gotologin" class="function-button"> 即刻体验</button> 
        </div>
      </div>
      <div class="footer">
        <!-- <button class="feedback-button">填写客户反馈</button> -->
      </div>
    </div>
  </template>
  
  <script>
  import user from "@/storage/user"
  export default {
    name: 'HomePage',
    data() {
      return {
        releaseNum:114514,
        recycleNum:1919810,
        scrollingText: "海量问卷随你选！！",
        scrollingTextIndex: 0,
        scrollingTexts: [
          "不止调查 | 考试 | 测评",
          "在线编辑，成为您的好助手！",
          "登录享受更多功能！"
        ]
      }
    },
    mounted() {
      setInterval(this.changeScrollingText, 5000);
    },
    methods: {
      gotostart(){
        this.$router.push('/questionairemanage');
      },
      navigate(page) {
        // 在此处处理页面导航逻辑
        console.log("Navigating to " + page);
      },
      changeScrollingText() {
        this.scrollingTextIndex = (this.scrollingTextIndex + 1) % this.scrollingTexts.length;
        this.scrollingText = this.scrollingTexts[this.scrollingTextIndex];
      },
      gotologin() {
        console.log(document.cookie);
        const userInfo = user.getters.getUser(user.state());
        console.log(userInfo);
        console.log(this.isLogin);
        if (userInfo) {
          console.log(document.cookie);
          this.$router.push('questionairemanage');
        }
        else {
          this.$router.push('/login');
          console.log("login!");
        }
      },
      gotoregister() {
        this.$router.push('/register');
        console.log("register!");
      }
    }
  }
  </script>
  
  <style scoped>
  body {
    background-image: url('@/assets/images/mainPaneBackground.png');
    /* background-size: cover; */
    /* background-repeat: no-repeat; */
  }

  .container {
    display: flex;
    min-height: 98vh;
    flex-direction: column;
    align-items: center;
    background-image: url('@/assets/images/background3.jpg');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
  }
  
  .content {
    margin-top: 200px;
    /* margin-left: 20px; */
  }

  .content button{
    font-size: 30px; /* 按钮字体大小 */
    background-color: transparent;
    border: none;
    cursor: pointer;
    color: #fff; 
    border: 2px solid #fff; 
    border-radius: 5px; 
    font-family: 'JinBuTi';
  }

  .scrolling-text{
    font-family: 'JinBuTi';
    font-size: 90px;
    margin-bottom: 50px;
    text-align: center;
    color: #fff;
  }

  .statistics{
    margin-bottom: 50px;
    text-align: center;
    font-size: 20px;
    font-family: 'JinBuTi';
    color: #fff;
  }
  
  .footer {
    margin-top: auto;
    margin-left: 1200px;
    margin-bottom: 20px;
    border-bottom: 10px;
  }
  
  /* .feedback-button {
    padding: 10px 20px;
    background-color: #007bff;
    color: #fff;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    
  } */
  </style>
  