<!-- components/EnergyChart.vue -->
<script setup lang="ts">
import { onMounted, computed } from "vue";
import { useProjectStore } from "@/stores/project.store";
import { storeToRefs } from "pinia";
import { parsePowerValueToString } from "@/utils";
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
  // scales: {
  //   y: {
  //     ticks: {
  //       callback: function (value: number, index: number, values: number[]) {
  //         return parsePowerValueToString(value);
  //       },
  //     },
  //   },
  // },
};

// https://www.chartjs.org/docs/latest/samples/line/segments.html
const chartData = computed(() => ({
  labels: powerData.value.map((dp) => dp.timestamp.toLocaleTimeString()), // X-axis labels
  datasets: [
    {
      label: "Power Production",
      data: powerData.value.map((dp) => dp.production), // Y-axis values
      borderColor: "blue", // Default color for actual data
      fill: true,
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
    <!-- <p v-if="status.fetchPowerData.value === 'loading'">Loading...</p>
    <p v-if="status.fetchPowerData.value === 'error'">
      {{ errorMsg.fetchPowerData.value }}
    </p> -->
    <div>
      <Line v-if="powerData.length" :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>
