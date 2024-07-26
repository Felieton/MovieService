<template>
  <v-container class="mt-16">
    <v-row justify="center">
      <v-col md="8">
        <v-card v-if="user.id" class="mb-16">
          <v-row justify="center">
            <div class="mt-6 medium-font">
              <v-img class="image" v-if="user.photo !== null" :src="user.photo"></v-img>
              <i v-else class="fas fa-user-circle fa-10x"></i>
            </div>
          </v-row>
          <v-row v-if="user" class="mt-5" justify="center">
            <h2>{{user.username}}</h2>
            <v-icon v-if="isOwner" @click="toSettings" class="ml-4">fas fa-cog</v-icon>
          </v-row>
          <v-row class="mt-5 mb-5" justify="center">
            <div><strong>Joined:&nbsp;&nbsp;</strong> {{joinDate}}</div>
          </v-row>
          <div v-if="user.settings">
            <v-row v-if="user.settings.email_visible" class="mt-5" justify="center">
              <div>{{user.email}}</div>
            </v-row>
          </div>
          <v-row class="mt-5 mb-12" justify="center">
            <v-col cols="8">
              <div class="aligned">{{user.description}}</div>
            </v-col>
          </v-row>
          <v-row v-if="user" class="mt-16" justify="center">
            <v-col class="justify-center d-flex align-center">
              <v-icon class="mr-4" color="red" large>fas fa-heart</v-icon>
              <h1 class="medium-font">Top Picks</h1>
            </v-col>
          </v-row>
          <div class="mb-16" v-if="topReviews.length > 0">
            <v-row justify="center">
              <v-col>
                <v-sheet color="#1f1f1f" class="mx-auto pt-4 mt-10 mb-10" elevation="8" max-width="1000">
                  <v-slide-group class="pa-2" active-class="success" show-arrows>
                    <v-slide-item v-for="review in topReviews" :key="review.id" >
                      <v-card :to="{ name: getRouteName(review.title), params:{ id: review.title.id } }" max-width="500" class="ma-3">
                        <v-img v-if="review.title.poster !== null" :src="review.title.poster" height="300" width="210"></v-img>
                        <v-img v-else src="@/assets/no-image.jpg" alt="" height="300" width="210"></v-img>
                        <div class="d-flex justify-center">
                          <v-card-title class="justify-center">{{review.rating}}</v-card-title>
                          <v-icon small color="yellow" large>fas fa-star</v-icon>
                        </div>
                      </v-card>
                    </v-slide-item>
                  </v-slide-group>
                </v-sheet>
              </v-col>
            </v-row>
            <v-row v-if="id">
              <v-col>
                <div class="d-flex justify-center">
                  <v-btn class="mr-2" :to="{ name: 'user_reviews' }">see all title reviews</v-btn>
                  <v-btn class="ml-2" :to="{ name: 'user_episode_reviews' }">check out episode reviews</v-btn>
                </div>
              </v-col>
            </v-row>
          </div>
          <div v-else>
            <v-row>
              <v-col>
                <div class="d-flex justify-center">
                  <h2 class="mt-8 mb-16">This user hasn't reviewed anything just yet</h2>
                </div>
              </v-col>
            </v-row>
          </div>
          <div v-if="user.settings">
            <div v-if="user.settings.watchlist_visible">
              <v-row v-if="user" justify="center">
                <v-col class="justify-center d-flex align-center">
                  <v-icon class="mr-4" color="red" large>fas fa-list-ul</v-icon>
                  <h1 class="medium-font">Watchlist</h1>
                </v-col>
              </v-row>
              <template v-if="this.user.watchlist.length > 0">
                <v-row justify="center">
                  <v-col>
                    <v-sheet color="#1f1f1f" class="mx-auto pt-4 mt-10 mb-10" elevation="8" max-width="1000">
                      <v-slide-group class="pa-2" active-class="success" show-arrows>
                        <v-slide-item v-for="item in watchlist" :key="item.id" >
                          <v-card :to="{ name: getRouteName(item), params:{ id: item.id } }" max-width="500" class="ma-3">
                            <v-img v-if="item.poster !== null" :src="item.poster" height="300" width="210"></v-img>
                            <v-img v-else src="@/assets/no-image.jpg" alt="" height="300" width="210"></v-img>
                          </v-card>
                        </v-slide-item>
                      </v-slide-group>
                    </v-sheet>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col>
                    <div class="d-flex justify-center">
                      <v-btn class="mb-6" :to="{ name: 'user_watchlist' }">whole watchlist</v-btn>
                    </div>
                  </v-col>
                </v-row>
              </template>
              <div v-else>
                <v-row>
                  <v-col>
                    <div class="d-flex justify-center">
                      <h2 class="mt-8 mb-10">This user's watchlist is empty</h2>
                    </div>
                  </v-col>
                </v-row>
              </div>
            </div>
          </div>
        </v-card>
      </v-col>
    </v-row>
    <router-view></router-view>
  </v-container>
</template>

<script>
export default {
  name: "User",
  data: () => ({
    joinDate: {},
    user: {},
    topReviews: [],
    id: 0,
    watchlist: [],
    isOwner: false
  }),
  created() {
    this.id = this.$route.params.id
    if (this.id.toString() === this.$store.getters.loggedUser.id.toString()) {
      this.isOwner = true
    }
    this.$store.dispatch('api/user/loadOne', this.id).then((res) => {
      this.user = res.data
      this.joinDate = res.data.date_joined.split('T')[0]
      if (this.user.settings.watchlist_visible && this.user.watchlist.length > 0) {
        this.$store.dispatch('api/title/loadMany', {ids: this.user.watchlist.toString(), perPage: 5})
            .then((res) => {
          this.watchlist = res.data.results
        })
      }
    })

    this.$store.dispatch('api/review/loadMany', {user: this.id, sortBy: "-rating", perPage: 5,
      isAccepted: "True", titleIsNull: ""}).then((res) => {
      this.topReviews = res.data.results
    }, (err) => {
        console.log(err)
    })

  },
  methods: {
    getRouteName: function(title) {
      if (title.type === "M") {
        return 'movies_single'
      }
      else
        return 'series_single'
    },
    toSettings() {
      this.$router.push({ path: '/user/' + this.id + '/settings/'});
    },
  }
}
</script>

<style scoped>
.image {
  object-fit: cover;
  width:300px;
  height:300px;
  border-radius: 50%;
}

.medium-font {
  font-size: 30px;
}

.aligned {
  text-align: center;
}
</style>