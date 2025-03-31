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

    <div>
      <h2 class="text-xl font-bold mb-4">Professionals Data</h2>
      <table id="profTable" class="display nowrap w-full">
        <thead>
          <tr>
            <th>Professional Name</th>
            <th>Email</th>
            <th>Phone Number</th>
            <th>Status</th>
            <th>Service Name</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(prof, index) in professionals" :key="index">
            
            <td>{{ prof.full_name }}</td>
            <td>{{ prof.email}}</td>
            <td>{{ prof.phone }}</td>
            <td>{{ prof.status }}</td>
            <td>{{ prof.experience }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div>
      <h2 class="text-xl font-bold mb-4">Customers Data</h2>
      <table id="custTable" class="display nowrap w-full">
        <thead>
          <tr>
            <th>Customer Name</th>
            <th>Email</th>
            <th>Phone Number</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(cust, index) in customers" :key="index">
            
            <td>{{ cust.full_name }}</td>
            <td>{{ cust.email}}</td>
            <td>{{ cust.phone }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div>
      <h2 class="text-xl font-bold mb-4">Service Requests Table</h2>
      <table id="serviceRequest" class="display nowrap w-full">
        <thead>
          <tr>
            <th>Date</th>
            <th>Customer Name</th>
            <th>Service Name</th>
            <th>Professional Name</th>
            <th>Rating</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(serviceRequest, index) in servicerequests" :key="index">
            <td>{{ serviceRequest.date }}</td>
            <td>{{ serviceRequest.customer_name }}</td>
            <td>{{ serviceRequest.service_name }}</td>
            
            <td>{{ serviceRequest.assignee_id }}</td>
            <td>{{ serviceRequest.rating }}</td>
            <td>{{ serviceRequest.status }}</td>
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
      customers: [],
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

      // Fetch professionals data
      fetch("http://127.0.0.1:5000/api/v2/admin/get/professionals")
        .then((response) => response.json())
        .then((data) => {
          this.professionals = data.data || data;
          this.$nextTick(() => {
            $("#profTable").DataTable({
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
          console.error("Error fetching professionals data:", error);
        });

      // Fetch customers data
      fetch("http://127.0.0.1:5000/api/v2/admin/get/customers")
        .then((response) => response.json())
        .then((data) => {
          this.customers = data.data || data;
          this.$nextTick(() => {
            $("#custTable").DataTable({
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
          console.error("Error fetching customers data:", error);
        });

      // Fetch service requests data
      fetch("http://127.0.0.1:5000/api/v2/admin/get/servicerequests")
        .then((response) => response.json())
        .then((data) => {
          this.servicerequests = data.data || data;
          this.$nextTick(() => {
            $("#serviceRequest").DataTable({
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
          console.error("Error fetching service requests data:", error);
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
