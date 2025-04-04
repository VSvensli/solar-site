import {
  createRouter,
  createWebHistory,
  type RouteRecordRaw,
} from "vue-router";

import Home from "@/pages/Home.vue";
import UserDashboard from "@/pages/UserDashboard.vue";
import ProjectDetails from "@/pages/ProjectDetails.vue";
import Login from "@/pages/Login.vue";
import Checkout from "@/pages/Checkout.vue";
import CreateAccount from "@/pages/CreateAccount.vue";

const routes: RouteRecordRaw[] = [
  { path: "/", component: Home, name: "Home" },
  {
    path: "/projects/:id",
    component: ProjectDetails,
    name: "ProjectDetails",
  },
  {
    path: "/profile",
    component: UserDashboard,
    name: "UserDashboard",
  },
  {
    path: "/login",
    component: Login,
    name: "Login",
  },
  {
    path: "/checkout",
    component: Checkout,
    name: "Checkout",
  },
  {
    path: "/create-account",
    component: CreateAccount,
    name: "CreateAccount",
  },
];
const router = createRouter({
  history: createWebHistory(),
  routes: routes,
});

export default router;
