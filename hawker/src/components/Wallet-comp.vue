<template>
  <div class="text-center">
    <span class="font-medium font-sm">Your Wallet</span>

      <!-- Amount -->
      <router-link to="/topup">
        <div class="w-28 mx-auto mt-2 p-2 border border-warning border-2 rounded bg-white opacity-80">
          <span class="text-dark">$1.00</span>
        </div>
      </router-link>
  </div>
</template>

<script>
export default {
  name: 'Wallet',
}
</script>