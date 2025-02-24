<script setup lang="ts">
import { useUserStore } from "@/stores/user.store";
import { computed } from "vue";
import { formatDollar, formatEnergy, formatPower } from "@/utils";

const userStore = useUserStore();
const statistics = computed(() => userStore.userData.statistics);
</script>

<template>
  <h2 class="text-2xl/7 font-semibold text-gray-700 p-3">Overview</h2>

  <div class="space-y-3 p-3">
    <div class="flex justify-between">
      <span class="font-medium">Account Balance:</span>
      <span class="text-gray-700">{{ formatDollar(statistics.accountBalance) }}</span>
    </div>

    <div class="flex justify-between">
      <span class="font-medium">Total Invested:</span>
      <span class="text-gray-700">{{ formatDollar(statistics.totalInvested) }}</span>
    </div>

    <div class="flex justify-between">
      <span class="font-medium">Total Earnings:</span>
      <span class="text-gray-700">{{ formatDollar(statistics.totalEarnings) }}</span>
    </div>

    <div class="flex justify-between">
      <span class="font-medium">Energy Generated:</span>
      <span class="text-gray-700">{{ formatEnergy(statistics.totalEnergyGenerated) }}</span>
    </div>

    <div class="flex justify-between">
      <span class="font-medium">Max Power Generation:</span>
      <span class="text-gray-700">{{ formatPower(userStore.userData.statistics.maximumPowerGeneration) }}</span>
    </div>

    <div class="flex justify-between">
      <span class="font-medium">Cells Owned:</span>
      <span class="text-gray-700">{{ statistics.cellsOwned }}</span>
    </div>
  </div>
</template>
