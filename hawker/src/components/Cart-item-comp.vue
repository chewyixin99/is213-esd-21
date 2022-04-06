<template>
  <div class="text-left">
    <div class="grid grid-cols-3 md:grid-cols-4 my-3">
      <!-- Item Image -->
      <div class="col-span-2 md:col-span-3 p-3">
        <span class="col-span-2">{{item_data.name}}</span>
      </div>
      <!-- Item Detail -->
      <div class="p-3 col-span-1 text-center">
        <span class="font-semibold">${{item_data.price}}</span>
        <br>
        <div class="space-x-2 mt-2">
          <button type="button" @click="$emit('remove_item')" class="btn btn-danger w-10 rounded-full">-</button>
          <!-- <button type="button" class="btn btn-danger w-10 rounded-full">+</button> -->
        </div>
      </div>
    </div>
    <hr>
  </div>
</template>

<script>
export default {
  name: 'CartItem',
  props : {
    'item_data_prop': Object
  }, 
  data() {
    return {
      item_data: null  
    }
  },

  created() {
    this.item_data = this.item_data_prop
    console.log(this.item_data)
  },

}
</script>