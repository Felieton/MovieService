<template>
  <div>
    <v-container class="mt-16 mb-16">
      <v-row justify="center">
        <v-col>
          <div>
            <v-row class="mt-5" justify="center">
              <v-col class="justify-center d-flex align-center">
                <v-icon class="mr-4" color="red" large>fas fa-pen</v-icon>
                <h1 class="mb-4 mt-4">{{ "Add a new person" }}</h1>
              </v-col>
            </v-row>
            <v-form ref="form" v-model="formValid">
              <v-row justify="center">
                  <v-col class="d-flex" cols="10" sm="5">
                    <v-text-field v-model="chosenName" :rules="[requiredRule]" class="mr-16" label="First name*">First name</v-text-field>
                  </v-col>
              </v-row>
              <v-row justify="center">
                  <v-col class="d-flex" cols="10" sm="5">
                    <v-text-field v-model="chosenSurname" :rules="[requiredRule]" class="mr-16" label="Surname*">Surname</v-text-field>
                  </v-col>
              </v-row>
              <v-row justify="center">
                <v-col cols="6">
                  <div class="justify-center d-flex align-center">
                    <v-textarea label="Description*" v-model="personDescription" :rules="[requiredRule]" counter maxlength="255"></v-textarea>
                  </div>
                </v-col>
              </v-row>
              <v-row justify="center">
                <v-col cols="2">
                  <div class="justify-center d-flex align-center">
                    <v-select v-model="chosenCountry" :items="countries" item-text="name" item-value="id" label="Country" solo></v-select>
                  </div>
                </v-col>
              </v-row>
              <v-row justify="center">
                <v-col cols="10" sm="5">
                  <v-menu v-model="menu2" :close-on-content-click="false" transition="scale-transition"
                          offset-y max-width="290px" min-width="auto">
                    <template v-slot:activator="{ on, attrs }">
                      <v-text-field label="Birthdate" hint="DD/MM/YYYY format" persistent-hint prepend-icon="mdi-calendar"
                                    readonly v-model="chosenBirthdate" v-bind="attrs" v-on="on"></v-text-field>
                    </template>
                    <v-date-picker v-model="chosenBirthdate" no-title @input="menu2 = false"></v-date-picker>
                  </v-menu>
                </v-col>
              </v-row>
              <div>
                <v-row justify="center">
                  <v-col cols="3">
                    <div class="justify-center d-flex align-center">
                      <v-text-field class="mt-10" v-model="requestHeader" :rules="[requiredRule]" label="Request title*"></v-text-field>
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
                  <v-btn @click="sendPersonRequest()">
                    <div class="mr-4">Request adding person</div>
                    <v-icon color="red">fas fa-paper-plane</v-icon>
                  </v-btn>
                </v-row>
              </div>
            </v-form>
            <v-snackbar bottem right v-model="snackbar" :timeout="3000">
              {{ snackbarText }}
              <template v-slot:action="{ attrs }">
                <v-btn color="blue" text v-bind="attrs" @click="snackbar = false">
                  Close
                </v-btn>
              </template>
            </v-snackbar>
          </div>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>


<script>
const countriesNumber = 30
export default {
  name: "AddPerson",
  data: () => ({
    menu2: false,
    countries: [],
    chosenName: "",
    chosenSurname: "",
    chosenCountry: null,
    chosenBirthdate: null,
    personDescription: '',
    formValid: true,
    requestComment: "",
    requestHeader: "",
    snackbarText: "",
    snackbar: false,
    successRequestAlert: false,
    errorRequestAlert: false,
    requiredRule: v => !!v || 'This field is required'
  }),
  created() {
    this.$store.dispatch('api/country/loadMany', {perPage: countriesNumber}).then((res) => {
      this.countries = res.data.results
    })
  },
  methods: {
    validate (ref) {
      return ref.validate()
    },
    sendPersonRequest() {
      if (this.validate(this.$refs.form)) {
        this.$store.dispatch('api/personRequest/create', {
          action: 'A',
          header: this.requestHeader,
          description: this.requestComment,
          person_submission:  {
            name: this.chosenName,
            surname: this.chosenSurname,
            birthdate: this.chosenBirthdate,
            country: this.chosenCountry,
            description: this.personDescription
          }
        }).then(() => {
          this.snackbarText = "Request has been submitted";
          this.snackbar = true;
        }, () => {
          this.snackbarText = "An error occurred while submitting request";
          this.snackbar = true;
        })
      }
    }
  }
}
</script>

<style scoped>
</style>