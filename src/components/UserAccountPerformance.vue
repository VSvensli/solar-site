<script setup lang="ts">
import { onMounted, computed } from "vue";
import { storeToRefs } from "pinia";
import { useUserStore } from "@/stores/user.store";
import Chart from "primevue/chart";

const userStore = useUserStore();
const { userPerformance } = storeToRefs(userStore);

onMounted(() => {
  userStore.fetchUserPerformance();
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
    labels: userPerformance.value.map((item) => item.timestamp.toDateString()),
    datasets: [
      {
        data: userPerformance.value.map((item) => item.value),
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
