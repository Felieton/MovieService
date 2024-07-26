<template>
  <div>
    <v-container fluid class="primary">
      <v-row class="pt-6 justify-center">
        <span class="text-h6">Moderator queue</span>
      </v-row>
      <v-row class="py-4">
        <v-divider/>
      </v-row>
      <v-row>
        <v-tabs
            centered
            background-color="primary"
        >
          <v-tab
              v-for="(tab, ind) in tabs"
              :key="ind"
              :to="tab.to"
          >
            {{ tab.title }}
          </v-tab>
        </v-tabs>
      </v-row>
    </v-container>

    <v-container>
      <router-view/>
    </v-container>
  </div>
</template>

<script>
export default {
  name: "BaseMod",
  data () {
    return {
      tabs: [
        { title: 'Reviews', to: { name: 'mod_queue_reviews' } },
        { title: 'Title requests', to: { name: 'mod_queue_title' } },
        { title: 'Episode requests', to: { name: 'mod_queue_episode' } },
        { title: 'Person requests', to: { name: 'mod_queue_person' } },
      ]
    }
  },
}
</script>

<style scoped lang="scss">

/* tabs bar text color */
.v-tabs-bar.primary {
  .v-tab {
    color: var(--v-primary-text-base);
  }
}
.v-tabs::v-deep > .v-tabs-bar.primary .v-tabs-slider {
  color: var(--v-primary-text-base);
}
</style>