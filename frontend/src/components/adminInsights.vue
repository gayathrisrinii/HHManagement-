<script setup>
import { toast } from 'vue3-toastify';
import axios from 'axios';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
import { Pie } from 'vue-chartjs'
ChartJS.register(ArcElement, Tooltip, Legend)
</script>

<template>
    <div>
        <Pie :data="servicedata" :options="options" />
    </div>
    <div>
        <Pie :data="srdata" :options="options" />       
    </div>
</template>

<script>
export default {
  name: "AdminInsights",
  components: {
    Pie
  },
    props: {
        adminDetails: Object
    },
  data() {
    return {
      services: [],
      servicerequests: [],
      servicedata: {
        labels: [],
        datasets: []
      },
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
    console.log("Admin Details in Dashboard:", this.adminDetails);
  },
  methods: {
    getRandomColors(arraySize) {
        const colors = [];
        for (let i = 0; i < arraySize; i++) {
            const randomColor = `#${Math.floor(Math.random() * 16777215).toString(16).padStart(6, '0')}`;
            colors.push(randomColor);
        }
        return colors;
        },
    fetchData() {
        axios.get(`http://127.0.0.1:5000/api/v2/admin/get/servicerequests`)
        .then((response) => {
          if (response.data.isSuccess) {
            this.servicerequests = response.data.data;
            console.log("Fetched service requests:", this.servicerequests);
            const serviceCounts = this.servicerequests.reduce((acc, item) => {
                acc[item.service_name] = (acc[item.service_name] || 0) + 1;
                return acc;
                }, {});
                console.log(serviceCounts)
            // Prepare chart data
            const statusCounts = this.servicerequests.reduce((acc, request) => {
              acc[request.status] = (acc[request.status] || 0) + 1;
              return acc;
            }, {});

            this.servicedata = {
            labels: Object.keys(serviceCounts),
            datasets: [
              {
                backgroundColor: this.getRandomColors(Object.keys(serviceCounts).length),
                data: Object.values(serviceCounts)
                
              }
            ]
          };
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