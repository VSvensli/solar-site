<script setup lang="ts">
import { useProjectStore } from "@/stores/project.store";
import { useUserStore } from "@/stores/user.store";
import { computed, onMounted } from "vue";
import { storeToRefs } from "pinia";

const projectStore = useProjectStore();
const userStore = useUserStore();
const { panelArray } = storeToRefs(projectStore);
const { selectedCellIds } = storeToRefs(userStore);

const props = defineProps<{ projectId: string }>();

const totalPrice = computed(() => {
  return selectedCellIds.value.reduce((acc, selection) => {
    return acc + (projectStore.findProjectById(selection.projectId)?.unitPrice || 0);
  }, 0);
});

const price = computed(() => {
  return selectedCellIds.value
    .filter((cell) => cell.projectId === props.projectId)
    .reduce((acc, selection) => {
      return acc + (projectStore.findProjectById(selection.projectId)?.unitPrice || 0);
    }, 0);
});

function isSelected(cellId: string) {
  return selectedCellIds.value.find((selection) => selection.cellId === cellId) ? true : false;
}

onMounted(() => {
  projectStore.fetchPanelArray(props.projectId);
});
</script>

<template>
  <div>
    <div>Current: {{ price }} Total: {{ totalPrice }}</div>
    CellSelector
    <div v-if="panelArray" class="flex flex-wrap gap-5">
      <div v-for="panel in panelArray" :key="panel.panelId">
        <div
          class="grid gap-1 p-2 bg-slate-200 shadow-md rounded-md"
          :style="{
            gridTemplateColumns: 'repeat(' + panel.cellColumns + ', 50px)',
            gridTemplateRows: 'repeat(' + panel.cellRows + ', 50px)',
          }"
        >
          <div
            v-for="cell in panel.cells"
            class="module"
            :key="cell.cellId"
            :class="{ 'border-4 border-red-400': isSelected(cell.cellId) }"
            :style="{ backgroundColor: cell.color }"
            @click="userStore.toggleCellSelection(cell.cellId, panel.panelId, projectId)"
          ></div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.module {
  clip-path: polygon(
    0% 5px,
    /* top left */ 5px 0%,
    /* top left */ calc(100% - 5px) 0%,
    /* top right */ 100% 5px,
    /* top right */ 100% calc(100% - 5px),
    /* bottom right */ calc(100% - 5px) 100%,
    /* bottom right */ 5px 100%,
    /* bottom left */ 0 calc(100% - 5px) /* bottom left */
  );
}
</style>
