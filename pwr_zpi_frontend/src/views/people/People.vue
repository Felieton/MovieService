<template>
  <div>
    <v-container class="mt-16 mb-16">
      <v-row justify="center">
        <v-col md="8">
          <div>
            <v-row class="mt-5" justify="center">
              <v-col class="justify-center d-flex align-center">
                <v-icon class="mr-4" color="red" large>fas fa-list-ul</v-icon>
                <h1 class="mb-4 mt-4 pointer">PEOPLE OF CINEMA</h1>
              </v-col>
            </v-row>
            <v-row class="mt-5" justify="center">
              <v-col class="d-flex" cols="12" sm="3">
                <v-select v-model="chosenCountry" :items="countries" item-text="name" item-value="id" label="Country" solo></v-select>
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
                <v-card v-for="(item, index) in people" :key="item.index" :to="{ name: 'people_single', params:
                 { id: item.id } }" class="elevation-12 ml-4 mr-4 mb-7">
                  <v-row>
                    <v-col cols="1" class="justify-center d-flex align-center">
                      <h1>{{index + 1 + (page - 1) * 10}}</h1>
                    </v-col>
                    <v-col cols="2">
                      <v-img class="round-image" v-if="item.photo !== null" :src="item.photo" height="150" width="100"></v-img>
                      <v-img class="round-image" v-else src="@/assets/no-image.jpg" height="150" width="100"></v-img>
                    </v-col>
                    <v-col cols="8">
                      <v-card-title>{{ item.name + " " + item.surname }}</v-card-title>
                      <v-card-subtitle>{{ item.birthdate }}</v-card-subtitle>
                      <v-card-text>{{ item.details }}</v-card-text>
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
const countriesNumber = 30
const yearBornFrom = 2010
const yearBornTo = 1900

export default {
  name: "People",
  data: () => ({
    defaultParameters: {sortBy: "-surname"},
    parameters: {sortBy: "-surname"},
    people: [],
    page: 1,
    pages: 0,
    countries: [],
    years: [],
    chosenCountry: null,
    chosenYear: null,
  }),
  created() {
    this.$store.dispatch('api/person/loadMany', this.parameters).then((res) => {
      this.updateList(res)
    })
    this.$store.dispatch('api/country/loadMany', {perPage: countriesNumber}).then((res) => {
      this.countries = res.data.results
    })
    this.generateYears()
  },
  computed: {
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
      this.$store.dispatch('api/person/loadMany', this.parameters).then((res) => {
        this.people = res.data.results
      })
    },
    changeDisplayedList() {
      this.parameters = JSON.parse(JSON.stringify(this.defaultParameters))
      this.parameters.country = this.chosenCountry
      this.parameters.birthYear = this.chosenYear
      this.$store.dispatch('api/person/loadMany', this.parameters).then((res) => {
        this.updateList(res)
      })
    },
    generateYears() {
      for (let year = yearBornFrom; year >= yearBornTo; year--) {
        this.years.push(year)
      }
    },
    updateList(res) {
      this.people = res.data.results
      this.count = res.data.count
      this.pages = this.getNumberOfPages()
      this.page = 1
    },
    cleanFilters() {
      this.chosenCountry = null
      this.chosenYear = null
      this.parameters = JSON.parse(JSON.stringify(this.defaultParameters))
      this.$store.dispatch('api/person/loadMany', this.defaultParameters).then((res) => {
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