<script setup lang="ts">
import { useAuthStore } from "@/stores/auth.store";
import { useRouter } from "vue-router";

const authStore = useAuthStore();
const router = useRouter();

function handleLogout() {
  authStore.userLogout();
  router.push({ name: "Home" });
}
</script>

<template>
  <div class="flex justify-between items-center w-full p-4 px-10 border-b-2 border-gray-200 font-mono font-semibold">
    <div class="flex space-x-4">
      <div @click="router.push({ name: 'Home' })" class="hover:text-gray-400 cursor-pointer">Home</div>
      <div
        v-if="authStore.isAuthenticated"
        @click="router.push({ name: 'UserDashboard' })"
        class="hover:text-gray-400 cursor-pointer"
      >
        Dashboard
      </div>
    </div>
    <div class="flex space-x-4">
      <div
        v-if="!authStore.isAuthenticated"
        @click="router.push({ name: 'Login' })"
        class="hover:text-gray-400 cursor-pointer"
      >
        Login
      </div>
      <div
        v-if="!authStore.isAuthenticated"
        @click="router.push({ name: 'CreateAccount' })"
        class="hover:text-gray-400 cursor-pointer"
      >
        Signup
      </div>
      <div v-if="authStore.isAuthenticated" @click="handleLogout" class="hover:text-gray-400 cursor-pointer">
        Logout
      </div>
    </div>
  </div>
</template>
