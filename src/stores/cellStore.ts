import { defineStore } from "pinia";
import { ref } from "vue";

type Cell = {
  id: string;
  ownerId: string;
  price: number;
  cellRow: number;
  cellColumns: number;
  color: string;
};

type Panel = {
  id: string;
  description: string;
  cells: Cell[];
};

type PanelArray = Panel[];

const mockPanels: PanelArray = [
  {
    id: "1",
    description: "Panel 1",
    cells: [
      {
        id: "1",
        ownerId: "1",
        price: 100,
        cellColumns: 0,
        cellRow: 0,
        color: "#FF0000",
      },
      {
        id: "2",
        ownerId: "1",
        price: 200,
        cellColumns: 0,
        cellRow: 1,
        color: "#FF0000",
      },
    ],
  },
  {
    id: "2",
    description: "Panel 2",
    cells: [
      {
        id: "1",
        ownerId: "1",
        price: 200,
        cellColumns: 0,
        cellRow: 0,
        color: "#FFF200",
      },
      {
        id: "2",
        ownerId: "1",
        price: 200,
        cellColumns: 0,
        cellRow: 1,
        color: "#FF0000",
      },
    ],
  },
];

export const useCell = defineStore("cell", () => {
  const panelArray = ref<PanelArray>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);

  const fetchPanelArray = async (projectId: string) => {
    loading.value = true;
    error.value = null;
    try {
      // const response = await fetch(`/api/projects/${projectId}/energy`);
      // if (!response.ok) throw new Error("Failed to fetch energy data");

      // const data: EnergyDataResponse = await response.json();
      panelArray.value = mockPanels;
    } catch (err) {
      error.value = (err as Error).message;
    } finally {
      loading.value = false;
    }
  };

  return { panelArray, fetchPanelArray, loading, error };
});
