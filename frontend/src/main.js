// import Vue from 'vue';
// import App from './App.vue';
// import router from '@/router/index.js';

// import { createApp } from 'vue' // 代替 import Vue from 'vue' 
// import App from './App'
// import router from './router'

// Vue.config.productionTip = false;

// new Vue({
//   router,
//   render: h => h(App)
// }).$mount('#app');


import { createApp } from 'vue'
import App from './App'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElIcon from '@element-plus/icons-vue'
import "@/assets/font/font.css";
import store from './storage/index'
 
import axios from 'axios'

const app = createApp(App)
app.use(ElementPlus, { size: 'small', zIndex: 3000 })
app.use(router)
app.use(store)
app.config.productionTip = false
app.config.globalProperties.$axios = axios;
axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://localhost:8000'
app.mount('#app')
Object.keys(ElIcon).forEach((key) => {
  app.component(key, ElIcon[key])
})

export default axios;

// Vue.prototype.$axios = axios

