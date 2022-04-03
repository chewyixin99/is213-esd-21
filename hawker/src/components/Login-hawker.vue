<template>
  <div class="mx-auto">
    
    <div class="rounded p-3 shadow">

      <!-- Tabs -->
      <div class="text-center">
        <ul class="nav nav-pills">
          <li class="nav-item">
              <a class="nav-link text-dark" aria-current="page" href="#">User</a>  
          </li>
          <li class="nav-item">
            <a class="nav-link active bg-warning text-dark" href="#/loginhawker">Hawker</a>
          </li>
        </ul>
      </div>

      <!-- Login Details -->
      <form>
        <div class="my-3 text-start">
          <label for="formGroupExampleInput" class="form-label">Email</label>
          <input type="text" class="form-control" id="formGroupExampleInput" placeholder="Enter Email">
        </div>
        <div class="mb-5 text-start">
          <label for="formGroupExampleInput2" class="form-label">Password</label>
          <input type="text" class="form-control" id="formGroupExampleInput2" placeholder="Enter Password">
        </div>
      </form>

      <!-- Buttons -->
      <div class="text-center">

          <!-- <button type="button" class="btn btn-danger w-24">Sign Up</button> -->
          <router-link to="/Hawkers">
            <button type="button" class="btn btn-warning w-full">Log In</button>
          </router-link>

          <div class="mt-2">
            <span class="text-warning">Create an account</span>
          </div>

      </div>

    </div>
  </div>
</template>

<script>
export default {
  name: 'LoginHawker',
}
</script>