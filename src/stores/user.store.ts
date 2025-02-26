import { defineStore } from "pinia";
import { ref } from "vue";
import { type UserData } from "./user.types";
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
      username: "",
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
      const response = await fetch(`${window.location.origin}/api/users/me/data`, {
        method: "GET",
        headers: {
          accept: "application/json",
          Authorization: `Bearer ${useAuthStore().userToken}`,
        },
      });
      if (!response.ok) throw new Error("Failed to fetch user data");
      const data = await response.json();

      userData.value = data as UserData;

      console.log(userData.value);

      status.fetchUserData.value = "success";
    } catch (err) {
      errorMsg.fetchUserData.value = (err as Error).message;
      status.fetchUserData.value = "error";
    }
  };

  async function postCellPurchaseRequest() {
    fetch("not implemented", {
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

  type CellSelection = {
    cellId: string;
    arrayId: string;
    projectId: string;
  };
  const selectedCellIds = ref<Array<CellSelection>>([]);
  function toggleCellSelection(cellId: string, arrayId: string, projectId: string) {
    const cellIndex = selectedCellIds.value.findIndex((cell) => cell.cellId === cellId);
    if (cellIndex === -1) {
      selectedCellIds.value.push({ cellId, arrayId, projectId });
    } else {
      selectedCellIds.value.splice(cellIndex, 1);
    }
  }

  return {
    status,
    errorMsg,
    selectedCellIds,
    postCellPurchaseRequest,
    fetchUserData,
    userData,
    toggleCellSelection,
  };
});
