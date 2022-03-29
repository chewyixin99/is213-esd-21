<template>
  <div id="nav">
    <NavBar/>
    <router-link to="/">Login</router-link> |
    <router-link to="/Hawkers">About</router-link>

    <router-view/>
  </div>
  
</template>

<script>
import NavBar from './components/NavBar.vue';


export default {
  name: 'App',
  components: {
    NavBar,
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

</style>
