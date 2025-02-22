<script setup lang="ts">
import { type Project } from "@/stores/project.types";

defineProps<{ project: Project }>();

// Note: Is it correct to handle the null case here?
</script>

<template>
  <div v-if="project != null">
    <h1 class="font-bold">Project description</h1>
    <h2>{{ project.name }}</h2>
    <p>{{ project.description }}</p>
    <p>Everything:</p>
    <p>{{ project }}</p>
  </div>
</template>
