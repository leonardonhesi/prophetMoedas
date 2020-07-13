import Vue from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify';
import VueSocketIO from 'vue-socket.io'
import SocketIO from "socket.io-client"
//  connection: SocketIO('http://127.0.0.1:5000'),
Vue.config.productionTip = false

Vue.use(new VueSocketIO({
  debug: false,
  connection: SocketIO('https://prophetdata.herokuapp.com'),
  vuex: {
      store,
      actionPrefix: 'SOCKET_',
      mutationPrefix: 'SOCKET_'
  }
}))

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
