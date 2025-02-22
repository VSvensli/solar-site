<script setup lang="ts">
import { computed } from "vue";
import { useProjectStore } from "@/stores/project.store";
import { type UserProject } from "@/stores/user.types";
import Tag from "primevue/tag";

const projectStore = useProjectStore();

const props = defineProps<{
  userProjectStatistics: UserProject;
}>();
const isNewPurchase = computed(() => {
  return new Date().getTime() - props.userProjectStatistics.timeOfPurchase.getTime() < 1000 * 60 * 60 * 24 * 7;
});
const project = computed(() => projectStore.findProjectById(props.userProjectStatistics.projectId));
</script>

<template>
  <div v-if="project" class="p-4 border-b-2 border-gray-300">
    <Tag v-if="isNewPurchase" severity="success" value="New" />
    <p class="text-2xl/7 font-bold text-gray-900">{{ project.name }}</p>
    <p class="text-sm text-gray-500">Owned since {{ userProjectStatistics.timeOfPurchase.toDateString() }}</p>
    <p class="text-sm text-gray-500">You own {{ userProjectStatistics.cellIds.length }} cells</p>
    <p class="text-sm text-gray-500">Percentage of cells owned {{ userProjectStatistics.percentageOwned }}</p>
  </div>
</template>
