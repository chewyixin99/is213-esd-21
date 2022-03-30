<template>
  <div class="container w-96 mt-4 px-4 text-center">
    <span class="text-3xl font-bold">Login e-Hawker</span>
    <Login class="mt-3"/>
  </div>
</template>

<script>
// @ is an alias to /src
import Login from '@/components/Login-comp.vue'

export default {
  name: 'Home',
  components: {
    Login
  }
}
</script>
