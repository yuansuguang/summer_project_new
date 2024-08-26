<template>
  <div class="login">
    <!-- <div ref="vantaRef" style="width: 100%; height: 100vh"></div> -->
    <div class="mainLogin"
      style="width: 800px; height: 500px; border-radius: 10px; background-color: transparent;display: flex;flex-direction: row; align-items: center;"
      :style="{
        boxShadow: `var(--el-box-shadow-dark)`,
        borderRadius: `var(--el-border-radius-round)`,
      }">
      <span>&emsp;</span>
      <span>&emsp;</span>
      <img style="width: 400px; height: 400px" src="@/assets/images/pic1.png" />
      <span>&emsp;</span>
      <span>&emsp;</span>

      <span>&emsp;</span>

      <div style="display: flex; align-items: center; height: 500px; width: 400px; background-color: #ffffff; border-top-right-radius: 10px;border-bottom-right-radius: 10px;" :style="{
            boxShadow: `var(--el-box-shadow-dark)`,
          }">
        <el-container>
          <el-header style="font-family: 'JinBuTi'; color:#000000; font-size: 20px">
            <h1>登录</h1>
          </el-header>
          <el-main style="display: flex; justify-content: center;" >
            <el-form ref="loginForm" style="max-width: 400px; " :model="loginForm" status-icon :rules="loginRules"
              size="default" label-width="auto" class="loginForm">
              <el-form-item label="用户名" prop="user">
                <el-input v-model="loginForm.user" autocomplete="off" />
              </el-form-item>
              <el-form-item label="密码" prop="pass">
                <el-input v-model="loginForm.pass" type="password" autocomplete="off" />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="login()">
                  登录
                </el-button>
              </el-form-item>
            </el-form>
          </el-main>
        </el-container>
      </div>
    </div>
  </div>

</template>

<script>
// import * as THREE from "three";
// import WAVES from "vanta/src/vanta.waves";
// import { VANTA } from "vanta";
export default {
  data() {
    return {
      loginForm: {
        user: '',
        pass: '',
      },

    };
  },
  // mounted() {
  //   this.vantaEffect = WAVES({
  //     el: this.$refs.vantaRef,
  //     THREE: THREE,
  //   });
  //   VANTA.WAVES({
  //     el: this.$refs.vantaRef,
  //     /*以下为样式配置*/
  //     mouseControls: true,
  // touchControls: true,
  // gyroControls: false,
  // minHeight: 200.00,
  // minWidth: 200.00,
  // scale: 1.00,
  // scaleMobile: 1.00,
  // color: 0x17a4ae,
  // waveSpeed: 0.95
  //   });
  // },
  // beforeDestroy() {
  //   if (this.vantaEffect) {
  //     this.vantaEffect.destroy();
  //   }
  // },
  methods: {
    // login() {
    //   // 在这里执行登录操作，可以发送请求到后端验证用户身份，可以留到后端实现的时候再弄
    //   // 此处为示例，仅在控制台输出用户名和密码
    //   const self = this;
    //   const formData = new FormData();
    //   formData.append("username", self.username);
    //   formData.append("password", self.password);

    //   self.$axios({
    //     method: 'post',
    //     url: '/user/api/login/',
    //     data: formData,
    //   }).then(res => {
    //     switch (res.data.status_code) {
    //       case 1:
    //         this.$store.dispatch('saveUserInfo', {user: {
    //             'username': this.form.username,
    //             'confirmed': true,
    //           }});
    //         this.$message.success('登录成功！');
    //         break;
    //       case 2:
    //         this.$message.success('already logged in');
    //         break;
    //       case 3:
    //         this.$message.success('username not found');
    //         break;
    //       case 4:
    //         this.$message.success('unverified account');
    //         break;
    //       case 5:
    //         this.$message.success('wrong password');
    //         break;
    //       case -1:
    //         this.$message.success('sys error');
    //         break;
    //     }
    //   })
    //   .catch(err => {
    //       console.log(err);
    //     })
    //   console.log('用户名：', this.username);
    //   console.log('密码：', this.password);
    //   // 登录成功后可以进行页面跳转或其他操作
    // }
    login() {
      // 此处修正为访问loginForm的属性
      const formData = new FormData();
      formData.append("username", this.loginForm.user);
      formData.append("password", this.loginForm.pass);

      this.$axios({
        method: 'post',
        url: '/user/api/login/',
        data: formData,
      }).then(res => {
        switch (res.data.status_code) {
          case 1:
            this.$store.dispatch('saveUserInfo', {
              user: {
                'username': this.loginForm.user,
                'confirmed': true,
              }
            });
            this.$message.success('登录成功！');
            this.$router.push('/');
            break;
          case 2:
            break;
          case 3:
            break;
          case 4:
            break;
          case 5:
            break;
          case -1:
            break;
        }
      }).catch(err => {
        console.log(err);
      });
      console.log('用户名：', this.loginForm.user);  // 修改为loginForm.user
      console.log('密码：', this.loginForm.pass);   // 修改为loginForm.pass
      // 登录成功后可以进行页面跳转或其他操作
    }
  }
};
</script>

<style scoped>
.login {
  background-image: url('@/assets/images/background1.png');
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: row;
  height: 98vh;
}

.login-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
}

input[type="text"],
input[type="password"] {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 3px;
}

button {
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
</style>