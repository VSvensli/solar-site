<script setup lang="ts">
import { type Project } from "@/stores/project.types";

defineProps<{ project: Project }>();
</script>

<template>
  <div v-if="project != null" class="p-3">
    <h2 class="text-2xl/7 font-semibold text-gray-700 pb-1">{{ project.name }}</h2>
    <p class="text-gray-900 text-md">
      {{ project.description }}
    </p>
  </div>
  <div class="grid gap-1 text-sm text-gray-500 grid-style">
    <div class="flex items-center gap-2">
      <img src="@/assets/icons/location.svg" class="w-6 h-6 fill-current text-white" />
      <p class="truncate">
        {{ project.locationCity }},
        {{ project.locationCountry }}
      </p>
    </div>
    <div class="flex items-center gap-2">
      <img src="@/assets/icons/power.svg" class="w-6 h-6 fill-current text-white" />
      <p>{{ project.installedCapacity }}</p>
    </div>
    <div class="flex items-center gap-2">
      <img src="@/assets/icons/panel.svg" class="w-6 h-6 fill-current text-white" />
      <p>{{ project.numberOfCells }} cells</p>
    </div>
    <div class="flex items-center gap-2">
      <img src="@/assets/icons/price.svg" class="w-6 h-6 fill-current text-white" />
      <p>${{ project.unitPrice }}/cell</p>
    </div>
    <div class="flex items-center gap-2">
      <img src="@/assets/icons/biddingZone.svg" class="w-6 h-6 fill-current text-white" title="Bidding Zone" />
      <p>{{ project.locationBiddingZone }}</p>
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
