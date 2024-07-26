<template>
  <div>
    <v-container class="mt-16 mb-16">
      <v-row justify="center">
        <v-col md="8">
          <div>
            <v-row v-if="reviewer" class="mt-5" justify="center">
              <v-col class="justify-center d-flex align-center">
                <v-icon class="mr-4" color="red" large>fas fa-pen</v-icon>
                <h1 class="mb-4 mt-4 pointer" @click="toUserProfile(reviewer.id)">
                  {{ reviewer.username + "'s " + type + " reviews" }}</h1>
              </v-col>
            </v-row>
            <v-row class="mt-5 mt-2 mb-10" justify="center">
              <v-btn-toggle mandatory tile group>
                <v-btn @click="updateList('-created')" value="left">Newest</v-btn>
                <v-btn @click="updateList('created')" value="center">Oldest</v-btn>
                <v-btn @click="updateList('-rating')" value="right">Rating down</v-btn>
                <v-btn @click="updateList('rating')" value="justify">Rating up</v-btn>
              </v-btn-toggle>
            </v-row>
            <v-row>
              <v-col>
                <div v-if="type === 'title'">
                  <v-card v-for="item in reviews" :key="item.id" class="mb-7">
                    <v-row>
                      <v-col cols="2" class="ml-10">
                        <v-img class="round-image" v-if="item.title.poster !== null" :src="item.title.poster"
                               height="200" max-width="133"></v-img>
                        <v-img class="round-image" v-else src="@/assets/no-image.jpg" height="200" width="133"></v-img>
                      </v-col>
                      <v-col cols="9" class="ml-10">
                        <div class="d-flex justify-space-between">
                          <div class="justify-center">
                            <v-card-title @click="toTitle(item.title)" class="pointer">{{item.title.title}}</v-card-title>
                            <v-card-subtitle>{{item.created.split('T')[0]}}</v-card-subtitle>
                          </div>
                          <div class="d-flex justify-center align-center mr-4">
                            <v-icon color="yellow" large>fas fa-star</v-icon>
                            <h3 class="ml-2 xd">{{item.rating}}</h3>
                          </div>
                        </div>
                        <v-card-text class="text--primary">{{item.body}}
                        </v-card-text>
                        <v-card-actions v-if="isOwner">
                          <v-btn @click="deleteReview(item.id)" class="d-flex justify-end" color="#ff5252" text>
                            <i class="fas fa-trash-alt mr-1"></i>
                            <div>delete</div>
                          </v-btn>
                        </v-card-actions>
                      </v-col>
                    </v-row>
                  </v-card>
                </div>
                <div v-else>
                  <v-card v-for="item in reviews" :key="item.id" class="elevation-12 ml-4 mr-4 mb-7">
                    <v-row>
                      <v-col cols="10">
                        <v-card-title class="pointer" @click="toEpisode(item.episode)">{{ "S" + item.episode.season +
                        ", Ep" + item.episode.number + " - " + item.episode.name}}</v-card-title>
                        <v-card-subtitle>{{item.created.split('T')[0]}}</v-card-subtitle>
                        <v-card-text>{{ item.body }}</v-card-text>
                      </v-col>
                      <v-col cols="2" class="justify-center d-flex align-center">
                        <v-icon color="yellow" large>fas fa-star</v-icon>
                        <h1 class="ml-2">{{ item.rating }} </h1>
                      </v-col>
                      <v-col>
                        <v-btn @click="deleteReview(item.id)" class="d-flex justify-end" color="#ff5252" text>
                          <i class="fas fa-trash-alt mr-1"></i>
                          <div>delete</div>
                        </v-btn>
                      </v-col>
                    </v-row>
                  </v-card>
                </div>
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
  name: "ReviewsListUser",
  props: ['type', 'naming'],
  data: () => ({
    userid: 0,
    reviewer: {},
    reviews: [],
    page: 1,
    pages: 0,
    count: 0,
    isOwner: false
  }),
  created() {
    this.userid = this.$route.params.id
    if (this.userid.toString() === this.$store.getters.loggedUser.id.toString()) {
      this.isOwner = true
    }
    this.$store.dispatch('api/user/loadOne', this.userid).then((res) => {
      this.reviewer = res.data
    })
    this.$store.dispatch('api/review/loadMany', {user: this.userid, sortBy: "-rating", isAccepted: "True",
      titleIsNull: this.getType()}).then((res) => {
      this.count = res.data.count
      this.pages = this.getNumberOfPages()
      this.reviews = res.data.results
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
      this.$store.dispatch('api/review/loadMany', {user: this.userid, sortBy: "-rating",
        isAccepted: "True", titleIsNull: this.getType(), page: page}).then((res) => {
        this.reviews = res.data.results
      })
    },
    updateList(param) {
      this.$store.dispatch('api/review/loadMany', {user: this.userid, isAccepted: "True",
        titleIsNull: this.getType(), sortBy: param}).then((res) => {
        this.reviews = res.data.results
      })
      this.page = 1
    },
    toUserProfile(id) {
      if (this.$store.getters.isAuthenticated) {
        this.$router.push({ path: '/user/' + id });
      }
    },
    getId() {
      if (this.type === 'title') {
        return this.$route.params.id
      }
      else
        return this.$route.params.epid
    },
    getType() {
      if (this.type === 'title') {
        return ""
      }
      else
        return "True"
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
    deleteReview(reviewId) {
      this.reviews.splice(this.reviews.length - 1)
      this.$store.dispatch('api/review/remove', reviewId).then(() => {
        if (!this.reviews.length) {
          this.page = this.page -1
        }
        this.$store.dispatch('api/review/loadMany', {user: this.userid, sortBy: "-rating",
          isAccepted: "True", titleIsNull: this.getType(), page: this.page}).then((res) => {
          this.count = res.data.count
          this.reviews = res.data.results
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