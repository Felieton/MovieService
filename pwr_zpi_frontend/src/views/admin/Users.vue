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
          <v-toolbar-title class="text-capitalize">Users</v-toolbar-title>
        </v-toolbar>

        <v-dialog
            v-model="dialog"
            max-width="500px"
        >
          <v-card>
            <v-card-title>
              <span class="text-h5">Edit User</span>
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-form ref="itemForm" v-model="itemFormValid">
                  <v-row>
                    <v-col
                        cols="12"
                        sm="6"
                        md="4"
                    >
                      <v-text-field
                          v-model="editedItem.id"
                          label="Id"
                          disabled
                      ></v-text-field>
                    </v-col>
                    <v-col
                        cols="12"
                        sm="6"
                    >
                      <v-text-field
                          v-model="editedItem.username"
                          label="Username"
                          :rules="rules.username"
                          required
                          counter="16"
                      />
                    </v-col>
                    <v-col
                        cols="12"
                        sm="6"
                    >
                      <v-text-field
                          v-model="editedItem.email"
                          label="Email"
                          :rules="rules.email"
                          required
                      />
                    </v-col>
                    <v-col
                        cols="12"
                        sm="6"
                    >
                      <v-select
                          v-model="editedItem.groups"
                          label="Groups"
                          :rules="rules.groups"
                          :items="groups"
                          item-text="name"
                          item-value="id"
                          multiple
                          required
                      />
                    </v-col>

                  </v-row>
                </v-form>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                  color="primary"
                  text
                  @click="closeFormDialog"
              >
                Cancel
              </v-btn>
              <v-btn
                  color="primary"
                  text
                  @click="saveItem"
              >
                Save
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </template>

      <template v-slot:item.groups="{ item }">
        {{ getVerboseGroups(item.groups) }}
      </template>

      <template v-slot:item.last_login="{ item }">
        {{ item.last_login | formatDateTime }}
      </template>

      <template v-slot:item.actions="{ item }">
        <v-icon
            small
            class="mr-2"
            @click="openEditItem(item)"
        >
          mdi-pencil
        </v-icon>
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
import moment from "moment";

export default {
  name: "Users",
  data () {
    return {
      rules: {
        username: [
          (v => !!v || 'Username is required'),
          (v => v?.length <= 16 || 'Username is too long')
        ],
        email: [
          (v => !!v || 'Email is required'),
          (v => /.+@.+\..+/.test(v) || 'Email must be valid'),
        ],
        groups: [
          (v => !!v || 'User must have at least one group'),
          (v => !!v?.length || 'User must have at least one group'),
        ],
      },
      defaultItem: {
        id: 1,
      },
      groups: [],
      editedIndex: -1,
      editedItem: {
        id: -1,
      },
      itemFormValid: true,
      dialog: false,
      totalDataItems: 0,
      options: {
        sortBy: ['id'],
        sortDesc: [false],
      },
      MAP_GROUP: {},
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
        { text: 'Username', value: 'username' },
        { text: 'Email', value: 'email' },
        { text: 'Groups', value: 'groups' },
        { text: 'Last login', value: 'last_login' },
        { text: 'Actions', value: 'actions', align: 'end', sortable: false },
      ],
    }
  },
  async created() {
    await this.loadGroups()
  },
  watch: {
    options: {
      handler () {
        console.log(this.options)
        this.getDataFromApi()
      },
      deep: true,
    },
    dialog (val) {
      val || this.closeFormDialog()
    },
  },
  methods: {
    async loadGroups () {
      const res = await this.$store.dispatch("api/group/loadMany")
      this.groups = res.data.results
      const map_group = {}
      this.groups.forEach( el => map_group[el.id] = el.name)
      this.MAP_GROUP = map_group
    },

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

      const res = await this.$store.dispatch("api/user/loadMany", params)

      const { results, count } = res.data
      return { results, count }
    },

    openEditItem (item) {
      this.editedIndex = this.dataItems.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialog = true
    },

    closeFormDialog () {
      this.dialog = false
      this.$nextTick( () => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },

    async saveItem () {
      if (!this.$refs.itemForm.validate()) return

      const item = Object.assign({}, this.editedItem)
      const itemIndex = this.editedIndex
      this.closeFormDialog()
      try {
        await this.$store.dispatch("api/user/update", item)
        Object.assign(this.dataItems[itemIndex], item)
        this.showSnackSuccess('User modified')
      } catch (err) {
        if (err.response) {
          const errorMsg = this.formatResponseErrors(err.response)
          this.showSnackError(`Could not modify the user. Errors: ${errorMsg}`)
        }
        else {
          this.showSnackError('Could not modify the user. Please try again later')
        }
      }
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

    getVerboseGroups (groups) {
      if (!groups || !groups.length) return ''
      return groups.map(g => this.MAP_GROUP[g]).join(', ')
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

</style>