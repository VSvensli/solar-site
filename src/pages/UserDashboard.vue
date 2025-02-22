<script setup lang="ts">
import { onMounted } from "vue";
import UserProjectCard from "@/components/UserProjectCard.vue";
import UserAccountBalance from "@/components/UserAccountStatistics.vue";
import UserAccountPerformance from "@/components/UserAccountPerformance.vue";
import { useUserStore } from "@/stores/user.store";
const userProjectStore = useUserStore();

onMounted(() => {
  userProjectStore.fetchUserProjects();
});
</script>

<template>
  <div>
    <div class="grid grid-cols-2 gap-5">
      <div class="bg-white p-4 rounded-lg shadow-md">
        <UserAccountPerformance />
      </div>
      <div class="bg-white p-4 rounded-lg shadow-md">
        <UserAccountBalance />
      </div>
    </div>
    <UserProjectCard
      v-for="userProject in userProjectStore.userProjects"
      :key="userProject.projectId"
      :userProjectStatistics="userProject"
    />
  </div>
</template>
