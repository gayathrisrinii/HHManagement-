<template>
    <div>
        <div>
            <h2 class="text-xl font-bold mb-4">Service Requested</h2>
            <table id="serviceRequest1" :key="servicerequests1.length" class="display nowrap w-full">
                <thead>
                <tr>
                    <th>Service Name</th>
                    <th>Customer Name</th>
                    <th>Action</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="(serviceRequest, index) in servicerequests1" :key="index">
                    <td>{{ serviceRequest.service_name }}</td>
                    <td>{{ serviceRequest.customer_name }}</td>
                    <td>
                        <button class="table-button approve" @click="acceptService(serviceRequest.service_request_id)">Accept</button>
                    </td>
                </tr>
                </tbody>
            </table>
        </div>

        <div>
            <h2 class="text-xl font-bold mb-4">Service History</h2>
            <table id="serviceRequest2" :key="servicerequests2.length" class="display nowrap w-full">
                <thead>
                <tr>
                    <th>Date</th>
                    <th>Customer Name</th>
                    <th>Service Name</th>
                    <th>Status</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="(serviceRequest, index) in servicerequests2" :key="index">
                    <td>{{ serviceRequest.date }}</td>
                    <td>{{ serviceRequest.customer_name }}</td>
                    <td>{{ serviceRequest.service_name }}</td>
                    <td>{{ serviceRequest.status }}</td>
                </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
import $ from 'jquery';
import 'datatables.net';
import { toast } from 'vue3-toastify';

export default {
  name: "profDashboard",
  props: {
    professionalDetails:  Object,
    },
  data() {
    return {
      servicerequests1: [],
      servicerequests2: [],
    };
  },
  mounted() {
    console.log("Professional Details:", this.professionalDetails);
    this.fetchData();
  },
  methods: {
    fetchData() {
    fetch(`http://127.0.0.1:5000/api/v2/professional/get/servicerequest1?status=Requested`)
        .then((response) => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then((data) => {
            this.servicerequests1 = data.data || data;
            this.$nextTick(() => {
                if ($.fn.DataTable.isDataTable("#serviceRequest1")) {
                    $("#serviceRequest1").DataTable().destroy();
                }
                $("#serviceRequest1").DataTable({
                    responsive: true,
                    paging: true,
                    searching: true,
                    ordering: true,
                    info: true,
                });
            });
        })
        .catch((error) => {
            console.error("Error fetching service requests data:", error);
        });

    fetch("http://127.0.0.1:5000/api/v2/professional/get/servicerequest2?id=" + this.professionalDetails.id)
        .then((response) => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then((data) => {
            this.servicerequests2 = data.data || data;
            this.$nextTick(() => {
                if ($.fn.DataTable.isDataTable("#serviceRequest2")) {
                    $("#serviceRequest2").DataTable().destroy();
                }
                $("#serviceRequest2").DataTable({
                    responsive: true,
                    paging: true,
                    searching: true,
                    ordering: true,
                    info: true,
                });
            });
        })
        .catch((error) => {
            console.error("Error fetching service requests data:", error);
        });
},

    acceptService(serviceId) {
      if (!this.professionalDetails || !this.professionalDetails.id) {
        toast.error('Professional details are missing or invalid.');
        return;
      }
      const professional_id = this.professionalDetails.id;
      fetch("http://127.0.0.1:5000/api/v2/professional/accept-service?id=" + this.professionalDetails.id, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ service_request_id: serviceId, professional_id }),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          return response.json().catch(() => {
            throw new Error("Invalid JSON response");
          });
        })
        .then((data) => {
          if (data.isSuccess) {

            console.log("Data : ",data)
            toast.success('Service accepted successfully!');
            $("#serviceRequest1").DataTable().destroy();
            $("#serviceRequest2").DataTable().destroy();
            this.fetchData(); // Reload or update the table data
          } else {
            toast.error('Failed to accept the service: ' + (data.message || 'Unknown error'));
          }
        })
        .catch((error) => {
          console.error('Error accepting service:', error);
          toast.error('An error occurred while accepting the service.');
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
