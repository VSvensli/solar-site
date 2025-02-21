<script setup lang="ts">
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";

const authStore = useAuthStore();
const router = useRouter();

function handleUserIconClick() {
  if (authStore.isAuthenticated) {
    // Redirect to the user's profile if authenticated
    router.push({ name: "UserProfile" });
  } else {
    // Redirect to the login/signup page if not authenticated
    router.push({ name: "Login" });
  }
}
function handleLogout() {
  authStore.logout();
  router.push({ name: "Home" });
}
</script>

<template>
  <div class="bg-gray-800 text-white p-4 drop-shadow-sm">
    <router-link to="/" class="text-white hover:text-gray-400">
      Home
    </router-link>

    <div
      @click="handleUserIconClick"
      class="text-white hover:text-gray-400 cursor-pointer hover:underline"
    >
      Profile
    </div>
    <button
      v-if="authStore.isAuthenticated"
      @click="handleLogout"
      class="hover:underline"
    >
      Logout
    </button>
  </div>
</template>
