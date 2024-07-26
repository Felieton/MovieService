<template>
  <v-container class="my-4">
    <v-row class="justify-center">
      <v-col class="col-12 col-sm-10 col-xl-6">
        <DataManager
            :item-actions="itemActions"
            item-name="genre"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import DataManager from "@/components/admin/db/DataManager";

export default {
  name: "Genres",
  components: {
    DataManager,
  },
  data () {
    return {
      itemActions: {
        loadMany: 'api/genre/loadMany',
        remove: 'api/genre/remove',
        update: 'api/genre/update',
        create: 'api/genre/create'
      },
    }
  },
}
</script>

<style scoped>

</style>