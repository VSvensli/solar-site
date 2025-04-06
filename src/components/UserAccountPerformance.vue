<script setup lang="ts">
import { computed } from "vue";
import { useUserStore } from "@/stores/user.store";
import {
  Chart as ChartJS,
  CategoryScale,
  LineElement,
  PointElement,
  LinearScale,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Line } from "vue-chartjs";

ChartJS.register(CategoryScale, LineElement, PointElement, LinearScale, Title, Tooltip, Legend);

const userStore = useUserStore();

const chartOptions = {
  plugins: {
    legend: {
      display: false,
    },
  },
  elements: {
    point: {
      radius: 3,
      backgroundColor: "green",
    },
    line: {
      tension: 0.4,
      borderColor: "green",
    },
  },
  scales: {
    y: {
      ticks: {
        callback: function (tickValue: string | number) {
          return "$ " + tickValue;
        },
      },
    },
  },
};
const chartData = computed(() => {
  return {
    labels: userStore.userData.performance.map((item) => new Date(item.timestamp).toDateString()),
    datasets: [
      {
        data: userStore.userData.performance.map((item) => item.value),
        fill: true,
      },
    ],
  };
});
</script>

<template>
  <div>
    <h2 class="text-2xl/7 font-semibold text-gray-700 p-3">Historic performance</h2>
    <Line :data="chartData" :options="chartOptions" />
  </div>
</template>
