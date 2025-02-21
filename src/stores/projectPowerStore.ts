import { defineStore } from "pinia";
import { ref } from "vue";

export type PowerDataPoint = {
  timestamp: Date;
  production: number;
  isPredicted: boolean;
};

export type PowerDataResponse = PowerDataPoint[];

const mockPowerDataResponse: PowerDataResponse = [
  {
    timestamp: new Date("2025-02-21T08:00:00Z"),
    production: 150,
    isPredicted: false,
  },
  {
    timestamp: new Date("2025-02-21T09:00:00Z"),
    production: 175,
    isPredicted: false,
  },
  {
    timestamp: new Date("2025-02-21T10:00:00Z"),
    production: 200,
    isPredicted: false,
  },
  {
    timestamp: new Date("2025-02-21T11:00:00Z"),
    production: 180,
    isPredicted: false,
  },
  {
    timestamp: new Date("2025-02-21T12:00:00Z"),
    production: 210,
    isPredicted: false,
  },
  {
    timestamp: new Date("2025-02-21T13:00:00Z"),
    production: 300,
    isPredicted: false,
  },
  {
    timestamp: new Date("2025-02-21T14:00:00Z"),
    production: 220,
    isPredicted: true,
  },
  {
    timestamp: new Date("2025-02-21T15:00:00Z"),
    production: 200,
    isPredicted: true,
  },
  {
    timestamp: new Date("2025-02-21T16:00:00Z"),
    production: 180,
    isPredicted: true,
  },
  {
    timestamp: new Date("2025-02-21T17:00:00Z"),
    production: 100,
    isPredicted: true,
  },
];

// Note: This should have a location ID as input instad of the project id
export const usePowerStore = defineStore("power", () => {
  const powerData = ref<PowerDataResponse>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);

  const fetchPowerData = async (projectId: string) => {
    loading.value = true;
    error.value = null;
    try {
      // const response = await fetch(`/api/projects/${projectId}/energy`);
      // if (!response.ok) throw new Error("Failed to fetch energy data");

      // const data: PowerDataResponse = await response.json();
      powerData.value = mockPowerDataResponse;
    } catch (err) {
      error.value = (err as Error).message;
    } finally {
      loading.value = false;
    }
  };

  return { powerData, fetchPowerData, loading, error };
});
