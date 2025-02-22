import { defineStore } from "pinia";
import { ref } from "vue";
import { useUserStore } from "./user.store";

const mockId = "123";

export const useAuthStore = defineStore("auth", () => {
  const userStore = useUserStore();
  const status = ref<"idle" | "loading" | "success" | "error">("idle");
  const errorMsg = ref<string | null>(null);
  const isAuthenticated = ref<boolean>(false);

  const login = async (email: string, password: string) => {
    status.value = "loading";
    errorMsg.value = null;
    try {
      // const response = await fetch("/api/login");
      // if (!response.ok) throw new Error("Failed to login");

      // const data = await response.json();
      userStore.currentUserId = mockId;
      isAuthenticated.value = true;
      status.value = "success";
    } catch (err) {
      errorMsg.value = (err as Error).message;
      status.value = "error";
    }
  };

  const logout = async () => {
    status.value = "loading";
    errorMsg.value = null;
    try {
      // const response = await fetch("/api/logout");
      // if (!response.ok) throw new Error("Failed to logout");

      // const data = await response.json();
      userStore.currentUserId = null;
      isAuthenticated.value = false;
      status.value = "success";
    } catch (err) {
      errorMsg.value = (err as Error).message;
      status.value = "error";
    }
  };

  return {
    status,
    errorMsg,
    isAuthenticated,
    login,
    logout,
  };
});
