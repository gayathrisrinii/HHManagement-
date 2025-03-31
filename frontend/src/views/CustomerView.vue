<script setup>
import { ref } from 'vue';  
import SearchView from '@/components/searchView.vue'
import CustDashboard from '@/components/custDashboard.vue'
import CustInsights from '@/components/custInsights.vue'
import { jwtDecode } from 'jwt-decode';

const activeTab = ref('dashboard');
</script>

<template>
  <div>
    <h1>Customer Page</h1>
    <p>Welcome to the customer panel</p>
    
    <div class="nav-tabs">
      <button 
        class="btn me-2" 
        :class="{'btn-primary': activeTab === 'dashboard', 'btn-outline-primary': activeTab !== 'dashboard'}" 
        @click="activeTab = 'dashboard'">
        Dashboard
      </button>
      <button 
        class="btn me-2" 
        :class="{'btn-primary': activeTab === 'search', 'btn-outline-primary': activeTab !== 'search'}" 
        @click="activeTab = 'search'">
        Search
      </button>
      <button 
        class="btn" 
        :class="{'btn-primary': activeTab === 'insights', 'btn-outline-primary': activeTab !== 'insights'}" 
        @click="activeTab = 'insights'">
        Insights
      </button>
    </div>
    
    <div v-if="activeTab === 'dashboard'">
      <CustDashboard :customerDetails="customerDetails" />
    </div>

    <div v-if="activeTab === 'search'">
      <SearchView />
    </div>

    <div v-if="activeTab === 'insights'">
      <CustInsights :customerDetails="customerDetails" />
    </div>
  </div>
</template>

<script>
export default {
  name: 'CustomerView',
  created() {
    this.checkIfLoggedIn();
  },
  data() {
    return {
      customerDetails: {},
    };
  },
  mounted() {

  },
  methods: {
    logout() {
      localStorage.removeItem('token');
      this.$router.push('/login');
    },
    checkIfLoggedIn() {
      const token = localStorage.getItem('token');
      if (!token) {
        this.$router.push('/login');
        return;
      }
      const decoded = jwtDecode(token);
      console.log(decoded);
      if (decoded.usertype !== 'CL') {
        this.logout();
      }
      else {
        this.customerDetails = decoded;
        console.log("Customer details set:", this.customerDetails);
      }
    }
  }
}
</script>

<style>
.nav-tabs {
  margin-bottom: 20px;
}
</style>