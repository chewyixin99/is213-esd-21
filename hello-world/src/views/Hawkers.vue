<template>
  <div>
    <!-- Welcome Message and Wallet -->
    <div class="grid grid-cols-5 shadow bgimg">
      <div class="col-span-3 text-left p-3">
        <span class="my-auto text-3xl font-bold text-white shadow-lg">Welcome to Prime Hawker</span>
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
</script>


<style scoped>
.bgimg {
  background-image: url('../assets/hawkerbg.jpg');
  background-size: 100%;
  /* filter: brightness(50%); */
}
</style>