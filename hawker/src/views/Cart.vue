<template>
  <div>
    <!-- Welcome Message and Wallet -->
    <div class="grid grid-cols-5">
      <div class="col-span-3 text-left p-3 my-auto">
        <h1 class="font-medium text-3xl">My Order</h1>
      </div>
      <div class="col-span-2 p-3">
        <Wallet :key="reRender"/>
      </div>
    </div>

    <div
      v-for="(item, index) in globalState.selected_items"
      :key="item.item_id"
      class="mt-3"
    >
      <CartItem :item_data_prop="item" @remove_item="removeItem(index)" />
    </div>

    <div class="mt-3 text-left px-3 flex justify-content-between">
      <span class="font-semibold">Total Amount Payable</span>
      <span class="text-xl">${{ totalAmount }}</span>
    </div>

    <div class="mt-3 md:text-right px-3">
      <button
        type="button"
        @click="createOrder"
        class="btn btn-warning w-full md:w-48"
      >
        <span v-if="isLoading">Processing payment...</span> 
        <span v-else>Pay</span>
      </button>
    </div>

    <div class="mt-3">
      <p :class="msgStatus">{{ userMsg }}</p>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from "axios";
import CartItem from "@/components/Cart-item-comp.vue";
import Wallet from "@/components/Wallet-comp.vue";
import { globalState, stateSetters } from "../store";

export default {
  name: "Cart",
  components: {
    CartItem,
    Wallet,
  },

  data() {
    return {
      globalState,
      stateSetters,
      totalAmount: 0.0,
      selectedHawker: null,
      isLoading: false,
      userMsg: "",
      msgStatus: "",
      reRender: 0,
    };
  },

  created() {
    this.getTotalAmount();
  },

  methods: {
    removeItem(index) {
      console.log("==== removeing item ====");
      stateSetters.removeSelectedItem(index);
      this.getTotalAmount();
    },

    getTotalAmount() {
      this.totalAmount = 0;
      if (globalState.selected_items.length !== 0) {
        this.selectedHawker = globalState.selected_items[0].hawker_id;
        globalState.selected_items.map(
          (item) => (this.totalAmount += item.price)
        );
      }
      this.totalAmount = Number.parseFloat(this.totalAmount).toFixed(2);
    },

    async createOrder() {
      var finalItems = [];
      this.isLoading = true;

      this.globalState.selected_items.forEach((item) => {
        var itemAdded = false
        finalItems.forEach((finalItem) => {
          if (item.item_id === finalItem.item_id) {
            finalItem.quantity += 1
            itemAdded = true
          }
        })

        if (!itemAdded) {
          finalItems.push({
            item_id: item.item_id,
            quantity: 1
          })
          itemAdded = false
        }
      })

      if (finalItems.length === 0) {
        this.userMsg = "Please add items to your cart first."
        this.msgStatus = "text-red-600"
        this.isLoading = false
      } else if (Number(this.globalState.avail_balance) < Number(this.totalAmount)) {
        this.userMsg = "Insufficient funds, please top up your wallet."
        this.msgStatus = "text-red-600"
        this.isLoading = false
      } else {
        finalItems = JSON.stringify(finalItems);

        const orderData = {
          user_id: globalState.user_id,
          hawker_id: this.selectedHawker,
          items: finalItems,
          status: "pending",
          total_price: Number(this.totalAmount),
          discount: 0.0,
          final_price: Number(this.totalAmount),
        };

        const place_order_URL = `http://localhost:5100/place_order`;
        axios
          .post(place_order_URL, orderData)
          .then((response) => {
            console.log(`=== order created ===`);
            // console.log(response.data.data);
            console.log(response)
            this.isLoading = false;
            this.userMsg = "Order successfully placed."
            this.msgStatus = "text-green-600"
            this.stateSetters.clearSelectedItems()
            this.getTotalAmount()
            this.forceReRender()
          })
          .catch((error) => {
            console.log(`=== ERROR creating items ===`);
            console.log(error.message);
            this.isLoading = false;
            this.userMsg = "Failed to process order. Please try again.";
            this.msgStatus = "text-red-600"
          });
      }
    },

    forceReRender() {
      this.reRender += 1
    }
  },
};
</script>


<style scoped>
</style>