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
    line: {
      tension: 0.4,
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
        borderColor: "#3e95cd",
        fill: false,
      },
    ],
  };
});
</script>

<template>
  <div>
    <Chart type="line" :data="chartData" :options="chartOptions" class="h-[30rem]" />
  </div>
</template>
