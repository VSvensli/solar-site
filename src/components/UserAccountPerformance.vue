<script setup lang="ts">
import { computed } from "vue";
import { useUserStore } from "@/stores/user.store";
import Chart from "primevue/chart";

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
        callback: function (value: number, index: number, values: number[]) {
          return "$ " + value;
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
    <Chart type="line" :data="chartData" :options="chartOptions" />
  </div>
</template>
