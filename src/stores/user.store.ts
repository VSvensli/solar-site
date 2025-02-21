import { defineStore } from "pinia";
import { ref } from "vue";
import { type UserFunds, type UserProject } from "./user.types";

const mockUserFunds: UserFunds = {
  accountBalance: 1000,
};

const mockUserProjects: Array<UserProject> = [
  {
    projectId: "1",
    cellIds: ["1", "2"],
    percentageOwned: 0.023,
  },
  {
    projectId: "2",
    cellIds: ["1", "2"],
    percentageOwned: 0.5,
  },
  {
    projectId: "3",
    cellIds: ["1", "2"],
    percentageOwned: 0.01,
  },
];

export const useUserStore = defineStore("user", () => {
  const status = ref<"idle" | "loading" | "success" | "error">("idle");
  const errorMsg = ref<string | null>(null);
  const userProjects = ref<Array<UserProject>>([]);

  const currentUserId = ref<string | null>(null);

  const fetchUserProjects = async () => {
    status.value = "loading";
    errorMsg.value = null;
    try {
      // const response = await fetch(`/api/users/${userId}/projects`);
      // if (!response.ok) throw new Error("Failed to fetch user projects");

      // const data: UserProjects = await response.json();
      userProjects.value = mockUserProjects;
      status.value = "success";
    } catch (err) {
      errorMsg.value = (err as Error).message;
      status.value = "error";
    }
  };

  const userFunds = ref<UserFunds>({ accountBalance: 0 });

  const fetchUserFunds = async () => {
    status.value = "loading";
    errorMsg.value = null;
    try {
      // const response = await fetch(`/api/users/${userId}/funds`);
      // if (!response.ok) throw new Error("Failed to fetch user funds");

      // const data: UserFunds = await response.json();
      userFunds.value = mockUserFunds;
      status.value = "success";
    } catch (err) {
      errorMsg.value = (err as Error).message;
      status.value = "error";
    }
  };
  return {
    status,
    errorMsg,
    fetchUserProjects,
    fetchUserFunds,
    currentUserId,
    userFunds,
    userProjects,
  };
});
