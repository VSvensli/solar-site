<script setup lang="ts">
import { useProjectStore } from "../stores/project.store";
import ProjectCard from "../components/ProjectCard.vue";

const projectStore = useProjectStore();
</script>

<template>
  <div>
    <div class="text-2xl/7 font-semibold transform translate-y-1/2 translate-x-1/8 bg-slate-50 text-gray-400 p-2 w-28">
      Projects
    </div>
    <div class="border-2 border-gray-300 rounded-lg p-3">
      <div class="space-y-2">
        <ProjectCard
          v-for="project in projectStore.projects"
          :key="project.projectId"
          :project="project"
          class="[&:not(:last-child)]:border-b-2 p-4 border-gray-300"
        ></ProjectCard>
        <div v-if="projectStore.projects.length === 0 && projectStore.status.fetchProjects != 'loading'">
          <p>No projects</p>
        </div>
      </div>
    </div>
  </div>
</template>
