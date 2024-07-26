<template>
  <v-layout>
    <v-app-bar app color="primary" dark>
      <v-btn plain text class="no-text-transform" to="/">
        <i class="fas fa-film fa-3x mr-4"></i>
        <h1>Movie Service</h1>
      </v-btn>

      <v-spacer></v-spacer>
      <template>
        <v-autocomplete v-model="select" :loading="loading" :items="items" :search-input.sync="search" cache-items
            class="mx-4" flat hide-no-data hide-details label="Search movies and series" solo-inverted item-text="title"
                        item-value="id" v-on:keyup.enter="goToFound"></v-autocomplete>
      </template>
      <v-btn @click="goToFound" class="ml-1" icon>
        <i class="fas fa-search"></i>
      </v-btn>
      <v-spacer></v-spacer>
      <div>
        <v-btn v-if="this.$store.getters.isAuthenticated" text class="mr-4" to="/add">Add</v-btn>
        <v-btn text class="mr-4" to="/movies">Movies base</v-btn>
        <v-btn text class="mr-4" to="/series">Series base</v-btn>
        <v-btn text to="/people">People base</v-btn>
      </div>
      <v-spacer></v-spacer>

      <v-btn text v-if="!this.$store.getters.isAuthenticated" to="/login">
        <h3 class="mr-2">Login</h3>
        <v-icon>mdi-open-in-new</v-icon>
      </v-btn>

      <div class="mr-2" v-if="this.$store.getters.isAuthenticated">
        <v-btn v-if="this.$store.getters.loggedUser" text class="no-text-transform" @click="redirectToUser">
          <v-img class="image" v-if="this.$store.getters.loggedUser.photo !== null" :src="this.$store.getters.loggedUser.photo"></v-img>
          <i v-else class="fas fa-user-circle fa-2x"></i>
          <h3 class="ml-2">{{this.$store.getters.loggedUser.username}}</h3>
        </v-btn>
        <v-menu :close-on-click="true" offset-y>
          <template v-slot:activator="{ on, attrs }">
            <v-btn class="adjust-margin-left" icon v-bind="attrs" v-on="on">
              <i class="fas fa-chevron-down"></i>
            </v-btn>
          </template>

          <v-card>
            <v-list>
              <v-list-item>
                <v-btn text @click="redirectToUser">
                  <v-icon class="mr-2">fas fa-user-circle</v-icon>
                  Your profile
                </v-btn>
              </v-list-item>
            </v-list>

            <v-divider></v-divider>

            <template v-if="$store.getters.loggedUserIsStaff">
              <v-list>
                <v-list-item>
                  <v-btn class="grow justify-start" text :to="{ name: 'mod' }">
                    <v-icon class="mr-2">fas fa-wrench</v-icon>
                    ModCP
                  </v-btn>
                </v-list-item>
                <v-list-item v-if="$store.getters.loggedUserIsAdmin">
                  <v-btn class="grow justify-start" text :to="{ name: 'admin' }">
                    <v-icon class="mr-2">fas fa-crown</v-icon>
                    AdminCP
                  </v-btn>
                </v-list-item>
              </v-list>
              <v-divider></v-divider>
            </template>

            <v-list>
              <v-list-item>
                <v-btn @click="toSettings()" class="grow justify-start" text>
                  <v-icon class="mr-2">fas fa-cog</v-icon>
                  Settings
                </v-btn>
              </v-list-item>
              <v-list-item>
                <v-btn class="grow justify-start" text @click="logout">
                  <v-icon class="mr-2">fas fa-sign-out-alt</v-icon>
                  Logout
                </v-btn>
              </v-list-item>
            </v-list>
          </v-card>
        </v-menu>
      </div>
      <div>
        <v-tooltip v-if="!$vuetify.theme.dark" bottom>
          <template v-slot:activator="{ on }">
            <v-btn v-on="on" color="info" small fab @click="darkMode">
              <v-icon class="mr-1">mdi-moon-waxing-crescent</v-icon>
            </v-btn>
          </template>
          <span>Dark Mode On</span>
        </v-tooltip>

        <v-tooltip v-else bottom>
          <template v-slot:activator="{ on }">
            <v-btn v-on="on" color="info" small fab @click="darkMode">
              <v-icon color="yellow">mdi-white-balance-sunny</v-icon>
            </v-btn>
          </template>
          <span>Dark Mode Off</span>
        </v-tooltip>
      </div>
    </v-app-bar>

    <v-main>
      <router-view/>
    </v-main>
    <Footer/>
  </v-layout>
</template>

<script>
import Footer from "../../components/Footer";

export default {
  name: "MainLayout",
  data: () => ({
    loading: false,
    items: [],
    search: null,
    select: null,
    userId: 0
  }),
  components: {
    Footer,
  },
  watch: {
    search (val) {
      val && val !== this.select && this.querySelections(val)
    },
  },
  created() {
    this.userId = this.$store.getters.loggedUser.id
  },
  methods: {
    logout: function () {
      this.$store.dispatch('logout');
      if (this.$router.currentRoute.fullPath !== '/')
        this.$router.push({ path: '/' });
    },
    redirectToUser() {
      if (this.$router.currentRoute.fullPath !== '/user/' + this.$store.getters.loggedUser.id)
        this.$router.push({ path: '/user/' + this.$store.getters.loggedUser.id });
    },
    async querySelections (v) {
      this.loading = true
      let res = await this.$store.dispatch('api/title/loadMany', {title: v})
      this.titles = res.data.results
      this.items = this.titles.filter(e => {
        return (e.title || '').toLowerCase().indexOf((v || '').toLowerCase()) > -1
      })
      this.loading = false
    },
    goToFound() {
      if (this.select !== null) {
        this.$store.dispatch('api/title/loadOne', this.select).then((res) => {
          if (res.data.type === 'S' && this.$router.currentRoute.fullPath !== '/series/' + this.select)
            this.$router.push('/series/' + this.select)
          else if (res.data.type === 'M' && this.$router.currentRoute.fullPath !== '/movies/' + this.select)
            this.$router.push('/movies/' + this.select)
          this.select = null
        })
      }
    },
    toSettings() {
      this.$router.push({ path: '/user/' + this.userId + '/settings/'});
    },
    darkMode() {
      this.$vuetify.theme.dark = !this.$vuetify.theme.dark;
    }
  }
}
</script>

<style scoped>
h1 {
  font-family: Bahnschrift, sans-serif;
}

.image {
  object-fit: cover;
  width:40px;
  height:40px;
  border-radius: 50%;
}

.no-text-transform {
  text-transform: none;
}

.adjust-margin-left {
  margin-left: -20px;
}

</style>