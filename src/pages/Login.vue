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
  <div>
    <Form
      v-slot="$form"
      :resolver="resolver"
      :initialValues="initialValues"
      @submit="onFormSubmit"
      class="flex justify-center flex-col gap-4"
    >
      <div class="flex flex-col gap-1">
        <InputText name="username" type="text" placeholder="Username" />
        <Message
          v-if="$form.username?.invalid"
          severity="error"
          size="small"
          variant="simple"
          >{{ $form.username.error?.message }}</Message
        >
      </div>
      <div class="flex flex-col gap-1">
        <InputText name="email" type="text" placeholder="Email" />
        <Message
          v-if="$form.email?.invalid"
          severity="error"
          size="small"
          variant="simple"
          >{{ $form.email.error?.message }}</Message
        >
      </div>
      <Button type="submit" severity="secondary" label="Submit" />
    </Form>
  </div>
</template>
