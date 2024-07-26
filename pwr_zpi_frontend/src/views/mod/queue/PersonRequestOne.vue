<template>
  <v-container class="py-16">
    <v-row class="pb-16 justify-center">
      <span class="text-h4">{{ requestAction }} request</span>
    </v-row>

    <v-row class="justify-center">
      <v-col
          v-for="person in people"
          :key="person.id"
          class="col-6 d-flex flex-column align-center"
      >
        <v-row class="pb-4">
          <v-chip
              class="ma-2"
              color="accent"
              outlined
              label
          >
            <span v-if="person.is_submission">New Person</span>
            <span v-else>Current Person</span>
          </v-chip>
        </v-row>
        <v-row>
          <span class="text-h4">{{ getFullName(person) }}</span>
        </v-row>
        <v-row>
          <v-col>
            <v-img
                v-if="person.photo"
                :src="person.photo"
                height="400"
                width="280"
            />
            <v-img
                v-else
                src="@/assets/no-image.jpg"
                height="444"
                width="330"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <h3>{{ person.details }}</h3>
            <p></p>
            <div v-if="person.birthdate">
              <strong>birthdate:&nbsp;&nbsp;</strong>{{ person.birthdate }}
            </div>
            <div v-else>
              <strong>birthdate:&nbsp;&nbsp;</strong>unknown
            </div>
          </v-col>
        </v-row>
      </v-col>
    </v-row>

    <v-divider class="my-8" />

    <template v-if="pr.status === STATUS_PENDING">
      <v-row class="py-8 justify-center">
        <span v-if="people.length > 1" class="text-h4">Do you accept the changes?</span>
        <span v-else class="text-h4">Do you accept new Person?</span>
      </v-row>

      <v-row class="col-10 offset-1">
        <v-form class="d-flex grow" ref="requestForm" v-model="requestFormValid">
          <v-textarea
              auto-grow
              counter="1000"
              label="Reason"
              required
              :rules="details.rules"
              v-model="details.value"
          ></v-textarea>
        </v-form>
      </v-row>

      <v-row class="justify-center">
        <v-col class="d-flex justify-end">
          <v-btn
              color="success"
              @click="acceptRequest(pr)"
          >
            <v-icon left>fas fa-check</v-icon>
            <span>Accept</span>
          </v-btn>
        </v-col>
        <v-col class="d-flex justify-start">
          <v-btn
              color="error darken-4"
              @click="rejectRequest(pr)"
          >
            <v-icon left>fas fa-times</v-icon>
            <span>Reject</span>
          </v-btn>
        </v-col>
      </v-row>
    </template>
    <template v-else>
      <v-row class="py-8 justify-center">
        <span class="text-h4">Request {{ requestStatusClosed }}</span>
      </v-row>
      <v-divider class="my-8" />
    </template>

    <template v-if="$store.getters.loggedUserIsAdmin && logs.length">
      <v-row>
        <v-col class="offset-1">
          <span class="text-h6">Logs</span>
        </v-col>
      </v-row>
      <v-row>
        <v-simple-table class="col-10 offset-1">
          <template v-slot:default>
            <thead>
            <tr>
              <th class="text-left">
                Id
              </th>
              <th class="text-left">
                Details
              </th>
              <th class="text-left">
                Moderator
              </th>
              <th class="text-left">
                Ip address
              </th>
              <th class="text-left">
                Created
              </th>
            </tr>
            </thead>
            <tbody>
            <tr
                v-for="item in logs"
                :key="item.id"
            >
              <td>{{ item.id }}</td>
              <td>{{ item.details }}</td>
              <td>
                <router-link
                  class="link-hover"
                  :to="{ name: 'UserProfile', params: { id: item.moderator.id } }"
                >
                  {{ item.moderator.username }}
                </router-link>
              </td>
              <td>{{ item.ip_address }}</td>
              <td>{{ item.created | formatDateTime }}</td>
            </tr>
            </tbody>
          </template>
        </v-simple-table>
      </v-row>
    </template>

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
  name: "PersonRequestOne",
  data () {
    return {
      requestFormValid: true,
      details: {
        rules: [
          (v => !!v || 'Reason is required'),
          (v => v?.length <= 1000 || 'Reason is too long')
        ],
        value: '',
      },
      pr: {},
      people: [],
      snack: {
        visible: false,
        color: '',
        text: '',
      },
      redirecting: false,
      STATUS_PENDING: 'P',
      STATUS_ACCEPTED: 'A',
      logs: [],
      ACTION: {
        ADD: 'A',
        EDIT: 'E',
        DELETE: 'R'
      }
    }
  },
  async created() {
    this.pr.id = this.$route.params.id
    const res = await this.$store.dispatch('api/personRequest/loadOne', this.pr.id)
    this.pr = res.data
    const people = []
    if (this.pr.person_submission) {
      this.pr.person_submission.is_submission = true
      if (this.pr.action !== this.ACTION.EDIT || this.pr.status === this.STATUS_PENDING) {
        people.push(this.pr.person_submission)
      }
    }
    if (this.pr.current_person) {
      people.push(this.pr.current_person)
    }
    this.people = people
    await this.loadLogs()
  },
  computed: {
    requestAction () {
      if (this.pr.action === this.ACTION.ADD) return 'Add'
      if (this.pr.action === this.ACTION.EDIT) return 'Edit'
      return 'Remove'
    },
    requestStatusClosed () {
      if (this.pr.status === this.STATUS_ACCEPTED) return 'accepted'
      return 'rejected'
    },
  },
  methods: {
    async loadLogs () {
      if (this.pr.status === this.STATUS_PENDING) return

      try {
        const res = await this.$store.dispatch(
            "api/requestLog/loadMany",
            { personRequest: this.pr.id }
        )
        const { results } = res.data
        this.logs = results
      } catch (err) {
        if (err.response) {
          const errorMsg = this.formatResponseErrors(err.response)
          this.showSnackError(`Could not retrieve request logs. Errors: ${errorMsg}`)
        }
        else {
          this.showSnackError(`Could not retrieve request logs. Please try again later`)
        }
      }
    },

    async acceptRequest (request) {
      if (!this.$refs.requestForm.validate()) {
        this.showSnackError('Provided dat is not valid')
        return
      }
      if (this.redirecting) return

      try {
        await this.$store.dispatch(
            "api/personRequest/accept",
            { id: request.id, details: this.details.value }
        )
        this.showSnackSuccess('Person request accepted. Redirecting...')
        this.goBackToQueue(3000)
      } catch (err) {
        if (err.response) {
          const errorMsg = this.formatResponseErrors(err.response)
          this.showSnackError(`Could not accept the request. Errors: ${errorMsg}`)
        }
        else {
          this.showSnackError(`Could not accept the request. Please try again later`)
        }
      }
    },

    async rejectRequest (request) {
      if (!this.$refs.requestForm.validate()) {
        this.showSnackError('Provided data is not valid')
        return
      }
      if (this.redirecting) return

      try {
        await this.$store.dispatch(
            "api/personRequest/reject",
            {id: request.id, details: this.details.value}
        )
        this.showSnackSuccess('Person request rejected. Redirecting...')
        this.goBackToQueue(3000)
      } catch (err) {
        if (err.response) {
          const errorMsg = this.formatResponseErrors(err.response)
          this.showSnackError(`Could not reject the request. Errors: ${errorMsg}`)
        }
        else {
          this.showSnackError(`Could not reject the request. Please try again later`)
        }
      }
    },

    goBackToQueue (delay) {
      this.redirectAfterDelay({ name: 'mod_queue_person' }, delay)
    },

    redirectAfterDelay (route, delay) {
      this.redirecting = true
      setTimeout( () => {
        this.$router.push(route)
      }, delay)
      this.redirecting = false
    },

    getFullName(person) {
      return person.name + ' ' + person.surname
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
      return moment(String(value)).format('YYYY-MM-DD hh:mm:ss')
    },
  },
}
</script>

<style scoped>

</style>