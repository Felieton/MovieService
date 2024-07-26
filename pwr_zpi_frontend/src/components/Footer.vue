<template>
  <v-footer app color="primary blue" bottom absolute padless>
    <v-row justify="center" no-gutters>
      <v-btn to="/privacy-policy" color="white" text rounded class="my-2">
        Privacy policy
      </v-btn>
      <v-btn to="/about-us" color="white" text rounded class="my-2">
        About Us
      </v-btn>
      <v-btn to="/contact" color="white" text rounded class="my-2">
        Contact
      </v-btn>
      <v-col class="primary blue py-4 text-center white--text" cols="12">
        © 2021 Movie Service | All rights reserved.
      </v-col>
    </v-row>
  </v-footer>
</template>

<script>
export default {
  name: 'Footer',
}
</script>

<style scoped>

</style>