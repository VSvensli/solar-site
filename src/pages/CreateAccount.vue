<script setup lang="ts">
import Button from "primevue/button";
import { useRouter } from "vue-router";
import { ref } from "vue";
import InputText from "primevue/inputtext";
import Password from "primevue/password";

const router = useRouter();
const email = ref("");

const handleSubmit = () => {};
</script>

<template>
  <div class="flex justify-center items-center h-screen shadow">
    <div class="flex justify-center flex-col gap-4 shadow-md p-40 rounded-md">
      <h1 class="text-2xl font-bold">Create Account</h1>
      <Form @submit="handleSubmit">
        <div class="flex flex-col gap-1">
          <InputText
            v-model="email"
            name="email"
            type="text"
            placeholder="e-mail"
          />
        </div>
        <div class="flex flex-col gap-1 mt-1">
          <Password
            name="password"
            placeholder="Password"
            :feedback="false"
            disabled
            fluid
          />
        </div>
        <div class="flex flex-col gap-1 mt-1 mb-1">
          <Password
            name="confirmPassword"
            placeholder="Confirm Password"
            :feedback="false"
            disabled
            fluid
          />
        </div>
        <Button type="submit" severity="secondary" label="Submit" />
      </Form>
      <h4>
        Note: There is currently no form of password handling, so only email is
        needed to create a new account
      </h4>
    </div>
  </div>
</template>
