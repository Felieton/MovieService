<template>
  <div>
    <v-container class="mt-16 mb-16">
      <v-row justify="center">
        <v-col>
          <div>
            <v-row class="mt-5" justify="center">
              <v-col class="justify-center d-flex align-center">
                <v-icon class="mr-4" color="red" large>fas fa-pen</v-icon>
                <h1 class="mb-4 mt-4">{{ "Add a new title" }}</h1>
              </v-col>
            </v-row>
            <v-form ref="form" v-model="formValid">
              <v-row justify="center">
                <div class="justify-center d-flex align-center">
                  <v-col class="d-flex" cols="10" sm="5">
                    <v-text-field v-model="chosenTitle" :rules="[requiredRule]" class="mr-16" label="Title...">Title</v-text-field>
                  </v-col>
                  <v-col class="d-flex" cols="10" sm="5">
                    <v-select v-model="chosenType" :rules="[requiredRule]" :items="['Movie', 'Series']" label="Type..." solo></v-select>
                  </v-col>
                </div>
              </v-row>
              <v-row justify="center">
                <div class="justify-center d-flex align-center">
                  <v-text-field v-model="chosenYear" :rules="[requiredRule, numberRule, yearRule]" class="mr-16" label="Year: YYYY">Title</v-text-field>
                  <v-menu v-model="menu2" :close-on-content-click="false" transition="scale-transition"
                          offset-y max-width="290px" min-width="auto">
                    <template v-slot:activator="{ on, attrs }">
                      <v-text-field label="Release date" hint="DD/MM/YYYY format" persistent-hint prepend-icon="mdi-calendar"
                          readonly v-model="chosenReleased" v-bind="attrs" v-on="on"></v-text-field>
                    </template>
                    <v-date-picker v-model="chosenReleased" no-title @input="menu2 = false"></v-date-picker>
                  </v-menu>
                </div>
              </v-row>
              <v-row justify="center">
                <v-col cols="6">
                  <div class="justify-center d-flex align-center">
                    <v-textarea label="Plot..." v-model="plot" counter maxlength="255"></v-textarea>
                  </div>
                </v-col>
              </v-row>
              <v-row justify="center">
                <div class="justify-center d-flex align-center mt-8">
                  <v-col>
                    <v-select v-model="chosenGenres" :items="genres" item-text="name" item-value="id"
                              multiple label="Genres" solo></v-select>
                    <v-select v-model="chosenCountries" :items="countries" multiple item-text="name"
                              item-value="id" label="Countries" solo></v-select>
                    <v-select v-model="chosenLanguages" :items="languages" multiple item-text="name"
                              item-value="id" label="Languages" solo></v-select>
                  </v-col>
                </div>
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
                <v-row class="mt-10" justify="center">
                  <div class="medium-font">Cast members</div>
                </v-row>
                <v-row justify="center" v-for="(castMember, index) in castMembers" :key="index">
                  <div class="justify-center d-flex align-center">
                    <v-col class="d-flex" cols="10" sm="6">
                      <v-select v-model="castMember.person" :items="people" :item-text="getPersonName"
                                item-value="id" label="Person" solo></v-select>
                    </v-col>
                    <v-col class="d-flex" cols="10" sm="6">
                      <v-select v-model="castMember.roles" multiple :items="castRoles" item-text="name"
                                item-value="id" label="Role" solo></v-select>
                    </v-col>
                  </div>
                </v-row>
                <v-row justify="center">
                  <v-btn @click="addNewCastMember()" icon>
                    <v-icon color="red">fas fa-plus</v-icon>
                  </v-btn>
                </v-row>
                <v-row justify="center">
                  <v-col cols="3">
                    <div class="justify-center d-flex align-center">
                      <v-text-field class="mt-10" :rules="[requiredRule]" v-model="requestHeader" label="Request title"></v-text-field>
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
                  <v-btn @click="sendTitleRequest()">
                    <div class="mr-4">Request adding title</div>
                    <v-icon color="red">fas fa-paper-plane</v-icon>
                  </v-btn>
                </v-row>
              </div>
            </v-form>
          </div>
        </v-col>
      </v-row>
    </v-container>
    <div class="justify-center">
      <form>
        <v-card width="50%" class="justify-center mb-16">
          <v-card-text >
            <v-text-field label="Search By" v-model="searchBy"></v-text-field>
            <v-select
                :items="modes"
                item-text="state"
                item-value="value"
                label="Mode"
                persistent-hint
                return-object
                single-line
                v-model="selectedMode"
            ></v-select>
            <v-select
                :items="sites"
                item-text="state"
                item-value="value"
                label="Site"
                persistent-hint
                return-object
                single-line
                v-model="selectedSite"
            ></v-select>
            <v-btn  width="20%" @click="scrapeFilm()">Fill data</v-btn>
          </v-card-text>
        </v-card>
      </form>
      <v-alert :value="successAlert" type="success">Successfully retrieved data</v-alert>
      <v-alert :value="errorAlert" type="error">An error occurred while retrieving data</v-alert>
      <v-alert :value="loadingAlert" type="info">Retrieving data...</v-alert>
      <v-alert :value="successRequestAlert" type="success" dismissible>Request has been submitted</v-alert>
      <v-alert :value="errorRequestAlert" type="error" dismissible>An error occurred while submitting request</v-alert>
      <v-alert :value="loadingRequestAlert" type="info">Sending request...</v-alert>
    </div>
  </div>
