import Vue from 'vue'
import App from './App.vue'
import router from './router'
import './plugins/element.js'
import './assets/css/global.css'
import ElementUI from 'element-ui'   
import axios from 'axios'
import 'element-ui/lib/theme-chalk/index.css'   //引用 element-ui 样式

Vue.use(ElementUI)  //最后要use ElementUI ，不然会报错
Vue.config.productionTip = false

axios.defaults.baseURL = 'http://127.0.0.1:8010'
Vue.prototype.$http = axios
Vue.prototype.$my_window = window.sessionStorage


new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
