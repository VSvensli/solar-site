<script setup lang="ts">
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";
import { ref } from "vue";
import InputText from "primevue/inputtext";
import Password from "primevue/password";
import Button from "primevue/button";

const authStore = useAuthStore();
const router = useRouter();

const email = ref("");
const password = ref("");
const error = ref("");

async function handleSubmit() {
  error.value = "";
  try {
    await authStore.login(email.value, password.value);
    router.push({ name: "UserProfile" });
  } catch (err) {
    error.value = "Invalid email or password.";
    console.error("Login error:", err);
  }
}
</script>

<template>
  <div class="max-w-md mx-auto my-8 p-6 bg-white rounded shadow">
    <h2 class="text-2xl font-bold mb-4 text-center">Login</h2>
    <form @submit.prevent="handleSubmit">
      <div class="mb-4">
        <label for="email" class="block text-gray-700 mb-1">Email</label>
        <InputText
          id="email"
          v-model="email"
          type="email"
          placeholder="Enter your email"
          class="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
        />
      </div>
      <div class="mb-4">
        <label for="password" class="block text-gray-700 mb-1">Password</label>
        <Password
          id="password"
          v-model="password"
          feedback="false"
          toggleMask
          placeholder="Enter your password"
          class="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
        />
      </div>
      <div v-if="error" class="mb-4 text-red-500">
        {{ error }}
      </div>
      <Button
        type="submit"
        label="Login"
        class="w-full bg-blue-500 hover:bg-blue-600 text-white p-2 rounded"
      />
    </form>
  </div>
</template>
