<template>
  <div class="text-left">
    <div class="grid grid-cols-3 md:grid-cols-4">
      <!-- Item Image -->
      <div class="col-span-1 p-3">
        <div class="shadow">
          <img src="../assets/hawkerimg.jpg" class="img-thumbnail">
        </div>
      </div>
      <!-- Item Detail -->
      <div class="p-3 col-span-2 md:col-span-3 grid grid-cols-3">
        <span class="col-span-2">Item Name</span>
        <div class="text-center">
          <span class="col-span-1 font-semibold">Price</span>
          <br>
          <button type="button" class="btn btn-primary">+</button>
        </div>
      </div>
    </div>
    <hr>
  </div>
</template>

<script>
export default {
  name: 'Item',
}
</script>