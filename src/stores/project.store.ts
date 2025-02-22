import { defineStore } from "pinia";
import { ref } from "vue";
import {
  type Project,
  type EnergyDataPoint,
  type PowerDataPoint,
  type Panel,
} from "./project.types";

const mockProjects: Project[] = [
  {
    id: "1",
    name: "Berlin Project",
    locationCity: "Berlin",
    locationCountry: "Germany",
    locationBiddingZone: "DE",
    installedCapacity: "100 MW",
    description: "This is a project in Berlin",
    numberOfCells: 1000,
    isCompleted: true,
    completedDate: new Date("2021-01-01"),
  },
  {
    id: "2",
    name: "Hamburg Project",
    locationCity: "Hamburg",
    locationCountry: "Germany",
    locationBiddingZone: "DE",
    installedCapacity: "200 MW",
    description: "This is a project in Hamburg",
    numberOfCells: 30403,
    isCompleted: false,
    completedDate: new Date("2025-06-01"),
  },
  {
    id: "3",
    name: "Oslo Project",
    locationCity: "Oslo",
    locationCountry: "Norway",
    locationBiddingZone: "NO2",
    installedCapacity: "300 MW",
    description: "This is a project in Oslo",
    numberOfCells: 2000,
    isCompleted: true,
    completedDate: new Date("2023-01-01"),
  },
  {
    id: "4",
    name: "Frankfurt Project",
    locationCity: "Frankfurt",
    locationCountry: "Germany",
    locationBiddingZone: "DE",
    installedCapacity: "400 MW",
    description: "This is a project in Frankfurt",
    numberOfCells: 100,
    isCompleted: true,
    completedDate: new Date("2024-01-01"),
  },
  {
    id: "5",
    name: "Cologne Project",
    locationCity: "Cologne",
    locationCountry: "Germany",
    locationBiddingZone: "DE",
    installedCapacity: "500 MW",
    description: "This is a project in Cologne",
    numberOfCells: 10,
    isCompleted: true,
    completedDate: new Date("2025-01-01"),
  },
];

const mockEnergyDataResponse: Array<EnergyDataPoint> = [
  { timestamp: new Date("2025-02-21T08:00:00Z"), production: 150 },
  { timestamp: new Date("2025-02-21T09:00:00Z"), production: 175 },
  { timestamp: new Date("2025-02-21T10:00:00Z"), production: 200 },
  { timestamp: new Date("2025-02-21T11:00:00Z"), production: 180 },
  { timestamp: new Date("2025-02-21T12:00:00Z"), production: 210 },
];
const mockPowerDataResponse: Array<PowerDataPoint> = [
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

const mockPanels: Array<Panel> = [
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

export const useProjectStore = defineStore("project", () => {
  const status = {
    fetchProjects: ref<"idle" | "loading" | "success" | "error">("idle"),
    fetchProject: ref<"idle" | "loading" | "success" | "error">("idle"),
    fetchEnergyData: ref<"idle" | "loading" | "success" | "error">("idle"),
    fetchPowerData: ref<"idle" | "loading" | "success" | "error">("idle"),
    fetchPanelArray: ref<"idle" | "loading" | "success" | "error">("idle"),
  };
  const errorMsg = {
    fetchProject: ref<string | null>(null),
    fetchProjects: ref<string | null>(null),
    fetchEnergyData: ref<string | null>(null),
    fetchPowerData: ref<string | null>(null),
    fetchPanelArray: ref<string | null>(null),
  };
  const projects = ref<Project[]>([]);
  const currentProject = ref<Project | null>(null);

  async function fetchProjects() {
    status.fetchProjects.value = "loading";
    // projects.value = await fetch("https://api.example.com/projects")
    //   .then((res) => {
    //     if (!res.ok) {
    //       throw new Error("Failed to fetch projects");
    //     }
    //     return res;
    //   })
    //   .then((res) => res.json())
    //   .catch((error) => {
    //     status.value = "error";
    //     console.error(error);
    //     return [];
    //   });

    await new Promise((resolve) => setTimeout(resolve, 1000));
    status.fetchProjects.value = "success";
    projects.value = [...mockProjects];
  }

  function findProjectById(id: string) {
    return projects.value.find((project) => project.id === id);
  }

  async function fetchProject(projectId: string) {
    status.fetchProject.value = "loading";
    // const response = await fetch(`https://api.example.com/projects/${id}`);
    // currentProject.value = await response.json();
    status.fetchProject.value = "success";
    currentProject.value =
      mockProjects.find((project) => project.id === projectId) || null;
  }

  const energyData = ref<Array<EnergyDataPoint>>([]);
  async function fetchEnergyData(projectId: string) {
    status.fetchEnergyData.value = "loading";

    try {
      // const response = await fetch(`/api/projects/${projectId}/energy`);
      // if (!response.ok) throw new Error("Failed to fetch energy data");

      // const data: EnergyDataResponse = await response.json();
      energyData.value = mockEnergyDataResponse;
    } catch (err) {
      errorMsg.fetchEnergyData.value = (err as Error).message;
      status.fetchEnergyData.value = "error";
    } finally {
      status.fetchEnergyData.value = "success";
    }
  }
  const powerData = ref<Array<PowerDataPoint>>([]);
  async function fetchPowerData(projectId: string) {
    status.fetchPowerData.value = "loading";
    try {
      // const response = await fetch(`/api/projects/${projectId}/energy`);
      // if (!response.ok) throw new Error("Failed to fetch energy data");

      // const data: PowerDataResponse = await response.json();
      powerData.value = mockPowerDataResponse;
    } catch (err) {
      errorMsg.fetchPowerData.value = (err as Error).message;
      status.fetchPowerData.value = "error";
    } finally {
      status.fetchPowerData.value = "success";
    }
  }
  const panelArray = ref<Array<Panel>>([]);
  async function fetchPanelArray(projectId: string) {
    status.fetchPanelArray.value = "loading";
    try {
      // const response = await fetch(`/api/projects/${projectId}/energy`);
      // if (!response.ok) throw new Error("Failed to fetch energy data");

      // const data: EnergyDataResponse = await response.json();
      panelArray.value = mockPanels;
      status.fetchPanelArray.value = "success";
    } catch (err) {
      errorMsg.fetchPanelArray.value = (err as Error).message;
      status.fetchPanelArray.value = "error";
    } finally {
    }
  }

  return {
    projects,
    status,
    errorMsg,
    fetchEnergyData,
    energyData,
    fetchPowerData,
    powerData,
    panelArray,
    fetchPanelArray,
    currentProject,
    findProjectById,
    fetchProjects,
    fetchProject,
  };
});
