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

const chartData = computed(() => {
  return {
    labels: userPerformance.value.map((item) => item.timestamp),
    datasets: [
      {
        label: "Performance",
        data: userPerformance.value.map((item) => item.value),
        borderColor: "#3e95cd",
        fill: false,
      },
    ],
  };
});
</script>

<template>
  <div class="card">
    <Chart type="line" :data="chartData" class="h-[30rem]" />
  </div>
</template>
