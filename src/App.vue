<script setup lang="ts">
import MainLayout from "./layouts/MainLayout.vue";
import { onMounted } from "vue";
import { useProjectStore } from "./stores/projectStore";

const projectStore = useProjectStore();

// Optimize at some point
onMounted(() => {
  projectStore.fetchProjects();
});
</script>

<template>
  <MainLayout />
</template>
