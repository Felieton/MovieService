<template>
  <v-container class="my-4">
    <v-row class="justify-center">
      <v-col class="col-12 col-sm-10 col-xl-6">
        <DataManager
            :item-actions="itemActions"
            item-name="cast role"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import DataManager from "@/components/admin/db/DataManager";

export default {
  name: "CastRoles",
  components: {
    DataManager,
  },
  data () {
    return {
      itemActions: {
        loadMany: 'api/castRole/loadMany',
        remove: 'api/castRole/remove',
        update: 'api/castRole/update',
        create: 'api/castRoles/create'
      },
    }
  },
}
</script>

<style scoped>

</style>