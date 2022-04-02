<template>
  <div id="app">
    <!-- Welcome Message and Wallet -->
    <div class="grid grid-cols-5 shadow bgimg">
      <div class="col-span-3 text-left p-3 my-auto">
        <h1 class="text-3xl font-bold text-white shadow-lg">Welcome to e-Hawker</h1>
      </div>
      <div class="col-span-2 p-3 text-white">
        <Wallet/>
      </div>
    </div>

    <div class="mt-3">
      <router-link to="/hawkerstall">
            <Hawker/>
      </router-link>
      <router-link to="/hawkerstall">
            <Hawker/>
      </router-link>
      <router-link to="/hawkerstall">
            <Hawker/>
      </router-link>
    </div>
  </div>
</template>

<script>
  // @ is an alias to /src
  import Hawker from '@/components/Hawker-comp.vue'
  import Wallet from '@/components/Wallet-comp.vue'

  export default {
    name: 'Hawkers',
    components: {
      Hawker,
      Wallet,
    }
  }
  console.log("Hello")

  const get_hawker_URL = "http://localhost:5002/hawker";

  const app = Vue.createApp({
    computed: {
      hasHawkers: function(){
        console.log("Compute Hawker")
        // return this.hawkers.length > 0;
      }
    },
    data(){
      return {
        hawkers: [],
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
      };
    },
    methods: {
      getAllHawkers(){
        console.log("=== Open Hawker ===")
        const response =
          fetch(get_hawker_URL)
            .then( data => {
              console.log(response);
              if (data.code === 404){
                this.message = data.message;
              } else {
                this.hawkers = data.data.hawkers;
              }
            })
            .catch(error => {
              console.log(this.message + error);
            });
      },

    }
    

  });
  app.mount('#app');

</script>


<style scoped>
.bgimg {
  background-image: url('../assets/hawkerbg.jpg');
  background-size: 100%;
  /* filter: brightness(50%); */
}
</style>