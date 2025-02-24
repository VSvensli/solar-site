<script setup lang="ts">
import { useUserStore } from "@/stores/user.store";
import { useProjectStore } from "@/stores/project.store";
import { useRouter } from "vue-router";
import Button from "primevue/button";
import { useToast } from "primevue/usetoast";

const toast = useToast();
const userStore = useUserStore();
const projectStore = useProjectStore();

const router = useRouter();

async function processPayment() {
  await userStore.postCellPurchaseRequest();

  if (userStore.status.fetchProjectProfits === "success") {
    toast.add({
      severity: "error",
      summary: "Error",
      detail: "Failed to process payment",
    });
    router.push({ name: "UserDashboard" });
  } else {
    console.log("Failed to process payment");
    toast.add({
      severity: "error",
      summary: "Error",
      detail: "Failed to process payment",
    });
  }
}
</script>

<template>
  <div>
    <h1>Checkout</h1>
    <div>
      <h2>Selected Cells</h2>
      <ul>
        <li v-for="cell in userStore.selectedCellIds" :key="cell">Cell {{ cell }}</li>
      </ul>
      <Button @click="userStore.selectedCellIds = []" label="Clear Selection" />
    </div>
    <div>
      <Button
        @click="
          router.push({
            name: 'ProjectDetails',
            params: { id: `${projectStore.currentProject?.projectId}` },
          })
        "
        label="Back to Project"
      />
    </div>
    <div>
      <Button
        @click="processPayment()"
        label="Proceed to
      Payment"
      />
    </div>
  </div>
</template>
