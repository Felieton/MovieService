<template>
  <div>
    <v-row justify="center">
      <v-col md="8">
        <v-card class="mt-16 mb-16">
          <v-row justify="center">
            <v-col class="justify-center d-flex align-center">
              <v-icon class="mr-4" x-large>fas fa-cog</v-icon>
              <h1 class="mb-4 mt-4 pointer">
                Settings</h1>
            </v-col>
          </v-row>
          <v-row class="mt-10" justify="center">
            <div class="justify-center d-flex align-center">
              <div class="mr-6">Visible email on profile</div>
              <v-switch @change="updateEmailVisibility()" v-model="emailVisible"></v-switch>
            </div>
          </v-row>
          <v-row justify="center">
            <div class="justify-center d-flex align-center">
              <div class="mr-6">Visible watchlist on profile</div>
              <v-switch @change="updateWatchlistVisibility()" v-model="watchlistVisible"></v-switch>
            </div>
          </v-row>
          <v-row justify="center">
            <v-col cols="6">
              <div class="justify-center d-flex align-center">
                <div class="mr-6">Update your bio:</div>
                <v-textarea label="Your bio..." v-model="bio" counter maxlength="255"></v-textarea>
              </div>
            </v-col>
          </v-row>
          <v-row justify="center">
            <v-btn @click="updateBio()">Update bio</v-btn>
          </v-row>
          <v-row justify="center">
            <v-col cols="6">
              <div class="justify-center d-flex align-center">
                <div class="mr-6">Upload your new avatar:</div>
                <v-file-input class="mr-8" v-model="avatar" accept="image/*" label="Avatar"></v-file-input>
              </div>
            </v-col>
          </v-row>
          <v-row justify="center">
            <v-btn class="mr-4" @click="updateAvatar()" :disabled="!avatar">update avatar</v-btn>
            <v-btn @click="removeAvatar()" :disabled="removeButtonDisabled">remove current avatar</v-btn>
          </v-row>
          <v-row justify="center" class="mt-10">
            <v-col cols="2">
              <v-form ref="form" v-model="formValid">
                <v-text-field label="Current password" v-model="currentPassword" :rules="passwordRules" dense required type="password"></v-text-field>
                <v-text-field label="New password" v-model="newPassword" :rules="[requiredRule, lengthRule]" dense required type="password"></v-text-field>
                <v-text-field v-model="rePassword" :rules="[requiredRule, lengthRule, passwordConfirmationRule]" dense required type="password"></v-text-field>
              </v-form>
            </v-col>
          </v-row>
          <v-row justify="center">
            <v-btn @click="changePassword()" class="mb-8 submit-btn">Change</v-btn>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
    <v-snackbar bottem right v-model="snackbar" :timeout="3000">
      {{ snackbarText }}
      <template v-slot:action="{ attrs }">
        <v-btn color="blue" text v-bind="attrs" @click="snackbar = false">
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
import axios from "axios";
import storeCfg from '../../store/config'

export default {
  name: "UserSettings",
  data: () => ({
    defaultParameters: {},
    emailVisible: false,
    watchlistVisible: true,
    userId: 0,
    user: {},
    bio: "",
    removeButtonDisabled: true,
    avatar: null,
    formValid: true,
    snackbarText: "",
    snackbar: false,
    currentPassword: "",
    newPassword: "",
    rePassword: "",
    passwordRules: [
      v => !!v || 'Password is required'
    ],
    requiredRule: v => !!v || 'Password is required',
    lengthRule: v => (v && v.length >= 8) || 'Password must be at least 8 characters',
  }),
  computed: {
    passwordConfirmationRule() {
      return () => (this.newPassword === this.rePassword) || 'Passwords must match'
    }
  },
  created() {
    this.userId = this.$route.params.id
    this.$store.dispatch('api/user/loadOne', this.userId).then((res) => {
      this.user = res.data
      this.emailVisible = res.data.settings.email_visible
      this.watchlistVisible = res.data.settings.watchlist_visible
      if (!this.$store.getters.loggedUser.photo) {
        this.removeButtonDisabled = true
      }
    })
  },
  methods: {
    updateEmailVisibility() {
      this.$store.dispatch('api/user/update', {id: this.userId, settings: {id: this.user.settings.id,
          email_visible: this.emailVisible}})
    },
    updateWatchlistVisibility() {
      this.$store.dispatch('api/user/update', {id: this.userId, settings: {id: this.user.settings.id,
          watchlist_visible: this.watchlistVisible}})
    },
    updateAvatar() {
      this.$store.dispatch('api/user/update', {id: this.userId, file: {name: "photo", content: this.avatar}}).then(()=> {
        this.$store.dispatch('api/user/loadOne', this.userId).then((res)=> {
          let user = this.$store.getters.loggedUser
          user.photo = res.data.photo
          this.removeButtonDisabled = false
          this.$store.commit('loggedUser', {
            loggedUser:  user
          })
        })
      })
    },
    removeAvatar() {
      this.$store.dispatch('api/user/update', {id: this.userId, photo: null}).then(() => {
        let user = this.$store.getters.loggedUser
        user.photo = null
        this.removeButtonDisabled = true
        this.$store.commit('loggedUser', {
          loggedUser:  user
        })
      })
    },
    changePassword: function () {
      if (this.validate(this.$refs.form)) {
        let data = {
          old_password: this.currentPassword,
          new_password1: this.newPassword,
          new_password2: this.rePassword
        };
        axios.post(storeCfg.baseUrl + `o/password/change/`, data).then(() => {
          this.snackbarText = "Your password was successfully changed"
          this.snackbar = true
        }, (err) => {
          this.snackbarText = this.formatResponseErrors(err.response)
          this.snackbar = true
        })
      }
    },
    formatResponseErrors (response) {
      return response.data.detail ||
          Object.entries(response.data).map(
              ([key, value]) => `${key} -> ${value}`
          ).join(', ')
    },
    updateBio() {
      this.$store.dispatch('api/user/update', {id: this.userId, description: this.bio}).then(() => {
        if (this.bio === "") {
          this.snackbarText = "Your bio was successfully removed"
        }
        else {
          this.snackbarText = "Your bio was successfully updated"
        }
        this.snackbar = true
      })
    },
    validate (ref) {
      return ref.validate()
    },
  }
}
</script>

<style scoped>

</style>