<template>
  <div>
    <!-- Welcome Message and Wallet -->
    <div class="grid grid-cols-5">
      <div class="col-span-3 text-left p-3">
        <span class="text-3xl font-bold">Top Up</span>
      </div>
      <div class="col-span-2 p-3">
        <Wallet/>
      </div>
    </div>

    <div class="mt-3 px-3">
      <!-- Login Details -->
      <form>
        <div class="my-3 text-left flex align-middle justify-content-between">
          <label for="formGroupExampleInput" class="form-label my-auto">Top Up Amount:</label>
          <input type="text" class="form-control w-24 text-center" id="formGroupExampleInput" placeholder="$10">
        </div>
        <div class="mb-3 text-start">
          <label for="formGroupExampleInput2" class="form-label">Card Number</label>
          <input type="text" class="form-control" id="formGroupExampleInput2" placeholder="Enter Card Number">
        </div>
        <div class="mb-3 text-start grid grid-cols-2 gap-x-4">
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

          <button type="button" class="btn btn-danger w-full md:w-24">Cancel</button>
          <button type="button" class="btn btn-primary w-full md:w-24">Top Up</button>

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

