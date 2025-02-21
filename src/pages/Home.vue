<script setup lang="ts">
import { useProjectStore } from "../stores/projectStore";
import { onMounted } from "vue";
import ProjectCard from "../components/ProjectCard.vue";

const projectStore = useProjectStore();

onMounted(() => {
  projectStore.fetchProjects();
});
</script>

<template>
  <div>
    <h1 class="font-bold">Home Page</h1>
    <p>Here you can see all projects</p>
    <div class="space-y-2">
      <ProjectCard
        v-for="project in projectStore.projects"
        :key="project.id"
        :project="project"
      />
      <div
        v-if="
          projectStore.projects.length === 0 &&
          projectStore.status.fetchProjects != 'loading'
        "
        class="p-4"
      >
        <p>No projects</p>
      </div>
      <div
        v-if="projectStore.status.fetchProjects === 'loading'"
        class="loading"
      >
        <p>Loading...</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Add cracy loading animation*/
@keyframes loading {
  0% {
    background-color: #f3f3f3;
  }
  50% {
    background-color: #e0e0e0;
  }
  100% {
    background-color: #f3f3f3;
  }
}

.loading {
  animation: loading 1s infinite;
}
</style>
