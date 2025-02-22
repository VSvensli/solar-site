<script setup lang="ts">
import { useUserStore } from "@/stores/user.store";
import { useProjectStore } from "@/stores/project.store";
import { useRouter } from "vue-router";
import Button from "primevue/button";

const userStore = useUserStore();
const projectStore = useProjectStore();

const router = useRouter();
</script>

<template>
  <div>
    <h1>Checkout</h1>
    <div>
      <h2>Selected Cells</h2>
      <ul>
        <li v-for="cell in userStore.selectedCells" :key="cell">
          Cell {{ cell }}
        </li>
      </ul>
      <Button @click="userStore.selectedCells = []" label="Clear Selection" />
    </div>
    <div>
      <Button
        @click="
          router.push({
            name: 'ProjectDetails',
            params: { id: `${projectStore.currentProject?.id}` },
          })
        "
        label="Back to Project"
      />
    </div>
  </div>
</template>
