<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { addServices } from '@/controller/admin';
import { toast } from 'vue3-toastify';
import DataView from '@/components/dataView.vue';
import ReportView from '@/components/ReportView.vue';
import ProfView from '@/components/ProfView.vue';
import AdminInsights from '@/components/adminInsights.vue'

const users = ref([]);
const activeTab = ref('profile');

onMounted(async () => {
  try {
    const response = await axios.get('https://api.example.com/users');
    users.value = response.data;
  } catch (error) {
    console.error('Error fetching users:', error);
  }
});
</script>
<template>
  <div>
    <div class="nav-tabs">
      <button 
        class="btn me-2" 
        :class="{'btn-primary': activeTab === 'profile', 'btn-outline-primary': activeTab !== 'profile'}" 
        @click="activeTab = 'profile'">
        Prof Status
      </button>
      <button 
        class="btn me-2" 
        :class="{'btn-primary': activeTab === 'data', 'btn-outline-primary': activeTab !== 'data'}" 
        @click="activeTab = 'data'">
        Search
      </button>
      <button 
        class="btn me-2" 
        :class="{'btn-primary': activeTab === 'service', 'btn-outline-primary': activeTab !== 'service'}" 
        @click="activeTab = 'service'">
        Service
      </button>
      <button 
        class="btn me-2" 
        :class="{'btn-primary': activeTab === 'insights', 'btn-outline-primary': activeTab !== 'insights'}" 
        @click="activeTab = 'insights'">
        Insights
      </button>
      <button 
        class="btn" 
        :class="{'btn-primary': activeTab === 'report', 'btn-outline-primary': activeTab !== 'report'}" 
        @click="activeTab = 'report'">
        Report
      </button>
    </div>
    
    <div v-if="activeTab === 'profile'">
      <ProfView />
      <!-- Add profile content here -->
      
    </div>

    <div v-if="activeTab === 'service'">
      <h2>Service</h2>
      <div class="form-container">
        <h2 class="text-xl font-bold mb-4">Add New Service</h2>
        <form @submit.prevent="serviceFormSubmit">
          <div class="form-group">
            <label for="serviceName">Service Name</label>
            <input
              v-model="form.service_name"
              type="text"
              id="serviceName"
              placeholder="Enter service name"
              required
            />
          </div>
          <div class="form-group">
            <label for="description">Description</label>
            <textarea
              v-model="form.description"
              id="description"
              placeholder="Enter description (optional)"
            ></textarea>
          </div>
          <div class="form-group">
            <label for="category">Category</label>
            <input
              v-model="form.category"
              type="text"
              id="category"
              placeholder="Enter category (optional)"
            />
          </div>
          <div class="form-group">
            <label for="basePrice">Base Price</label>
            <input
              v-model="form.base_price"
              type="number"
              step="0.01"
              id="basePrice"
              placeholder="Enter base price"
              required
            />
          </div>
          <button type="submit" class="form-submit-button">Add Service</button>
        </form>
      </div>
    </div>
    <div v-if="activeTab === 'data'">
      
      <DataView>
        
      </DataView>
    </div>
    <div v-if="activeTab === 'insights'">
      <AdminInsights/>
    </div>
    <div v-if="activeTab === 'report'">
      <h2>Report</h2>

      
      <ReportView />
      <!-- Add report content here -->
    </div>


  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        service_name: '',
        description: '',
        category: '',
        base_price: null,
      },
    };
  },
  methods: {
    async serviceFormSubmit() {
      console.log(this.form);
      try {
        await addServices(this.form.service_name, this.form.description, this.form.category, this.form.base_price);
        toast.success("Service added successfully!");
        // Clear form data
        this.form = {
          service_name: '',
          description: '',
          category: '',
          base_price: null,
        };
      } catch (error) {
        console.error("Error adding service:", error);
        toast.error("Failed to add service. Please try again.");
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
