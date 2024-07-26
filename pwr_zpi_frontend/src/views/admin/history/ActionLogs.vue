<template>
  <v-container>

    <v-data-table
        height="420px"
        :headers="headers"
        :items="dataItems"
        :loading="loading"
        :options.sync="options"
        :server-items-length="totalDataItems"
        :footer-props="{ 'items-per-page-options': [10, 15, 30] }"
        :no-data-text="noDataText.current"
        class="elevation-1"
    >
      <template v-slot:top>
        <v-toolbar flat>
          <v-toolbar-title class="text-capitalize">Action logs</v-toolbar-title>
        </v-toolbar>
      </template>

      <template v-slot:item.log_type="{ item }">
        {{ getVerboseLogType(item.log_type) }}
      </template>

      <template v-slot:item.moderator="{ item }">
        {{ getVerboseUser(item.moderator) }}
      </template>

      <template v-slot:item.user="{ item }">
        {{ getVerboseUser(item.user) }}
      </template>

      <template v-slot:item.created="{ item }">
        {{ item.created | formatDateTime }}
      </template>
    </v-data-table>

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
import moment from 'moment'

export default {
  name: "ActionLogs",
  data () {
    return {
      totalDataItems: 0,
      options: {},
      MAP_LOG_TYPE: {
        A: 'Admin',
        M: 'Moderator',
        U: 'User'
      },
      snack: {
        visible: false,
        color: '',
        text: '',
      },
      dataItems: [],
      loading: true,
      noDataText: {
        init: 'No data available',
        current: 'No data available'
      },
      headers: [
        { text: 'Id', value: 'id', align: 'start', width: '70' },
        { text: 'Type', value: 'log_type' },
        { text: 'Details', value: 'details' },
        { text: 'Perpetrator', value: 'moderator' },
        { text: 'Ip address', value: 'ip_address' },
        { text: 'Target', value: 'user' },
        { text: 'Created', value: 'created' },
      ],
    }
  },
  watch: {
    options: {
      handler () {
        console.log(this.options)
        this.getDataFromApi()
      },
      deep: true,
    },
  },
  methods: {
    async getDataFromApi () {
      this.loading = true
      this.noDataText.current = this.noDataText.init
      try {
        const data = await this.fetchData()
        this.dataItems = data.results
        this.totalDataItems = data.count
      } catch (err) {
        const err_info = 'Could not load the data'
        this.noDataText.current = err_info
        this.dataItems = []
        this.totalDataItems = 0
        this.showSnackError(err_info)
      }
      this.loading = false
    },

    formatSortByParam(sortBy, sortDesc) {
      return sortBy.map( (el, ind) => (sortDesc[ind] ? '-' : '') + el ).join(',')
    },

    async fetchData () {
      const {sortBy, sortDesc, page, itemsPerPage} = this.options
      const params = {
        page: page,
        perPage: itemsPerPage,
        sortBy: this.formatSortByParam(sortBy, sortDesc)
      }

      const res = await this.$store.dispatch("api/actionLog/loadMany", params)

      const { results, count } = res.data
      return { results, count }
    },

    showSnack ( { text, color }) {
      this.snack.text = text
      this.snack.color = color
      this.snack.visible = true
    },

    showSnackInfo (text) {
      const color = this.$vuetify.theme.currentTheme.info
      this.showSnack({text, color })
    },

    showSnackSuccess (text) {
      const color = this.$vuetify.theme.currentTheme.success
      this.showSnack({text, color })
    },

    showSnackError (text) {
      const color = this.$vuetify.theme.currentTheme.error
      this.showSnack({text, color })
    },

    getVerboseLogType (log_type) {
      if (!log_type || !(log_type in this.MAP_LOG_TYPE)) return ''
      return this.MAP_LOG_TYPE[log_type]
    },

    getVerboseUser (user) {
      if (!user) return ''
      if (typeof user !== 'object') return user
      return user.username
    },

  },
  filters: {
    formatDateTime (value) {
      if (!value) return ''
      return moment(String(value)).format('YYYY-MM-DD hh:mm:ss')
    },
  },
}
</script>

<style scoped>

</style>