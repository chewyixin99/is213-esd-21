<template>   
  <div class="w-96 mx-auto mt-3 px-3 ">
    <!-- Title -->
    <div class="text-left mb-2">
      <h1 class="font-medium text-3xl">Order Activity</h1>
    </div>

    <!-- Order List -->
    <div class="pt-3" v-for="order in orders.slice().reverse()" :key="order">
      <!-- HEADERS -->
      <div class="flex justify-content-between">

        <!-- LHS -->
        <div class="text-left">
          <span class="font-semibold">Order ID: {{order.order_id}}</span><br>
          <!-- <span>{{order.time}}</span> -->
          <span class="font-semibold">Item</span><br>         
        </div>

        <!-- RHS -->
        <div class="text-right">
          <span class="badge bg-warning text-dark">Status: {{order.status}}</span><br>
          <span class="font-semibold">Qty</span>
        </div>

      </div>

      <!-- ITEM LIST -->
      <div class="pb-3" v-for="item in order.items" :key="item">
        <div class="flex justify-content-between">
          <!-- LHS -->
          <div class="text-left">
            <span class="font-semibold">{{item.item_id}}</span><br>     
          </div>
          <!-- RHS -->
          <div class="text-right">
            <span class="text-dark">{{item.quantity}}</span><br>
          </div>
        </div>
      </div>

      <span>Time of Order: {{order.time}} </span><br>
      <span>Order Price: ${{order.price}} </span>
      <!-- <div>{{ (new Date(order.time))-(Date.now()) }}</div> -->
      <!-- BUTTONS -->
      <!-- {{order.status}} -->
      <!-- if pending -->
      <div v-if="order.status == 'pending'" class="flex space-x-4">
        <button @click="rejectOrder(order.order_id)" type="button" class="btn btn-danger w-full">Reject</button>
        <button @click="acceptOrder(order.order_id)" type="button" class="btn btn-warning w-full">Accept</button>
      </div>
      <!-- if rejected -->
      <div v-if="order.status == 'rejected'" class="flex space-x-4">
        <button type="button" class="btn btn-secondary w-full disabled">Rejected</button>
      </div>
      <!-- if accepted -->
      <div v-if="order.status == 'accepted'" class="flex space-x-4">
        <button @click="completeOrder(order.order_id)" type="button" class="btn btn-success w-full">Complete</button>
      </div>
      <!-- if completed -->
      <div v-if="order.status == 'completed'" class="flex space-x-4">
        <button type="button" class="btn btn-secondary w-full disabled">Completed</button>
      </div>

      <hr class="mt-3">
    </div>

  </div>
</template>

<script>
// @ is an alias to /src
import axios from 'axios';

const get_Order_URL = "http://localhost:8000/order";
const get_Item_URL = "http://localhost:8000/item";
const accept_Order_URL = "http://localhost:8000/accept_order";
const reject_Order_URL = "http://localhost:8000/reject_order";
const complete_Order_URL = "http://localhost:8000/complete_order";

export default {
  name: 'HawkerActivity',
  components: {
  },

  data(){
    return {
      orders: [],
      items: [],
      hawker_id: null,
    }
  },

  created: function(){
    console.log("=== open created ===")
    this.hawker_id = localStorage.getItem("user_id")
    this.getOrders()
  },

  methods:{
    getOrders(){
      console.log("=== open getOrders ===")
      console.log(get_Order_URL + "/hawker/" + this.hawker_id)
      axios
      .get(get_Order_URL + "/hawker/" + this.hawker_id)
      .then(response => {
        console.log(response.data.data.orders)
        this.orders = response.data.data.orders

        let order_compilation = []
        for (let order of response.data.data.orders){
          console.log(order)
          let processedOrder = {
            "order_id" : order.order_id,
            "status" : order.status,
            "items" : eval(order.items),
            "time" : order.time,
            "price" : order.final_price
          }
          console.log(eval(order.items)[0])
          console.log(typeof(order.items))
          console.log("----")
          console.log(typeof(eval(order.items)))
          order_compilation.push(processedOrder)
        }
        this.orders = order_compilation
      })
      .catch(error => {
        console.log(error)
      })
    },
    millisToMinutesAndSeconds(millis){

        var minutes = Math.floor(millis / 60000);
        var seconds = ((millis % 60000) / 1000).toFixed(0);
        return minutes + ":" + (seconds < 10 ? '0' : '') + seconds;

      millisToMinutesAndSeconds(298999); // "4:59"
      millisToMinutesAndSeconds(60999);  // "1:01"
    },

    // getItems(){
    //   console.log("=== open getItems ===")
    //   axios
    //   .get(get_Item_URL + "/item/" + this.item_id)
    //   .then(response => {
    //     console.log(response.data.data)
    //     this.orders = response.data.data
    //   })
    //   .catch(error => {
    //     console.log(error)
    //   })
    // },

    // getJSON(str){
    //   return JSON.parse(str)
    // },

    acceptOrder(order_id){
      console.log("=== open acceptOrder ===")
      console.log(order_id)
      axios
      .post(accept_Order_URL + "/" + order_id)
      .then(response => {
        console.log(response.data)
      })
      .catch(error =>{
        console.log(error.message)
      })
    },

    rejectOrder(order_id){
      console.log("=== open rejectOrder ===")
      console.log(order_id)
      axios
      .post(reject_Order_URL + "/" + order_id)
      .then(response => {
        console.log(response.data)
      })
      .catch(error =>{
        console.log(error.message)
      })
    },

    completeOrder(order_id){
      console.log("=== open completeOrder ===")
      console.log(order_id)
      axios
      .post(complete_Order_URL + "/" + order_id)
      .then(response => {
        console.log(response.data)
      })
      .catch(error =>{
        console.log(error.message)
      })
    },

  }

}
</script>

/