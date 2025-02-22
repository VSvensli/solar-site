<!-- components/EnergyChart.vue -->
<script setup lang="ts">
import { onMounted, computed } from "vue";
import { useEnergyStore } from "@/stores/projectEnergyStore";
import { storeToRefs } from "pinia";
import Chart from "primevue/chart";

const props = defineProps<{ projectId: string | null }>();

const energyStore = useEnergyStore();
const { energyData, loading, error } = storeToRefs(energyStore);

onMounted(() => {
  if (props.projectId) {
    energyStore.fetchEnergyData(props.projectId);
  } else {
    console.warn("Project ID is null. Skipping fetch.");
  }
});

// Note: Not needed as EnergyChart is always destroyed/re-created when projectId changes (e.g., in a new page)
// watch(
//   () => props.projectId,
//   (newProjectId) => {
//     if (newProjectId) {
//       energyStore.fetchEnergyData(newProjectId);
//     }
//   }
// );

// Prepare chart data
const chartData = computed(() => ({
  labels: energyData.value.map((dp) => dp.timestamp), // X-axis labels
  datasets: [
    {
      label: "Energy Production",
      data: energyData.value.map((dp) => dp.production), // Y-axis values
      backgroundColor: "blue",
    },
  ],
}));
</script>

<template>
  <div class="bg-white p-4 rounded-lg shadow-md">
    <h2>Energy Production History</h2>

    <p v-if="loading">Loading...</p>
    <p v-if="error">{{ error }}</p>
    <div>
      <Chart type="bar" :data="chartData" />
    </div>
  </div>
</template>
