<script setup lang="ts">
import { onMounted } from "vue";
import UserProjectCard from "@/components/UserProjectCard.vue";
import UserAccountBalance from "@/components/UserAccountStatistics.vue";
import UserAccountPerformance from "@/components/UserAccountPerformance.vue";
import { useUserStore } from "@/stores/user.store";
const userStore = useUserStore();

onMounted(() => {
  userStore.fetchUserData();
});
</script>

<template>
  <div>
    <div class="grid grid-cols-2 gap-5 mb-5">
      <div class="bg-white p-4 rounded-lg shadow-md">
        <UserAccountPerformance />
      </div>
      <div class="bg-white p-4 rounded-lg shadow-md">
        <UserAccountBalance />
      </div>
    </div>
    <div class="text-2xl/7 font-semibold transform translate-y-1/2 translate-x-1/8 bg-slate-50 text-gray-400 p-2 w-40">
      My projects
    </div>
    <div class="space-y-2 border-2 border-gray-300 rounded-lg p-3">
      <UserProjectCard
        v-for="userProject in userStore.userData.projects"
        :key="userProject.projectId"
        :userProject="userProject"
        class="[&:not(:last-child)]:border-b-2 p-4 border-gray-300"
      />
    </div>
  </div>
</template>
