<template>
  <div id="app">
    <normalPageHeader v-if="showHeader"/>
    <!-- <fillQnmyvote/> -->
    <!-- <qnCreate/> -->
    <!-- <FillInTheBlank/> -->
    <!-- <qnCollect/> -->
    <!-- <myform/> -->
    <router-view/>
    <!-- <fillQn/> -->
    <!-- <qnCreate/> -->
    <!-- <qnDataview/> -->
  </div>
</template>

<script>
import user from './storage/user';
import normalPageHeader from './components/header/normalPageHeader.vue';
// import myform from './views/qn-createpane/qnEdit.vue';
// import qnCollect from './views/qn-manage/qnCollect.vue';
// import fillQn from './views/qn-fillpane/fillQnmytest.vue'
// import qnCreate from './views/qn-createpane/qnCreate.vue'
// import qnDataview from './views/qn-data/qnTestDataview.vue'

export default {
  name: 'App',
  components:{
  normalPageHeader,
  // fillQnmyvote,
  // qnEdit,
  // qnCollect
  // SingleChoice,
  // editPageHeader,
  // myform
  // fillQn,
  // qnCreate,
  // qnDataview
  },
  data(){
    return {
      isLogin : false,
      showHeader: true,
    }
  },
  mounted(){
    const userInfo = user.getters.getUser(user.state())
    this.isLogin = !!userInfo;
    this.$router.afterEach((to) => {
      this.showHeader = to.meta.noNav;
    });
  },
}
</script>

<style>
 @media screen and (min-width: 600px) {
  #app {
    min-height: 820px;
    min-width: 1400px;
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    background-color: rgb(241, 241, 241);
    position: relative;
  }
  normalPageHeader {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    z-index: 1000;
  }
 }
router-view{
  position: center;
}
</style>
