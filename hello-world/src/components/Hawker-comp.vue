<template>
  <div class="text-left">
    <div class="grid grid-cols-3 md:grid-cols-4">
      <!-- Hawker Image -->
      <div class="col-span-1 p-3">
        <div class="shadow">
          <img src="../assets/hawkerimg.jpg" class="img-thumbnail">
        </div>
      </div>
      <!-- Hawker Detail -->
      <div class="p-3 col-span-2 md:col-span-3">
        <span>Hawker Name</span>
        <br>
        <span>Operating Hours: 8am - 9pm</span>
      </div>
    </div>
    <hr>
  </div>
</template>

<script>
export default {
  name: 'Hawker',
}
</script>