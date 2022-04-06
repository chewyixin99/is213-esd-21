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

    <div v-for="(item, index) in globalState.selected_items" :key="item.item_id" class="mt-3">
      <CartItem :item_data_prop="item" @remove_item="removeItem(index)"/>
    </div>

    <div class="mt-3 text-left px-3 flex justify-content-between">
      <span class="font-semibold">Total Amount Payable</span>
      <span class="text-xl">${{totalAmount}}</span>
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
import { globalState, stateSetters } from '../store'

export default {
  name: 'Cart',
  components: {
    CartItem,
    Wallet
  },

  data() {
    return {
      globalState,
      stateSetters,
      totalAmount: 0.00,
    }
  },

  created() {
    this.getTotalAmount()
  },

  methods: {
    removeItem(index) {
      console.log("==== removeing item ====")
      stateSetters.removeSelectedItem(index)
      this.getTotalAmount()
    },

    getTotalAmount() {
      this.totalAmount = 0
      globalState.selected_items.map((item) => (
        this.totalAmount += item.price
      ))
      this.totalAmount = Number.parseFloat(this.totalAmount).toFixed(2)
    }
  }

}
</script>


<style scoped>

</style>