import { defineStore } from "pinia";
import { ref } from "vue";
import { type UserStatistics, type UserProject, type UserPerformaceDataPoint, type UserData } from "./user.types";
import { useAuthStore } from "./auth.store";

export const useUserStore = defineStore("user", () => {
  const status = {
    fetchUserData: ref<"idle" | "loading" | "success" | "error">("idle"),
    postCellPurchaseRequest: ref<"idle" | "loading" | "success" | "error">("idle"),
  };

  const errorMsg = {
    fetchUserData: ref<string | null>(null),
    postCellPurchaseRequest: ref<string | null>(null),
  };

  const userData = ref<UserData>({
    userInfo: {
      id: "",
      name: "",
      email: "",
    },
    statistics: {
      accountBalance: 0,
      cellsOwned: 0,
      projectsOwned: 0,
      totalInvested: 0,
      totalEarnings: 0,
      totalEnergyGenerated: 0,
      maximumPowerGeneration: 0,
    },
    performance: [],
    projects: [],
  });

  const fetchUserData = async () => {
    status.fetchUserData.value = "loading";
    errorMsg.fetchUserData.value = null;
    try {
      const response = await fetch("http://127.0.0.1:8000/users/me/data", {
        method: "GET",
        headers: {
          accept: "application/json",
          Authorization: `Bearer ${useAuthStore().userToken}`,
        },
      });
      if (!response.ok) throw new Error("Failed to fetch user data");
      const data = await response.json();

      userData.value = data as UserData;

      status.fetchUserData.value = "success";
    } catch (err) {
      errorMsg.fetchUserData.value = (err as Error).message;
      status.fetchUserData.value = "error";
    }
  };

  async function postCellPurchaseRequest() {
    fetch("https://your-backend-url.com/api/endpoint", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(selectedCellIds.value),
    })
      .then((response) => {
        if (response.status === 401) {
          throw new Error("Unauthorized");
        } else if (!response.ok) {
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
    selectedCellIds,
    postCellPurchaseRequest,
    fetchUserData,
    userData,
  };
});
