<script setup lang="ts">
import { useProjectStore } from "@/stores/project.store";
import { useUserStore } from "@/stores/user.store";
import { onMounted } from "vue";
import { storeToRefs } from "pinia";

const projectStore = useProjectStore();
const userStore = useUserStore();
const { panelArray } = storeToRefs(projectStore);
const { selectedCellIds } = storeToRefs(userStore);

const props = defineProps<{ projectId: string }>();

function isSelected(cellId: string) {
  return selectedCellIds.value.find((selection) => selection.cellId === cellId) ? true : false;
}

onMounted(() => {
  projectStore.fetchPanelArray(props.projectId);
});
</script>

<template>
  <div>
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
    5px 0%,
    calc(100% - 5px) 0%,
    100% 5px,
    100% calc(100% - 5px),
    calc(100% - 5px) 100%,
    5px 100%,
    0 calc(100% - 5px)
  );
}
</style>
