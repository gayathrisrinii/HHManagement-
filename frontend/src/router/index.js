import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import AdminView from "../views/AdminView.vue";
import Login from "../views/Login.vue";
import customersignup from "@/views/customersignup.vue";
import professionalSignUp from "@/views/professionalSignUp.vue";
import CustomerView from "@/views/CustomerView.vue";
import ProfessionalView from "@/views/ProfessionalView.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },

  {
    path: "/admin",
    name: "admin",
    component: AdminView,
  },
  {
    path: "/login",
    name: "login",
    component: Login,
  },
  {
    path: "/signup/customer",
    name: "customer-register",
    component: customersignup,
  },
  {
    path: "/signup/professional",
    name: "professional-register",
    component: professionalSignUp,
  },
  {
    path: "/customer",
    name: "customer-view",
    component: CustomerView,
  },
  {
    path: "/professional",
    name: "professional-view",
    component: ProfessionalView,
  },
  {
    path: "/logout",
    name: "logout",
    beforeEnter: (to, from, next) => {
      logoutUser();
      next("/login");
    },
  },
];

function logoutUser() {
  localStorage.removeItem("token"); // Clear the token from localStorage
  console.log("User logged out successfully");
}

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
