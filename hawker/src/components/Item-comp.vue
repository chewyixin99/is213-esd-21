<template>
  <div class="text-left">
    <div class="grid grid-cols-3 md:grid-cols-4 my-3">
      <!-- Item Image -->
      <div class="col-span-1 p-2">
        <div class="shadow">
          <img src="../assets/hawkerimg.jpg" class="img-thumbnail">
        </div>
      </div>
      <!-- Item Detail -->
      <div class="col-span-2 md:col-span-3 flex justify-content-between px-3">
        <div class="my-auto">
          <span class="col-span-2 font-semibold">{{item_data.name}}</span><br>
          <span class="col-span-1">${{item_data.price}}</span>
        </div>
        <div class="my-auto">
          <button type="button" class="btn btn-primary" :disabled="globalState.user_id === null" @click="addToCart">Add</button>
        </div>
      </div>
    </div>
    <hr>
  </div>
</template>

<script>
import { globalState, stateSetters } from '../store'

export default {
  name: 'Item',
  props : {
    'item_data_prop': Object
  }, 
  // receives:
  // item_data - object of item's data

  data() {
    return {
      item_data: null,
      globalState,
      stateSetters,
    }
  },

  created() {
    this.item_data = this.item_data_prop
    // console.log(this.item_data)
  },

  methods: {
    addToCart() {
      console.log("=== Adding item to cart ===")
      stateSetters.addSelectedItem(this.item_data)
    }
  }
}
</script>