<script setup lang="ts">
import { type Project } from "@/stores/project.types";

defineProps<{ project: Project }>();
</script>

<template>
  <div v-if="project != null">
    <h1 class="font-bold">Project description</h1>
    <h2>{{ project.name }}</h2>
    <p>{{ project.description }}</p>
    <p>Created at: {{ project.completedDate.toDateString() }}</p>
    <p>Everything:</p>
    <p>{{ project }}</p>
  </div>
</template>
