<script setup lang="ts">
import { useProjectStore } from "@/stores/project.store";
import { useUserStore } from "@/stores/user.store";
import { onMounted } from "vue";
import { storeToRefs } from "pinia";

const projectStore = useProjectStore();
const { panelArray } = storeToRefs(projectStore);

const props = defineProps<{ projectId: string }>();

onMounted(() => {
  projectStore.fetchPanelArray(props.projectId);
});
</script>

<template>
  <div>
    {{ panelArray }}
  </div>
  <div>
    CellSelector
    <div v-if="panelArray" class="flex flex-wrap gap-5">
      <div v-for="panel in panelArray" :key="panel.id">
        <div
          class="grid gap-1 p-2 bg-slate-200 shadow-md rounded-md"
          :style="{
            gridTemplateColumns: 'repeat(' + panel.cellColumns + ', 50px)',
            gridTemplateRows: 'repeat(' + panel.cellRows + ', 50px)',
          }"
        >
          <div v-for="cell in panel.cells" class="bg-blue-500 module" :key="cell.id">
            {{ cell.id }}
          </div>
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
