<template>
  <v-container class="center-screen">
    <v-row align="center" justify="center">
      <v-col md="9">
        <v-card class="elevation-16">
          <v-window v-model="screen">
            <v-window-item :value="1">
              <v-row>
                <v-col md="6">
                  <v-card-text class="mt-10">
                    <h3 class="text-center">Login into your account</h3>
                    <h6 class="description-text">Login into your account to explore all the possibilities
                      <br>of our great service!
                    </h6>
                    <v-row justify="center">
                      <v-col md="8">
                        <v-form ref="loginForm" v-model="loginValid">
                          <v-text-field label="Username" v-model="loginUsername" dense required
                                        :rules="loginUsernameRules" class="mt-10"></v-text-field>
                          <v-text-field label="Password" v-model="loginPassword" dense required
                                        :rules="loginPasswordRules" type="password" class="mt-4"></v-text-field>
                          <p class="bad-credentials" v-if="loginBadCredentials">Incorrect username or password.</p>
                          <v-btn class="mt-8 submit-btn" block @click="login()">Login</v-btn>
                        </v-form>
                        <h5 class="use-socials-text">Or log in using</h5>
                        <div class="social-buttons">
                          <v-btn depressed outlined color="grey" class="mr-2"
                                 @click="authWithProvider('google')">
                            <v-icon color="red">fab fa-google</v-icon>
                          </v-btn>
                          <v-btn depressed outlined color="grey" class="ml-2"
                                 @click="authWithProvider('facebook')">
                            <v-icon color="blue">fab fa-facebook-f</v-icon>
                          </v-btn>
                        </div>
                      </v-col>
                    </v-row>
                  </v-card-text>
                </v-col>
                <v-col md="6" class="rounded-pane-color rounded-right">
                  <v-btn icon class="exit-button" to="/">
                    <v-icon color="white">fas fa-times</v-icon>
                  </v-btn>
                  <div class="rounded-pane-text text-center">
                    <v-card-text class="white--text">
                      <h3>Don't have an Account yet?</h3>
                      <h6 class="mt-2">
                        Click the button and start the ultra-quick account
                        <br>creation process!
                      </h6>
                      <div class="mt-4">
                        <v-btn outlined dark @click="screen++">SIGN UP</v-btn>
                      </div>
                    </v-card-text>
                  </div>
                </v-col>
              </v-row>
            </v-window-item>
            <v-window-item :value="2">
              <v-row>
                <v-col class="rounded-pane-color rounded-left">
                  <div class="rounded-pane-text text-center">
                    <v-card-text class="white--text">
                      <h3>Already Signed up?</h3>
                      <h6 class="mt-2">Login into your account to explore all the possibilities
                        <br>of our great service!
                      </h6>
                    </v-card-text>
                    <div class="text-center">
                      <v-btn outlined dark @click="screen--">Log in</v-btn>
                    </div>
                  </div>
                </v-col>
                <v-col>
                  <v-btn icon class="exit-button close-signup-btn" to="/">
                    <v-icon>fas fa-times</v-icon>
                  </v-btn>
                  <v-card-text class="mt-6">
                    <h3 class="text-center">Sign up</h3>
                    <h6 class="description-text">
                      Click the button and start the ultra-quick account
                      <br>creation process!
                    </h6>
                    <v-row align="center" justify="center">
                      <v-col md="8">
                        <v-form ref="registerForm" v-model="registerValid">
                          <v-text-field label="Username" v-model="registerUsername" dense class="mt-6" required
                                        :rules="registerUsernameRules"></v-text-field>
                          <v-text-field label="Email" v-model="registerEmail" dense class="mt-4" required
                                        :rules="emailRules"></v-text-field>
                          <v-text-field label="Password" v-model="registerPassword" dense type="password" class="mt-4"
                                        required :rules="registerPasswordRules"></v-text-field>
                          <ul class="bad-credentials no-bull" v-if="registerBadCredentials">
                            <li v-for="item in this.registerErrorMessages" :key="item.message">
                              {{ item.message }}
                            </li>
                          </ul>
                          <v-btn class="mt-8 submit-btn" block @click="register()">Sign up</v-btn>
                        </v-form>
                        <h5 class="use-socials-text">Or sign up using</h5>
                        <div class="social-buttons">
                          <v-btn depreseed outlined color="grey" class="mr-2"
                                 @click="authWithProvider('google')">
                            <v-icon color="red">fab fa-google</v-icon>
                          </v-btn>
                          <v-btn depreseed outlined color="grey" class="ml-2"
                                 @click="authWithProvider('facebook')">
                            <v-icon color="blue">fab fa-facebook-f</v-icon>
                          </v-btn>
                        </div>
                      </v-col>
                    </v-row>
                  </v-card-text>
                </v-col>
              </v-row>
            </v-window-item>
          </v-window>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data: () => ({
        screen: 1,
        loginUsername: '',
        loginPassword: '',
        registerUsername: '',
        registerEmail: '',
        registerPassword: '',
        loginValid: true,
        registerValid: true,
        loginBadCredentials: false,
        registerBadCredentials: false,
        registerErrorMessages: [],
        loginUsernameRules: [
          v => !!v || 'Username is required',
        ],
        loginPasswordRules: [
          v => !!v || 'Password is required',
        ],
        registerUsernameRules: [
          v => !!v || 'Name is required',
          v => (v && v.length <= 16) || 'Username must be less than 16 characters',
        ],
        registerPasswordRules: [
          v => !!v || 'Password is required',
          v => (v && v.length >= 8) || 'Password must be at least 8 characters',
        ],
        emailRules: [
          v => !!v || 'Email is required',
          v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
        ]
      }
  ),
  props: {
    source: String
  },
  methods: {
    login: function () {
      if (this.validate(this.$refs.loginForm)) {
        this.$store.dispatch('login', {
          user: { username: this.loginUsername, password: this.loginPassword },
        }).then(this.loginSuccessful,
            () => { this.reset(this.$refs.loginForm)
              this.loginBadCredentials = true; })
      }
      else this.loginBadCredentials = false;
    },
    authWithProvider: function (provider) {
      this.$store.dispatch('authWithProvider', provider).then(this.loginSuccessful)
    },
    loginSuccessful: function() {
      this.$router.push('/')
    },
    register: function () {
      if (this.validate(this.$refs.registerForm)) {
        this.$store.dispatch('register', {
          user: { email: this.registerEmail, password1: this.registerPassword,
            password2: this.registerPassword, username: this.registerUsername },
        }).then(() => this.$router.push('/email-sent'), (err) => {
          this.registerErrorMessages = [];
          this.getRegisterErrorMessage(err.response.data)
          this.registerBadCredentials = true;
        })
      }
      else this.registerBadCredentials = false;
    },
    getRegisterErrorMessage: function(errorData) {
      if(errorData.email != null) {
        for (let i in errorData.email) {
          this.registerErrorMessages.push({ message: errorData.email[i] });
        }
      }
      if(errorData.username != null) {
        for (let i in errorData.username) {
          this.registerErrorMessages.push({ message: errorData.username[i] });
        }
      }
      if(errorData.password1 != null) {
        for (let i in errorData.password1) {
          this.registerErrorMessages.push({ message: errorData.password1[i] });
        }
      }
      if(errorData.non_field_errors != null) {
        for (let i in errorData.non_field_errors) {
          this.registerErrorMessages.push({ message: errorData.non_field_errors[i] });
        }
      }
    },
    validate (ref) {
      return ref.validate()
    },
    reset (ref) {
      ref.reset()
    },
  },
}
</script>

