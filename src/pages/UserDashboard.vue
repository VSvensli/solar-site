<script setup lang="ts">
import { onMounted } from "vue";
import UserProjectCard from "@/components/UserProjectCard.vue";
import UserAccountBalance from "@/components/UserAccountBalance.vue";
import UserAccountPerformance from "@/components/UserAccountPerformance.vue";
import { useUserStore } from "@/stores/user.store";
const userProjectStore = useUserStore();

onMounted(() => {
  userProjectStore.fetchUserProjects();
});
</script>

<template>
  <div>
    <UserProjectCard
      v-for="userProject in userProjectStore.userProjects"
      :key="userProject.projectId"
      :userProjectStatistics="userProject"
    />
    <UserAccountBalance />
    <UserAccountPerformance />
  </div>
</template>
