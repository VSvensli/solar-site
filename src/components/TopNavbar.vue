<script setup lang="ts">
import { useAuthStore } from "@/stores/auth.store";
import { useRouter } from "vue-router";

const authStore = useAuthStore();
const router = useRouter();

function handleUserIconClick() {
  if (authStore.isAuthenticated) {
    // Redirect to the user's profile if authenticated
    router.push({ name: "UserDashboard" });
  } else {
    // Redirect to the login/signup page if not authenticated
    router.push({ name: "Login" });
  }
}
function handleLogout() {
  authStore.userLogout();
  router.push({ name: "Home" });
}
</script>

<template>
  <div class="bg-gray-800 text-white p-4 flex justify-between items-center">
    <router-link to="/" class="text-white hover:text-gray-400"> Home </router-link>

    <div @click="handleUserIconClick" class="text-white hover:text-gray-400 cursor-pointer hover:underline">
      <span v-if="authStore.isAuthenticated">My Dashboard</span>
      <span v-else>Login/Signup</span>
    </div>
    <button v-if="authStore.isAuthenticated" @click="handleLogout" class="hover:underline">Logout</button>
  </div>
</template>
