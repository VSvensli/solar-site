import router from "./router";
import PrimeVue from "primeVue/config";
import { createPinia } from "pinia";
import { createApp } from "vue";
import "./assets/tailwind.css";
import "./style.css";
import App from "./App.vue";

const app = createApp(App);
app.use(createPinia());
app.use(router);
app.use(PrimeVue, {
  theme: "none",
});
app.mount("#app");
