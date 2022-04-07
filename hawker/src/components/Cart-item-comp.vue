<template>
  <div class="text-left">
    <div class="m-3 flex justify-content-between">
      <!-- Item Detail -->
      <div>
        <span class="font-semibold">{{item_data.name}}</span><br>
        <span>${{item_data.price}}</span>
      </div>
      <button type="button" @click="$emit('remove_item')" class="btn btn-danger">Remove</button>
      <!-- <button type="button" class="btn btn-danger w-10 rounded-full">+</button> -->
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
    // console.log(this.item_data)
  },

}
</script>