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
      <div class="p-2 col-span-2 md:col-span-3 grid grid-cols-3">
        <span class="col-span-2">{{item_data.name}}</span>
        <div class="text-center">
          <span class="col-span-1 font-semibold">Price</span>
          <br>
          <button type="button" class="btn btn-primary" @click="addToCart">+</button>
        </div>
      </div>
    </div>
    <hr>
  </div>
</template>

<script>
import { stateSetters } from '../store'

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