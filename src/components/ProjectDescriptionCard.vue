<script setup lang="ts">
import { type Project } from "@/stores/projectStore";

defineProps<{ project: Project | null }>();

// Note: Is it correct to handle the null case here?
</script>

<template>
  <div v-if="project != null" class="p-4 border-1 shadow-lg rounded-lg">
    <h1 class="font-bold">Project description</h1>
    <h2>{{ project.name }}</h2>
    <p>{{ project.description }}</p>
  </div>
</template>
