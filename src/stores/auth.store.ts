import { defineStore } from "pinia";
import { ref } from "vue";

export const useAuthStore = defineStore("auth", () => {
  const status = {
    createUser: ref<"idle" | "loading" | "success" | "error">("idle"),
    userLogin: ref<"idle" | "loading" | "success" | "error">("idle"),
    userLogout: ref<"idle" | "loading" | "success" | "error">("idle"),
  };

  const errorMsg = {
    createUser: ref<string | null>(null),
    userLogin: ref<string | null>(null),
    userLogout: ref<string | null>(null),
  };

  const isAuthenticated = ref<boolean>(false);
  const userToken = ref<string | null>(null);

  async function createUser(username: string, password: string) {
    status.createUser.value = "loading";
    errorMsg.createUser.value = null;
    await fetch("/api/users", {
      method: "POST",
      headers: {
        accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, password }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then(() => {
        status.createUser.value = "success";
      })
      .catch((error) => {
        status.createUser.value = "error";
        errorMsg.createUser.value = error.message;
      });
  }

  async function userLogin(username: string, password: string) {
    status.userLogin.value = "loading";
    errorMsg.userLogin.value = null;
    await fetch("/api/token", {
      method: "POST",
      headers: {
        accept: "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({
        grant_type: "password",
        username: username,
        password: password,
      }),
    })
      .then((response) => {
        if (response.status === 401) {
          throw new Error("Unauthorized");
        } else if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        userToken.value = data.access_token;
        isAuthenticated.value = true;
        status.userLogin.value = "success";
      })
      .catch((error) => {
        isAuthenticated.value = false;
        status.userLogin.value = "error";
        userToken.value = null;
        errorMsg.userLogin.value = error.message;
      });
  }

  async function userLogout() {
    status.userLogout.value = "loading";
    errorMsg.userLogout.value = null;
    try {
      // const response = await fetch("/api/logout");
      // if (!response.ok) throw new Error("Failed to logout");

      // const data = await response.json();
      userToken.value = null;
      isAuthenticated.value = false;
      status.userLogout.value = "success";
    } catch (err) {
      errorMsg.userLogout.value = (err as Error).message;
      status.userLogout.value = "error";
    }
  }

  return {
    status,
    errorMsg,
    isAuthenticated,
    userLogin,
    userLogout,
    createUser,
    userToken,
  };
});
