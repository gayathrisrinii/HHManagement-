<script setup>
import { toast } from 'vue3-toastify';
import axios from 'axios';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
import { Pie } from 'vue-chartjs'
ChartJS.register(ArcElement, Tooltip, Legend)

</script>
<template>
    <div>
        <!-- <Pie :data="data" :options="options" /> -->

       
    </div>
    <div>
        <Pie :data="srdata" :options="options" />

       
    </div>
</template>

<script>


export default {
  name: "ProfInsights",
  components: {
    Pie
  },
    props: {
        professionalDetails: Object
    },
  data() {
    return {
      services: [],
      servicerequests: [],
      servicedata: {},
      srdata: {
        labels: [],
        datasets: []
      },
      options: {
  responsive: true,
  maintainAspectRatio: false
}
    };
  },
  mounted() {
    this.fetchData();
    console.log("Professional Details in Dashboard:", this.professionalDetails);
  },
  methods: {
    fetchData() {
      // Fetch services data
      axios.get("http://127.0.0.1:5000/api/v2/admin/get/services")
        .then((response) => {
          this.services = response.data.data || response.data;
          this.$nextTick(() => {
          console.log("Fetched services data:", this.services);
          });
        })
        .catch((error) => {
          console.error("Error fetching services data:", error);
        });

        axios.get(`http://127.0.0.1:5000/api/v2/professional/get/servicerequest2?id=${this.professionalDetails.id}`)
        .then((response) => {
          if (response.data.isSuccess) {
            this.servicerequests = response.data.data;
            console.log("Fetched service requests:", this.servicerequests);

            // Prepare chart data
            const statusCounts = this.servicerequests.reduce((acc, request) => {
              acc[request.status] = (acc[request.status] || 0) + 1;
              return acc;
            }, {});

            this.srdata = {
              labels: ['Requested', 'InProgress', 'Completed'],
              datasets: [
                {
                  backgroundColor: ['#41B883', '#E46651', '#00D8FF'],
                  data: [
                    statusCounts['Requested'] || 0,
                    statusCounts['InProgress'] || 0,
                    statusCounts['Completed'] || 0
                  ]
                }
              ]
            };
          } else {
            toast.error(response.data.message || "Failed to fetch service requests.");
          }
        })
        .catch((error) => {
          console.error("Error fetching service requests data:", error);
          toast.error("An error occurred while fetching service requests.");
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
