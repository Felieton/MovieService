<template>
  <div>
    <v-container class="mt-16 mb-16">
      <v-row justify="center">
        <v-col md="8">
          <div>
            <v-row class="mt-5" justify="center">
              <v-col class="justify-center d-flex align-center">
                <v-icon class="mr-4" color="red" large>fas fa-list-ul</v-icon>
                <h1 class="mb-4 mt-4 pointer">{{ header }}</h1>
              </v-col>
            </v-row>
            <v-row class="mt-5" justify="center">
              <v-col class="d-flex" cols="12" sm="3">
                <v-select v-model="chosenGenre" :items="genres" item-text="name" item-value="id"
                          label="Genre" solo></v-select>
              </v-col>
              <v-col class="d-flex" cols="12" sm="3">
                <v-select v-model="chosenCountry" :items="countries" item-text="name" item-value="id"
                          label="Country" solo></v-select>
              </v-col>
              <v-col class="d-flex" cols="12" sm="3">
                <v-select v-model="chosenYear" :items="years" label="Year" solo></v-select>
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
                <v-card v-for="(item, index) in items" :key="item.id" :to="{ name: getRouteName, params:
                 { id: item.id } }" class="elevation-12 ml-4 mr-4 mb-7">
                  <v-row>
                    <v-col cols="1" class="justify-center d-flex align-center">
                      <h1>{{index + 1 + (page - 1) * 10}}</h1>
                    </v-col>
                    <v-col cols="2">
                      <v-img class="round-image" v-if="item.poster !== null" :src="item.poster"
                             height="150" max-width="100"></v-img>
                      <v-img class="round-image" v-else src="@/assets/no-image.jpg" height="150" width="100"></v-img>
                    </v-col>
                    <v-col cols="7">
                      <v-card-title>{{ item.title }}</v-card-title>
                      <v-card-subtitle>{{ item.year }}</v-card-subtitle>
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
  </div>
</template>

<script>
const genresNumber = 30
const countriesNumber = 30
const yearsNumber = 30

export default {
  name: "TitlesList",
  props: ['type', 'header'],
  data: () => ({
    defaultParameters: {},
    parameters: {},
    items: [],
    page: 1,
    pages: 0,
    genres: [],
    countries: [],
    years: [],
    count: 0,
    chosenGenre: null,
    chosenCountry: null,
    chosenYear: null,
  }),
  created() {
    this.defaultParameters = {type: this.type, sortBy: "-rating"}
    this.parameters = {type: this.type, sortBy: "-rating"}
    this.$store.dispatch('api/title/loadMany', this.parameters).then((res) => {
      this.updateList(res)
    })
    this.$store.dispatch('api/genre/loadMany', {perPage: genresNumber}).then((res) => {
      this.genres = res.data.results
    })
    this.$store.dispatch('api/country/loadMany', {perPage: countriesNumber}).then((res) => {
      this.countries = res.data.results
    })
    this.generateYears()
  },
  computed: {
    getRouteName: function() {
      if (this.type === "M") {
        return 'movies_single'
      }
      else
        return 'series_single'
    },
    getPages: function () {
      return this.pages
    }
  },
  methods: {
    getNumberOfPages() {
      let counter = Math.floor(this.count / 10);
      if (this.count % 10 !== 0) {
        counter ++
      }
      return counter
    },
    next(page) {
      this.parameters.page = page
      this.$store.dispatch('api/title/loadMany', this.parameters).then((res) => {
        this.items = res.data.results
      })
    },
    changeDisplayedList() {
      this.parameters = JSON.parse(JSON.stringify(this.defaultParameters))
      this.parameters.genres = this.chosenGenre
      this.parameters.countries = this.chosenCountry
      this.parameters.year = this.chosenYear
      this.$store.dispatch('api/title/loadMany', this.parameters).then((res) => {
        this.updateList(res)
      })
    },
    generateYears() {
      let currentYear = new Date().getFullYear()
      for (let year = currentYear; year > (currentYear - yearsNumber); year--) {
        this.years.push(year)
      }
    },
    updateList(res) {
      this.items = res.data.results
      this.count = res.data.count
      this.pages = this.getNumberOfPages()
      this.page = 1
    },
    cleanFilters() {
      this.chosenGenre = null
      this.chosenCountry = null
      this.chosenYear = null
      this.parameters = JSON.parse(JSON.stringify(this.defaultParameters))
      this.$store.dispatch('api/title/loadMany', this.defaultParameters).then((res) => {
        this.updateList(res)
      })
    }
  }
}
</script>

<style scoped>
.round-image {
  border-radius: 10%
}

.no-text-transform {
  text-transform: none;
}
</style>