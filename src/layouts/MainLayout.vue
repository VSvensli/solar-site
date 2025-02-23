<script setup lang="ts">
import TopNavbar from "../components/TopNavbar.vue";
import { RouterView } from "vue-router";
import Toast from "primevue/toast";
</script>

<template>
  <Toast />
  <TopNavbar />
  <div class="container-sm mx-10 p-4">
    <RouterView />
  </div>
</template>
