<template>
  <div class="report-view">
    <h1>Generate Report</h1>
    <form @submit.prevent="generateReport">
      <div>
        <label for="adminEmail">Admin Email:</label>
        <input
          type="email"
          id="adminEmail"
          v-model="adminEmail"
          required
          placeholder="Enter admin email"
        />
      </div>
      <div>
        <label for="reportType">Report Type:</label>
        <select id="reportType" v-model="reportType">
          <option value="daily">Daily</option>
          <option value="monthly">Monthly</option>
        </select>
      </div>
      <button type="submit">Generate Report</button>
    </form>

    <div v-if="taskId" class="task-status">
      <h2>Task Status</h2>
      <p>Task ID: {{ taskId }}</p>
      <p>Status: {{ taskStatus }}</p>
      <button @click="checkTaskStatus">Check Status</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ReportView",
  data() {
    return {
      adminEmail: "",
      reportType: "daily",
      taskId: null,
      taskStatus: "Pending...",
    };
  },
  methods: {
    async generateReport() {
      try {
        const response = await axios.post("http://127.0.0.1:5000/report/generate_report", {
          admin_email: this.adminEmail,
          report_type: this.reportType,
        });

        this.taskId = response.data.task_id;
        this.taskStatus = "Pending...";
      } catch (error) {
        console.error("Error generating report:", error);
        alert("Failed to generate report. Please try again.");
      }
    },
    async checkTaskStatus() {
      if (!this.taskId) return;

      try {
        const response = await axios.get(`http://127.0.0.1:5000/task_status/${this.taskId}`);
        this.taskStatus = response.data.status;
      } catch (error) {
        console.error("Error checking task status:", error);
        alert("Failed to check task status. Please try again.");
      }
    },
  },
};
</script>

<style scoped>
.report-view {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #f9f9f9;
}

form div {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

input,
select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  padding: 10px 15px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

.task-status {
  margin-top: 20px;
  padding: 15px;
  border: 1px solid #007bff;
  border-radius: 8px;
  background-color: #e9f7ff;
}
</style>
