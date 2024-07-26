<template>
  <v-container class="my-4">
    <v-row class="justify-center">
      <v-col class="col-12 col-sm-10 col-xl-6">
        <DataManager
            :item-actions="itemActions"
            item-name="site"
            item-name-plural="sites"
            :extra-headers="extraHeaders"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import DataManager from "@/components/admin/db/DataManager";

export default {
  name: "Sites",
  components: {
    DataManager,
  },
  data () {
    return {
      itemActions: {
        loadMany: 'api/scraperSite/loadMany',
        remove: 'api/scraperSite/remove',
        update: 'api/scraperSite/update',
        create: 'api/scraperSite/create'
      },
      extraHeaders: [
        {
          text: 'Netloc',
          value: 'netloc',
          required: true,
          counter: 255,
          rules: [
            (v => !!v || 'Netloc is required'),
            (v => v?.length <= 255 || 'Netloc is too long'),
            (v => v?.split('.').length >= 3 || 'Required format is www.example_domain.tld')
          ]
        },
        {
          text: 'Title',
          value: 'title',
          required: false,
          counter: 255,
          rules: [
            (v => v?.length <= 255 || 'Title is too long')
          ]
        },
        {
          text: 'Director',
          value: 'director',
          required: false,
          counter: 255,
          rules: [
            (v => v?.length <= 255 || 'Director is too long')
          ]
        },
        {
          text: 'Genres',
          value: 'genres',
          required: false,
          counter: 255,
          rules: [
            (v => v?.length <= 255 || 'Genres is too long')
          ]
        },
        {
          text: 'Countries',
          value: 'countries',
          required: false,
          counter: 255,
          rules: [
            (v => v?.length <= 255 || 'Countries is too long')
          ]
        },
        {
          text: 'Year',
          value: 'year',
          required: false,
          counter: 255,
          rules: [
            (v => v?.length <= 255 || 'Year is too long')
          ]
        },
        {
          text: 'Release Date',
          value: 'release_date',
          required: false,
          counter: 255,
          rules: [
            (v => v?.length <= 255 || 'Release date is too long')
          ]
        },
        {
          text: 'Duration',
          value: 'duration',
          required: false,
          counter: 255,
          rules: [
            (v => v?.length <= 255 || 'Duration is too long')
          ]
        },
        {
          text: 'Plot',
          value: 'plot',
          required: false,
          counter: 255,
          rules: [
            (v => v?.length <= 255 || 'Plot is too long')
          ]
        },
      ],
    }
  },
}
</script>

<style scoped>

</style>