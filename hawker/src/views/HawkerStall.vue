<template>
  <div>
    <!-- Welcome Message and Wallet -->
    <div class="bg-warning text-gray text-lg font-medium py-3">
      <span>Hawker Name</span>
    </div>

    <div class="mt-3">
      <Item/>
      <Item/>
      <Item/>
    </div>


  </div>
</template>

<script>
// @ is an alias to /src
import Item from '@/components/Item-comp.vue'


export default {
  name: 'HawkerStall',
  components: {
    Item,
  }
}
</script>


<style scoped>

</style>