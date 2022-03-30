<template>
  <div class="container mt-4 px-4 text-left">
    <span class="text-3xl font-bold">Login Prime Hawker</span>
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
