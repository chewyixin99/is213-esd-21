<template>
  <div>
    <!-- Welcome Message and Wallet -->
    <div class="grid grid-cols-5">
      <div class="col-span-3 text-left p-3 my-auto">
        <h1 class="font-medium text-3xl">My Order</h1>
      </div>
      <div class="col-span-2 p-3">
        <Wallet/>
      </div>
    </div>

    <div class="mt-3">
      <CartItem/>
      <CartItem/>
      <CartItem/>
    </div>

    <div class="mt-3 text-left px-3 flex justify-content-between">
      <span class="font-semibold">Total Amount Payable</span>
      <span class="text-xl">$30.00</span>
    </div>

    <div class="mt-3 md:text-right px-3">
      <button type="button" class="btn btn-warning w-full md:w-48">Pay</button>
    </div>

  </div>
</template>

<script>
// @ is an alias to /src
import CartItem from '@/components/Cart-item-comp.vue'
import Wallet from '@/components/Wallet-comp.vue'


export default {
  name: 'Cart',
  components: {
    CartItem,
    Wallet
  }
}
</script>


<style scoped>

</style>