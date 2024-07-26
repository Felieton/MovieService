<template>
  <v-container class="mt-16">
    <v-row justify="center">
      <v-col md="8">
        <v-row class="mt-5" justify="center">
          <v-col class="justify-center d-flex align-center">
            <v-icon class="mr-4" color="red" large>fas fa-pen</v-icon>
            <h1 class="mb-4 mt-4">{{ "Add new..." }}</h1>
          </v-col>
        </v-row>
        <v-row class="mt-16" justify="center">
          <v-col class="justify-center d-flex align-center flex-column">
            <i @click="toTitle" class="pointer color-red fas fa-film fa-10x"></i>
            <div>Movie/Series</div>
          </v-col>
          <v-col class="justify-center d-flex align-center flex-column">
            <i @click="toEpisode" class="pointer color-red fas fa-ticket-alt fa-10x"></i>
            <div>Episode</div>
          </v-col>
          <v-col class="justify-center d-flex align-center flex-column">
            <i @click="toPerson" class="pointer color-red fas fa-user-alt fa-10x"></i>
            <div class="mt-4">Person</div>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "Add",
  methods: {
    toTitle(){
      this.$router.push('/add/title/');
    },
    toEpisode(){
      this.$router.push('/add/episode/');
    },
    toPerson(){
      this.$router.push('/add/person/');
    }
  }
}
</script>

<style scoped>
.color-red {
  color: #F44336
}

.pointer {
  cursor: pointer;
}
</style>