import { defineStore } from "pinia";
import { ref } from "vue";
import { type Project, type EnergyDataPoint, type PowerDataPoint, type Panel } from "./project.types";

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
    cellRows: 5,
    cellColumns: 3,
    cells: [
      { id: "0", ownerId: "1", price: 0.5, cellIndex: 0, color: "blue" },
      { id: "1", ownerId: "1", price: 0.5, cellIndex: 1, color: "blue" },
      { id: "2", ownerId: "1", price: 0.5, cellIndex: 2, color: "blue" },
      { id: "3", ownerId: "1", price: 0.5, cellIndex: 3, color: "blue" },
      { id: "4", ownerId: "1", price: 0.5, cellIndex: 4, color: "blue" },
      { id: "5", ownerId: "1", price: 0.5, cellIndex: 5, color: "blue" },
      { id: "6", ownerId: "1", price: 0.5, cellIndex: 6, color: "blue" },
      { id: "7", ownerId: "1", price: 0.5, cellIndex: 7, color: "blue" },
      { id: "8", ownerId: "1", price: 0.5, cellIndex: 8, color: "blue" },
      { id: "9", ownerId: "1", price: 0.5, cellIndex: 9, color: "blue" },
      { id: "10", ownerId: "1", price: 0.5, cellIndex: 10, color: "blue" },
      { id: "11", ownerId: "1", price: 0.5, cellIndex: 11, color: "blue" },
      { id: "12", ownerId: "1", price: 0.5, cellIndex: 12, color: "blue" },
      { id: "13", ownerId: "1", price: 0.5, cellIndex: 13, color: "blue" },
      { id: "14", ownerId: "1", price: 0.5, cellIndex: 14, color: "blue" },
    ],
  },
  {
    id: "2",
    description: "Panel 2",
    cellRows: 5,
    cellColumns: 3,
    cells: [
      { id: "16", ownerId: "1", price: 0.5, cellIndex: 0, color: "blue" },
      { id: "17", ownerId: "1", price: 0.5, cellIndex: 1, color: "blue" },
      { id: "18", ownerId: "1", price: 0.5, cellIndex: 2, color: "blue" },
      { id: "19", ownerId: "1", price: 0.5, cellIndex: 3, color: "blue" },
      { id: "20", ownerId: "1", price: 0.5, cellIndex: 4, color: "blue" },
      { id: "21", ownerId: "1", price: 0.5, cellIndex: 5, color: "blue" },
      { id: "22", ownerId: "1", price: 0.5, cellIndex: 6, color: "blue" },
      { id: "23", ownerId: "1", price: 0.5, cellIndex: 7, color: "blue" },
      { id: "24", ownerId: "1", price: 0.5, cellIndex: 8, color: "blue" },
      { id: "25", ownerId: "1", price: 0.5, cellIndex: 9, color: "blue" },
      { id: "26", ownerId: "1", price: 0.5, cellIndex: 10, color: "blue" },
      { id: "27", ownerId: "1", price: 0.5, cellIndex: 11, color: "blue" },
      { id: "28", ownerId: "1", price: 0.5, cellIndex: 12, color: "blue" },
      { id: "29", ownerId: "1", price: 0.5, cellIndex: 13, color: "blue" },
      { id: "30", ownerId: "1", price: 0.5, cellIndex: 14, color: "blue" },
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
    fetchEarnedSince: ref<"idle" | "loading" | "success" | "error">("idle"),
  };
  const errorMsg = {
    fetchProject: ref<string | null>(null),
    fetchProjects: ref<string | null>(null),
    fetchEnergyData: ref<string | null>(null),
    fetchPowerData: ref<string | null>(null),
    fetchPanelArray: ref<string | null>(null),
    fetchEarnedSince: ref<string | null>(null),
  };
  const projects = ref<Project[]>([]);
  const currentProject = ref<Project | null>(null);

  async function fetchProjects() {
    status.fetchProjects.value = "loading";
    fetch("http://127.0.0.1:8000/projects", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        projects.value = data;
        status.fetchProjects.value = "success";
      })
      .catch((error) => {
        status.fetchProjects.value = "error";
        errorMsg.fetchProjects.value = error.message;
      });
  }

  function findProjectById(id: string): Project | undefined {
    return projects.value.find((project) => project.id === id);
  }

  async function fetchProject(projectId: string) {
    status.fetchProjects.value = "loading";
    const url = `http://127.0.0.1:8000/projects/${projectId}`;
    fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        currentProject.value = { ...data, completedDate: new Date(data.completedDate) };
        status.fetchProject.value = "success";
      })
      .catch((error) => {
        status.fetchProject.value = "error";
        errorMsg.fetchProject.value = error.message;
      });
  }
  const energyData = ref<Array<EnergyDataPoint>>([]);
  async function fetchEnergyData(projectId: string) {
    status.fetchEnergyData.value = "loading";
    const url = `http://127.0.0.1:8000/projects/${projectId}/energy`;
    fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json() as Promise<Array<EnergyDataPoint>>;
      })
      .then((data) => {
        energyData.value = data.map((point) => ({ ...point, timestamp: new Date(point.timestamp) }));
        status.fetchEnergyData.value = "success";
      })
      .catch((error) => {
        status.fetchEnergyData.value = "error";
        errorMsg.fetchEnergyData.value = error.message;
      });
  }
  const powerData = ref<Array<PowerDataPoint>>([]);
  async function fetchPowerData(projectId: string) {
    status.fetchPowerData.value = "loading";
    const url = `http://127.0.0.1:8000/projects/${projectId}/power`;
    fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json() as Promise<Array<PowerDataPoint>>;
      })
      .then((data) => {
        powerData.value = data.map((point) => ({ ...point, timestamp: new Date(point.timestamp) }));
        status.fetchPowerData.value = "success";
      })
      .catch((error) => {
        status.fetchPowerData.value = "error";
        errorMsg.fetchPowerData.value = error.message;
      });
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
