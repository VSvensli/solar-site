import { defineStore } from "pinia";
import { ref } from "vue";
import { type Project, type EnergyDataPoint, type PowerDataPoint, type Panel } from "./project.types";

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
    fetch("/projects", {
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
    return projects.value.find((project) => project.projectId === id);
  }

  async function fetchProject(projectId: string) {
    status.fetchProjects.value = "loading";
    const url = `/projects/${projectId}`;
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
    const url = `/projects/${projectId}/energy`;
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
    const url = `/projects/${projectId}/power`;
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
    const url = `/projects/${projectId}/panels`;
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
        return response.json() as Promise<Array<Panel>>;
      })
      .then((data) => {
        panelArray.value = data.map((panel) => ({ ...panel }));
        status.fetchPanelArray.value = "success";
      })
      .catch((error) => {
        status.fetchPanelArray.value = "error";
        errorMsg.fetchPanelArray.value = error.message;
      });
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
