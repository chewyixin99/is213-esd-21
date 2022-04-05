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

    {{order}}

  </div>
</template>

<script>
// @ is an alias to /src
import axios from 'axios';
import CartItem from '@/components/Cart-item-comp.vue'
import Wallet from '@/components/Wallet-comp.vue'

const get_Order_URL = "http://localhost:5004/order/user/1000";

export default {
  name: 'Cart',
  components: {
    CartItem,
    Wallet
  },
  data(){
    return {
      orders: [],
    }
  },

  created: function(){
    console.log("=== created ===")
    this.getOrders()
  },

  methods: {
    getOrders(){
      console.log("=== Open getOrders ===")
      axios
      .get(get_Order_URL)
      .then(response => {
        console.log(response.data.data.orders)
        // this.orders = response.data.data.hawkers
      })
      .catch(error => {
        console.log("=== error getOrders ===")
        console.log(error.message)
      })
    }
  }

}
</script>


<style scoped>

</style>