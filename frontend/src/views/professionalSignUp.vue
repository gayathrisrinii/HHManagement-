<script setup>
import { professionalRegister } from '@/controller/auth';
import axios from 'axios'; // Import axios for API calls
import { toast } from 'vue3-toastify';
</script>

<template>
  <div class="form-container">
    <h1 class="text-center">Professional Signup</h1>
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

      <div class="form-group">
        <label for="experience" class="form-label">Experience</label>
        <input type="text" v-model="form.experience" class="form-control" id="experience" placeholder="Enter your experience" />
        <span v-if="errors.experience" class="text-danger">{{ errors.experience }}</span>
      </div>

      <div class="form-group">
        <label for="service_name" class="form-label">Service Name</label>
        <select v-model="form.service_name" class="form-control" id="service_name">
          <option value="" disabled>Select a service</option>
          <option v-for="service in services" :key="service.id" :value="service.service_name">
            {{ service.service_name }}
          </option>
        </select>
        <span v-if="errors.service_name" class="text-danger">{{ errors.service_name }}</span>
      </div>

      <button type="submit" class="form-submit-button">Submit</button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'registerView',
  data() {
    return {
      form: {
        email: '',
        password: '',
        full_name: '',
        phone: '',
        address: '',
        pin_code: '',
        experience: '',
        service_name: ''
      },
      errors: {},
      services: [] // Add a new array to store services
    };
  },
  methods: {
    async fetchServices() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/v2/admin/get/services');
        this.services = response.data.data; // Assume the API returns an array of services
        console.log('Services:', this.services);

      } catch (error) {
        console.error('Failed to fetch services:', error);
      }
    },
    submitForm() {
      // Handle form submission
      // Example: Validate form and send data to the server
      this.errors = {}; // Clear previous errors
      // Perform validation and set errors if any
      // Send form data to the server
      //console.log(this.form); // Log form data to the console

      // Validate each field
      if (!this.form.email) {
        this.errors.email = "Email is required.";
      } else if (!/\S+@\S+\.\S+/.test(this.form.email)) {
        this.errors.email = "Invalid email format.";
      }

      if (!this.form.password) {
        this.errors.password = "Password is required.";
      } else if (this.form.password.length < 6) {
        this.errors.password = "Password must be at least 6 characters long.";
      }

      if (!this.form.full_name) {
        this.errors.full_name = "Full name is required.";
      } else if (this.form.full_name.length < 3) {
        this.errors.full_name = "Full Name must be at least 3 characters long.";
      }

      if (!this.form.phone) {
        this.errors.phone = "Phone number is required.";
      } else if (!/^\d{10}$/.test(this.form.phone)) {
        this.errors.phone = "Phone number must be 10 digits.";
      }

      if (!this.form.address) {
        this.errors.address = "Address is required.";
      } else if (this.form.address.length < 3) {
        this.errors.address = "Give proper address.";
      }

      if (!this.form.pin_code) {
        this.errors.pin_code = "Pin code is required.";
      } else if (!/^\d{6}$/.test(this.form.pin_code)) {
        this.errors.pin_code = "Pin code must be 6 digits.";
      }

      if (!this.form.experience) {
        this.errors.experience = "Experience is required.";
      } else if (isNaN(this.form.experience) || parseFloat(this.form.experience) < 0) {
        this.errors.experience = "Experience must be a valid positive number.";
      }

      if (!this.form.service_name) {
        this.errors.service_name = "Service name is required.";
      }

      // If there are validation errors, stop the form submission
      if (Object.keys(this.errors).length > 0) {
        return;
      }

      const response = professionalRegister(
        this.form.email,
        this.form.password,
        this.form.full_name,
        this.form.phone,
        this.form.address,
        this.form.pin_code,
        this.form.service_name,
        this.form.experience
      );
      response
        .then(data => {
          console.log('Registration successful:', data);
          toast.success('Registration successful! Redirecting to login page...');
          setTimeout(() => {
            this.$router.push('/login'); // Redirect to login page
          }, 3000);
        })
        .catch(error => {
          console.error('Registration failed:', error);
        });
    }
  },
  mounted() {
    this.fetchServices(); // Fetch services when the component is mounted
  }
};
</script>