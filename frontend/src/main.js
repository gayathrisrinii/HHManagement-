import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"
import Vue3Toastify  from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';

createApp(App).use(router).use(Vue3Toastify,
    {
      autoClose: 3000,
      // Add the following options as needed
      position: "bottom-right",
      draggable: true,
    }).mount('#app')
