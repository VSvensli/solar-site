import {
  createRouter,
  createWebHistory,
  type RouteRecordRaw,
} from "vue-router";

import Home from "@/pages/Home.vue";
import UserProfile from "@/pages/UserDashboard.vue";
import ProjectDetails from "@/pages/ProjectDetails.vue";
import Login from "@/pages/Login.vue";

const routes: RouteRecordRaw[] = [
  { path: "/", component: Home, name: "Home" },
  {
    path: "/projects/:id",
    component: ProjectDetails,
    name: "ProjectDetails",
  },
  {
    path: "/profile",
    component: UserProfile,
    name: "UserProfile",
  },
  {
    path: "/login",
    component: Login,
    name: "Login",
  },
];
const router = createRouter({
  history: createWebHistory(),
  routes: routes,
});

export default router;
