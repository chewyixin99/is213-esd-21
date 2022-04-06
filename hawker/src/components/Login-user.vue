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

          <button @click="login" type="button" class="btn btn-warning w-full">Log In</button>

          <div v-if="error" class="mt-1 text-danger">{{this.errorMsg}}</div>

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
import { stateSetters } from "../store"

export default {
  name: 'LoginUser',
  data(){
    return{
      stateSetters,
      email: "",
      password: "",
      error: null,
      errorMsg: ""
    }
  },

  methods: {
      // setUserId(user_id){
      //   // console.log("=== set user id ===")
      //   localStorage.setItem("user_id", user_id)
      //   console.log(`Successfully set User ID: ${user_id}`)
      // },

      async login(){

        if (this.email == "" || this.password == "") {
          this.error = true
          this.errorMsg = "Please fill up all fields."
          return null
        }

        let params = {
          email: this.email,
          password: this.password,
        }

        const url = "http://localhost:5001/user/authenticate" || "http://localhost:8000/user/authenticate"
        
        await axios.post(url, params)
          .then((response)=>{
            if (response.data.code == 203) {
              localStorage.setItem("user_id", response.data.data)
              this.stateSetters.updateUser_id(response.data.data)
              console.log(`Successfully set Customer's User ID: ${response.data.data}..`)
              this.$router.replace({name: "Hawkers"});
              return response.data.data
            }
            else {
              this.error = true
              this.errorMsg = "Incorrect email or password. Please try again.."
              console.log("Incorrect password")
            }
          })
          .catch((err)=>{
            this.error = true
            this.errorMsg = "Incorrect email or password. Please try again.."
            console.log("Incorrect email")
          })

        // if (response.data){
        //   let response_userid = response.data.data
        //   localStorage.setItem("user_id", response_userid)
        //   console.log(`Successfully set User ID: ${response_userid}.. Routing>>`)
        //   this.$router.replace({name: "Hawkers"});
        // }

        // else {
        //     this.error = "Unsuccessful login";
        //     console.log(this.error)
        //   }
        
      }
    }
}
</script>