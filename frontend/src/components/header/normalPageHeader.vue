<template>
  <div class="header">
    <div class="home" @click="handleClick(1)" style="position: relative; cursor: pointer;">
      <img src="@/assets/images/mylogo1.png" alt="Logo" class="logo">
      <span style="font-family: 'JinBuTi'; font-size: 20px; top: -17px; position: relative; right:27px;">问卷星球</span>
    </div>
    <!-- <el-menu :default-active="activeIndex2" class="el-menu-demo" mode="horizontal" background-color="#000000"
      text-color="#fff" active-text-color="#C0C0C0" @select="handleSelect">
      <el-menu-item index="1">Processing Center</el-menu-item>
      <el-sub-menu index="2">
        <template #title>Workspace</template>
        <el-menu-item index="2-1">item one</el-menu-item>
        <el-menu-item index="2-2">item two</el-menu-item>
        <el-menu-item index="2-3">item three</el-menu-item>
        <el-sub-menu index="2-4">
          <template #title>item four</template>
          <el-menu-item index="2-4-1">item one</el-menu-item>
          <el-menu-item index="2-4-2">item two</el-menu-item>
          <el-menu-item index="2-4-3">item three</el-menu-item>
        </el-sub-menu>
      </el-sub-menu>
      <el-menu-item index="3" disabled>Info</el-menu-item>
      <el-menu-item index="4">Orders</el-menu-item>
    </el-menu> -->
    <el-dropdown>
      <el-button type="primary" color="white" size="default" style="font-size: 17px; margin-left: 10px; font-family: 'JinBuTi';">
        核心功能<el-icon style="vertical-align: middle"><ArrowDown /></el-icon>
      </el-button>
      <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item @click="handleClick(6)" style=" height: 30px; font-size: 15px;">问卷广场</el-dropdown-item>
          <el-dropdown-item @click="handleClick(2)" style=" height: 30px; font-size: 15px;">创建问卷</el-dropdown-item>
    <!-- <el-dropdown-item>Action 4</el-dropdown-item>
          <el-dropdown-item>Action 5</el-dropdown-item> -->
    </el-dropdown-menu>
      </template>
    </el-dropdown>
    <el-dropdown>
      <el-button type="primary" color="white" size="default" style="font-size: 17px; margin-left: 10px; font-family: 'JinBuTi';">
        个人中心<el-icon style="vertical-align: middle"><ArrowDown /></el-icon>
      </el-button>
      <template #dropdown>
        
        <el-dropdown-menu style=" display: flex; flex-direction: column; align-items: center; align-content: center;">
          <el-dropdown-item @click="handleClick(4)" style=" height: 30px; font-size: 15px;">问卷管理</el-dropdown-item>
          <el-dropdown-item @click="handleClick(4)" style=" height: 30px; font-size: 15px;">我的收藏</el-dropdown-item>
           <el-dropdown-item @click="handleClick(5)" style=" height: 30px; font-size: 15px;">回收空间</el-dropdown-item>
    <!-- <el-dropdown-item>Action 4</el-dropdown-item>
          <el-dropdown-item>Action 5</el-dropdown-item> -->
    </el-dropdown-menu>
      </template>
    </el-dropdown>
    <div class="auth1" v-if="!isLogin">
      <el-button class="loginButton" @click="gotologin" size="default" color="#626aef" :dark="isDark">登录</el-button>
      <el-button class="registerButton" @click="gotoregister" size="default" color="#626aef" :dark="isDark" plain>注册</el-button>
    </div>

    <el-tour v-model="open">
      <el-tour-step
        title="尚未登录"
        description="这些功能需要您登录后才能使用"
      />
      <el-tour-step
        title="用户未登录"
        description="登录后可以进行相应操作"
        :target="loginButton"
        placement="bottom"
      />
      <el-tour-step
        title="还没有账号？"
        description="点击注册按钮，注册账号"
        :target="registerButton"
        placement="bottom"
      />
    </el-tour>

    <div class="auth2" v-if="isLogin">
      <el-dropdown>
        <el-avatar :size="45">
          <img src="@/assets/images/avator1.jpg"/>
        </el-avatar>
        <template #dropdown>
          <div style="min-width: 200px;max-height: 150px; display: flex; flex-direction: column; align-items: center">
            <el-span style="font-size: 30px; margin-top: 20px; font-family: 'JinBuTi'; color: pink;">{{ userName }}</el-span>
            <el-span style="margin-top: 20px; font-size: 15px; align-self: self-start;">&emsp;邮箱：</el-span>
            <el-span style="margin-top: 5px; font-size: 15px; align-self: self-start; margin-bottom: 10px">&emsp;{{ mailbox }}</el-span>
          </div>
        </template>
      </el-dropdown>
      
      <!-- <el-span>&emsp;{{ userName }}&emsp;&emsp;&emsp;</el-span> -->
      <el-button @click="gotologout" size="default" link style="margin-left: 30px;">登出</el-button>
    </div>
  </div>
