<template>
  <div class="mt-16">
    <v-row v-if="person.id" justify="center">
      <v-col md="8">
        <v-row class="reduced-margin">
          <v-col cols="12" sm="9">
            <div v-if="person" class="big-font">{{person.name + " " + person.surname}}</div>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" sm="3" class="mt-5">
            <v-img v-if="person.photo !== null" :src="person.photo" height="400" width="280"></v-img>
            <v-img v-else src="@/assets/no-image.jpg" alt="" height="444" width="330"></v-img>
          </v-col>
          <v-col cols="12" sm="4" class="mt-5">
            <h3>{{person.details}}</h3>
            <p></p>
            <div v-if="person.birthdate">
              <strong>birthdate:&nbsp;&nbsp;</strong>{{person.birthdate}}
            </div>
            <div v-else><strong>birthdate:&nbsp;&nbsp;</strong>unknown</div>
          </v-col>
        </v-row>
        <div class="mb-16">
          <div class="mt-12 mb-2 medium-font">Known from</div>
          <v-row>
            <v-col md="12">
              <template>
                <v-sheet class="mx-auto pt-4" elevation="8">
                  <v-slide-group class="pa-2" active-class="success" show-arrows>
                    <v-slide-item v-for="item in titles" :key="item.id" >
                      <v-card max-width="180" class="ma-3" :to="{ name: getRouteName(item), params:{ id: item.id } }">
                        <v-img v-if="item.poster !== null" :src="item.poster" height="250" width="180"></v-img>
                        <v-img v-else src="@/assets/no-image.jpg" alt="" height="250" width="180"></v-img>
                        <p class="text-center mt-2">{{item.title}}</p>
                      </v-card>
                    </v-slide-item>
                  </v-slide-group>
                </v-sheet>
              </template>
            </v-col>
          </v-row>
        </div>
      </v-col>
    </v-row>
  </div>
</template>

<script>

const titleLimit = 100

export default {
  name: "Person",
  data: () => ({
    person: {},
    titles: []
  }),
  created() {
    let id = this.$route.params.id
    this.$store.dispatch('api/person/loadOne', id).then((res) => {
      this.person = res.data
      this.loadData(res.data)
    })
  },
  methods: {
    async loadData(person) {
      let resChars = await this.$store.dispatch('api/title/loadMany', {charactersPerson: person.id, perPage: titleLimit})
      this.$store.dispatch('api/title/loadMany', {castMembersPerson: person.id, perPage: titleLimit}).then((res) => {
        const data = [...resChars.data.results, ...res.data.results]
        this.titles = [...new Map(data.map(item => [item['id'], item])).values()]
      })
    },
    getRouteName: function(title) {
      if (title.type === "M") {
        return 'movies_single'
      }
      else
        return 'series_single'
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