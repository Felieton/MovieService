<template>
  <v-container>

    <v-app-bar app>
      <div class="ml-auto">
        <v-btn text class="text-none" to="/">Visit site</v-btn>
      </div>

      <v-divider vertical />

      <v-btn text v-if="!this.$store.getters.isAuthenticated" to="/login">
        <h3 class="text-none">Login</h3>
        <v-icon>mdi-open-in-new</v-icon>
      </v-btn>

      <div class="d-flex align-center" v-if="this.$store.getters.isAuthenticated">
        <div class="d-flex align-center">
          <v-avatar size="40" class="mx-2">
            <v-img v-if="$store.getters.loggedUser.photo" :src="$store.getters.loggedUser.photo" />
            <v-icon size="30" v-else>fas fa-user-circle</v-icon>
          </v-avatar>
          <h3>{{this.$store.getters.loggedUser.username}}</h3>
        </div>

        <v-menu :close-on-click="true" offset-y>
          <template v-slot:activator="{ on, attrs }">
            <v-btn class="adjust-margin-left" icon v-bind="attrs" v-on="on">
              <i class="fas fa-chevron-down"></i>
            </v-btn>
          </template>

          <v-card>
            <v-list>
              <v-list-item-group>
                <v-list-item :to="{ name: 'UserProfile', params: { id: this.$store.getters.loggedUser.id } }">
                  <v-list-item-icon>
                    <v-icon>fas fa-user-circle</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content>
                    <v-list-item-title>
                      Profile
                    </v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-list-item-group>
            </v-list>
          </v-card>
        </v-menu>
      </div>
    </v-app-bar>

    <v-navigation-drawer dark app permanent>
      <v-row
          class="fill-height"
          no-gutters
      >
        <!-- most left nav drawer -->
        <v-navigation-drawer
            dark
            mini-variant
            mini-variant-width="56"
            permanent
        >
          <!-- icon in the left top corner -->
          <v-list-item
              class="px-2"
              to="/admin"
              v-ripple=false
              style="background-color: #1a1a1a; color: #1a1a1a"
          >
            <v-list-item-avatar>
              <v-icon>fas fa-film</v-icon>
            </v-list-item-avatar>
          </v-list-item>

          <v-divider/>

          <!-- category icons on the left -->
          <v-list dense subheader>
            <v-list-item-group mandatory v-model="categoryId">
              <v-list-item
                  link
                  v-ripple=false
                  v-for="(cat, ind) in categories"
                  :key="ind"
                  :value="ind"
              >
                <v-list-item-action>
                  <v-icon>{{ cat.icon }}</v-icon>
                </v-list-item-action>
              </v-list-item>
            </v-list-item-group>
          </v-list>
        </v-navigation-drawer>

        <!-- category name in the right drawer -->
        <div class="grow">
          <v-list class="pb-0" style="background-color: #262626;">
            <v-list-item-group>
              <v-list-item disabled>
                <v-list-item-title>{{categories[categoryId].title}}</v-list-item-title>
              </v-list-item>
            </v-list-item-group>
          </v-list>

          <v-divider/>

          <!-- pages under certain category -->
          <v-list class="grow pt-0">
            <v-list-item-group>
              <v-list-item
                  link
                  v-for="(item, ind) in categories[categoryId].pages"
                  :key="ind"
                  :to="item.to"
                  :exact="item.exact"
              >
                <v-list-item-title v-text="item.title"></v-list-item-title>
              </v-list-item>
            </v-list-item-group>
          </v-list>
        </div>

      </v-row>
    </v-navigation-drawer>

    <v-main>
      <router-view/>
    </v-main>

  </v-container>
</template>

<script>
export default {
  name: "AdminLayout",
  beforeCreate() {
    this.$vuetify.theme.dark = true
  },
  data () {
    return {
      categories: [
        {
          title: 'General',
          icon: 'mdi-view-dashboard',
          pages: [
            {
              title: 'Dashboard',
              to: { name: 'admin' },
              exact: true,
            },
            {
              title: 'Users',
              to: { name: 'admin_users' },
              exact: true,
            },
          ]
        },
        {
          title: 'Data',
          icon: 'fas fa-database',
          pages: [
            {
              title: 'Genres',
              to: { name: 'admin_db_genres' },
              exact: true,
            },
            {
              title: 'Languages',
              to: { name: 'admin_db_languages' },
              exact: true,
            },
            {
              title: 'Countries',
              to: { name: 'admin_db_countries' },
              exact: true,
            },
            {
              title: 'Cast roles',
              to: { name: 'admin_db_cast_roles' },
              exact: true,
            },
          ]
        },
        {
          title: 'History',
          icon: 'fas fa-history',
          pages: [
            {
              title: 'Action logs',
              to: { name: 'admin_history_actions' },
              exact: true,
            },
            {
              title: 'Requests',
              to: { name: 'admin_history_requests' },
              exact: true,
            },
          ]
        },
        {
          title: 'Scraper',
          icon: 'fas fa-download',
          pages: [
            {
              title: 'Sites',
              to: {name: 'admin_scraper_sites'},
              exact: true
            }
          ]
        }
      ],
      categoryId: 0,
    }
  },
}
</script>

<style lang="scss" scoped>

.theme--light {
  .v-app-bar.v-toolbar.v-sheet {
    background-color: #666666;
  }
  .v-btn {
    color: #fff;
  }
}

.theme--dark {
  .v-app-bar.v-toolbar.v-sheet {
    background-color: #404040;
  }
}

</style>
