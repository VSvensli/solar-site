<script setup lang="ts">
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";
import { ref } from "vue";
import InputText from "primevue/inputtext";
import Password from "primevue/password";
import { useToast } from "primevue/usetoast";
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
  <div class="flex justify-center items-center h-screen shadow">
    <Form
      @submit="handleSubmit"
      class="flex justify-center flex-col gap-4 shadow-md p-4 rounded-md"
    >
      <div class="flex flex-col gap-1">
        <InputText
          v-model="email"
          name="email"
          type="text"
          placeholder="e-mail"
        />
      </div>
      <div class="flex flex-col gap-1">
        <Password
          name="password"
          placeholder="Password"
          :feedback="false"
          fluid
        />
      </div>
      <Button type="submit" severity="secondary" label="Submit" />
    </Form>
  </div>
</template>
