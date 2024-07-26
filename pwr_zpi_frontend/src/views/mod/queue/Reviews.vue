<template>
  <v-container>
    <v-row
        v-for="item in items"
        :key="item.id"
    >
      <v-col>
        <v-card>
          <v-row>
            <v-col>
              <v-card-title>
                <router-link
                    class="link-hover"
                    :to="getReviewedLink(item)"
                >
                  {{ getReviewedName(item) }}
                </router-link>
              </v-card-title>
              <v-card-text>
                <p>
                  {{ item.body }}
                </p>
              </v-card-text>
              <v-card-subtitle class="subtitle-2">
                <span>Submitted by </span>
                <router-link
                    class="link-hover"
                    :to="{ name: 'UserProfile', params: { id: item.user.id } }"
                >
                  {{ item.user.username }}
                </router-link>
                <span> • </span>
                <span>{{ item.created | formatDateTime }}</span>
              </v-card-subtitle>
            </v-col>
            <v-col class="col-2">
              <v-card-actions class="justify-end">
                <v-tooltip
                    top
                    color="success"
                >
                  <template
                      v-slot:activator="{ on, attrs }"
                  >
                    <v-btn
                        icon
                        color="accent"
                        v-bind="attrs"
                        v-on="on"
                        @click="acceptReview(item)"
                    >
                      <v-icon>fas fa-check</v-icon>
                    </v-btn>
                  </template>
                  <span>Accept</span>
                </v-tooltip>
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
                        @click="rejectReview(item)"
                    >
                      <v-icon>fas fa-times</v-icon>
                    </v-btn>
                  </template>
                  <span>Reject</span>
                </v-tooltip>
              </v-card-actions>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>

    <v-row v-if="loading">
      <v-col class="d-flex justify-center">
        <v-progress-circular
            indeterminate
            color="primary"
        />
      </v-col>
    </v-row>
    <v-row v-else-if="!items.length">
      <v-col class="d-flex justify-center">
        <span class="text-h6">{{ noDataText.current }}</span>
      </v-col>
    </v-row>
    <v-row v-else>
      <v-col class="col-8 offset-2">
        <div class="d-flex justify-center">
          <v-pagination
              v-model="pagination.page"
              :length="pagination.length"
          />
        </div>
      </v-col>
    </v-row>

    {{ /* TODO: Snack is not showing at the bottom */ }}
    <v-snackbar
        app
        bottom
        v-model="snack.visible"
        :timeout="4000"
        :color="snack.color"
    >
      {{ snack.text }}

      <template v-slot:action="{ attrs }">
        <v-btn
            v-bind="attrs"
            text
            @click="snack.visible = false"
        >
          Close
        </v-btn>
      </template>
    </v-snackbar>

  </v-container>
</template>

<script>
import moment from "moment";

export default {
  name: "Reviews",
  data () {
    return {
      loading: true,
      pagination: {
        page: 0,
        length: 0,
      },
      snack: {
        visible: false,
        color: '',
        text: '',
      },
      noDataText: {
        init: 'No reviews in the queue',
        current: 'No reviews in the queue'
      },
      items: [],
      totalItems: 0,
      TITLE_SERIES: 'S',
      TITLE_MOVIE: 'M'
    }
  },
  async created() {
    this.pagination.page = 1
  },
  watch: {
    // since pagination's @input is triggered even if the page 'changes' to the same page
    // (click on current page triggers it)
    // watcher approach is better
    'pagination.page': function () {
      this.updateData()
    }
  },
  methods: {
    async updateData () {
      this.loading = true
      try {
        const data = await this.fetchData()
        this.items = data.results
        this.totalItems = data.count
        this.pagination.length = data.total_pages
      } catch (err) {
        const err_info = 'Could not load the data'
        this.noDataText.current = err_info
        this.items = []
        this.totalItems = 0
        this.showSnackError(err_info)
      }
      this.loading = false
    },

    async fetchData () {
      const res = await this.$store.dispatch(
          "api/review/loadMany", { page: this.pagination.page, isAccepted: 0 }
      )

      const { results, count, total_pages } = res.data
      return { results, count, total_pages }
    },

    async acceptReview (review) {
      try {
        await this.$store.dispatch("api/review/accept", review.id)
        this.showSnackSuccess('Review accepted')
      } catch (err) {
        if (err.response) {
          const errorMsg = this.formatResponseErrors(err.response)
          this.showSnackError(`Could not accept the review. Errors: ${errorMsg}`)
        }
        else {
          this.showSnackError(`Could not accept the review. Please try again later`)
        }
      }
      await this.updateData()
    },

    async rejectReview (review) {
      try {
        await this.$store.dispatch("api/review/reject", review.id)
        this.showSnackSuccess('Review rejected')
      } catch (err) {
        if (err.response) {
          const errorMsg = this.formatResponseErrors(err.response)
          this.showSnackError(`Could not reject the review. Errors: ${errorMsg}`)
        }
        else {
          this.showSnackError(`Could not reject the review. Please try again later`)
        }
      }
      await this.updateData()
    },

    getReviewedName (item) {
      if (item.episode) return item.episode.name
      return item.title.title
    },

    getReviewedLink (item) {
      if (item.episode) {
        return {
          name: 'episode_single',
          params: { id: item.episode.title, epid: item.episode.id }
        }
      }

      const routeName = item.title.type === this.TITLE_MOVIE ? 'movies_single' : 'series_single'
      return {
        name: routeName,
        params: { id: item.title.id }
      }
    },

    showSnack ( { text, color }) {
      this.snack.text = text
      this.snack.color = color
      this.snack.visible = true
    },

    showSnackSuccess (text) {
      const color = this.$vuetify.theme.currentTheme.success
      this.showSnack({text, color })
    },

    showSnackError (text) {
      const color = this.$vuetify.theme.currentTheme.error
      this.showSnack({text, color })
    },

    formatResponseErrors (response) {
      return response.data.detail ||
          Object.entries(response.data).map(
              ([key, value]) => `${key} -> ${value}`
          ).join(', ')
    },
  },
  filters: {
    formatDateTime (value) {
      if (!value) return ''
      return moment(String(value)).format('YYYY-MM-DD hh:mm')
    },
  },
}
</script>

<style scoped>
.row + .row {
  margin-top: 30px;
}
</style>