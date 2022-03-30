<template>
  <div>
    <div>
      <div class="bg-warning p-3">
        <Wallet/>
      </div>
    </div>

    
    <div class="w-96 mx-auto mt-3 px-3 ">
      <!-- Title -->
      <div class="text-left mb-2">
        <h1 class="font-medium text-3xl">Top Up Wallet</h1>
      </div>

      <!-- CC Details -->
      <form>
        <div class="mb-3 text-left flex align-middle justify-content-between">
          <label for="formGroupExampleInput" class="form-label my-auto">Top Up Amount:</label>
          <div class="flex">
            <span class="my-auto mr-2">$</span>
            <input type="text" class="form-control w-24 text-center" id="formGroupExampleInput" placeholder="10">
          </div>
        </div>
        <div class="mb-3 text-start">
          <label for="formGroupExampleInput2" class="form-label">Card Number</label>
          <input type="text" class="form-control" id="formGroupExampleInput2" placeholder="Enter Card Number">
        </div>
        <div class="mb-5 text-start grid grid-cols-2 gap-x-4">
          <div class="col-span-1">
            <label for="formGroupExampleInput2" class="form-label">Expiry Date</label>
            <input type="text" class="form-control" id="formGroupExampleInput2" placeholder="">
          </div>
          <div class="col-span-1">
            <label for="formGroupExampleInput2" class="form-label">CVV</label>
            <input type="text" class="form-control" id="formGroupExampleInput2" placeholder="">
          </div>
        </div>
      </form>

      <!-- Buttons -->
      <div class="text-end flex mx-auto space-x-4">

          <button type="button" class="btn btn-outline-danger w-full">Cancel</button>
          <button type="button" class="btn btn-warning w-full">Top Up</button>

      </div>

    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import Wallet from '@/components/Wallet-comp.vue'

export default {
  name: 'TopUp',
  components: {
    Wallet,
  }
}
</script>

