<script setup lang="ts">
import { computed } from "vue";
import { useProjectStore } from "@/stores/project.store";
import { type UserProject } from "@/stores/user.types";

const projectStore = useProjectStore();

const props = defineProps<{
  userProjectStatistics: UserProject;
}>();

const project = computed(() =>
  projectStore.findProjectById(props.userProjectStatistics.projectId)
);
</script>

<template>
  <div v-if="project" class="p-4 border-1 shadow-lg rounded-lg">
    Project name: {{ project.name }} Number of cells:{{
      userProjectStatistics.cellIds.length
    }}
    Percentage of cells owned {{ userProjectStatistics.percentageOwned }} Time
    of purchase: {{ userProjectStatistics.timeOfPurchase }}
  </div>
</template>
