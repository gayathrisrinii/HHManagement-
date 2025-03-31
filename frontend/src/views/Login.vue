<script setup>
import { login } from '@/controller/auth'
import { toast } from 'vue3-toastify';
import {jwtDecode} from 'jwt-decode';


</script>
<template>
  <div class="form-container">
    <h1 class="text-center">Login</h1>
    <form @submit.prevent="submit_login">
      <div class="form-group">
        <label for="email">Email address</label>
        <input type="email" class="form-control" id="email" v-model="email" placeholder="Enter your email" />
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input type="password" class="form-control" id="password" v-model="password" placeholder="Enter your password" />
      </div>
      <div class="form-group">
        <label for="usertype">User Type</label>
        <select class="form-control" id="usertype" v-model="usertype">
          <option value="AL">Admin</option>
          <option value="PL">Professional</option>
          <option value="CL">Customer</option>
        </select>
      </div>
      <button type="submit" class="form-submit-button">Submit</button>
    </form>
  </div>
</template>

<script >


export default {
  name: 'LoginView',
  data() {
    return {
      email: '',
      password: '',
      usertype: ''
    };
  },
  created() {
    const token = localStorage.getItem('token');
    if (token) {
      const decoded = jwtDecode(token);
      if (decoded.usertype === 'CL') {
        this.$router.push('/customer');
      }
      else if(decoded.usertype === 'AL'){
        this.$router.push('/admin');
      }
      else if(decoded.usertype === 'PL'){
        this.$router.push('/professional');
      }
    }
  },
  methods: {
    async submit_login() {
      // Implement login logic here
 
      try {
        const response = await login(this.email, this.password, this.usertype);
        console.log('API Response:', response)
        if(response.isSuccess) {
          console.log('Login successful:', response,response.data.usertype=='CL');
          toast('Login successful', { type: 'success' });
          this.$emit('login'); // Emit login event
          if (response.data.usertype == 'AL') {
            this.$router.push('/admin');
          } else if (response.data.usertype == 'CL') {
            console.log('Customer login');
            this.$router.push('/customer');
          } else if (response.data.usertype == 'PL') {
            this.$router.push('/professional');
          } else {
            console.error('User type not recognized:', response.data.usertype);
            toast('User type not recognized', { type: 'error' });
          }
        } else {
          console.error('Login failed:', response.message);
          console.log(this.email, this.password, this.usertype)
          toast('Login failed: ' + response.message, { type: 'error' });
        }
      } catch (error) {
        if (error.response && error.response.status === 401) {
          toast(error.response.data.message, { type: 'error' });
        } else {
          console.error('Login error:', error);
          toast('An error occurred during login.'+error.message, { type: 'error' });
        }
      }
    }
  },
  mounted() {
    const urlParams = new URLSearchParams(window.location.search);
    const type = urlParams.get('type');
    if (type) {
      this.usertype = type;
    }
  }
}
</script>