import router from "./router";
import { createPinia } from "pinia";
import { createApp } from "vue";
import PrimeVue from "primeVue/config";
import ToastService from "primevue/toastservice";
import "./assets/tailwind.css";
import "./style.css";
import App from "./App.vue";

const app = createApp(App);
app.use(createPinia());
app.use(router);
app.use(ToastService);
app.use(PrimeVue, {
  theme: "none",
});
app.mount("#app");
