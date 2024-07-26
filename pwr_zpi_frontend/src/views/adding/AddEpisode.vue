<template>
  <div>
    <v-container class="mt-16 mb-16">
      <v-row justify="center">
        <v-col>
          <div>
            <v-row class="mt-5" justify="center">
              <v-col class="justify-center d-flex align-center">
                <v-icon class="mr-4" color="red" large>fas fa-pen</v-icon>
                <h1 class="mb-4 mt-4">{{ "Add a new episode" }}</h1>
              </v-col>
            </v-row>
            <v-form ref="form" v-model="formValid">
              <v-row justify="center">
                <div class="justify-center d-flex align-center">
                  <v-col class="d-flex mt-4" cols="10" sm="5">
                    <v-select v-model="chosenSeries" :items="series" :rules="[requiredRule]" item-text="title" item-value="id" label="Series" solo></v-select>
                  </v-col>
                  <v-col class="d-flex" cols="10" sm="5">
                    <v-text-field v-model="chosenName" :rules="[requiredRule]" class="mr-16" label="episode title..."></v-text-field>
                  </v-col>
                  <v-col cols="10" sm="5">
                    <v-menu v-model="menu2" :close-on-content-click="false" transition="scale-transition"
                            offset-y max-width="290px" min-width="auto">
                      <template v-slot:activator="{ on, attrs }">
                        <v-text-field label="Release date" hint="DD/MM/YYYY format" persistent-hint prepend-icon="mdi-calendar"
                                      readonly v-model="chosenReleased" v-bind="attrs" v-on="on"></v-text-field>
                      </template>
                      <v-date-picker v-model="chosenReleased" no-title @input="menu2 = false"></v-date-picker>
                    </v-menu>
                  </v-col>
                </div>
              </v-row>
              <v-row justify="center">
                <div class="justify-center d-flex align-center">
                  <v-col class="d-flex" cols="10" sm="5">
                    <v-text-field v-model="chosenSeason" :rules="[requiredRule, numberRule]" class="mr-16" label="season..."></v-text-field>
                  </v-col>
                  <v-col class="d-flex" cols="10" sm="5">
                    <v-text-field v-model="chosenNumber" :rules="[requiredRule, numberRule]" class="mr-16" label="number..."></v-text-field>
                  </v-col>
                </div>
              </v-row>
              <v-row justify="center">
                <v-col cols="6">
                  <div class="justify-center d-flex align-center">
                    <v-textarea label="Description..." v-model="episodeDescription" :rules="[requiredRule]" counter maxlength="255"></v-textarea>
                  </div>
                </v-col>
              </v-row>
              <div>
                <v-row class="mt-10" justify="center">
                  <div class="medium-font">Characters</div>
                </v-row>
                <v-row justify="center" v-for="(char, index) in characters" :key="index">
                  <div class="justify-center d-flex align-center">
                    <v-col class="d-flex" cols="10" sm="6">
                      <v-text-field v-model="char.name" class="mr-16" label="Character name...">Title</v-text-field>
                    </v-col>
                    <v-col class="d-flex" cols="10" sm="6">
                      <v-select v-model="char.person" :items="people" :item-text="getPersonName"
                                item-value="id" label="Person" solo></v-select>
                    </v-col>
                  </div>
                </v-row>
                <v-row justify="center">
                  <v-btn class="mb-10" @click="addNewCharacterForm()" icon>
                    <v-icon color="red">fas fa-plus</v-icon>
                  </v-btn>
                </v-row>
              </div>
              <div>
                <v-row justify="center">
                  <v-col cols="3">
                    <div class="justify-center d-flex align-center">
                      <v-text-field class="mt-10" v-model="requestHeader" :rules="[requiredRule]" label="Request title"></v-text-field>
                    </div>
                  </v-col>
                </v-row>
                <v-row justify="center">
                  <v-col cols="6">
                    <div class="justify-center d-flex align-center">
                      <v-textarea label="Request comment" v-model="requestComment" counter maxlength="255"></v-textarea>
                    </div>
                  </v-col>
                </v-row>
                <v-row class="mt-16" justify="center">
                  <v-btn @click="sendEpisodeRequest()">
                    <div class="mr-4">Request adding episode</div>
                    <v-icon color="red">fas fa-paper-plane</v-icon>
                  </v-btn>
                </v-row>
              </div>
            </v-form>
            <v-alert :value="successRequestAlert" type="success" dismissible>Request has been submitted</v-alert>
            <v-alert :value="errorRequestAlert" type="error" dismissible>An error occurred while submitting request</v-alert>
          </div>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>


<script>
const personNumber = 999
const titlesNumber = 99
export default {
  name: "AddEpisode",
  data: () => ({
    menu2: false,
    characters: [{name: "", person: null}],
    people: [],
    series: [],
    chosenName: "",
    chosenSeason: null,
    chosenNumber: null,
    chosenSeries: null,
    chosenReleased: null,
    episodeDescription: '',
    formValid: true,
    requestComment: "",
    requestHeader: "",
    successRequestAlert: false,
    errorRequestAlert: false,
    requiredRule: v => !!v || 'This field is required',
    numberRule: v  => {
      if (!isNaN(parseFloat(v)) && v <= 100) return true;
      return 'this field must be less than 100';
    },
  }),
  created() {
    this.$store.dispatch('api/person/loadMany', {sortBy: "name", perPage: personNumber}).then((res) => {
      this.people = res.data.results
    })
    this.$store.dispatch('api/title/loadMany', {type: "S", sortBy: "title", perPage: titlesNumber}).then((res) => {
      this.series = res.data.results
    })
  },
  methods: {
    validate (ref) {
      return ref.validate()
    },
    addNewCharacterForm() {
      this.characters.push({name: "", person: undefined})
    },
    getPersonName(person) {
      return `${person.name} ${person.surname}`;
    },
    sendEpisodeRequest() {
      let filteredCharacters = this.characters.filter((char) => char.name && char.person)
      if (this.validate(this.$refs.form)) {
        this.$store.dispatch('api/episodeRequest/create', {
          action: 'A',
          header: this.requestHeader,
          description: this.requestComment,
          episode_submission:  {
            name: this.chosenName,
            released: this.chosenReleased,
            season: this.chosenSeason,
            number: this.chosenNumber,
            title: this.chosenSeries,
            characters: filteredCharacters
          }
        }).then(() => {
          this.successRequestAlert = true;
          setTimeout(()=> {
            this.successRequestAlert = false
          }, 2000)
        }, () => {
          this.errorRequestAlert = true;
          setTimeout(()=> {
            this.errorRequestAlert = false
          }, 2000)
        })
        this.successRequestAlert = false;
        this.errorRequestAlert = false;
      }
    }
  }
}
</script>

<style scoped>
.medium-font {
  font-size: 30px;
}
</style>