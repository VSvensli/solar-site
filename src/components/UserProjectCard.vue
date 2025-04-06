<script setup lang="ts">
import { computed } from "vue";
import { useProjectStore } from "@/stores/project.store";
import { type UserProject } from "@/stores/user.types";
import Tag from "primevue/tag";
import { useRouter } from "vue-router";

const router = useRouter();
const projectStore = useProjectStore();

const props = defineProps<{
  userProject: UserProject;
}>();

const isNewPurchase = computed(() => {
  return new Date().getTime() - new Date(props.userProject.timeOfPurchase).getTime() < 1000 * 60 * 60 * 24 * 30;
});
const project = computed(() => projectStore.findProjectById(props.userProject.projectId));
</script>
<template>
  <div v-if="project">
    <div class="flex gap-3">
      <p
        class="text-2xl/7 font-bold text-gray-900 hover:underline cursor-pointer"
        @click="router.push({ path: `/projects/${project.projectId}` })"
      >
        {{ project.name }}
      </p>
      <Tag v-if="isNewPurchase" severity="success" value="New purchase" />
    </div>
    <p class="text-xs text-gray-500 pb-3">Owner since {{ new Date(userProject.timeOfPurchase).toDateString() }}</p>
    <p class="text-sm text-gray-500">
      You own <b class="text-blue-400">{{ userProject.cellIds.length }} </b> cells in this project, which is
      <b class="text-blue-400">{{ userProject.percentageOwned }}%</b> of the total cells.
    </p>
  </div>
</template>
