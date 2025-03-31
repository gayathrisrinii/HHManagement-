<template>
   
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
            <th>Delete</th>
            <th>Accept / Reject</th>

          </tr>
        </thead>
        <tbody>
          <tr v-for="(prof, index) in professionals" :key="index">
            
            <td>{{ prof.full_name }}</td>
            <td>{{ prof.email}}</td>
            <td>{{ prof.phone }}</td>
            <td>{{ prof.status }}</td>
            <td>{{ prof.experience }}</td>
            <td><button class="table-button delete" @click="deleteProfessional(prof.pid)">Delete</button></td>
            <td> 
              <button class="table-button approve" @click="acceptProfessional(prof.pid)">Accept</button>
              <button class="table-button reject" @click="rejectProfessional(prof.pid)">Reject</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

   

  </template>
  
  <script>
import $ from 'jquery';
import 'datatables.net';
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';

export default {
  name: "ProfView",
  data() {
    return {
      professionals: [],
    };
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    fetchData() {
      // Fetch services data

      // Fetch professionals data
      fetch("http://127.0.0.1:5000/api/v2/admin/get/professionals")
        .then((response) => response.json())
        .then((data) => {
          this.professionals = data.data || data;
          console.log("Professionals data:", this.professionals);
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

      
    },
    acceptProfessional(pid) {
        fetch(`http://127.0.0.1:5000/api/v2/admin/acceptpro?id=${pid}`)
        .then((response) => response.json())
        .then(() => {
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
          toast.success(`Accepted professional with ID: ${pid}`);
          this.fetchData();
        })
        .catch((error) => {
          console.error("Error accepting professional:", error);
          toast.error("Failed to accept professional.");
        });
    },
    rejectProfessional(pid) {
        fetch(`http://127.0.0.1:5000/api/v2/admin/rejectpro?id=${pid}`)
        .then((response) => response.json())
        .then(() => {
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
          toast.success(`Rejected professional with ID: ${pid}`);
          this.fetchData();
        })
        .catch((error) => {
          console.error("Error rejecting professional:", error);
          toast.error("Failed to reject professional.");
        });
    },
    deleteProfessional(pid) {
        fetch(`http://127.0.0.1:5000/api/v2/admin/deletepro?id=${pid}`)
        .then((response) => response.json())
        .then(() => {
            this.$nextTick(() => {
              $('#profTable').DataTable().destroy();
              this.fetchData();
          });
          toast.success(`Deleted professional with ID: ${pid}`);
 
        })
        .catch((error) => {
          console.error("Error deleting professional:", error);
          toast.error("Failed to delete professional.");
        });
    }

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
