<script setup lang="ts">
import { onMounted } from "vue";
import { useRoute } from "vue-router";
import { useRouter } from "vue-router";
import { useProjectStore } from "../stores/project.store";
import { useUserStore } from "../stores/user.store";
import { useAuthStore } from "../stores/auth.store";
import ProjectDescriptionCard from "../components/ProjectDescriptionCard.vue";
import EnergyChart from "../components/EnergyChart.vue";
import PowerChart from "../components/PowerChart.vue";
import CellSelector from "../components/CellSelector.vue";
import Button from "primevue/button";

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const projectStore = useProjectStore();
const userStore = useUserStore();

onMounted(async () => {
  if (route.params.id === undefined) {
    throw new Error("No project id provided");
  }
  if (typeof route.params.id !== "string") {
    throw new Error("Project id is not a string");
  }
  await projectStore.fetchProject(route.params.id);

  if (projectStore.currentProject === null) {
    throw new Error("Project not found");
  }

  window.document.title = projectStore.currentProject.name;
});
</script>

<template>
  <div v-if="projectStore.currentProject">
    <div class="bg-white p-4 mt-5 mb-4 border-1 shadow-md rounded-lg">
      <ProjectDescriptionCard :project="projectStore.currentProject" />
    </div>
    <div class="grid grid-cols-2 gap-5">
      <div class="bg-white p-4 rounded-lg shadow-md">
        <EnergyChart :projectId="projectStore.currentProject.id" />
      </div>
      <div class="bg-white p-4 rounded-lg shadow-md">
        <PowerChart :projectId="projectStore.currentProject.id" />
      </div>
    </div>
    <div class="bg-white p-4 mt-4 rounded-lg shadow-md">
      <CellSelector :projectId="projectStore.currentProject.id" />
    </div>
    <Button
      v-if="userStore.selectedCellIds.length == 0 || !authStore.isAuthenticated"
      disabled="true"
      label="Checkout"
    />
    <Button
      v-else
      label="Checkout"
      @click="() => router.push({ name: 'Checkout' })"
    />
  </div>
  <div v-else>No project found</div>
</template>
