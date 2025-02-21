import { defineStore } from "pinia";
import { ref } from "vue";

export type Project = {
  id: string;
  name: string;
  locationCity: string;
  locationCountry: string;
  locationBiddingZone: string;
  installedCapacity: string;
  description: string;
  purchasedCellPercentage: string;
  isCompleted: boolean;
  completedDate: Date;
};

const mockProjects: Project[] = [
  {
    id: "1",
    name: "Berlin Project",
    locationCity: "Berlin",
    locationCountry: "Germany",
    locationBiddingZone: "DE",
    installedCapacity: "100 MW",
    description: "This is a project in Berlin",
    purchasedCellPercentage: "100%",
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
    purchasedCellPercentage: "50%",
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
    purchasedCellPercentage: "75%",
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
    purchasedCellPercentage: "25%",
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
    purchasedCellPercentage: "0%",
    isCompleted: true,
    completedDate: new Date("2025-01-01"),
  },
];

export const useProjectStore = defineStore("project", () => {
  const status = {
    fetchProjects: ref<"idle" | "loading" | "success" | "error">("idle"),
    fetchProject: ref<"idle" | "loading" | "success" | "error">("idle"),
  };
  const errorMsg = {
    fetchProject: ref<string | null>(null),
    fetchProjects: ref<string | null>(null),
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
  async function fetchProject(id: string) {
    status.fetchProject.value = "loading";
    // const response = await fetch(`https://api.example.com/projects/${id}`);
    // currentProject.value = await response.json();
    status.fetchProject.value = "success";
    currentProject.value =
      mockProjects.find((project) => project.id === id) || null;
  }
  return {
    projects,
    status,
    currentProject,
    fetchProjects,
    fetchProject,
  };
});
