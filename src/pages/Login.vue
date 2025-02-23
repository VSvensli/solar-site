<script setup lang="ts">
import { useAuthStore } from "@/stores/auth.store";
import { useRouter } from "vue-router";
import { ref } from "vue";
import InputText from "primevue/inputtext";
import Password from "primevue/password";
import Button from "primevue/button";
import { useToast } from "primevue/usetoast";
import Toast from "primevue/toast";

const toast = useToast();

const show = () => {
  toast.add({ severity: "error", summary: "Failed to login", detail: "Incorrect username or password", life: 3000 });
};
const authStore = useAuthStore();
const router = useRouter();

const username = ref("");

const handleLoginSubmit = async () => {
  await authStore.userLogin(username.value, "password");
  if (authStore.status.userLogin === "success") {
    router.push({ name: "UserDashboard" });
  } else {
    show();
  }
};
</script>

<template>
  <Toast />
  <div class="flex justify-center items-center h-screen shadow">
    <div class="flex justify-center flex-col gap-4 shadow-md p-4 rounded-md">
      <h1 class="text-2xl font-bold">Login</h1>
      <div class="flex flex-col gap-1">
        <InputText v-model="username" name="username" type="text" placeholder="username" />
      </div>
      <div class="flex flex-col gap-1">
        <Password name="password" placeholder="Password" :feedback="false" disabled fluid />
      </div>
      <Button @click="handleLoginSubmit" severity="secondary" label="Login" />
      <h3>Setup new account here:</h3>
      <h3 @click="router.push({ name: 'CreateAccount' })" class="cursor-pointer text-blue-500">Create Account</h3>
      <h6>
        Note: There is currently no form of password handling, so only email/username is needed to login. All users have
        password "password".
      </h6>
    </div>
  </div>
</template>
