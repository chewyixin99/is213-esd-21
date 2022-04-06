<template>
  <div>
    <!-- Welcome Message and Wallet -->
    <div class="grid grid-cols-5 shadow bgimg">
      <div class="col-span-3 text-left p-3 my-auto">
        <h1 class="text-3xl font-bold text-white 
        shadow-lg">Welcome to HawkerSG</h1>
      </div>
      <div class="col-span-2 p-3 text-white">
        <Wallet/>
      </div>
    </div>

  
    <div v-for="hawker in hawkers" :key="hawker.hawker_id">
      <router-link :to="{ path: '/hawkerstall', query: { hawker_id: hawker.hawker_id, hawker_name: hawker.username }}">      
        <Hawker :hawker_name="hawker.username" :opening_hours="hawker.opening_hours" :closing_hours="hawker.closing_hours"/>
      </router-link>
    </div>
        
    <!-- <ul>
      <li v-for="hawker in hawkers" :key="hawker.hawker_id">
        <ul>{{hawker.username}}</ul>
      </li>
    </ul> -->
  </div>
</template>

<script>
// @ is an alias to /src
import axios from "axios";
import Hawker from "@/components/Hawker-comp.vue";
import Wallet from "@/components/Wallet-comp.vue";
import { globalState } from "../store"

export default {
  name: "Hawkers",
  components: {
    Hawker,
    Wallet,
  },


  data() {
    return {
      // hawkers: [],
      // message: "",
      // closing_hours: "",
      // cuisine: "",
      // email: "",
      // halal: false,
      // has_vegetarian_option: false,
      // hawker_id: "",
      // opening_hours: "",
      // password: "",
      // username: "",
      // wallet_id: null
      hawkers: null,
      globalState
      // info: "",
    };
  },

  created: function () {
    this.getHawkers();
  },

  methods: {
    getHawkers() {
      console.log("=== open getHawker ===");
      const get_Hawker_URL = "http://localhost:8000/hawker";
      axios
        .get(get_Hawker_URL)
        .then((response) => {
          // console.log(response.data.data.hawkers);
          this.hawkers = response.data.data.hawkers;
        })
        .catch((error) => {
          console.log("=== error getHawker ===");
          console.log(error.message);
        });
    },
  },

  // mounted () {
  //   axios
  //   .get(get_Hawker_URL)
  //   .then(response => (this.info = response))
  //   console.log(this.info)
  // }
};
</script>


<style scoped>
.bgimg {
  background-image: url("../assets/hawkerbg.jpg");
  background-size: 100%;
  /* filter: brightness(50%); */
}
</style>