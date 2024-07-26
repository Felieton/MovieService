// import devtools from '@vue/devtools'
import Vue from 'vue'
import App from './App.vue'
import router from './router'
import axios from "axios";
import store from './store'
import vuetify from './plugins/vuetify'

Vue.config.productionTip = false

axios.interceptors.response.use( (response) => {
  console.log('intercepted: ', response)
  return response
}, (err) => {
  const response = err.response
  // no response received or request was not even made
  if (!response) return Promise.reject(err)

  console.log('intercepted err: ', response)

  if (response.status === 401 && response.data.code === 'token_not_valid') {
    console.log('Refreshing token...')
    return store.dispatch('refreshToken').then( () => {
      // resend request
      console.log('resending request...')
      return axios(err.config)
    })
  } // refresh user data including groups on access denied
  else if(response.status === 403) {
    const userData = { userId: store.getters.loggedUser.id}
    console.log('Refreshing user data...')
    return store.dispatch('initLoggedUserData', userData).then( () => {
      return Promise.reject(err)
    })
  }

  return Promise.reject(err)
})

new Vue({
  store,
  router,
  render: h => h(App),
  vuetify,

  computed: {
    isAuthenticated: function () {
      return this.$store.getters.isAuthenticated()
    }
  }
}).$mount('#app')

if (process.env.NODE_ENV === 'development') {
  // devtools.connect('http://localhost', '8098')
}
