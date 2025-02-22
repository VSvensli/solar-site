<script setup lang="ts">
import { type Project } from "@/stores/project.types";
import { useRouter } from "vue-router";
import Button from "primevue/button";
import Tag from "primevue/tag";

defineProps<{ project: Project }>();

const router = useRouter();

function goToProject(id: string) {
  router.push({ path: `/projects/${id}` });
}
</script>

<template>
  <div class="p-4 border-b-2 border-gray-300">
    <div>
      <Tag v-if="project.isCompleted" severity="secondary" value="Completed" />
      <Tag v-else severity="warn" value="Under construction" />

      <h2 class="text-2xl/7 font-bold text-gray-900">{{ project.name }}</h2>
    </div>
    <p class="text-sm text-gray-500">{{ project.description }}</p>
    <div class="mt-2">
      <p class="text-sm text-gray-500">Location: {{ project.locationCity }}, {{ project.locationCountry }}</p>
      <p class="text-sm text-gray-500">Capacity: {{ project.installedCapacity }}</p>
      <p class="text-sm text-gray-500">Completed: {{ project.completedDate }}</p>
      <p class="text-sm text-gray-500">Cells: {{ project.numberOfCells }}</p>
      <p class="text-sm text-gray-500">Price: ${{ project.unitPrice }}/cell</p>
    </div>
    <Button v-if="project.id" @click="goToProject(project.id)" label="View project" />
  </div>
</template>
