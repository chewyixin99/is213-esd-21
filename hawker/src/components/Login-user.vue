<template>
  <div class="mx-auto">
    
    <div class="rounded p-3 shadow">

      <!-- Tabs -->
      <div class="text-center">
        <ul class="nav nav-pills">
          <li class="nav-item">
            <a class="nav-link active bg-warning text-dark" aria-current="page" href="#">User</a>
          </li>
          <li class="nav-item">
              <a class="nav-link text-dark" href="#/loginhawker">Hawker</a>
          </li>
        </ul>
      </div>

      <!-- Login Details -->
      <form>
        <div class="my-3 text-start">
          <label for="formGroupExampleInput" class="form-label">Email</label>
          <input v-model="email" type="text" class="form-control" id="formGroupExampleInput" placeholder="Enter Email">
        </div>
        <div class="mb-5 text-start">
          <label for="formGroupExampleInput2" class="form-label">Password</label>
          <input v-model="password" type="text" class="form-control" id="formGroupExampleInput2" placeholder="Enter Password">
        </div>
      </form>

      <!-- Buttons -->
      <div class="text-center">

          <!-- <router-link to="/Hawkers"> -->
            <button @click="login" type="button" class="btn btn-warning w-full">Log In</button>
          <!-- </router-link> -->

          <div class="mt-2">
            <router-link to="account">
              <span class="text-warning">Create an account</span>
            </router-link>
          </div>

      </div>

    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'LoginUser',
  data(){
    return{
      email: "",
      password: "",
      user_id: "",
      error: "",
    }
  },

  methods: {
      // setUserId(user_id){
      //   // console.log("=== set user id ===")
      //   localStorage.setItem("user_id", user_id)
      //   console.log(`Successfully set User ID: ${user_id}`)
      // },

      async login(){

        let params = {
          email: this.email,
          password: this.password,
        }

        let response = await axios.post('http://localhost:5001/user/authenticate', params);

        if (response.data){

          let response_userid = response.data.data

          // if (response_usertype == "customer"){
          localStorage.setItem("user_id", response_userid)
          console.log(`Successfully set User ID: ${response_userid}.. Routing>>`)
          this.$router.replace({name: "Hawkers"});

        }

        else {

          let response = await axios.post('http://localhost:5002/hawker/authenticate', params);
          
          if (response){

            let response_userid = response.data.data

            localStorage.setItem("hawker_id", response_userid)
            console.log(`Successfully set Hawker ID: ${response_userid}.. Routing>>`)
            this.$router.replace({name: "Order"});
          }
          
          else {
              this.error = "Unsuccessful login";
              console.log(this.error)
            }
        }
      }
    }
}
</script>