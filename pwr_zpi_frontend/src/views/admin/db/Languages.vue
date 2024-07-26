<template>
  <v-container class="my-4">
    <v-row class="justify-center">
      <v-col class="col-12 col-sm-10 col-xl-6">
        <DataManager
            :item-actions="itemActions"
            item-name="language"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import DataManager from "@/components/admin/db/DataManager";

export default {
  name: "Languages",
  components: {
    DataManager,
  },
  created() {
    // this.$store.dispatch("api/lang/create")
  },
  data () {
    return {
      itemActions: {
        loadMany: 'api/lang/loadMany',
        remove: 'api/lang/remove',
        update: 'api/lang/update',
        create: 'api/lang/create'
      },
    }
  },
}
</script>

<style scoped>

</style>