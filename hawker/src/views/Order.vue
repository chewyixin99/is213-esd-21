<template>   
  <div class="w-96 mx-auto mt-3 px-3 ">
    <!-- Title -->
    <div class="text-left mb-2">
      <h1 class="font-medium text-3xl">My Orders</h1>
    </div>
    
    <!-- Order List -->
    <div v-if="processedOrder.length === 0">
      <div class="flex justify-content-between py-3">
        <p>You don't have any orders at the moment. Visit any hawker to start ordering!</p>
      </div>
    </div>

    <div v-else v-for="order in processedOrder.slice().reverse()" :key="order">
      <!-- order details -->
      <div class="flex justify-content-between py-3">

        <div class="text-left">
          <span class="font-semibold">{{order.hawker_name}} stall</span><br>
          <!-- <span class="font-semibold">{{order.hawker_id}}</span><br> -->
          <span :class="getStatus(order.status)">Status: {{order.status}}</span><br>
          <span>{{order.time}}</span>
        </div>

        <div class="text-right">
          <span class="text-sm">Order ID: {{order.order_id}}</span><br><br>
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

const get_Order_URL = "http://localhost:5004/order";
const get_Hawker_URL = "http://localhost:5002/hawker";

export default {
  name: 'order',
  components: {
  },

  data(){
    return {
      globalState,
      orders: [],
      hawkers: [],
      processedOrder: []
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
        for (let order of this.orders){
          // console.log(order.final_price)
          // console.log(order.hawker_id)
          // console.log(order.order_id)
          // console.log(order.status)
          // console.log(order.time)
          
          axios
          .get(get_Hawker_URL + "/" + order.hawker_id)
          .then (response => {
            console.log(response.data.data.username)
            var newOrder = {
            "final_price": order.final_price,
            "hawker_id": order.hawker_id,
            "order_id": order.order_id,
            "status": order.status,
            "time": order.time,
            "hawker_name": response.data.data.username,
          }
          this.processedOrder.push(newOrder)
          })
          .catch(error =>{
            console.log(error)
          })
        }
      })
      .catch(error => {
        console.log(error)
      })
    },

    getStatus(val){
      if (val == "rejected"){
        return ("badge bg-danger");
      } else if (val == "accepted" | val == "pending"){
        return ("badge bg-warning text-dark");
      } else {
        return ("badge bg-success");
      }
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