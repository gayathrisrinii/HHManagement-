<script setup>
import {customerRegister} from '@/controller/auth'
import { toast } from 'vue3-toastify';

</script>

<template>
  <div class="form-container">
    <h1 class="text-center">Customer Signup</h1>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="email">Email</label>
        <input type="email" v-model="form.email" class="form-control" id="email" placeholder="Enter your email" />
        <span v-if="errors.email" class="text-danger">{{ errors.email }}</span>
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input type="password" v-model="form.password" class="form-control" id="password" placeholder="Enter your password" />
        <span v-if="errors.password" class="text-danger">{{ errors.password }}</span>
      </div>
      <div class="form-group">
        <label for="full_name" class="form-label">Full Name</label>
        <input type="text" v-model="form.full_name" class="form-control" id="full_name" placeholder="Enter your full name" />
        <span v-if="errors.full_name" class="text-danger">{{ errors.full_name }}</span>
      </div>
      <div class="form-group">
        <label for="phone" class="form-label">Phone</label>
        <input type="text" v-model="form.phone" class="form-control" id="phone" placeholder="Enter your phone number" />
        <span v-if="errors.phone" class="text-danger">{{ errors.phone }}</span>
      </div>
      <div class="form-group">
        <label for="address" class="form-label">Address</label>
        <input type="text" v-model="form.address" class="form-control" id="address" placeholder="Enter your address" />
        <span v-if="errors.address" class="text-danger">{{ errors.address }}</span>
      </div>
      <div class="form-group">
        <label for="pin_code" class="form-label">Pin Code</label>
        <input type="text" v-model="form.pin_code" class="form-control" id="pin_code" placeholder="Enter your pin code" />
        <span v-if="errors.pin_code" class="text-danger">{{ errors.pin_code }}</span>
      </div>
      <button type="submit" class="form-submit-button">Submit</button>
    </form>
  </div>
</template>

/* eslint-disable */
<script>
export default {
  name: 'registerView',
  // eslint-disable-next-line no-unused-vars
  data() {
  
    return {
      form: {
        email: '',
        password: '',
        full_name: '',
        phone: '',
        address: '',
        pin_code: ''
      },
      errors: {}
    };
  },
  methods: {
    submitForm() {
      this.errors = {}; // Clear previous errors

      // Validate email
      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!this.form.email) {
        this.errors.email = "Email is required.";
      } else if (!emailPattern.test(this.form.email)) {
        this.errors.email = "Please enter a valid email address.";
      }

      // Validate password
      if (!this.form.password) {
        this.errors.password = "Password is required.";
      } else if (this.form.password.length < 6) {
        this.errors.password = "Password must be at least 6 characters long.";
      }

      // Validate full name
      if (!this.form.full_name) {
        this.errors.full_name = "Full Name is required.";
      } else if (this.form.full_name.length < 3) {
        this.errors.full_name = "Full Name must be at least 3 characters.";
      }

      // Validate phone
      const phonePattern = /^[0-9]{10}$/;
      if (!this.form.phone) {
        this.errors.phone = "Phone number is required.";
      } else if (!phonePattern.test(this.form.phone)) {
        this.errors.phone = "Phone number must be 10 digits.";
      }

      // Validate address
      if (!this.form.address) {
        this.errors.address = "Address is required.";
      } else if (this.form.address.length < 3) {
        this.errors.address = "Give proper address.";
      }

      // Validate pin code
      const pinCodePattern = /^[0-9]{6}$/;
      if (!this.form.pin_code) {
        this.errors.pin_code = "Pin Code is required.";
      } else if (!pinCodePattern.test(this.form.pin_code)) {
        this.errors.pin_code = "Pin Code must be 6 digits.";
      }

      // If there are validation errors, stop the form submission
      if (Object.keys(this.errors).length > 0) {
        return;
      }

      const response = customerRegister(this.form.email, this.form.password, this.form.full_name, this.form.phone, this.form.address, this.form.pin_code);
      response.then(data => {
        

        console.log('Registration successful:', data);
      
      this.$router.push('/login');
      toast('Registration successful!', { type: 'success' });

      }).catch(error => {
        console.error('Registration failed:', error);

      });
  
    }
  }
}
</script>