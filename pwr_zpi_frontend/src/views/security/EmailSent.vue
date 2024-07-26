<template>
  <v-container class="center-screen">
    <v-row align="center" justify="center">
      <v-col md="10">
        <h1 class="mb-4">We've sent you a verification mail!</h1>
        <p class="mb-6">Go to your inbox and click on the link you've received<br>
        to confirm your account</p>
        <i class="fas fa-envelope-open-text fa-10x"></i>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "EmailSent.vue"
}
</script>

<style scoped>
.center-screen {
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  min-height: 100vh;
}
</style>