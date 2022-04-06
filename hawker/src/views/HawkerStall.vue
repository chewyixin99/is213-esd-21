<template>
  <div>
    <!-- Welcome Message and Wallet -->
    <div class="bg-warning text-gray text-lg font-medium py-3">
      <i>Hawker Stall</i>
      <p class="text-3xl">{{ hawker_name }}</p>
    </div>

    <div v-if="items === null" class="mt-3">
      <p>No items.</p>
    </div>
    <div v-else class="mt-3">
      <Item v-for="item in items" :key="item.item_id" :item_data_prop="item"/>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from "axios";
import Item from "@/components/Item-comp.vue";

export default {
  name: "HawkerStall",
  components: {
    Item,
  },

  data() {
    return {
      hawker_id: null,
      hawker_name: null,
      items: null,
    };
  },

  created: function () {
    this.hawker_id = this.$route.query.hawker_id;
    this.hawker_name = this.$route.query.hawker_name;

    // console.log(`=== getting ${this.hawker_id}'s items ===`);
    const get_Item_URL = `http://localhost:8000/item/hawker/${this.hawker_id}`;

    axios
      .get(get_Item_URL)
      .then((response) => {
        // console.log(response.data.data.items);
        this.items = response.data.data.items;
      })
      .catch((error) => {
        console.log(`=== ERROR getting ${this.hawker_id}'s items ===`);
        console.log(error.message);
      });
  },
};
</script>


<style scoped>
</style>