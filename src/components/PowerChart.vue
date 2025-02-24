<!-- components/EnergyChart.vue -->
<script setup lang="ts">
import { onMounted, computed } from "vue";
import { useProjectStore } from "@/stores/project.store";
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

ChartJS.register(CategoryScale, LineElement, PointElement, LinearScale, Title, Tooltip, Legend);

const props = defineProps<{ projectId: string | null }>();

const projectStore = useProjectStore();
const { powerData } = storeToRefs(projectStore);

onMounted(() => {
  if (props.projectId) {
    projectStore.fetchPowerData(props.projectId);
  } else {
    console.warn("Project ID is null. Skipping fetch.");
  }
});

const chartOptions = {
  plugins: {
    legend: {
      display: false,
    },
  },
  elements: {
    line: {
      tension: 0.4,
    },
  },
};

//https://www.chartjs.org/docs/latest/samples/line/segments.html
const chartData = computed(() => ({
  labels: powerData.value.map((dp) => dp.timestamp.toLocaleTimeString()),
  datasets: [
    {
      label: "Power Production",
      data: powerData.value.map((dp) => dp.production),
      pointRadius: 0,
      pointBackgroundColor: "gray",
      pointBorderColor: "gray",
      segment: {
        borderDash: (ctx: ScriptableLineSegmentContext) => {
          const index = ctx.p1DataIndex;
          return powerData.value[index]?.isPredicted ? [5, 5] : [];
        },
        borderColor: (ctx: ScriptableLineSegmentContext) => {
          const index = ctx.p1DataIndex;
          return powerData.value[index]?.isPredicted ? "rgba(201, 203, 207, 0.5)" : "rgba(54, 162, 235, 0.8)";
        },
      },
    },
  ],
}));
</script>

<template>
  <div>
    <h2 class="text-2xl/7 font-semibold text-gray-700 p-3">Power production</h2>
    <div>
      <Line v-if="powerData.length" :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>
