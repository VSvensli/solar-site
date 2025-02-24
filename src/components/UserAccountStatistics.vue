<script setup lang="ts">
import { useUserStore } from "@/stores/user.store";
import { computed } from "vue";
import { formatDollar, formatEnergy, formatPower } from "@/utils";
import Button from "primevue/button";

const userStore = useUserStore();
const statistics = computed(() => userStore.userData.statistics);
</script>

<template>
  <div>
    <div>
      <p class="text-2xl/7 font-bold text-gray-900">Overview</p>
      <p class="text-xl text-gray-900">Balance: {{ formatDollar(statistics.accountBalance) }}</p>
      <p class="text-md font-medium text-gray-900">Total invested: {{ formatDollar(statistics.totalInvested) }}</p>
      <p class="m-0">Total earned: {{ formatDollar(statistics.totalEarnings) }}</p>
      <p class="m-0">Total energy generated: {{ formatEnergy(statistics.totalEnergyGenerated) }}</p>
      <p class="m-0">
        Max power generation capacity:
        {{ formatPower(userStore.userData.statistics.maximumPowerGeneration) }}
      </p>
      <p class="m-0">Number of cells owned {{ statistics.cellsOwned }}</p>
    </div>
    <div v-tooltip="'Not implemented'">
      <Button label="Add funds" disabled />
    </div>
  </div>
</template>
