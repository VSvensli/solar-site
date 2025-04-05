import { createRouter, createWebHistory, type RouteRecordRaw } from "vue-router";

import Home from "@/pages/Home.vue";
import UserDashboard from "@/pages/UserDashboard.vue";
import ProjectDetails from "@/pages/ProjectDetails.vue";
import Login from "@/pages/Login.vue";
import Checkout from "@/pages/Checkout.vue";
import CreateAccount from "@/pages/CreateAccount.vue";
import NotFound from "@/pages/NotFound.vue";
import { useAuthStore } from "@/stores/auth.store";

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
    meta: { requiresAuth: true },
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
    meta: { requiresAuth: true },
  },
  {
    path: "/create-account",
    component: CreateAccount,
    name: "CreateAccount",
  },
  {
    path: "/:pathMatch(.*)*",
    component: NotFound,
    name: "NotFound",
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes: routes,
});

router.beforeEach((to, _, next) => {
  const auth = useAuthStore();
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    next({ name: "Login" });
  } else {
    next();
  }
});

export default router;
