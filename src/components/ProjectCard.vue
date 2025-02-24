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
  <div class="flex justify-between items-center gap-3">
    <div class="w-full">
      <div class="flex gap-3 pb-3">
        <h2 class="text-2xl/7 font-bold text-gray-900">{{ project.name }}</h2>
        <div class="text-xs">
          <Tag v-if="project.isCompleted" severity="secondary" value="Completed" />
          <Tag v-else severity="warn" value="Under construction" />
        </div>
      </div>
      <div class="grid gap-1 text-sm text-gray-500 grid-style">
        <div class="flex items-center gap-2">
          <img src="@/assets/icons/location.svg" class="w-6 h-6 fill-current" />
          <p class="truncate">
            {{ project.locationCity }},
            {{ project.locationCountry }}
          </p>
        </div>
        <div class="flex items-center gap-2">
          <img src="@/assets/icons/construction.svg" class="w-6 h-6 fill-current" title="Constructed" />
          <p>{{ project.completedDate }}</p>
        </div>
        <div class="flex items-center gap-2">
          <img src="@/assets/icons/power.svg" class="w-6 h-6 fill-current" />
          <p>{{ project.installedCapacity }}</p>
        </div>
        <div class="flex items-center gap-2">
          <img src="@/assets/icons/panel.svg" class="w-6 h-6 fill-current" />
          <p>{{ project.numberOfCells }} cells</p>
        </div>
        <div class="flex items-center gap-2">
          <img src="@/assets/icons/price.svg" class="w-6 h-6 fill-current" />
          <p>${{ project.unitPrice }}/cell</p>
        </div>
      </div>
    </div>
    <div class="mx-5">
      <Button
        v-if="project.projectId"
        @click="goToProject(project.projectId)"
        label="View project"
        class="whitespace-nowrap"
      />
    </div>
  </div>
</template>

<style scoped>
.grid-style {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 0.3rem;
}
</style>
