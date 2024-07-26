<template>
  <div>
    <v-container class="mt-16 mb-16">
      <v-row justify="center">
        <v-col md="8">
          <div>
            <v-row v-if="user" class="mt-5" justify="center">
              <v-col class="justify-center d-flex align-center">
                <v-icon class="mr-4" color="red" large>fas fa-list-ul</v-icon>
                <h1 class="mb-4 mt-2 pointer" @click="toUserProfile(user.id)">
                  {{ user.username + "'s watchlist" }}</h1>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-card v-for="(item, index) in titles" :key="item.id" class="elevation-12 ml-4 mr-4 mb-7">
                  <v-row>
                    <v-col class="ml-4" cols="2">
                      <v-img class="round-image" v-if="item.poster !== null" :src="item.poster"
                             height="200" max-width="133"></v-img>
                      <v-img class="round-image" v-else src="@/assets/no-image.jpg" height="200" width="133"></v-img>
                    </v-col>
                    <v-col cols="7">
                      <v-card-title class="pointer" @click="toTitle(item)">{{ item.title }}</v-card-title>
                      <v-card-subtitle>{{ item.year }}</v-card-subtitle>
                      <v-card-text>{{ item.plot }}</v-card-text>
                    </v-col>
                    <v-col cols="2" class="justify-center d-flex align-center">
                      <v-icon color="yellow" large>fas fa-star</v-icon>
                      <h1 class="ml-2">{{ item.rating }} </h1>
                    </v-col>
                  </v-row>
                  <v-card-actions class="d-flex justify-end" v-if="isOwner">
                    <v-btn @click="deleteFromWatchlist(index)" class="d-flex justify-end" color="#ff5252" text>
                      <i class="fas fa-trash-alt mr-1"></i>
                      <div>delete</div>
                    </v-btn>
                  </v-card-actions>
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

export default {
  name: "UserWatchlist",
  data: () => ({
    userid: 0,
    user: {},
    page: 1,
    pages: 0,
    count: 0,
    isOwner: false,
    titles: []
  }),
  created() {
    this.userid = this.$route.params.id

    if (this.userid.toString() === this.$store.getters.loggedUser.id.toString()) {
      this.isOwner = true
    }

    this.$store.dispatch('api/user/loadOne', this.userid).then((res) => {
      this.user = res.data
      this.watchlist = res.data.watchlist
      this.$store.dispatch('api/title/loadMany', {ids: this.user.watchlist.toString()}).then((res) => {
            this.titles = res.data.results
            this.count = res.data.count
            this.pages = this.getNumberOfPages()
          })
    })

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
      this.$store.dispatch('api/title/loadMany', {ids: this.user.watchlist.toString(), page: page}).then((res) => {
        this.titles = res.data.results
      })
    },
    toUserProfile(id) {
      if (this.$store.getters.isAuthenticated) {
        this.$router.push({ path: '/user/' + id });
      }
    },
    getRouteName(title) {
      if (title.type === 'M') {
        return "movies_single"
      }
      else
        return "series_single"
    },
    toTitle(title) {
      if (title.type === "M") {
        this.$router.push({ path: '/movies/' + title.id });
      }
      else
        this.$router.push({ path: '/series/' + title.id });
    },
    toEpisode(episode) {
      this.$router.push({ path: '/series/' + episode.title + '/episodes/' + episode.id });
    },
    deleteFromWatchlist(titleIndex) {
      this.watchlist.splice(titleIndex, 1)
      this.titles.splice(this.titles.length - 1)
      this.$store.dispatch('api/user/update', {id: this.userid, watchlist: this.watchlist}).then(() => {
        if (!this.titles.length) {
          this.page = this.page -1
        }
        this.$store.dispatch('api/title/loadMany', {ids: this.watchlist.toString(), page: this.page}).then((res) => {
          this.count = res.data.count
          this.titles = res.data.results
          this.pages = this.getNumberOfPages()
        })
      })
    }
  }
}
</script>

<style scoped>
.pointer {
  cursor: pointer;
}

.round-image {
  border-radius: 10%
}
</style>