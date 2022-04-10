<template>
  <div>
    
    <div class="w-96 mx-auto mt-3 px-3 ">
      <!-- Title -->
      <div class="text-left mb-2">
        <h1 class="font-medium text-3xl">Create Account</h1>
      </div>

      <!-- Profile Details -->
      <form>
        <div class="mb-3 text-start">
          <label for="username" class="form-label">Name</label>
          <input type="text" class="form-control" id="username" v-model="username">
        </div>

        <div class="mb-3 text-start">
          <label for="email" class="form-label">Email</label>
          <input type="text" class="form-control" id="email" v-model="email">
        </div>

        <div class="mb-5 text-start">
          <label for="password" class="form-label">Password</label>
          <input type="password" class="form-control" id="password" v-model="password">
        </div>

      </form>

      <!-- Buttons -->
      <div class="text-end flex mb-3 mx-auto space-x-4">
          <button @click="cancel" type="button" class="btn btn-outline-danger w-full" href="#">Cancel</button>
          <button @click="createUser" type="button" href="/hawkers" class="btn btn-warning w-full">Create</button>
      </div>

      <div>
        <p :class="msgStatus">{{userMsg}}</p>
      </div> 

    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from 'axios';
import { stateSetters } from '../store'

// let userid = "1000";
const get_User_URL = "http://localhost:8000/user";
const get_Wallet_URL = "http://localhost:8000/wallet"

export default {
  name: 'Account',
  components: {
  },

  data(){
    return {
      stateSetters,
      username: "",
      email: "",
      password: "",
      user_id: "",
      userMsg: "",
      msgStatus: "",
    }
  },


  methods:{
    createUser(){
      console.log("=== Open CreateUser ===")
      axios
      .post(get_User_URL + "/" + this.email , {
        username: this.username,
        password: this.password,
      })
      .then((response) => {
        console.log(response.data.data)
        console.log(response.data.data['user_id']);
        this.user_id = response.data.data['user_id'];
        localStorage.setItem("user_id", response.data.data['user_id'])
        this.stateSetters.updateUser_id(response.data.data['user_id'])
        this.createWallet()
      })
      .catch((error) => {
        console.log(error)
        this.userMsg = "Error occured while creating your account. Please try again."
        this.msgStatus = "text-red-600"
      })
    },

    async createWallet(){
      console.log("=== Open CreateWallet ===")

      console.log(get_Wallet_URL + "/" + this.user_id)
      await axios
      .post(get_Wallet_URL + "/" + this.user_id , {
        available_balance: 0.0,
        total_balance: 0.0,
      })
      .then((response) => {
        console.log(response.data.data);
        this.userMsg = "Account created successfully. Redirecting you to our home page..."
        this.msgStatus = "text-green-600"
        this.$router.replace({name: "Hawkers"});
      })
      .catch((error) => {
        console.log(error)
        this.userMsg = "Error occured while creating your account. Please try again"
        this.msgStatus = "text-red-600"
      })
    },

    cancel() {
      this.$router.replace({name: "Login"})
    }
  }

}
</script>

