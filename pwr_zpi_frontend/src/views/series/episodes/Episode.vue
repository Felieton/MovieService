<template>
  <div class="mt-16">
    <v-row v-if="episode.id" justify="center">
      <v-col md="8">
        <v-row class="reduced-margin">
          <v-col cols="12" sm="10">
            <div v-if="episode" class="big-font">{{"S" + episode.season + ", EP" + episode.number + " - " + episode.name}}</div>
          </v-col>
          <v-col sm="2">
            <div class="justify-center d-flex align-center">
              <v-icon color="yellow" large>fas fa-star</v-icon>
              <h1 class="ml-2 xd">{{rating}}</h1>
            </div>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" sm="4" class="mt-12">
            <h1 class="pointer" @click="toSeries">{{title.title}}</h1>
            <h3>{{episode.plot}}</h3>
            <p></p>
            <div><strong>duration:&nbsp;</strong> {{stringifyDuration}}</div>
            <strong>released:&nbsp;&nbsp;</strong> {{episode.released}}
            <div><strong>genres:&nbsp;&nbsp;</strong> {{genres.map(el => el.name).join(', ')}} </div>
            <div><strong>languages:&nbsp;&nbsp;</strong> {{languages.map(el => el.name).join(', ')}} </div>
            <div><strong>countries:&nbsp;&nbsp;</strong> {{countries.map(el => el.name).join(', ')}} </div>
            <p></p>
            <div><strong>created by:</strong></div>
            <ul v-if="cast_members">
              <li v-for="member in cast_members" :key="member.id">
                <v-btn :to="{ name: 'people_single', params:{ id: member.person.id } }" text class="no-text-transform">
                  {{ member.person.name + " " + member.person.surname + " - " + member.roles.map(el => el.name).join(', ') }}
                </v-btn>
              </li>
            </ul>
          </v-col>
        </v-row>
        <div class="mb-16">
          <div class="mt-12 mb-2 medium-font">Cast</div>
          <v-row>
            <v-col md="12">
              <template>
                <v-sheet class="mx-auto pt-4" elevation="8">
                  <v-slide-group class="pa-2" active-class="success" show-arrows>
                    <v-slide-item v-for="item in characters" :key="item.id" >
                      <v-card max-width="180" class="ma-3" :to="{ name: 'people_single', params:{ id: item.id } }">
                        <v-img v-if="item.person.photo !== null" :src="item.person.photo" height="250" width="180"></v-img>
                        <v-img v-else src="@/assets/no-image.jpg" alt="" height="250" width="180"></v-img>
                        <p class="text-center mt-2">{{item.person.name + " " + item.person.surname}}</p>
                        <p class="text-center">as</p>
                        <p class="text-center">{{item.name}}</p>
                      </v-card>
                    </v-slide-item>
                  </v-slide-group>
                </v-sheet>
              </template>
            </v-col>
          </v-row>
        </div>
        <div class="mt-12 mb-16 medium-font">
          Reviews
          <div v-if="this.$store.getters.isAuthenticated">
            <div v-if="reviewed && userReview">
              <div class="mt-4 medium-small-font mb-2">Your review:</div>
              <v-card>
                <div class="d-flex justify-space-between">
                  <div class="justify-center">
                    <v-card-title>{{this.$store.getters.loggedUser.username}}</v-card-title>
                    <v-card-subtitle>{{userReview.created.split('T')[0]}}</v-card-subtitle>
                  </div>
                  <div class="small-font red-color mt-5" v-if="userReview.is_accepted === false">
                    This review is awaiting acceptance...
                  </div>
                  <div class="d-flex justify-center align-center mr-4">
                    <v-icon color="yellow" large>fas fa-star</v-icon>
                    <div class="ml-2 xd">{{userReview.rating}}</div>
                  </div>
                </div>
                <v-card-text class="text--primary">{{userReview.body}}
                </v-card-text>
                <v-card-actions>
                  <v-btn @click="deleteReview" class="d-flex justify-end" color="#ff5252" text>
                    <i class="fas fa-trash-alt mr-1"></i>
                    <div>delete</div>
                  </v-btn>
                </v-card-actions>
              </v-card>
            </div>
            <div v-else class="mt-4">
              <v-form ref="reviewForm" v-model="reviewValid">
                <v-rating v-model="reviewRating" length="10" required large background-color="yellow lighten-3" color="yellow"></v-rating>
                <v-textarea v-model="reviewText" :rules="reviewRules" label="Your review" counter maxlength="1000" full-width single-line></v-textarea>
                <div class="red-color small-font" v-if="!reviewValidRating">Your review has to include rating.</div>
                <v-btn class="d-flex mt-2" @click="submitReview()">Submit</v-btn>
              </v-form>
            </div>
          </div>
          <div class="mt-16 medium-small-font mb-2">Latest review:</div>
          <div v-if="latestReview">
            <v-card>
              <div class="d-flex justify-space-between">
                <div class="justify-center">
                  <v-card-title class="pointer" @click="toUserProfile">{{latestReview.user.username}}</v-card-title>
                  <v-card-subtitle>{{latestReview.created.split('T')[0]}}</v-card-subtitle>
                </div>
                <div class="d-flex justify-center align-center mr-4">
                  <v-icon color="yellow" large>fas fa-star</v-icon>
                  <div class="ml-2 xd">{{latestReview.rating}}</div>
                </div>
              </div>
              <v-card-text class="text--primary">{{latestReview.body}}
              </v-card-text>
            </v-card>
            <v-btn class="mt-10 no-text-transform" :to="{ name: 'episode_reviews' }">
              SEE MORE REVIEWS
            </v-btn>
          </div>
          <div class="medium-small-font red-color" v-else>
            This episode has currently no reviews.
          </div>
          <v-snackbar bottem v-model="snackbar" :timeout="2000">
            {{ snackbarText }}
            <template v-slot:action="{ attrs }">
              <v-btn color="blue" text v-bind="attrs" @click="snackbar = false">
                Close
              </v-btn>
            </template>
          </v-snackbar>
        </div>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import store from "../../../store";

