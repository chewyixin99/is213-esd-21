<template>
  <div>
    <div class="collapse" id="navbarToggleExternalContent">
      <!-- Conditional render for navbar -->
      <div v-if="globalState.user_id === null" class="bg-dark p-4">
        <router-link to="/hawkers">
          <div class="text-white mb-2">Hawker Stalls</div>
        </router-link>
        <router-link to="/">
          <div class="text-white">Log In</div>
        </router-link>
      </div>
      <div v-else-if="globalState.user_id >= 2000" class="bg-dark p-4">
        <router-link to="/">
          <div class="text-white">Log out</div>
        </router-link>
      </div>
      <div v-else class="bg-dark p-4">
          <router-link to="/hawkers">
            <div class="text-white mb-2">Hawker Stalls</div>
          </router-link>
          <router-link to="/order">
            <div class="text-white mb-2">My Orders</div>
          </router-link>
          <router-link to="/topup">
            <div class="text-white mb-2">Top Up Wallet</div>
          </router-link>
          <router-link to="/">
            <div class="text-white">Log out</div>
          </router-link>
      </div>
    </div>
    <nav class="navbar navbar-dark fixed-top bg-dark">
    <div class="container-fluid">
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarToggleExternalContent" aria-controls="navbarToggleExternalContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
        </button>
        <router-link to="/cart">
          <img src="../assets/cart.png" class="w-7 mr-2">
        </router-link>
    </div>
    </nav>
  </div>
</template>

<script>
import { globalState } from '../store'

export default {
  name: 'NavBar',
  data() {
    return {
      globalState
    }
  }
}
</script>