</template>

<script>
import user from "@/storage/user"

export default {
  name: 'normalPageHeader',
  data() {
    return {
      open: false,
      userName: '我爱软工',
      activeIndex: '1',
      mailbox:'fuckSE@buaa.edu.cn',
      isLogin: false,
      loginButton: '.loginButton',
      registerButton: '.registerButton',
    };
  },
  created() {
    const userInfo = user.getters.getUser(user.state());
    console.log(userInfo);
    console.log(this.isLogin);
    if (userInfo) {
      console.log('enter');
      this.isLogin = true;
      this.userName = userInfo.user.username;
    }
  },

  methods: {
    handleClick(key) {
      if (this.isLogin) {
        switch (key) {
          case 1:
            this.gobacktoHome();
            break;
          case 2:
            this.gotoqnCreate();
            break;
          case 3:
            this.gotoaccountCenter();
            break;
          case 4:
            this.gotoqnManage();
            break;
          case 5:
            this.gotoqnManage();
            break;
          case 6:
            this.gotoSquare();
            break;
          default:
            console.log('error');
            break;
        }
      } else {
        this.open = true;
      }
    },
    handleSelect(key, keyPath) {
      console.log(key, keyPath)
    },
    gobacktoHome: function () {
      this.$router.push('/');
    },
    gotoaccountCenter() {
      this.$router.push('/accountCenter');
    },
    gotologin() {
      this.$router.push('/login');
      console.log("login!");
    },
    gotoregister() {
      this.$router.push('/register');
      console.log("register!");
    },
    gotoqnManage() {
      this.$router.push('/questionairemanage');
      console.log("manage!");
    },
    gotoqnCreate() {
      this.$router.push('/questionaireCreate');
    },
    gotoCollect() {
      this.$router.push('/questionaireCollect');
    },
    gotoRecycle(){
      this.$router.push('/questionaireRecycle');
    },
    gotoSquare(){
     this.$router.push('/questionnaireSquare');
      
    },
    gotologout() {
      // this.isLogin = false;
      // this.userName = '
      this.$axios({
        method: 'get',
        url: '/user/api/logout/',
        // data: formData,
      }).then(res => {
        switch (res.data.status_code) {
          case 200:
            this.$store.dispatch('clear');
            console.log('run')
            location.reload();
            break;
          case 401:
            // this.$message.error('not logged in');
            // console.log(this.isLogin);
            this.$store.dispatch('clear');
            location.reload();
            break;
        }
      }).catch(err => {
        console.log(err);
      });
      this.$router.push('/');
    }
  }
}
</script>

<style>
.header {
  display: flex;
  align-items: center;
  /* justify-content: space-between; */
  width: 100%;
  padding: 10px;
  margin-top: -8px;
  background-color: white;
  /* position: relative; */
  position: fixed;
  z-index: 10;
  /* 确保头部在其他内容上方 */
}

.logo {
  width: 50px;
  height: 50px;
  margin-right: 30px;
}

.buttons {
  display: flex;
}

.buttons button {
  margin-right: 10px;
}


.auth1 {
  display: flex;
  position: absolute;
  top: 25%;
  right: 5%;
}

.auth2 {
  display: flex;
  position: absolute;
  align-items: center;
  top: 25%;
  right: 5%;
}

.nav-button {
  padding: 10px 20px;
  font-size: 22px;
  background-color: transparent;
  border: none;
  cursor: pointer;
  color: #fff;
  transition: color 0.3s;
}

.nav-button:hover {
  color: blue;
}
</style>