const charactersLimit = 100

export default {
  name: "Episode",
  data: () => ({
    episode: {},
    title: {},
    genres: [],
    languages: [],
    countries: [],
    characters: [],
    cast_members: [],
    reviewed: false,
    reviewRating: 0,
    reviewText: "",
    userReview: null,
    username: "",
    latestReview: null,
    reviewValid: true,
    reviewValidRating: true,
    snackbar: false,
    snackbarText: "You must have an account to see others' profiles",
    rating: null,
    reviewRules: [
      v => !!v || 'Review text is required',
      v => (v && v.length >= 16) || 'Review must be more than 16 characters',
    ],
  }),
  created() {
    let epid = this.$route.params.epid
    this.$store.dispatch('api/episode/loadOne', epid).then((res) => {
      this.episode = res.data
      this.title = res.data.title
      this.rating = Math.round(this.episode.rating * 10) / 10
      this.loadData(res.data)
      this.isReviewed(epid)
    })
  },
  computed: {
    stringifyDuration: function() {
      let duration = this.episode.duration
      let hours = Math.floor(duration / 60);
      if (hours === 0) {
        return duration + "min"
      }
      let minutes = duration % 60
      if (minutes === 0) {
        return hours + "h"
      }
      return hours + "h " + minutes + "min"
    },
  },
  methods: {
    loadData(episode) {
      this.$store.dispatch('api/genre/loadMany', {ids: episode.title.genres.toString()}).then((res) => {
        this.genres = res.data.results
      })
      this.$store.dispatch('api/lang/loadMany', {ids: episode.title.languages.toString()}).then((res) => {
        this.languages = res.data.results
      })
      this.$store.dispatch('api/country/loadMany', {ids: episode.title.countries.toString()}).then((res) => {
        this.countries = res.data.results
      })
      this.$store.dispatch('api/castMember/loadMany', {ids: episode.title.cast_members.toString()}).then((res) => {
        this.cast_members = res.data.results
      })
      this.$store.dispatch('api/character/loadMany', {ids: episode.characters.toString(),
        perPage: charactersLimit}).then((res) => {
        this.characters = res.data.results
      })
      this.loadReviews(episode)
    },
    loadReviews(episode) {
      if (this.$store.getters.isAuthenticated) {
        this.$store.dispatch('api/review/loadMany', {user: store.getters.loggedUser.id, episode: episode.id})
            .then((res) => {
              this.userReview = res.data.results[0]
            })
      }
      this.$store.dispatch('api/review/loadMany', {episode: episode.id, sortBy: "-created",
        isAccepted: "True"}).then((res) => {
        this.latestReview = res.data.results[0]
      })
    },
    isReviewed(episodeId) {
      this.$store.dispatch('api/review/loadMany',
          {episode: episodeId, user: store.getters.loggedUser.id}).then((res) => {
        this.reviewed = res.data.count !== 0
      })
    },
    submitReview() {
      if (this.validate(this.$refs.reviewForm)) {
        this.$store.dispatch('api/review/create', {user: store.getters.loggedUser.id, episode: this.episode.id,
          rating: this.reviewRating, body: this.reviewText}).then((res) => {
          this.reviewed = true
          this.reviewValidRating = true
          this.userReview = res.data
        }, () => {
          this.reviewValidRating = false
        })
      }
    },
    deleteReview() {
      this.$store.dispatch('api/review/loadMany', {user: store.getters.loggedUser.id, episode: this.episode.id})
          .then((res) => {this.$store.dispatch('api/review/remove', res.data.results[0].id).then(() => {
            this.reviewed = false
            this.reviewRating = 0
            this.reviewText = ""
            if (this.latestReview !== undefined && this.userReview.id === this.latestReview.id) {
              this.$store.dispatch('api/review/loadMany', {episode: this.episode.id, sortBy: "-created",
                isAccepted: "True"}).then((res) => {
                this.latestReview = res.data.results[0]
              })
              this.$store.dispatch('api/episode/loadOne', this.episode.id).then((res) => {
                this.rating = Math.round(res.data.rating * 10) / 10
              })
            }
          })
          })
    },
    toUserProfile() {
      if (this.$store.getters.isAuthenticated) {
        this.$router.push({ path: '/user/' + this.latestReview.user.id });
      }
      else
        this.snackbar = true
    },
    toSeries() {
      this.$router.push({ path: '/series/' + this.title.id });
    },
    validate (ref) {
      return ref.validate()
    },
  }
}
</script>

<style scoped lang="scss">
.big-font {
  font-size: 50px
}

.medium-font {
  font-size: 35px
}

.medium-small-font {
  font-size: 20px
}

.small-font {
  font-size: 13px
}

.reduced-margin {
  margin-bottom: -45px;
}

.no-text-transform {
  text-transform: none;
}

.red-color {
  color: var(--v-error-base);
}

.pointer {
  cursor: pointer;
}
</style>