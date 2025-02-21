<script setup lang="ts">
import TopNavbar from "../components/TopNavbar.vue";
import { RouterView } from "vue-router";
</script>

<template>
  <div>
    <TopNavbar />
    <RouterView />
  </div>
</template>
