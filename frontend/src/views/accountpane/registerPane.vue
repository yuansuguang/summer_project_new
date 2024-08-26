<template>
  <div class="register"
    style=" display: flex; justify-content: center; align-items: center;  height: 98vh; background-color:azure;">
    <div class="mainReg"
      style="width: 1000px; height: 500px; border-radius: 10px; background-color: transparent;display: flex;flex-direction: row; align-items: center;"
      :style="{
        boxShadow: `var(--el-box-shadow-dark)`
      }">
      <span>&emsp;</span>
      <span>&emsp;</span>
      <img style="width: 400px; height: 400px" src="@/assets/images/pic1.png" />
      <span>&emsp;</span>
      <span>&emsp;</span>

      <span>&emsp;</span>
      <div
        style="display: flex; align-items: center; height: 500px; width: 600px; background-color: #ffffff; border-top-right-radius: 10px;border-bottom-right-radius: 10px;"
        :style="{
          boxShadow: `var(--el-box-shadow-dark)`,
        }">
        <el-container>
          <el-header style="font-family: 'JinBuTi'; color:#000000; font-size: 20px">
            <h1>注册</h1>
          </el-header>
          <el-main style="display: flex; justify-content: center;">
            <el-form ref="ruleForm" style="max-width: 1000px " :model="ruleForm" status-icon :rules="rules"
              size="default" label-width="auto" class="registerForm">
              <el-form-item label="用户名" prop="user">
                <el-input v-model="ruleForm.user" type="username" autocomplete="off" />
              </el-form-item>
              <el-form-item label="密码" prop="pass">
                <el-input v-model="ruleForm.pass" type="password" autocomplete="off" style="width: 300px;" />
              </el-form-item>
              <el-form-item label="确认密码" prop="checkPass">
                <el-input v-model="ruleForm.checkPass" type="password" autocomplete="off" />
              </el-form-item>
              <el-form-item label="邮箱" prop="phone">
                <el-input v-model="ruleForm.phone" type="phone" autocomplete="off" />
                <!-- v-model.number="ruleForm.phone" -->
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="register('ruleForm')">
                  注册
                </el-button>
                <el-button @click="resetForm(ruleFormRef)">重置</el-button>
              </el-form-item>
            </el-form>
          </el-main>

        </el-container>
      </div>
    </div>
  </div>
</template>

<script>
// import { ref } from 'vue'

export default {
  data() {
    // var ruleFormRef = ref()

    var validateUser = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('用户名不能为空'))
      } else {
        callback()
      }
    }
    var validatePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('Please input the password'))
      } else {
        var reg_pwd = /^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{8,18}$/;
        if (!reg_pwd.test(value)) {
          callback(new Error('密码至少同时包含字母和数字，且长度为8-18'));
        } else {
          if (this.ruleForm.checkPass !== '') {
            this.$refs.ruleForm.validateField('checkPass');
          }
          callback();
        }
      }
    }

    var validatePass2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请重新输入密码'))
      } else if (value !== this.ruleForm.pass) {
        callback(new Error("密码输入不匹配"))
      } else {
        callback()
      }
    }

    var validatePhone = (rule, value, callback) => {
      // if (!value) {
      //   return callback(new Error('Please input the phone number'))
      // }
      // setTimeout(() => {
      //   if (!Number.isInteger(value)) {
      //     callback(new Error('Please input digits'))
      //   } else {
      //     if (value < 10000000000) {
      //       callback(new Error('Phone number must be 1XXXXXXXXXX'))
      //     } else if (value >= 20000000000) {
      //       callback(new Error('Phone number must be 1XXXXXXXXXX'))
      //     }
      //     else {
      //       callback()
      //     }
      //   }
      // }, 1000)
      callback()
    }

    // var rules = reactive({
    //   user: [{ validator: validateUser, trigger: 'blur' }],
    //   pass: [{ validator: validatePass, trigger: 'blur' }],
    //   checkPass: [{ validator: validatePass2, trigger: 'blur' }],
    //   phone: [{ validator: validatePhone, trigger: 'blur' }],
    // })

    // var submitForm = (formEl) => {
    //   if (!formEl) return
    //   formEl.validate((valid) => {
    //     if (valid) {
    //       console.log('submit!')
    //     } else {
    //       console.log('error submit!')
    //     }
    //   })
    // }

    // var resetForm = (formEl) => {
    //   if (!formEl) return
    //   formEl.resetFields()
    // }

    return {
      ruleForm: {
        user: '',
        pass: '',
        checkPass: '',
        phone: ''
      },
      rules: {
        user: [{ validator: validateUser, trigger: 'blur' }],
        pass: [{ validator: validatePass, trigger: 'blur' }],
        checkPass: [{ validator: validatePass2, trigger: 'blur' }],
        phone: [{ validator: validatePhone, trigger: 'blur' }],
      }
    }
    // var rules = reactive({
    //   user: [{ validator: validateUser, trigger: 'blur' }],
    //   pass: [{ validator: validatePass, trigger: 'blur' }],
    //   checkPass: [{ validator: validatePass2, trigger: 'blur' }],
    //   phone: [{ validator: validatePhone, trigger: 'blur' }],
    // })

    // var submitForm = (formEl) => {
    //   if (!formEl) return
    //   formEl.validate((valid) => {
    //     if (valid) {
    //       console.log('submit!')
    //     } else {
    //       console.log('error submit!')
    //     }
    //   })
    // }

    // var resetForm = (formEl) => {
    //   if (!formEl) return
    //   formEl.resetFields()
    // }
  },
  methods: {
    resetForm(formEl){
      if (!formEl) return
      formEl.resetFields()
    },
    register: function (formName) {
      console.log("using function");

      const self = this;
      const formData = new FormData();
      formData.append("username", self.ruleForm.user);
      formData.append("password1", self.ruleForm.pass);
      formData.append("password2", self.ruleForm.checkPass);
      formData.append("email", self.ruleForm.phone);

      console.log('step 1 success');

      this.$refs[formName].validate((valid) => {
        if (valid) {
          self.$axios({
            method: 'post',
            url: '/user/api/register/',
            data: formData,
          })
            .then(res => {
              switch (res.data.status_code) {
                case 1:
                  this.$store.dispatch('saveUserInfo', {
                    user: {
                      'username': this.ruleForm.username,
                      'confirmed': false,
                    }
                  });
                  this.$message.success('注册成功！');
                  setTimeout(() => {
                    this.$router.push('/login');
                  }, 1500);
                  break;
                case -1:
                  this.$message.warning('请检查填写的内容！');
                  break;
                case 2:
                  this.$message.warning('用户名已注册！');
                  break;
                case 3:
                  this.$message.error('邮箱已注册或不可用！');
                  break;
                case 4:
                  this.$message.error('密码不符合规则，需满足8-18，英文字母+数字！');
                  break;
                case 5:
                  this.$message.error('两次输入的密码不一致！');
                  break;
                case 6:
                  this.$message.error('邮件验证码发送失败，请检查邮箱是否填写正确！');
                  break;
              }
            })
            .catch(err => {
              console.log(err);
            })
        } else {
          console.log('提交失败!!');
          return false;
        }
      });
    }
  }
}



</script>

<style scoped>
.register {
  background-image: url('@/assets/images/background1.png')
}

/* .register .mainReg {
  border: 1px solid var(--el-border-color);
} */
</style>