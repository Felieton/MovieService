<template>
  <v-app class="movie-service">
    <router-view/>
  </v-app>
</template>

<script>

export default {
  name: 'App',

  data: () => ({
    //
  }),
};
</script>

<style lang="scss">
.movie-service.v-application.theme--dark .primary--text {
  color: var(--v-primary-text-base) !important;
  caret-color: var(--v-primary-text-base) !important;
}
</style>

<style lang="scss">
.v-application a {
  text-decoration: none;

  &:hover.link-hover {
    color: var(--v-accent-lighten1)
  }
}

::-webkit-scrollbar {
  width: 8px;
  height: 8px;
  background-color: #1f1f1f;
  transition: 0.9s;
}

::-webkit-scrollbar-thumb {
  background-color: #808080;
  width: 5px;
  border: 0;
  transition: 0.7s;
}

html {
  overflow-y: auto;
}
</style>
