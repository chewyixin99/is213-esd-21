<template>
  <div class="container w-96 mt-4 px-4 text-center">
    <span class="text-3xl font-bold">Login e-Hawker</span>
    <LoginUser class="mt-3"/>
    <!-- <LoginHawker class="mt-3"/> -->
  </div>
</template>

<script>
// @ is an alias to /src
import LoginUser from '@/components/Login-user.vue'
// import LoginHawker from '@/components/Login-hawker.vue'


export default {
  name: 'Login',
  components: {
    LoginUser,
    // LoginHawker,
  }
}
</script>
