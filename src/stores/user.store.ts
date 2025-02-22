import { defineStore } from "pinia";
import { ref } from "vue";
import {
  type UserStatistics,
  type UserProject,
  type UserPerformaceDataPoint,
} from "./user.types";

const mockUserPerformance: Array<UserPerformaceDataPoint> = [
  { timestamp: "2021-01-01", value: 1000 },
  { timestamp: "2021-01-02", value: 1001 },
  { timestamp: "2021-01-03", value: 1002 },
  { timestamp: "2021-01-04", value: 1003 },
  { timestamp: "2021-01-05", value: 1004 },
];

const mockUserStatistics: UserStatistics = {
  accountBalance: 1000,
  cellsOwned: 100,
  projectsOwned: 5,
  totalInvested: 10000,
  totalEarnings: 1000,
  totalEnergyGenerated: 10000,
  maximumPowerGeneration: 1000,
};

const mockUserProjects: Array<UserProject> = [
  {
    projectId: "1",
    cellIds: ["1", "2"],
    percentageOwned: 0.023,
    timeOfPurchase: new Date(Date.parse("2024-12-17T03:24:00Z")),
  },
  {
    projectId: "2",
    cellIds: ["1", "2"],
    percentageOwned: 0.5,
    timeOfPurchase: new Date("2024-12-17T03:24:00"),
  },
  {
    projectId: "3",
    cellIds: ["1", "2"],
    percentageOwned: 0.01,
    timeOfPurchase: new Date("2024-12-17T03:24:00"),
  },
];

export const useUserStore = defineStore("user", () => {
  const status = {
    fetchUserProjects: ref<"idle" | "loading" | "success" | "error">("idle"),
    fetchUserPerformance: ref<"idle" | "loading" | "success" | "error">("idle"),
    fetchUserStatistics: ref<"idle" | "loading" | "success" | "error">("idle"),
    fetchProjectProfits: ref<"idle" | "loading" | "success" | "error">("idle"),
    postCellPurchaseRequest: ref<"idle" | "loading" | "success" | "error">(
      "idle",
    ),
  };

  const errorMsg = {
    fetchProjectProfits: ref<string | null>(null),
    fetchUserProjects: ref<string | null>(null),
    fetchUserPerformance: ref<string | null>(null),
    fetchUserStatistics: ref<string | null>(null),
    postCellPurchaseRequest: ref<string | null>(null),
  };

  const userProjects = ref<Array<UserProject>>([]);
  const currentUserId = ref<string | null>(null);

  const fetchUserProjects = async () => {
    status.fetchUserProjects.value = "loading";
    errorMsg.fetchUserProjects.value = null;
    try {
      // const response = await fetch(`/api/users/${userId}/projects`);
      // if (!response.ok) throw new Error("Failed to fetch user projects");

      // const data: UserProjects = await response.json();
      userProjects.value = mockUserProjects;
      status.fetchUserProjects.value = "success";
    } catch (err) {
      errorMsg.fetchUserProjects.value = (err as Error).message;
      status.fetchUserProjects.value = "error";
    }
  };

  const userStatistics = ref<UserStatistics>({
    accountBalance: 0,
    cellsOwned: 0,
    projectsOwned: 0,
    totalInvested: 0,
    totalEnergyGenerated: 0,
    totalEarnings: 0,
    maximumPowerGeneration: 0,
  });

  const fetchUserStatistics = async () => {
    status.fetchUserStatistics.value = "loading";
    errorMsg.fetchUserStatistics.value = null;
    try {
      // const response = await fetch(`/api/users/${userId}/funds`);
      // if (!response.ok) throw new Error("Failed to fetch user funds");

      // const data: UserFunds = await response.json();
      userStatistics.value = mockUserStatistics;
      status.fetchUserStatistics.value = "success";
    } catch (err) {
      errorMsg.fetchUserStatistics.value = (err as Error).message;
      status.fetchUserStatistics.value = "error";
    }
  };

  const userPerformance = ref<Array<UserPerformaceDataPoint>>([]);
  async function fetchUserPerformance() {
    status.fetchUserPerformance.value = "loading";
    errorMsg.fetchUserPerformance.value = null;
    try {
      // const response = await fetch(`/api/users/${userId}/performance`);
      // if (!response.ok) throw new Error("Failed to fetch user performance");
      userPerformance.value = mockUserPerformance;
      status.fetchUserPerformance.value = "success";
    } catch (err) {
      errorMsg.fetchUserPerformance.value = (err as Error).message;
      status.fetchUserPerformance.value = "error";
    }
  }

  async function postCellPurchaseRequest() {
    fetch("https://your-backend-url.com/api/endpoint", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(selectedCellIds.value),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then(() => {
        status.postCellPurchaseRequest.value = "success";
      })
      .catch((error) => {
        status.postCellPurchaseRequest.value = "error";
        errorMsg.postCellPurchaseRequest.value = error.message;
      });
  }

  const selectedCellIds = ref<Array<string>>([]);

  return {
    status,
    errorMsg,
    fetchUserProjects,
    fetchUserPerformance,
    fetchUserStatistics,
    currentUserId,
    userStatistics,
    userPerformance,
    userProjects,
    selectedCellIds,
    postCellPurchaseRequest,
  };
});
