<template>
  <div>
    <v-container fluid>
      <v-row class="pt-6 justify-center">
        <span class="text-h6">Requests</span>
      </v-row>
      <v-row class="py-4">
        <v-divider/>
      </v-row>
      <v-row>
        <v-tabs
            centered
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
  name: "Requests",
  data () {
    return {
      tabs: [
        { title: 'Title', to: { name: 'admin_history_requests_title' } },
        { title: 'Episode', to: { name: 'admin_history_requests_episode' } },
        { title: 'Person', to: { name: 'admin_history_requests_person' } },
      ]
    }
  },
}
</script>

<style scoped>

</style>