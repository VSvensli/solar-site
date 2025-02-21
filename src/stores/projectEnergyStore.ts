import { defineStore } from "pinia";
import { ref } from "vue";

export type EnergyDataPoint = {
  timestamp: Date;
  production: number;
};

export type EnergyDataResponse = EnergyDataPoint[];

const mockEnergyDataResponse: EnergyDataResponse = [
  { timestamp: new Date("2025-02-21T08:00:00Z"), production: 150 },
  { timestamp: new Date("2025-02-21T09:00:00Z"), production: 175 },
  { timestamp: new Date("2025-02-21T10:00:00Z"), production: 200 },
  { timestamp: new Date("2025-02-21T11:00:00Z"), production: 180 },
  { timestamp: new Date("2025-02-21T12:00:00Z"), production: 210 },
];
// Note: Is this a better appriach than useProjectStore with regards to the error handling?
export const useEnergyStore = defineStore("energy", () => {
  const energyData = ref<EnergyDataResponse>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);

  const fetchEnergyData = async (projectId: string) => {
    loading.value = true;
    error.value = null;
    try {
      // const response = await fetch(`/api/projects/${projectId}/energy`);
      // if (!response.ok) throw new Error("Failed to fetch energy data");

      // const data: EnergyDataResponse = await response.json();
      energyData.value = mockEnergyDataResponse;
    } catch (err) {
      error.value = (err as Error).message;
    } finally {
      loading.value = false;
    }
  };

  return { energyData, fetchEnergyData, loading, error };
});
