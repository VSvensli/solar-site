<script setup lang="ts">
import Button from "primevue/button";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth.store";
import { ref } from "vue";
import { useToast } from "primevue/usetoast";
import InputText from "primevue/inputtext";
import Password from "primevue/password";

const authStore = useAuthStore();
const router = useRouter();
const username = ref("");
const toast = useToast();

async function handleSubmit() {
  await authStore.createUser(username.value, "password");
  if (authStore.status.createUser != "success") {
    toast.add({
      severity: "error",
      summary: "Error",
      detail: authStore.errorMsg.createUser,
      life: 3000,
    });
    return;
  }
  await authStore.userLogin(username.value, "password");
  if (authStore.status.userLogin != "success") {
    toast.add({
      severity: "error",
      summary: "Error",
      detail: authStore.errorMsg.userLogin,
      life: 3000,
    });
    return;
  }
  router.push({ name: "UserDashboard" });
}
</script>

<template>
  <div class="flex justify-center items-center h-screen shadow">
    <div class="flex justify-center flex-col gap-4 shadow-md p-40 rounded-md">
      <h1 class="text-2xl font-bold">Create Account</h1>
      <Form @submit.prevent="handleSubmit">
        <div class="flex flex-col gap-1">
          <InputText v-model="username" name="username" type="text" placeholder="usename" />
        </div>
        <div class="flex flex-col gap-1 mt-1">
          <Password name="password" placeholder="Password" :feedback="false" fluid />
        </div>
        <div class="flex flex-col gap-1 mt-1 mb-1">
          <Password name="confirmPassword" placeholder="Confirm Password" :feedback="false" fluid />
        </div>
        <Button type="submit" severity="secondary" label="Submit" />
      </Form>
      <h4 class="text-xs text-orange-400 font-bold">Not implemented</h4>
    </div>
  </div>
</template>
