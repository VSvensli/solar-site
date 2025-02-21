<script setup lang="ts">
import { type Project } from "@/stores/projectStore";
import { useRouter } from "vue-router";
defineProps<{ project: Project }>();

const router = useRouter();

function goToProject(id: string) {
  router.push({ path: `/projects/${id}` });
}
</script>

<template>
  <div class="p-4 border-1 shadow-lg rounded-lg">
    <h2 @click="goToProject(project.id)" class="cursor-pointer hover:underline">
      {{ project.name }}
    </h2>
    <p>{{ project.description }}</p>
  </div>
</template>
