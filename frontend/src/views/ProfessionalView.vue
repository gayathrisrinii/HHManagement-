<script setup>
import { ref } from 'vue';  
import SearchView from '@/components/searchView.vue';
import ProfDashboard from '@/components/profDashboard.vue';
import ProfInsights from '@/components/profInsights.vue';
import { jwtDecode } from 'jwt-decode';

const activeTab = ref('dashboard');
</script>

<template>
  <div>
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
      <ProfDashboard :professionalDetails="professionalDetails" />
    </div>

    <div v-if="activeTab === 'search'">
      <SearchView />
    </div>

    <div v-if="activeTab === 'insights'">
      <ProfInsights :professionalDetails="professionalDetails" />
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProfessionalView',
  created() {
    this.checkIfLoggedIn();
  },
  data() {
    return {
      professionalDetails: {},
    };
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
      if (decoded.usertype !== 'PL') {
        this.logout();
      } else {
        this.professionalDetails = decoded;
        console.log("Professional details set:", this.professionalDetails);
      }
    }
  }
};
</script>

<style>
.nav-tabs {
  margin-bottom: 20px;
}
</style>