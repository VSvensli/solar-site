<!-- components/EnergyChart.vue -->
<script setup lang="ts">
import { onMounted, computed } from "vue";
import { usePowerStore } from "@/stores/projectPowerStore";
import { storeToRefs } from "pinia";
import {
  Chart as ChartJS,
  CategoryScale,
  LineElement,
  PointElement,
  LinearScale,
  Title,
  Tooltip,
  Legend,
  type ScriptableLineSegmentContext,
} from "chart.js";
import { Line } from "vue-chartjs";

ChartJS.register(
  CategoryScale,
  LineElement,
  PointElement,
  LinearScale,
  Title,
  Tooltip,
  Legend
);

const props = defineProps<{ projectId: string | null }>();

const powerStore = usePowerStore();
const { powerData, loading, error } = storeToRefs(powerStore);

onMounted(() => {
  if (props.projectId) {
    powerStore.fetchPowerData(props.projectId);
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

// https://www.chartjs.org/docs/latest/samples/line/segments.html
const chartData = computed(() => ({
  labels: powerData.value.map((dp) => dp.timestamp), // X-axis labels
  datasets: [
    {
      label: "Energy Production",
      data: powerData.value.map((dp) => dp.production), // Y-axis values
      borderColor: "blue", // Default color for actual data
      fill: false,
      segment: {
        borderDash: (ctx: ScriptableLineSegmentContext) => {
          const index = ctx.p1DataIndex; // Get the next data point
          return powerData.value[index]?.isPredicted ? [5, 5] : []; // Dotted if next is predicted
        },
        borderColor: (ctx: ScriptableLineSegmentContext) => {
          const index = ctx.p1DataIndex;
          return powerData.value[index]?.isPredicted ? "red" : "blue"; // Change color dynamically
        },
      },
    },
  ],
}));
</script>

<template>
  <div>
    <h2>Site Power Production</h2>
    <p v-if="loading">Loading...</p>
    <p v-if="error">{{ error }}</p>
    <div>
      <Line v-if="powerData.length" :data="chartData" />
    </div>
  </div>
</template>

<style scoped>
.chart-container {
  width: 100%;
  height: 400px;
}
</style>
