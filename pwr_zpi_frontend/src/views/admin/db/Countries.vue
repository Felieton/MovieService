<template>
  <v-container class="my-4">
    <v-row class="justify-center">
      <v-col class="col-12 col-sm-10 col-xl-6">
        <DataManager
            :item-actions="itemActions"
            item-name="country"
            item-name-plural="countries"
            :extra-headers="extraHeaders"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import DataManager from "@/components/admin/db/DataManager";

export default {
  name: "Countries",
  components: {
    DataManager,
  },
  data () {
    return {
      itemActions: {
        loadMany: 'api/country/loadMany',
        remove: 'api/country/remove',
        update: 'api/country/update',
        create: 'api/country/create'
      },
      extraHeaders: [
        {
          text: 'Name',
          value: 'name',
          required: true,
          counter: 32,
          rules: [
            (v => !!v || 'Name is required'),
            (v => v?.length <= 32 || 'Name is too long')
          ]
        },
        {
          text: 'Short name',
          value: 'short_name',
          required: true,
          counter: 8,
          rules: [
            (v => !!v || 'Short name is required'),
            (v => v?.length <= 8 || 'Short name is too long')
          ]
        },
      ],
    }
  },
}
</script>

<style scoped>

</style>