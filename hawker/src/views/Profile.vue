<template>
  <div>
    
    <div class="w-96 mx-auto mt-3 px-3 ">
      <!-- Title -->
      <div class="text-left mb-2">
        <h1 class="font-medium text-3xl">My Profile</h1>
      </div>

      <!-- Profile Details -->
      <form>
        <div class="mb-3 text-start">
          <label for="formGroupExampleInput2" class="form-label">Name</label>
          <input type="text" class="form-control" id="formGroupExampleInput2" placeholder="Name">
        </div>

        <div class="mb-3 text-start">
          <label for="formGroupExampleInput2" class="form-label">Email</label>
          <input type="text" class="form-control" id="formGroupExampleInput2" placeholder="Email">
        </div>

        <div class="mb-5 text-start">
          <label for="formGroupExampleInput2" class="form-label">Password</label>
          <input type="text" class="form-control" id="formGroupExampleInput2" placeholder="Password">
        </div>

      </form>

      <!-- Buttons -->
      <div class="text-end flex mx-auto space-x-4">

          <button type="button" class="btn btn-outline-danger w-full">Cancel</button>
          <button type="button" class="btn btn-warning w-full">Save</button>

      </div>

    </div>
  </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: 'Profile',
  components: {
  }
}
</script>

