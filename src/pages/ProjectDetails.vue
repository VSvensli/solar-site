<script setup lang="ts">
import { onMounted, computed } from "vue";
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
import { storeToRefs } from "pinia";
import { formatDollar } from "@/utils";

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const projectStore = useProjectStore();
const userStore = useUserStore();

const { selectedCellIds } = storeToRefs(userStore);

const totalPrice = computed(() => {
  return selectedCellIds.value.reduce((acc, selection) => {
    return acc + (projectStore.findProjectById(selection.projectId)?.unitPrice || 0);
  }, 0);
});

const price = computed(() => {
  return selectedCellIds.value
    .filter((cell) => cell.projectId === route.params.id)
    .reduce((acc, selection) => {
      return acc + (projectStore.findProjectById(selection.projectId)?.unitPrice || 0);
    }, 0);
});

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
        <div class="pb-4 border-b-2 border-gray-200">
          <EnergyChart :projectId="projectStore.currentProject.projectId" />
        </div>
        <div>
          <PowerChart :projectId="projectStore.currentProject.projectId" />
        </div>
      </div>
      <div class="bg-white p-4 rounded-lg shadow-md flex flex-col relative">
        <div class="text-center flex-grow">
          <div>
            <p class="text-lg font-semibold">Total Price</p>
            <p class="text-xl text-gray-700">{{ formatDollar(totalPrice) }}</p>
          </div>
          <div class="mb-4">
            <p class="text-lg font-semibold">Project Price</p>
            <p class="text-xl text-gray-700">{{ formatDollar(price) }}</p>
          </div>
        </div>
        <div class="flex justify-end mt-4">
          <p v-if="!authStore.isAuthenticated" class="text-xs text-gray-400 p-4">
            You need to be logged in to checkout
          </p>
          <Button
            :disabled="userStore.selectedCellIds.length === 0 || !authStore.isAuthenticated"
            label="Checkout"
            @click="() => router.push({ name: 'Checkout' })"
          />
        </div>
      </div>
    </div>

    <div class="bg-white p-4 mt-4 rounded-lg shadow-md">
      <h2 class="text-2xl/7 font-semibold text-gray-700 p-3">Cell selection</h2>
      <div class="flex justify-center">
        <CellSelector :projectId="projectStore.currentProject.projectId" />
      </div>
    </div>
  </div>
  <div v-else>No project found</div>
</template>
