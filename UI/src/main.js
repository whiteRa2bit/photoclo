import Vue from 'vue'
import App from './App.vue'
import Router from './router';
import VueImg from 'v-img';

Vue.config.productionTip = false;
Vue.use(VueImg);

new Vue({
  router: Router,
  render: h => h(App),
}).$mount('#app');

