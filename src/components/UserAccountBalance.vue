<script setup lang="ts">
import { useUserStore } from "@/stores/user.store";
import { onMounted } from "vue";
import { storeToRefs } from "pinia";
import Card from "primevue/card";

const userFundsStore = useUserStore();
const { userFunds } = storeToRefs(userFundsStore);

onMounted(() => {
  userFundsStore.fetchUserFunds();
});
</script>

<template>
  <div>
    <Card>
      <template #title>Account balance</template>
      <template #content>
        <p class="m-0"></p>
        <p class="m-0">Available funds: {{ userFunds.accountBalance }}</p>
      </template>
    </Card>
  </div>
</template>
