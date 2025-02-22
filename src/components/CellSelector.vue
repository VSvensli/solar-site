<script setup lang="ts">
import { useProjectStore } from "@/stores/project.store";
import { useUserStore } from "@/stores/user.store";
import { onMounted } from "vue";
import { storeToRefs } from "pinia";

const projectStore = useProjectStore();
const userStore = useUserStore();
const { panelArray } = storeToRefs(projectStore);

const props = defineProps<{ projectId: string }>();

onMounted(() => {
  projectStore.fetchPanelArray(props.projectId);
});
</script>

<template>
  <div>
    CellSelector
    <div v-if="panelArray" class="flex flex-wrap gap-5">
      <div v-for="panel in panelArray" :key="panel.id">
        <div
          class="grid gap-1 p-2 bg-slate-500 shadow-sm rounded-md"
          :style="{
            gridTemplateColumns: 'repeat(' + panel.cellColumns + ', 50px)',
            gridTemplateRows: 'repeat(' + panel.cellRows + ', 50px)',
          }"
        >
          <div
            v-for="cell in panel.cells"
            class="bg-blue-200 rounded-xl border-5 border-blue-100 border-opacity-50"
            :key="cell.id"
          >
            {{ cell.id }}
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="w-100 h-100 bg-blue-100">hello</div>
</template>
