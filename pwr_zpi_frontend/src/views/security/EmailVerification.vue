<template>
  <v-container class="center-screen">
    <v-row align="center" justify="center">
      <v-col md="10">
        <div v-if="verified">
          <h1 class="mb-4">Your account has been successfully verified!</h1>
          <p class="mb-6">You can now log in to our service</p>
          <i class="fas fa-check fa-10x"></i>
          <v-row class="mt-16" align="center" justify="center">
            <v-col md="2">
              <v-btn dark block color="blue" to="/login">Login</v-btn>
            </v-col>
          </v-row>
        </div>
        <div v-if="!verified">
          <h1 class="mb-6">Something went wrong...</h1>
          <i class="fas fa-exclamation-triangle fa-10x"></i>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from "axios";
import storeCfg from '../../store/config'
export default {
  name: "EmailVerification.vue",
  data: () => ({
    verified: false
  }),
  created() {
    let data = {
      key: this.$route.params.key
    };
    axios.post(storeCfg.baseUrl + `o/registration/verify-email/`, data)
        .then(() => this.verified=true, () => this.verified=false)
  }
}
</script>

<style scoped>
.center-screen {
  display: flex;
  justify-content: center;
  text-align: center;
  align-items: center;
  height: 100%;
}
</style>
