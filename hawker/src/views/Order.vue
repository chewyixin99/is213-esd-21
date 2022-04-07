<template>   
  <div class="w-96 mx-auto mt-3 px-3 ">
    <!-- Title -->
    <div class="text-left mb-2">
      <h1 class="font-medium text-3xl">My Orders</h1>
    </div>

    <!-- Order List -->
    <div v-for="order in orders" :key="order">
      <!-- order details -->
      <div class="flex justify-content-between py-3">

        <div class="text-left">
          <span class="font-semibold">{{order.hawker_id}}</span><br>
          <span class="badge bg-warning text-dark">Status: {{order.status}}</span><br>
          <span>{{order.time}}</span>
        </div>

        <div>
          <span class="text-sm">${{order.total_price}}</span><br>
          <span class="text-sm">-${{order.discount}}</span><br>
          <span class="text-lg font-semibold">${{order.final_price}}</span>
        </div>

      </div>

      <hr>
    </div>

  </div>
</template>

<script>
// @ is an alias to /src
import axios from 'axios';
import { globalState } from '../store'

const get_Order_URL = "http://localhost:5004/order" || "http://localhost:8000/order";

export default {
  name: 'order',
  components: {
  },

  data(){
    return {
      globalState,
      orders: [],
    }
  },

  created: function(){
    console.log("=== open created ===")
    this.getOrders()


  },

  methods:{
    getOrders(){
      console.log("=== open getOrders ===")
      axios
      .get(get_Order_URL + "/user/" + globalState.user_id)
      .then(response => {
        console.log(response.data.data.orders)
        this.orders = response.data.data.orders
      })
      .catch(error => {
        console.log(error)
      })
    },
    // testing for order time out
    // processTimeout(){
    //   for (order in this.orders){
    //     let datetime = order.time
    //     let split_time = datetime.split(" ")[4]
    //     let seconds = split_time[0]*60*60+split_time[1]*60+split_time[2]

    //   }
    // }

  }

}
</script>