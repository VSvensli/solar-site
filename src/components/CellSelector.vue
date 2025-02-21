<script setup lang="ts">
import { useCell } from "@/stores/cellStore";
import { onMounted } from "vue";
import { storeToRefs } from "pinia";

const cellStore = useCell();
const { panelArray, loading, error } = storeToRefs(cellStore);

const props = defineProps<{ projectId: string }>();

onMounted(() => {
  cellStore.fetchPanelArray(props.projectId);
});
</script>

<template>
  <div class="w-100 h-100 bg-amber-500">
    CellSelector
    <div v-if="loading">Loading...</div>
    <div v-if="error">{{ error }}</div>
    <div v-if="panelArray">
      <div
        v-for="panel in panelArray"
        :key="panel.id"
        class="bg-gray-200 m-4 w-50"
      >
        Panel {{ panel.id }}
        <div
          v-for="cell in panel.cells"
          :key="cell.id"
          class="m-4 w-20"
          :style="`background-color: ${cell.color}`"
        >
          Cell {{ cell.id }}
        </div>
      </div>
    </div>
  </div>
</template>
