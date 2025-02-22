<!-- components/EnergyChart.vue -->
<script setup lang="ts">
import { onMounted, computed } from "vue";
import { useProjectStore } from "@/stores/project.store";
import { storeToRefs } from "pinia";
import Chart from "primevue/chart";
import { formatEnergy } from "@/utils";

const props = defineProps<{ projectId: string | null }>();

const peojectStore = useProjectStore();
const { energyData } = storeToRefs(peojectStore);

onMounted(() => {
  if (props.projectId) {
    peojectStore.fetchEnergyData(props.projectId);
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
  scales: {
    y: {
      ticks: {
        callback: function (value: number, index: number, values: number[]) {
          return formatEnergy(value);
        },
      },
    },
  },
};

const chartData = computed(() => ({
  labels: energyData.value.map((dp) => dp.timestamp.toDateString()), // X-axis labels
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
  <div>
    <h2>Energy Production History</h2>

    <!-- <p v-if="status.fetchEnergyData.value === 'loading'">Loading...</p>
    <p v-if="status.fetchEnergyData.value === 'error'">
      {{ errorMsg.fetchEnergyData.value }}
    </p> -->
    <div>
      <Chart type="bar" :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>
