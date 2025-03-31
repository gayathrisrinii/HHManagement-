<template>
  <div class="form-container">
    <h1 class="text-center">Register</h1>
    <form @submit.prevent="login">
      <div class="form-group">
        <label for="email">Email address</label>
        <input type="email" class="form-control" id="email" v-model="email" placeholder="Enter your email" />
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input type="password" class="form-control" id="password" v-model="password" placeholder="Enter your password" />
      </div>
      <button type="submit" class="form-submit-button">Submit</button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'registerView',
};
</script>