</template>


<script>
const genresNumber = 30
const countriesNumber = 30
const languageNumber = 30
const castRolesNumber = 30
const personNumber = 999

export default {
  name: "AddTitle",
  data: () => ({
    menu2: false,
    chosenTitle: null,
    chosenType: null,
    chosenYear: null,
    chosenReleased: null,
    chosenGenres: [],
    chosenCountries: [],
    chosenLanguages: [],
    characters: [{name: "", person: null}],
    castMembers: [{person: null, roles: []}],
    castRoles: [],
    genres: [],
    people: [],
    countries: [],
    languages: [],
    plot: "",
    formValid: true,
    requestComment: "",
    requestHeader: "",
    activePicker: null,
    searchBy: '',
    modes: [{value:'title' ,state: 'Title'}, {value: 'url', state: 'Url'}],
    selectedMode: null,
    sites: [{value:'filmweb', state: 'Filmweb'}, {value: 'imdb', state: 'Imdb'}, {value: 'other', state: 'Other'}],
    selectedSite: null,
    successAlert: false,
    errorAlert: false,
    loadingAlert: false,
    successRequestAlert: false,
    errorRequestAlert: false,
    loadingRequestAlert: false,
    numberRule: v  => {
      if (!isNaN(parseFloat(v)) && v >= 1800) return true;
      return 'Year has to be larger than 1800';
    },
    yearRule: v => (v && v.length === 4) || 'Year must be of 4 digits',
    requiredRule: v => !!v || 'This field is required',
  }),
  created() {
    this.$store.dispatch('api/genre/loadMany', {perPage: genresNumber}).then((res) => {
      this.genres = res.data.results
    })
    this.$store.dispatch('api/country/loadMany', {perPage: countriesNumber}).then((res) => {
      this.countries = res.data.results
    })
    this.$store.dispatch('api/lang/loadMany', {perPage: languageNumber}).then((res) => {
      this.languages = res.data.results
    })
    this.$store.dispatch('api/person/loadMany', {sortBy: "name", perPage: personNumber}).then((res) => {
      this.people = res.data.results
    })
    this.$store.dispatch('api/castRole/loadMany', {perPage: castRolesNumber}).then((res) => {
      this.castRoles = res.data.results
    })
  },
  methods: {
    addNewCharacter(char) {
      this.characters.push({name: char.name, person: char.person})
    },
    addNewCharacterForm() {
      this.characters.push({name: "", person: undefined})
    },
    addNewCastMember() {
      this.castMembers.push({person: undefined, roles: []})
    },
    getPersonName(person) {
      return `${person.name} ${person.surname}`;
    },
    validate (ref) {
      return ref.validate()
    },
    getCorrectType() {
      if (this.chosenType === 'Movie')
        this.chosenType = 'M'
      if (this.chosenType === 'Series')
        this.chosenType = 'S'
    },
    scrapeFilm: function () {
      this.$store.dispatch('api/scraper/getFilmByUrl', {
        url: this.searchBy,
        site: this.selectedSite.value,
        mode: this.selectedMode.value}).then((r) => {
        console.log(r.data);
        this.chosenTitle = r.data.title;
        this.chosenYear = r.data.year;
        if (r.data.characters.length > 0)
        {
          this.characters = []
        }
        for(const char of r.data.characters) {
          this.addNewCharacter({name: char, person: undefined});
        }

        for(let i=0; i < this.characters.length; i++)
        {
          const result = this.people.filter(obj => {
            return obj.name + " " + obj.surname === r.data.actors[i];
          })
          if(result.length > 0) {
            this.characters[i].person = result[0].id;
          }
        }
        let newGenres = [];
        for(let i=0; i < r.data.genres.length; i++) {
          const filmGenre = r.data.genres[i].toUpperCase();
          const res = this.genres.filter((genre) => {
            return genre.name.toUpperCase() === filmGenre
          });
          if(res.length > 0)
            newGenres.push(res[0].id)
        }
        this.chosenGenres = newGenres;

        let newCountries = [];
        for(let i=0; i < r.data.countries.length; i++) {
          const filmCountry = r.data.countries[i].toUpperCase();
          const res = this.countries.filter((country) => {
            return country.name.toUpperCase() === filmCountry
          });
          if(res.length > 0)
            newGenres.push(res[0].id)
        }
        this.plot = r.data.plot
        this.chosenCountries = newCountries;
        console.log(this.chosenGenres);
        console.log(this.characters)
        setTimeout(()=> {
          this.successAlert = false
        }, 2000)
        this.successAlert = true;
        this.loadingAlert = false;
      }).catch(() => {
        setTimeout(()=> {
          this.errorAlert = false
        }, 2000)
        this.errorAlert = true;
        this.loadingAlert = false;
      })
      this.loadingAlert = true;
      this.successAlert = false;
      this.errorAlert = false;
    },
    sendTitleRequest() {
      this.getCorrectType()
      let filteredCharacters = this.characters.filter((char) => char.name && char.person)
      let filteredCastMembers = this.castMembers.filter((castMember) => castMember.name && castMember.person)
      if (this.validate(this.$refs.form)) {
        this.$store.dispatch('api/titleRequest/create', {
          action: 'A',
          header: this.requestHeader,
          description: this.requestComment,
          title_submission:  {
          title: this.chosenTitle,
              year: this.chosenYear,
              released: this.chosenReleased,
              type: this.chosenType,
              plot: this.plot,
              languages: this.chosenLanguages,
              countries: this.chosenCountries,
              genres: this.chosenGenres,
              characters: filteredCharacters,
              cast_members: filteredCastMembers
          }
        }).then(() => {
          this.successRequestAlert = true;
          setTimeout(()=> {
            this.successRequestAlert = false
          }, 2000)
          this.loadingRequestAlert = false;
        }, () => {
          this.errorRequestAlert = true;
          setTimeout(()=> {
            this.errorRequestAlert = false
          }, 2000)
          this.loadingRequestAlert = false;
        })
        this.loadingRequestAlert = true;
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
.v-text-field, .v-btn, .v-card{
  width: 400px;
  margin-left: auto;
  margin-right: auto;
}

.v-alert{
  width: 80%;
  margin-left: auto;
  margin-right: auto;
}
</style>