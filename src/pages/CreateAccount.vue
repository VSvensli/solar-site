<script setup lang="ts">
import Button from "primevue/button";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth.store";
import { ref } from "vue";
import InputText from "primevue/inputtext";
import Password from "primevue/password";

const authStore = useAuthStore();
const router = useRouter();
const email = ref("");

const handleSubmit = () => {
  authStore.createUser(email.value, "password");
  router.push({ name: "UserDashboard" });
};
</script>

<template>
  <div class="flex justify-center items-center h-screen shadow">
    <div class="flex justify-center flex-col gap-4 shadow-md p-40 rounded-md">
      <h1 class="text-2xl font-bold">Create Account</h1>
      <Form @submit="handleSubmit">
        <div class="flex flex-col gap-1">
          <InputText v-model="email" name="email" type="text" disabled placeholder="e-mail" />
        </div>
        <div class="flex flex-col gap-1 mt-1">
          <Password name="password" placeholder="Password" :feedback="false" disabled fluid />
        </div>
        <div class="flex flex-col gap-1 mt-1 mb-1">
          <Password name="confirmPassword" placeholder="Confirm Password" :feedback="false" disabled fluid />
        </div>
        <Button type="submit" severity="secondary" label="Submit" disabled />
      </Form>
      <h4 class="text-xs text-orange-400 font-bold">Not implemented</h4>
    </div>
  </div>
</template>
