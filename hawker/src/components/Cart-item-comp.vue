<template>
  <div class="text-left">
    <div class="grid grid-cols-3 md:grid-cols-4 my-3">
      <!-- Item Image -->
      <div class="col-span-2 md:col-span-3 p-3">
        <span class="col-span-2">Item Name</span>
      </div>
      <!-- Item Detail -->
      <div class="p-3 col-span-1 text-center">
        <span class="font-semibold">Price</span>
        <br>
        <div class="space-x-2 mt-2">
          <button type="button" class="btn btn-danger w-10 rounded-full">-</button>
          <button type="button" class="btn btn-danger w-10 rounded-full">+</button>
        </div>
      </div>
    </div>
    <hr>
  </div>
</template>

<script>
export default {
  name: 'CartItem',
}
</script>