<template>
  <div class="mx-auto">
    
    <div class="rounded p-3 shadow">

      <!-- Tabs -->
      <div class="text-center">
        <ul class="nav nav-pills">
          <li class="nav-item">
              <a class="nav-link text-dark" aria-current="page" href="#">User</a>  
          </li>
          <li class="nav-item">
            <a class="nav-link active bg-warning text-dark" href="#/loginhawker">Hawker</a>
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

      </div>

    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'LoginHawker',

  data(){
    return{
      email: "",
      password: "",
      error: null,
      errorMsg: ""
    }
  },

   methods: {

      async login(){

        if (this.email == "" || this.password == "") {
          this.error = true
          this.errorMsg = "Please fill up all fields."
          return 
        }

        let params = {
          email: this.email,
          password: this.password,
        }

        const url = "http://localhost:5002/hawker/authenticate" || "http://localhost:8000/hawker/authenticate"

        await axios.post(url, params)
          .then((response)=>{
            if (response.data.code == 203) {
              localStorage.setItem("user_id", response.data.data)
              console.log(`Successfully set Hawker's User ID: ${response.data.data}..`)
              this.$router.replace({name: "HawkerActivity"});
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

      }
   }
}
</script>

