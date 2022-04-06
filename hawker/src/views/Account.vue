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
      <div class="text-end flex mx-auto space-x-4">
          <button type="button" class="btn btn-outline-danger w-full" href="#">Cancel</button>
          <button @click="createUser()" type="button" href="/hawkers" class="btn btn-warning w-full">Create</button>
      </div>

    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from 'axios';

// let userid = "1000";
const get_User_URL = "http://localhost:5001/user";
const get_Wallet_URL = "http://localhost:5005/wallet"

export default {
  name: 'Account',
  components: {
  },

  data(){
    return {
      username: "",
      email: "",
      password: "",
      user_id: localStorage.getItem("user_id"),
    }
  },
  // created: function(){
  //   console.log("=== created ===")
  //   this.getUser()
  // },

  methods:{
    // getUser(){
    //   axios
    //   .get(get_User_URL)
    //   .then(response => {
    //     console.log(response)
    //   })
    //   .catch(error => {
    //     console.log(error)
    //   })
    // }

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
        this.createWallet()
      })
      .catch(function(error){
        console.log(error);
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
      .then(function(response){
        console.log(response.data.data);
      })
      .catch(function(error){
        console.log(error);
      })
    }
  }

}
</script>

