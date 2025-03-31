<script setup>
import { toast } from 'vue3-toastify';
import axios from 'axios';
</script>
<template>
    <div>
        <div>
            <h2 class="text-xl font-bold mb-4">Services Table</h2>
            <table id="servicesTable" :key="services.length" class="display nowrap w-full">
                <thead>
                <tr>
                    <th>Service Name</th>
                    <th>Description</th>
                    <th>Category</th>
                    <th>Base Price</th>
                    <th>Action</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="(service, index) in services" :key="index">
                    <td>{{ service.service_name }}</td>
                    <td>{{ service.description }}</td>
                    <td>{{ service.category }}</td>
                    <td>{{ service.base_price }}</td>
                    <td>
                        <button class="table-button save" @click="bookService(service.id)">Book</button>
                    </td>
                </tr>
                </tbody>
            </table>
        </div>

        <div>
            <h2 class="text-xl font-bold mb-4">Service History</h2>
            <table id="serviceRequest" :key="servicerequests.length" class="display nowrap w-full">
                <thead>
                <tr>
                    <th>Date</th>
                    <th>Customer Name</th>
                    <th>Service Name</th>
                    <th>Professional Name</th>
                    <th>Rating</th>
                    <th>Status</th>
                    <th>Action</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="(serviceRequest, index) in servicerequests" :key="index">
                    <td>{{ serviceRequest.date }}</td>
                    <td>{{ serviceRequest.customer_name }}</td>
                    <td>{{ serviceRequest.service_name }}</td>
                    <td>{{ serviceRequest.professional_name || 'NOT ASSIGNED' }}</td>
                    <td>{{ serviceRequest.rating }}</td>
                    <td>{{ serviceRequest.status }}</td>
                    <td>
                      <button 
                          class="table-button save" 
                          @click="openPopup(serviceRequest.service_request_id)" 
                          :hidden="serviceRequest.status === 'Requested' || serviceRequest.status === 'Completed'">
                          Complete Service
                      </button>                    
                    </td>
                     <!-- Popup Modal -->
    <div v-if="showPopup" class="popup-overlay">
      <div class="popup-content">
        <h3>Rate and Review Service</h3>
        <p><strong>Service Name:</strong> {{ selectedService.service_name }}</p>
        <p><strong>Description:</strong> {{ selectedService.description }}</p>
        <p><strong>Date:</strong> {{ selectedService.date }}</p>
        <p><strong>Professional Name:</strong> {{ selectedService.professional_name }}</p>
        <form @submit.prevent="submitForm">
          <div>
            <label for="rating">Rating (1-5):</label>
            <input type="number" id="rating" v-model="rating" min="1" max="5" required />
          </div>
          <div>
            <label for="remarks">Remarks:</label>
            <textarea id="remarks" v-model="remarks" required></textarea>
          </div>
          <div>
            <button type="submit">Submit</button>
            <button type="button" @click="closePopup">Cancel</button>
          </div>
        </form>
      </div>
    </div>
                </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
import $ from 'jquery';
import 'datatables.net';

export default {
  name: "custDashboard",
  props: {
    customerDetails: Object
  },
  data() {
    return {
      showPopup: false,
      serviceRequestId: null,
      rating: null,
      remarks: '',
      selectedService: {},
      services: [],
      servicerequests: [],
    };
  },
  mounted() {
    this.fetchData();
    console.log("Customer Details in Dashboard:", this.customerDetails);
  },
  methods: {
    openPopup(serviceRequestId) {
      const serviceRequest = this.servicerequests.find(
        (request) => request.service_request_id === serviceRequestId
      );
      if (serviceRequest) {
        this.selectedService = serviceRequest;
      } else {
        console.error("Service request not found for ID:", serviceRequestId);
      }
      this.showPopup = true;
      this.serviceRequestId = serviceRequestId;
      this.showPopup = true;
    },
    closePopup() {
      this.showPopup = false;
      this.selectedService = {};
      this.rating = null;
      this.remarks = '';
    },
    async submitForm() {
      try {
        const response = await fetch('http://127.0.0.1:5000//api/v2/customer/completenow', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            service_request_id: this.selectedService.service_request_id,
            //service_request_id: this.serviceRequestId,
            rating: this.rating,
            remarks: this.remarks,
          }),
        });
        const result = await response.json();
        console.log(result)
        if (result.isSuccess) {
          toast.success('Service completed successfully!');
          this.fetchData();
        } else {
          toast.error('Error completing service.');
        }
      } catch (error) {
        console.error(error);
        toast.error('An error occurred. Please try again.');
      } finally {
        this.closePopup();
      }
    },
    fetchData() {
      // Fetch services data
      axios.get("http://127.0.0.1:5000/api/v2/admin/get/services")
        .then((response) => {
          this.services = response.data.data || response.data;
          this.$nextTick(() => {
            if ($.fn.DataTable.isDataTable("#servicesTable")) {
              $("#servicesTable").DataTable().destroy();
            }
            $("#servicesTable").DataTable({
              responsive: true,
              paging: true,
              searching: true,
              ordering: true,
              info: true,
            });
          });
        })
        .catch((error) => {
          console.error("Error fetching services data:", error);
          toast.error("Failed to fetch services data.");
        });

      // Fetch service requests data
      axios.get("http://127.0.0.1:5000/api/v2/customer/get/servicerequest?id=" + this.customerDetails.id)
        .then((response) => {
          this.servicerequests = response.data.data || response.data;
          console.log("Service requests response:", response.data);
          if (!response.data.isSuccess) {
            toast.error(response.data.message || "Failed to fetch service requests.");
          }
          this.$nextTick(() => {
            if ($.fn.DataTable.isDataTable("#serviceRequest")) {
              $("#serviceRequest").DataTable().destroy();
            }
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
          toast.error("An error occurred while fetching service requests.");
        });
    },
    bookService(serviceId) {
      console.log("Booking service with ID:", serviceId);
      axios.post("http://127.0.0.1:5000//api/v2/customer/booknow", {
        service_id: serviceId,
        customer_id: this.customerDetails.id,
      })
        .then((response) => {
          console.log("Service booking response:", response.data);
          console.log(response.data.isSuccess)
          if (response.data.isSuccess) {
            console.log(response.data.isSuccess)
            toast.success("Service requested successfully!");
            $("#serviceRequest").DataTable().destroy();
            $("#servicesTable").DataTable().destroy();

            this.fetchData();
          } else {
            console.error("Error response from server:", response.data);
            toast.error("Failed to request service. Please try again.");
          }
        })
        .catch((error) => {
          console.error("Error booking service:", error);
          toast.error("An error occurred while booking the service.");
        });
    },
  }
};
</script>
  
<style>
/* Optional styling for the table */
#servicesTable {
  width: 100%;
  border-collapse: collapse;
}
.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}
.popup-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 400px;
  text-align: center;
}
</style>
