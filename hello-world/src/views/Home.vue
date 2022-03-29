<template>
  <div class="home">
    <Login/>
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
