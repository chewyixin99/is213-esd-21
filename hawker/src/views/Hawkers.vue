<template>
  <div>
    <!-- Welcome Message and Wallet -->
    <div class="grid grid-cols-5 shadow bgimg">
      <div class="col-span-3 text-left p-3 my-auto">
        <h1 class="text-2xl font-bold text-white 
        shadow-lg">Welcome to Hawker<br>Pre-Orderation</h1>
      </div>
      <div class="col-span-2 p-3 text-white">
        <Wallet v-if="globalState.user_id !== null && globalState.user_id < 2000"/>
      </div>
    </div>

    <div class="container mt-3 flex">
      <select class="form-control mr-3" @change="changeFilter($event)">
        <option value="" selected disabled>Choose</option>
        <option v-for="filter in filters" :value="filter.id" :key="filter.id">{{ filter.name }}</option>
      </select>
      <br><br>
      <button @click="filterHawker" class="btn btn-warning w-full md:w-48">Filter</button>
    </div>
  
    <div v-for="hawker in hawkers" :key="hawker.hawker_id">
      <router-link :to="{ path: '/hawkerstall', query: { hawker_id: hawker.hawker_id, hawker_name: hawker.username }}">      
        <Hawker :hawker_name="hawker.username" :opening_hours="hawker.opening_hours" :closing_hours="hawker.closing_hours"/>
      </router-link>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from "axios";
import Hawker from "@/components/Hawker-comp.vue";
import Wallet from "@/components/Wallet-comp.vue";
import { globalState } from "../store"

const get_Hawker_URL = "http://localhost:5002/hawker";

export default {
  name: "Hawkers",
  components: {
    Hawker,
    Wallet,
  },

  data() {
    return {
      globalState,
      hawkers: null,
      filters: [
        { name: "All", id: 1 },
        { name: "Halal", id: 2 },
        { name: "Vegetarian", id: 3 },
      ],
      selectedfilter: null
    };
  },

  created: function () {
    this.getHawkers();
  },

  methods: {
    changeFilter(event) {
      this.selectedfilter = event.target.options[event.target.options.selectedIndex].text
    },

    filterHawker() {
      if (this.selectedfilter === 'All') {
        this.getHawkers()
      } else if (this.selectedfilter === 'Halal') {
        this.getHalal()
      } else if (this.selectedfilter === 'Vegetarian') {
        this.getVegetarian()
      }
    },

    getHawkers() {
      console.log("=== open getHawker ===");
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

    getHalal() {
      console.log("=== open getHalal ===")
      const get_Halal_URL = "http://localhost:5002/hawker/halal/1";
      axios
        .get(get_Halal_URL)
        .then((response) => {
          // console.log(response.data.data.hawkers);
          this.hawkers = response.data.data.hawkers;
        })
        .catch((error) => {
          console.log("=== error getHalal ===");
          console.log(error.message);
        });
    },

    getVegetarian() {
      console.log("=== open getVegetarian ===")
      const get_Vegetarian_URL = "http://localhost:5002/hawker/vegetarian/1";
      axios
        .get(get_Vegetarian_URL)
        .then((response) => {
          // console.log(response.data.data.hawkers);
          this.hawkers = response.data.data.hawkers;
        })
        .catch((error) => {
          console.log("=== error getVegetarian ===");
          console.log(error.message);
        });
    }
  },
};
</script>


<style scoped>
.bgimg {
  background-image: url("../assets/hawkerbg.jpg");
  background-size: 100%;
}
</style>