<style scoped lang="scss">
.center-screen {
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  min-height: 85vh;
}

.exit-button {
  float: right;
}

.description-text {
  text-align: center;
  color: grey;
  margin-top: 8px;
}

.use-socials-text{
  text-align: center;
  color: grey;
  margin: 20px 0;
}

.social-buttons {
  margin-bottom: 32px;
}

.rounded-pane-text {
  text-align: center;
  padding: 180px 0;
}

.rounded-right {
  border-bottom-left-radius: 250px;
}

.rounded-left {
  border-bottom-right-radius: 250px;
}

.bad-credentials {
  margin-top: 16px;
  font-family: "Roboto", sans-serif;
  color: var(--v-error-base);
}

.no-bull {
  text-align: left;
}

.theme--light {
  .rounded-pane-color {
    background-color: var(--v-primary-base);
  }
  .v-btn.submit-btn {
    background-color: var(--v-primary-base) !important;
    color: #fff;
  }
  .v-btn.close-signup-btn i {
    color: var(--v-primary-base);
  }
}

.theme--dark {
  .rounded-pane-color {
    background-color: var(--v-accent-base);
  }
  .v-btn.submit-btn {
    background-color: var(--v-accent-base) !important;
    color: #fff;
  }
  .v-btn.close-signup-btn i {
    color: var(--v-accent-base);
  }
}
</style>