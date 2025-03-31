<template>
    <div>
      <h2 class="text-xl font-bold mb-4">Services Table</h2>
      <table id="servicesTable" class="display nowrap w-full">
        <thead>
          <tr>
            <th>Service Name</th>
            <th>Description</th>
            <th>Category</th>
            <th>Base Price</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(service, index) in services" :key="index">
            <td>{{ service.service_name }}</td>
            <td>{{ service.description }}</td>
            <td>{{ service.category }}</td>
            <td>{{ service.base_price }}</td>
          </tr>
        </tbody>
      </table>
    </div>
</template>

<script>
import $ from 'jquery';
import 'datatables.net';

export default {
  name: "DataView",
  data() {
    return {
      services: [],
      servicerequests: [],
      professionals: [],
    };
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    fetchData() {
      // Fetch services data
      fetch("http://127.0.0.1:5000/api/v2/admin/get/services")
        .then((response) => response.json())
        .then((data) => {
          this.services = data.data || data;
          this.$nextTick(() => {
            $("#servicesTable").DataTable({
              responsive: true,
              paging: true,
              searching: true,
              ordering: true,
              info: true,
              destroy: true,
            });
          });
        })
        .catch((error) => {
          console.error("Error fetching services data:", error);
        });
    },
  },
};
</script>
  
<style>
/* Optional styling for the table */
#servicesTable {
  width: 100%;
  border-collapse: collapse;
}
</style>
