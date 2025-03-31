<script setup>
import { jwtDecode } from 'jwt-decode';
import { logout } from '@/controller/auth';

</script>
<script>
const pages = [
  { Name: "Home", Path: "/" },
  { Name: "Login", Path: "/login" },
  { Name: "Customer Signup", Path: "/signup/customer" },
  { Name: "Professional Signup", Path: "/signup/professional" },
];

export default {
  name: "App",
 
  data() {
    return {
      navitems: [], // Initialize as empty
      showMenu: false,
      heading: "Welcome To HH Management", // Add a reactive heading property
      isLoggedIn: !!localStorage.getItem('token'), // Reactive property for login state
    };
  },
  watch: {
    isLoggedIn: {
      immediate: true,
      handler() {
        this.updateHeading(); // Update heading when login state changes
        this.updateNavItems(); // Update navigation items when login state changes
      },
    },
  },
  mounted() {
    this.updateNavItems(); // Update navigation items when the component is mounted
    this.updateHeading(); // Update heading when the component is mounted
  },
  methods: {
    getnavdata() {
      const token = localStorage.getItem('token');
      if (token) {
        return []; // Return empty for logged-in users
      } else {
        return pages; // Return pages for non-logged-in users
      }
    },
    updateNavItems() {
      this.navitems = this.getnavdata(); // Update navigation items
    },
    updateHeading() {
      const token = localStorage.getItem('token');
      if (token) {
        try {
          const decoded = jwtDecode(token);
          if (decoded.usertype === 'AL') {
            this.heading = "Admin Dashboard";
          } else if (decoded.usertype === 'CL') {
            this.heading = "Customer Dashboard";
          } else if (decoded.usertype === 'PL') {
            this.heading = "Professional Dashboard";
          } else {
            this.heading = "Welcome To HH Management";
          }
        } catch (error) {
          console.error("Invalid token:", error);
          this.heading = "Welcome To HH Management";
        }
      } else {
        this.heading = "Welcome To HH Management";
      }
    },
    toggleMenu() {
      this.showMenu = !this.showMenu;
    },
    handleLogin() {
      this.isLoggedIn = true; // Update login state
      this.updateNavItems(); // Update navigation items after login
      this.updateHeading(); // Update heading after login
    },
    handleLogout() {
      if (confirm("Are you sure you want to log out?")) {
        logout(); // Call the logout function
        localStorage.removeItem('token'); // Remove token from localStorage
        this.isLoggedIn = false; // Update login state
        this.updateNavItems(); // Update navigation items after logout
        this.updateHeading(); // Update heading after logout
        this.$router.push('/login'); // Redirect to login page
      }
    },
  },
};
</script>

<template>
  <header class="d-flex justify-content-between align-items-center p-3 bg-light shadow-sm">
    <h1 class="m-0">{{ heading }}</h1> <!-- Use reactive heading -->
    <div v-if="isLoggedIn">
      <button @click="handleLogout" class="btn btn-danger">Logout</button>
    </div>
  </header>
  <nav v-if="!isLoggedIn" class="navbar bg-primary py-3 shadow">
    <ul class="d-flex justify-content-center gap-4 m-0 p-0">
      <li v-for="page in navitems" :key="page.Path" class="nav-item">
        <router-link 
          :to="page.Path" 
          class="nav-link  px-3 py-2 rounded text-white"
          active-class="active-link text-black"
        >
          {{ page.Name }}
        </router-link>
      </li>
    </ul>
  </nav>
  <div class="container my-3">
    <router-view @login="handleLogin" /> <!-- Listen for login event -->
  </div>

  <footer class="flex  align-items-center p-3 bg-light shadow-sm">
    <span class="text-muted">© 2025 Company, Inc</span>
  </footer>
  <ToastContainer />
</template>

<style>
@import "./assets/style.css";
@import "./assets/datatables.css";

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

header, footer {
  border-bottom: 1px solid #ddd;
  background-color: #f8f9fa; /* Match header and footer background */
}

header h1, footer span {
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.navbar {
  background-color: #007bff;
}

.nav-item {
  list-style: none;
}

.nav-link {
  font-weight: bold;
  text-decoration: none;
  transition: background-color 0.3s ease, color 0.3s ease;
  color: #ffffff;
}

.nav-link:hover {
  background-color: #0056b3;
  color: #ffffff; /* Ensure text color remains white on hover */
}

.navbar ul {
  padding: 0;
  margin: 0;
}

.navbar li {
  display: inline-block;
}

.nav-link.active-link {
  background-color: #ffffff;
  color: #000000 !important; /* Change text color to a highlighted orange */
  font-weight: bold;
  border: 1px solid #007bff;
}

footer .nav-link {
  color: #6c757d; /* Muted text color for footer links */
}

footer .nav-link:hover {
  color: #333; /* Darker color on hover */
}
</style>

