<template>
  <div class="account"
    style=" display: flex; justify-content: center; align-items: center;  height: 100vh; background-color:azure">
    <div class="mainAccount" style="width: 1400px; height: 600px;">
      <el-tabs :tab-position="tabPosition" v-model="activeName" class="demo-tabs" @tab-click="handleClick">
        <el-tab-pane label="Account Info" name="first">
          <div class="info" style="width: 1340px; height: 600px; background-color: white; display: flex; position: relative;" :style="{
            boxShadow: `var(--el-box-shadow-light)`,
            borderRadius: `var(--el-border-radius-round)`,
          }">
            <div style="position: relative; top: 10%; left: 5%;">
              <el-avatar :size="100" :src="urlAvatar"/>
            </div>
            <div style="position: relative; top: 30%; left: -3%; display: flex; flex-direction: column; align-items: flex-start;">
              <span style="font-size: larger; margin-top: 5px; color:black;">Basic Info</span>
              <span style="font-size: large; margin-top: 10px">Username:{{ username }}</span>
              <span style="font-size: large; margin-top: 10px">Email:{{ email }}</span>
            </div>
          </div>
        </el-tab-pane>
        <el-tab-pane label="My serveys" name="second">
        <div class="info" style="width: 1340px; height: 600px; background-color: white; display: flex; position: relative;" :style="{
            boxShadow: `var(--el-box-shadow-light)`,
            borderRadius: `var(--el-border-radius-round)`,
          }">
            <div style="position: relative; top: 30%; left: 3%; display: flex; flex-direction: column; align-items: flex-start;">
              <span style="font-size: larger; margin-top: 5px; color:black;">Basic Info</span>
              <span style="font-size: large; margin-top: 10px">Username:{{ username }}</span>
              <span style="font-size: large; margin-top: 10px">Email:{{ email }}</span>
            </div>
          </div>
        </el-tab-pane>
        <el-tab-pane label="Role" name="third">Role</el-tab-pane>
        <el-tab-pane label="Task" name="fourth">Task</el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>
<script>
// import { reactive, ref, toRefs } from 'vue'

// const state = reactive({
//   urlAvatar:'https://gd-hbimg.huaban.com/568596a661d0b580c4259ca5303d1ba5c35947d619442-LB7XdX'
// })
// const {urlAvatar} = toRefs(state)

// const activeName = ref('first')
// const tabPosition = ref('top')

// const handleClick = (tab, event) => {
//   console.log(tab, event)
// }


export default {
  data() {
    return {
      username: '',
      email: '',
    }
  },
  created() {
    this.$axios({
      method: 'get',
      url: '/user/api/userinfo/',
    })
    .then(res => {
      switch (res.data.status_code) {
        case 1:
          this.username = res.data.username;
          this.email = res.data.email;
          break;
        case 2:
           // 未登录弹窗
           break;
        case 3:
           // 用户不存在
           break;
      }
    })
    .catch(err => {
      console.log(err);
    })
  }
}
</script>


<style>
.demo-tabs>.el-tabs__content {
  padding: 32px;
  color: #6b778c;
  font-size: 32px;
  font-weight: 600;
}
</style>