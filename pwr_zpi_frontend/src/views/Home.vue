<template>
  <div>
    <div>
      <template>
        <v-sheet class="mx-auto pt-4 mt-12" elevation="8" max-width="1100">
          <h1 class="big-text">NEWLY RELEASED MOVIES</h1>
          <v-slide-group class="pa-2" active-class="success" show-arrows>
            <v-slide-item v-for="item in this.movies" :key="item.id" >
              <v-card :to="{ name: 'movies_single', params:{ id: item.id } }" max-width="180" class="ma-3">
                <v-img v-if="item.poster !== null" :src="item.poster" height="250"></v-img>
                <v-img v-else src="@/assets/no-image.jpg" alt="" height="250" width="180"></v-img>
                <v-card-title class="justify-center smaller-font">{{item.title}}</v-card-title>
              </v-card>
            </v-slide-item>
          </v-slide-group>
        </v-sheet>
      </template>
    </div>
    <div>
      <template>
        <v-sheet class="mx-auto pt-4 mt-12" elevation="8" max-width="1100">
          <h1 class="big-text">THE FRESHEST SERIES</h1>
          <v-slide-group class="pa-2" active-class="success" show-arrows>
            <v-slide-item v-for="item in this.series" :key="item.id" >
              <v-card :to="{ name: 'series_single', params:{ id: item.id } }" max-width="180" class="ma-3">
                <v-img v-if="item.poster !== null" :src="item.poster" height="250" width="180"></v-img>
                <v-img v-else src="@/assets/no-image.jpg" alt="" height="250" width="180"></v-img>
                <v-card-title class="justify-center">{{item.title}}</v-card-title>
              </v-card>
            </v-slide-item>
          </v-slide-group>
        </v-sheet>
      </template>
    </div>
    <div class="mb-16">
      <template>
        <v-sheet class="mx-auto pt-4 mt-12" elevation="8" max-width="1100">
          <h1 class="big-text">BORN THIS MONTH</h1>
          <v-slide-group class="pa-2" active-class="success" show-arrows>
            <v-slide-item v-for="item in this.people" :key="item.id" >
              <v-card :to="{ name: 'people_single', params:{ id: item.id } }" max-width="180" class="ma-3">
                <v-img v-if="item.photo !== null" :src="item.photo" height="250" width="180"></v-img>
                <v-img v-else src="@/assets/no-image.jpg" alt="" height="250" width="180"></v-img>
                <v-card-title class="justify-center">{{item.name + " " + item.surname}}</v-card-title>
              </v-card>
            </v-slide-item>
          </v-slide-group>
        </v-sheet>
      </template>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home',
  data: () => ({
    movies: [],
    series: [],
    people: []
  }),
  created() {
    this.$store.dispatch('api/title/loadMany', {type: "M", sortBy: "-released"}).then((res) => {
      this.movies = res.data.results
    })
    this.$store.dispatch('api/title/loadMany', {type: "S", sortBy: "-released"}).then((res) => {
      this.series = res.data.results
    })
    this.$store.dispatch('api/person/loadMany', {birthMonth: 12}).then((res) => {
      this.people = res.data.results
    })
  }
}
</script>

<style>
.big-text {
  text-align: center;
  font-size: 30px;
  font-family: Bahnschrift, sans-serif;
}

</style>
