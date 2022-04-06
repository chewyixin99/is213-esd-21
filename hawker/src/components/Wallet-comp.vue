<template>
  <div class="text-center">
    <span class="font-medium font-sm">Your Wallet</span>

      <!-- Amount -->
      <router-link to="/topup">
        <div class="w-28 mx-auto mt-2 p-2 border border-warning border-2 rounded bg-white opacity-80">
          <span class="text-dark">${{total_balance}}</span>
        </div>
      </router-link>
  </div>
</template>

<script>
import axios from 'axios';
import { globalState } from '../store'

const get_Wallet_URL = "http://localhost:8000/wallet";

export default {
  name: 'Wallet',
  data(){
    return{
      avail_balance: 0,
      total_balance: 0,
      globalState
    }
  },

  created: function(){
    console.log("=== open Created ===")
    this.getAmt()
  },

  methods: {
    getAmt(){
      console.log("=== Open getAmt ===")
      axios
      .get(get_Wallet_URL + "/" + this.globalState.user_id)
      .then(response => {
        // console.log(response.data.data)
        this.avail_balance = response.data.data['available_balance']
        this.total_balance = response.data.data['total_balance']
        // console.log(this.total_balance)
      })
      .catch(error => {
        console.log(error)
      })
    }
  }
}
</script>