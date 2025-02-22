<script setup lang="ts">
import { useUserStore } from "@/stores/user.store";
import { onMounted } from "vue";
import { storeToRefs } from "pinia";
import Card from "primevue/card";

const userStore = useUserStore();
const { userStatistics } = storeToRefs(userStore);

onMounted(() => {
  userStore.fetchUserStatistics();
});
</script>

<template>
  <div>
    <Card>
      <template #title>Account Overview</template>
      <template #content>
        <p class="m-0"></p>
        <p class="m-0">Available funds: {{ userStatistics.accountBalance }}</p>
        <p class="m-0">Total invested: {{ userStatistics.totalInvested }}</p>
        <p class="m-0">Total earned: {{ userStatistics.totalEarnings }}</p>
        <p class="m-0">
          Total energy generated: {{ userStatistics.totalEnergyGenerated }}
        </p>
        <p class="m-0">
          Max power generation capacity:
          {{ userStatistics.maximumPowerGeneration }}
        </p>
        <p class="m-0">Number of cells owned {{ userStatistics.cellsOwned }}</p>
      </template>
    </Card>
  </div>
</template>
