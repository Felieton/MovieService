<template>
  <v-container>
    <v-data-table
        height="420px"
        :headers="headers"
        :items="dataItems"
        :loading="loading"
        :footer-props="{ 'items-per-page-options': [10, 15, 30] }"
        class="elevation-1"
    >
      <template v-slot:top>
        <v-toolbar flat>
          <v-toolbar-title class="text-capitalize">{{dataItemNamePlural}}</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-dialog
              v-model="dialog"
              max-width="500px"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                  color="primary"
                  dark
                  class="mb-2"
                  v-bind="attrs"
                  v-on="on"
              >
                New {{dataItemName}}
              </v-btn>
            </template>
            <v-card>
              <v-card-title>
                <span class="text-h5">{{ formTitle }}</span>
              </v-card-title>

              <v-card-text>
                <v-container>
                  <v-form ref="itemForm" v-model="itemFormValid">
                    <v-row>
                      <v-col
                          v-if="idFieldVisible"
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
                          md="4"
                          v-for="header in dataExtraHeaders"
                          :key="header.value"
                      >
                        <v-text-field
                            v-model="editedItem[header.value]"
                            :label="header.text"
                            :rules="header.rules"
                            :required="header.required"
                            :counter="header.counter"
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
          <v-dialog v-model="dialogDelete" max-width="500px">
            <v-card>
              <v-card-title
                  class="text-h6 text-break text-center justify-center"
              >
                Are you sure you want to delete this {{dataItemName}}?
              </v-card-title>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" text @click="closeDeleteItem">Cancel</v-btn>
                <v-btn color="primary" text @click="deleteItem">OK</v-btn>
                <v-spacer></v-spacer>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-toolbar>
      </template>
      <template v-slot:item.actions="{ item }">
        <v-icon
            small
            class="mr-2"
            @click="openEditItem(item)"
        >
          mdi-pencil
        </v-icon>
        <v-icon
            small
            @click="openDeleteItem(item)"
        >
          mdi-delete
        </v-icon>
      </template>
      <template v-slot:no-data>
        {{noDataInfo}}
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
const itemActionsKeys = ['loadMany', 'remove', 'update', 'create']

export default {
  name: "DataManager",
  props: {
    itemActions: {
      type: Object,
      required: true,
      validator: (value) => itemActionsKeys.every( (key) => key in value )
    },
    itemName: String,
    itemNamePlural: String,
    extraHeaders: {
      type: Array
    },
  },
  data () {
    return {
      itemFormValid: true,
      dataItemName: this.itemName || 'item',
      snack: {
        visible: false,
        color: '',
        text: '',
      },
      dialog: false,
      dialogDelete: false,
      dataItems: [],
      loading: true,
      noDataInfo: 'No data available',
      initialHeaders: [
        { text: 'Id', value: 'id', align: 'start', width: '70' },
        {
          text: 'Name',
          value: 'name',
          required: true,
          counter: 32,
          rules: [
            (v => !!v || 'Name is required'),
            (v => v?.length <= 32 || 'Name is too long')
          ]
        },
        { text: 'Actions', value: 'actions', align: 'end', sortable: false }
      ],
      editedIndex: -1,
      editedItem: {
        id: -1,
      },
      defaultItem: {
        id: 1,
      },
    }
  },
  async created() {
    try {
      this.dataItems = await this.getDataItems()
    } catch (err) {
      const err_info = 'Could not load the data'
      this.showSnackError(err_info)
      this.noDataInfo = err_info
    }
    this.loading = false
  },
  computed: {
    formTitle () {
      return (this.editedIndex === -1 ? 'New' : 'Edit') + ` ${this.dataItemName}`
    },
    idFieldVisible () {
      return this.editedIndex !== -1
    },
    dataItemNamePlural () {
      return this.itemNamePlural || `${this.dataItemName}s`
    },
    dataExtraHeaders () {
      if (!this.extraHeaders || !this.extraHeaders.length) return this.initialHeaders.slice(1, -1)
      return this.extraHeaders
    },
    headers () {
      return [
        this.initialHeaders[0],
        ...this.dataExtraHeaders,
        this.initialHeaders[this.initialHeaders.length - 1]
      ]
    },
  },
  watch: {
    dialog (val) {
      val || this.closeFormDialog()
    },
    dialogDelete (val) {
      val || this.closeDeleteItem()
    },
  },
  methods: {
    async getDataItems () {
      const res = await this.$store.dispatch(this.itemActions.loadMany, { perPage: 100 })
      return res.data.results
    },

    capitalize (text) {
      return text.charAt(0).toUpperCase() + text.slice(1)
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

    openEditItem (item) {
      this.editedIndex = this.dataItems.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialog = true
    },

    openDeleteItem (item) {
      this.editedIndex = this.dataItems.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialogDelete = true
    },

    async deleteItem () {
      const item = Object.assign({}, this.editedItem)
      const itemIndex = this.editedIndex
      this.closeDeleteItem()
      try {
        await this.$store.dispatch(this.itemActions.remove, item.id)
        this.dataItems.splice(itemIndex, 1)
        this.showSnackSuccess(`${this.capitalize(this.dataItemName)} deleted`)
      } catch (err) {
        if (err.response) {
          const errorMsg = this.formatResponseErrors(err.response)
          this.showSnackError(`Could not remove the ${this.dataItemName}. Errors: ${errorMsg}`)
        }
        else {
          this.showSnackError(`Could not remove the ${this.dataItemName}. Please try again later`)
        }
      }
    },

    closeFormDialog () {
      this.dialog = false
      this.$nextTick( () => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },

    closeDeleteItem () {
      this.dialogDelete = false
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
      if (itemIndex > -1) {
        try {
          await this.$store.dispatch(this.itemActions.update, item)
          Object.assign(this.dataItems[itemIndex], item)
          this.showSnackSuccess(`${this.capitalize(this.dataItemName)} modified`)
        } catch (err) {
          if (err.response) {
            const errorMsg = this.formatResponseErrors(err.response)
            this.showSnackError(`Could not modify the ${this.dataItemName}. Errors: ${errorMsg}`)
          }
          else {
            this.showSnackError(`Could not modify the ${this.dataItemName}. Please try again later`)
          }
        }
      }
      else {
        try {
          delete item.id
          const res = await this.$store.dispatch(this.itemActions.create, item)
          const newItem = res.data
          this.dataItems.push(newItem)
          this.showSnackSuccess(`${this.capitalize(this.dataItemName)} created`)
        } catch (err) {
          if (err.response) {
            const errorMsg = this.formatResponseErrors(err.response)
            this.showSnackError(`Could not create the ${this.dataItemName}. Errors: ${errorMsg}`)
          }
          else {
            this.showSnackError(`Could not create the ${this.dataItemName}. Please try again later`)
          }
        }
      }
    },
  },
}
</script>

<style scoped>

</style>