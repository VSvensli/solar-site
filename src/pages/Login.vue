<script setup lang="ts">
import { useAuthStore } from "@/stores/auth.store";
import { useRouter } from "vue-router";
import { ref } from "vue";
import InputText from "primevue/inputtext";
import Password from "primevue/password";
import Button from "primevue/button";

const authStore = useAuthStore();
const router = useRouter();

const email = ref("");
const error = ref("");

async function handleSubmit() {
  error.value = "";
  try {
    await authStore.userLogin(email.value, "password");
    router.push({ name: "UserDashboard" });
  } catch (err) {
    error.value = "Invalid email or password.";
    console.error("Login error:", err);
  }
}
</script>

<template>
  <div class="flex justify-center items-center h-screen shadow">
    <div class="flex justify-center flex-col gap-4 shadow-md p-4 rounded-md">
      <h1 class="text-2xl font-bold">Login</h1>
      <Form @submit="handleSubmit">
        <div class="flex flex-col gap-1">
          <InputText v-model="email" name="email" type="text" placeholder="e-mail" />
        </div>
        <div class="flex flex-col gap-1">
          <Password name="password" placeholder="Password" :feedback="false" disabled fluid />
        </div>
        <Button type="submit" severity="secondary" label="Submit" />
      </Form>
      <h3>Setup new account here:</h3>
      <h3 @click="router.push({ name: 'CreateAccount' })" class="cursor-pointer text-blue-500">Create Account</h3>
      <h6>
        Note: There is currently no form of password handling, so only email/username is needed to login. All users have
        password "password".
      </h6>
    </div>
  </div>
</template>
