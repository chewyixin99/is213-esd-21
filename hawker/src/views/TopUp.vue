<template>
  <div>
    <div class="bg-warning p-3">
      <Wallet/>
    </div>
    
    <div class="w-96 mx-auto mt-3 px-3 ">
      <!-- Title -->
      <div class="text-left mb-2">
        <h1 class="font-medium text-3xl">Top Up Wallet</h1>
      </div>

      <form>
        <!-- Amount -->
        <div class="mb-3 flex justify-content-between">
          <label for="amount" class="form-label my-auto">Top Up Amount:</label>
          <div class="flex">
            <span class="my-auto mr-2">$</span>
            <input type="text" class="form-control w-24 text-center" id="amount" v-model="amount">
          </div>
        </div>

        <!-- Amount buttons -->
        <div class="mb-3 flex space-x-4">
          <button @click="getValue(10)" type="button" class="btn btn-warning w-full">$10</button>
          <button @click="getValue(20)" type="button" class="btn btn-warning w-full">$20</button>
          <button @click="getValue(50)" type="button" class="btn btn-warning w-full">$50</button>
        </div>

        <!-- CC Details -->
        <div class="mb-3 text-start">
          <label for="ccno" class="form-label">Credit Card Number</label>
          <input type="text" class="form-control" id="ccno" v-model="ccno" placeholder="0000 0000 0000 0000">
        </div>

        <div class="flex space-x-4">
          <div class="mb-3 text-start">
            <label for="expiry" class="form-label">Expiry</label>
            <input type="text" class="form-control" id="expiry" v-model="expiry" placeholder="05/22">
          </div>

          <div class="mb-5 text-start">
            <label for="cvv" class="form-label">CVV</label>
            <input type="text" class="form-control" id="cvv" v-model="cvv" placeholder="123">
          </div>
        </div>

      </form>

      <!-- Buttons -->
      <div class="text-end flex mx-auto space-x-4">
          <button @click="cancel" type="button" class="btn btn-outline-danger w-full">Cancel</button>
          <button @click="topup" type="button" class="btn btn-warning w-full">Top Up</button>
      </div>

    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from 'axios';
import Wallet from '@/components/Wallet-comp.vue'
import { globalState } from '../store'

const get_Wallet_URL = "http://localhost:8000/wallet";

export default {
  name: 'TopUp',
  components: {
    Wallet,
  },

  data(){
    return {
      globalState,
      amount: 0,
      ccno: "5678 4165 4124 7669",
      expiry: "05/22",
      cvv: "369",
      user_id: null, 
    }
  },

  created() {
    this.user_id = this.globalState.user_id
  },

  methods:{
    getValue(val){
      // console.log(val)
      this.amount = val
    },

    topup(){
      console.log("=== open topup ===")
      console.log(this.amount)

      axios
      .put(get_Wallet_URL + "/" + this.user_id, {
        amount_to_add_to_available_balance: parseFloat(this.amount),
        amount_to_add_to_total_balance: parseFloat(this.amount),
      })
      .catch(error => {
        console.log(error.response.data)
      })
      // .get(get_Wallet_URL + "/" + this.globalState.user_id)
      // .then(response => {
      //   console.log(response.data.data)
      // })
    },

    cancel() {
      this.$router.replace({name: "Hawker"})
    }
  }

}
</script>

