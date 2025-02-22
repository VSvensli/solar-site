<script setup lang="ts">
import { useUserStore } from "@/stores/user.store";
import { onMounted } from "vue";
import { storeToRefs } from "pinia";
import { formatDollar, formatEnergy, formatPower } from "@/utils";
import Button from "primevue/button";

const userStore = useUserStore();
const { userStatistics } = storeToRefs(userStore);

onMounted(() => {
  userStore.fetchUserStatistics();
});
</script>

<template>
  <div>
    <div>
      <p class="text-2xl/7 font-bold text-gray-900">Overview</p>
      <p class="text-xl text-gray-900">Balance: {{ formatDollar(userStatistics.accountBalance) }}</p>
      <p class="text-md font-medium text-gray-900">Total invested: {{ formatDollar(userStatistics.totalInvested) }}</p>
      <p class="m-0">Total earned: {{ formatDollar(userStatistics.totalEarnings) }}</p>
      <p class="m-0">Total energy generated: {{ formatEnergy(userStatistics.totalEnergyGenerated) }}</p>
      <p class="m-0">
        Max power generation capacity:
        {{ formatPower(userStatistics.maximumPowerGeneration) }}
      </p>
      <p class="m-0">Number of cells owned {{ userStatistics.cellsOwned }}</p>
    </div>
    <Button label="Add funds" icon="pi-dollar" @click="userStore.fetchUserStatistics" />
  </div>
</template>
