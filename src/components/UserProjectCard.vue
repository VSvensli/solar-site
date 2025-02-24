<script setup lang="ts">
import { computed } from "vue";
import { useProjectStore } from "@/stores/project.store";
import { type UserProject } from "@/stores/user.types";
import Tag from "primevue/tag";

const projectStore = useProjectStore();

const props = defineProps<{
  userProject: UserProject;
}>();

const isNewPurchase = computed(() => {
  return new Date().getTime() - new Date(props.userProject.timeOfPurchase).getTime() < 1000 * 60 * 60 * 24 * 7;
});
const project = computed(() => projectStore.findProjectById(props.userProject.projectId));
</script>

<template>
  <div v-if="project" class="p-4 border-b-2 border-gray-300">
    <Tag v-if="isNewPurchase" severity="success" value="New" />
    <p class="text-2xl/7 font-bold text-gray-900">{{ project.name }}</p>
    <p class="text-sm text-gray-500">Owned since {{ userProject.timeOfPurchase }}</p>
    <p class="text-sm text-gray-500">You own {{ userProject.cellIds.length }} cells</p>
    <p class="text-sm text-gray-500">Percentage of cells owned {{ userProject.percentageOwned }}</p>
    {{ project.projectId }}
  </div>
</template>
