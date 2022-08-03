<template>
  <div class="text-center">
    <span class="font-medium font-sm">Your Wallet</span>

      <!-- Amount -->
      <router-link to="/topup">
        <div class="w-28 mx-auto mt-2 p-2 border border-warning border-2 rounded bg-white opacity-80">
          <span class="text-dark text-xl font-medium">${{avail_balance}}</span><br/>
          <span class="text-dark text-xs">(${{total_balance}})</span>
        </div>
      </router-link>
  </div>
</template>

<script>
import axios from 'axios';
import { globalState, stateSetters } from '../store'

const get_Wallet_URL = "http://localhost:8000/wallet";

export default {
  name: 'Wallet',
  data(){
    return{
      globalState,
      stateSetters,
      user_id: null,
      avail_balance: 0,
      total_balance: 0,
    }
  },

  created: function(){
    console.log("=== open Created ===")
    this.user_id = this.globalState.user_id
    this.getAmt()
  },

  methods: {
    getAmt(){
      console.log("=== Open getAmt ===")
      axios
      .get(get_Wallet_URL + "/" + this.user_id)
      .then(response => {
        // console.log(response.data.data)
        this.avail_balance = Number.parseFloat(response.data.data['available_balance']).toFixed(2)
        this.total_balance = Number.parseFloat(response.data.data['total_balance']).toFixed(2)
        this.stateSetters.update_availBalance(this.avail_balance)
        this.stateSetters.update_totalBalance(this.total_balance)
        // console.log(this.total_balance)
      })
      .catch(error => {
        console.log(error)
      })
    }
  }
}
</script>