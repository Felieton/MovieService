<template>
  <div>
    <v-container class="mt-16 mb-16">
      <v-row justify="center">
        <v-col md="8">
          <div>
            <v-row v-if="video" class="mt-5" justify="center">
              <v-col class="justify-center d-flex align-center">
                <v-icon class="mr-4" color="red" large>fas fa-pen</v-icon>
                <h1 class="mb-4 mt-4">{{ video[naming] + "'s reviews" }}</h1>
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
                <v-card v-for="item in reviews" :key="item.id" class="mb-7">
                  <div class="d-flex justify-space-between">
                    <div class="justify-center">
                      <v-card-title class="pointer" @click="toUserProfile(item.user.id)">{{item.user.username}}</v-card-title>
                      <v-card-subtitle>{{item.created.split('T')[0]}}</v-card-subtitle>
                    </div>
                    <div class="d-flex justify-center align-center mr-4">
                      <v-icon color="yellow" large>fas fa-star</v-icon>
                      <div class="ml-2 xd">{{item.rating}}</div>
                    </div>
                  </div>
                  <v-card-text class="text--primary">{{item.body}}
                  </v-card-text>
                  <v-card-actions
                      v-if="$store.getters.loggedUserIsMod"
                      class="justify-end">
                    <v-tooltip
                        top
                        color="error"
                    >
                      <template
                          v-slot:activator="{ on, attrs }"
                      >
                        <v-btn
                            icon
                            color="accent"
                            v-bind="attrs"
                            v-on="on"
                            @click="deleteReview(item)"
                        >
                          <v-icon>fas fa-trash-alt</v-icon>
                        </v-btn>
                      </template>
                      <span>Delete</span>
                    </v-tooltip>
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
      <v-snackbar bottem v-model="snackbar" :timeout="2000">
        {{ snackbarText }}
        <template v-slot:action="{ attrs }">
          <v-btn color="blue" text v-bind="attrs" @click="snackbar = false">
            Close
          </v-btn>
        </template>
      </v-snackbar>
      <router-view></router-view>
    </v-container>
  </div>
</template>

<script>

export default {
  name: "ReviewsList",
  props: ['type', 'naming'],
  data: () => ({
    video: {},
    reviews: [],
    page: 1,
    pages: 0,
    count: 0,
    snackbar: false,
    snackbarText: "You must have an account to see others' profiles",
    isAbleToDelete: false,
    lastUpdateParam: '-created'
  }),
  created() {
    if (this.$store.getters.loggedUserIsMod) {
      this.isAbleToDelete = true
    }

    this.$store.dispatch('api/' + this.type + '/loadOne', this.getId()).then((res) => {
      this.video = res.data
    })

    this.$store.dispatch('api/review/loadMany', {[this.type]: this.getId(),
      isAccepted: "True", sortBy: '-created'}).then((res) => {
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
      this.$store.dispatch('api/' + this.type + '/loadMany', {[this.type]: this.getId(),
          isAccepted: "True", sortBy: '-created', page: page}).then((res) => {
        this.items = res.data.results
      })
    },
    updateList(param) {
      this.$store.dispatch('api/review/loadMany', {[this.type]: this.getId(),
        isAccepted: "True", sortBy: param}).then((res) => {
        this.reviews = res.data.results
      })
      this.page = 1
      this.lastUpdateParam = param
    },
    async deleteReview(review) {
      await this.$store.dispatch("api/review/remove", review.id)
      this.updateList(this.lastUpdateParam)
    },
    toUserProfile(id) {
      if (this.$store.getters.isAuthenticated) {
        this.$router.push({ path: '/user/' + id });
      }
      else
        this.snackbar = true
    },
    getId() {
      if (this.type === 'title') {
        return this.$route.params.id
      }
      else
        return this.$route.params.epid
    },
  }
}
</script>

<style scoped>
.pointer {
  cursor: pointer;
}
</style>