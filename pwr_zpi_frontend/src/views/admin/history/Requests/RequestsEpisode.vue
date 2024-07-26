<template>
  <v-container>
    <v-row
        v-for="item in items"
        :key="item.id"
        :set="closedChip = getRequestClosedChip(item)"
    >
      <v-col>
        <v-card>
          <v-row>
            <v-col class="col-10">
              <div class="d-flex justify-start">
                <v-chip
                    class="ma-2"
                    :color="item.chip.color"
                    outlined
                    label
                >
                  <v-icon left>
                    {{ item.chip.icon }}
                  </v-icon>
                  {{ item.chip.text }}
                </v-chip>
                <v-chip
                    class="ma-2"
                    :color="closedChip.color"
                    outlined
                    label
                >
                  <v-icon left>
                    {{ closedChip.icon }}
                  </v-icon>
                  {{ closedChip.text }}
                </v-chip>
              </div>
              <div v-if="item.current_episode" class="d-flex text-break text-subtitle-1 px-4 pt-4">
                <router-link
                    class="link-hover"
                    :to="{ name: 'episodes_single', params: { id: item.current_episode.id }}"
                >
                  {{ item.current_episode.name }}
                </router-link>
              </div>
              <v-card-title class="text-break">{{ item.header }}</v-card-title>
              <v-card-text>
                <p v-if="item.description">{{ item.description }}</p>
                <p v-else class="text--secondary">No description provided</p>
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
            <v-col class="col-2 d-flex flex-column justify-end">
              <v-card-actions class="justify-end">
                <v-tooltip
                    top
                    color="info"
                >
                  <template
                      v-slot:activator="{ on, attrs }"
                  >
                    <v-btn
                        icon
                        color="accent"
                        v-bind="attrs"
                        v-on="on"
                        :to="{ name: 'admin_history_requests_episode_one', params: { id: item.id } }"
                    >
                      <v-icon>arrow_forward_ios</v-icon>
                    </v-btn>
                  </template>
                  <span>More info</span>
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
  name: "RequestsEpisode",
  data () {
    return {
      requestChip: {
        delete: {
          text: 'Delete',
          color: 'red darken-1',
          icon: 'delete_outline'
        },
        add: {
          text: 'Add',
          color: 'green darken-1',
          icon: 'local_fire_department'
        },
        edit: {
          text: 'Edit',
          color: 'lime darken-1',
          icon: 'edit'
        },
        closed: {
          accepted: {
            text: 'Accepted',
            color: 'green lighten-1',
            icon: 'done'
          },
          rejected: {
            text: 'Rejected',
            color: 'red lighten-1',
            icon: 'close'
          }
        }
      },
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
        init: 'No requests in the history',
        current: 'No requests in the history'
      },
      items: [],
      totalItems: 0,
      STATUS_PENDING: 'P',
      STATUS_ACCEPTED: 'A',
      ACTION: {
        ADD: 'A',
        EDIT: 'E',
        DELETE: 'R'
      }
    }
  },
  created() {
    this.pagination.page = 1
  },
  watch: {
    'pagination.page': function () {
      this.updateData()
    },
  },
  methods: {
    async updateData () {
      this.loading = true
      try {
        const data = await this.fetchData()
        data.results.forEach( (el) => this.setItemsChip(el) )
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
      /*
      fields = [
            'id', 'action', 'user', 'header', 'description',
            'current_episode', 'status', 'created',
        ]
       */
      const res = await this.$store.dispatch(
          "api/episodeRequest/loadMany",
          { page: this.pagination.page, isClosed: 1 }
      )

      const { results, count, total_pages } = res.data
      return { results, count, total_pages }
    },

    setItemsChip (item) {
      if (item.action === this.ACTION.ADD) item.chip = this.requestChip.add
      else if (item.action === this.ACTION.EDIT) item.chip = this.requestChip.edit
      else item.chip = this.requestChip.delete
    },

    getRequestClosedChip (request) {
      if (request.status === this.STATUS_ACCEPTED) return this.requestChip.closed.accepted
      return this.requestChip.closed.rejected
    },

    formatResponseErrors (response) {
      return response.data.detail ||
          Object.entries(response.data).map(
              ([key, value]) => `${key} -> ${value}`
          ).join(', ')
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