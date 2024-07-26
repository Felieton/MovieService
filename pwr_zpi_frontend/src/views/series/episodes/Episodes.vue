<template>
  <div>
    <v-container class="mt-16 mb-16">
      <v-row justify="center">
        <v-col md="8">
          <div>
            <v-row v-if="title" class="mt-5" justify="center">
              <v-col class="justify-center d-flex align-center">
                <v-icon class="mr-4" color="red" large>fas fa-list-ul</v-icon>
                <h1 class="mb-4 mt-4">{{ title.title + "'s episodes" }}</h1>
              </v-col>
            </v-row>
            <v-row class="mt-5" justify="center">
              <v-col class="d-flex" cols="12" sm="3">
                <v-select v-model="chosenSeason" :items="seasons" label="Season" solo></v-select>
              </v-col>
              <v-col class="d-flex" cols="12" sm="1">
                <v-btn @click="changeDisplayedList" class="mt-1" icon>
                  <i class="fas fa-search"></i>
                </v-btn>
                <v-btn class="mt-1 no-text-transform" text @click="cleanFilters" icon>
                  <i class="fas fa-broom"></i>
                </v-btn>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-card v-for="item in episodes" :key="item.id" :to="{ name: 'episode_single', params:
                 { epid: item.id } }" class="elevation-12 ml-4 mr-4 mb-7">
                  <v-row>
                    <v-col cols="10">
                      <v-card-title>{{ "S" + item.season + ", Ep" + item.number + " - " + item.name}}</v-card-title>
                      <v-card-subtitle>{{ item.released }}</v-card-subtitle>
                      <v-card-text>{{ item.plot }}</v-card-text>
                    </v-col>
                    <v-col cols="2" class="justify-center d-flex align-center">
                      <v-icon color="yellow" large>fas fa-star</v-icon>
                      <h1 class="ml-2">{{ item.rating }} </h1>
                    </v-col>
                  </v-row>
                </v-card>
                <div class="text-center">
                  <v-pagination v-model="page" :length="getPages" @input="next"></v-pagination>
                </div>
              </v-col>
            </v-row>
          </div>
        </v-col>
      </v-row>
      <router-view></router-view>
    </v-container>
    <router-view></router-view>
  </div>
</template>

<script>
// const seasonsNumber = 30

export default {
  name: "Episodes",
  data: () => ({
    defaultParameters: {},
    parameters: {},
    episodes: [],
    page: 1,
    pages: 0,
    seasons: [],
    chosenSeason: null,
    title: null
  }),
  created() {
    let id = this.$route.params.id
    this.$store.dispatch('api/title/loadOne', id).then((res) => {
      this.title = res.data
      this.generateSeasons()
    })
    this.defaultParameters = {title: id, sortBy: "id"}
    this.parameters = {title: id, sortBy: "id"}
    this.$store.dispatch('api/episode/loadMany', this.parameters).then((res) => {
      this.updateList(res)
    })
  },
  computed: {
    getPages: function () {
      return this.pages
    }
  },
  methods: {
    generateSeasons() {
      let seasonsCount = this.title.seasons_count
      for (let i = 1; i <= seasonsCount; i++) {
        this.seasons.push(i)
      }
    },
    getNumberOfPages() {
      let counter = Math.floor(this.count / 10);
      if (this.count % 10 !== 0) {
        counter ++
      }
      return counter
    },
    next(page) {
      this.parameters.page = page
      this.$store.dispatch('api/episode/loadMany', this.parameters).then((res) => {
        this.episodes = res.data.results
      })
    },
    changeDisplayedList() {
      this.parameters = JSON.parse(JSON.stringify(this.defaultParameters))
      this.parameters.season = this.chosenSeason
      this.$store.dispatch('api/episode/loadMany', this.parameters).then((res) => {
        this.updateList(res)
      })
    },
    updateList(res) {
      this.episodes = res.data.results
      this.count = res.data.count
      this.pages = this.getNumberOfPages()
      this.page = 1
    },
    cleanFilters() {
      this.chosenSeason = null
      this.parameters = this.defaultParameters
      this.parameters = JSON.parse(JSON.stringify(this.defaultParameters))
      this.$store.dispatch('api/episode/loadMany', this.defaultParameters).then((res) => {
        this.updateList(res)
      })
    }
  }
}
</script>

<style scoped>
.no-text-transform {
  text-transform: none;
}
</style>