<script setup lang="ts">
import { useProjectStore } from "../stores/project.store";
import ProjectCard from "../components/ProjectCard.vue";

const projectStore = useProjectStore();
</script>

<template>
  <div>
    <h1 class="font-bold">Home Page</h1>
    <p>Here you can see all projects</p>
    <div class="space-y-2 border-2 border-gray-300 rounded-lg p-3">
      <ProjectCard
        v-for="project in projectStore.projects"
        :key="project.projectId"
        :project="project"
        class="[&:not(:last-child)]:border-b-2 p-4 border-gray-300"
      ></ProjectCard>
      <div v-if="projectStore.projects.length === 0 && projectStore.status.fetchProjects != 'loading'">
        <p>No projects</p>
      </div>
      <div v-if="projectStore.status.fetchProjects === 'loading'" class="loading">
        <p>Loading...</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
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
