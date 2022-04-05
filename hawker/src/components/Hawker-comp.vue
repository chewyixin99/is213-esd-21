<template>
  <div class="text-left">
    <div class="grid grid-cols-3 md:grid-cols-4 my-3">
      <!-- Hawker Image -->
      <div class="col-span-1 p-2">
        <div class="shadow">
          <img src="../assets/hawkerimg.jpg" class="img-thumbnail h-full">
        </div>
      </div>
      <!-- Hawker Detail -->
      <div class="p-2 col-span-2 md:col-span-3">
        <span>{{hawker_name}}</span>
        <br>
        <span>Operating Hours: {{operating_hours}}</span>
      </div>
    </div>
    <hr>
  </div>
</template>

<script>
export default {
  name: 'Hawker',
  props : ['hawker_name', 'opening_hours', 'closing_hours'], // note: props defined in camelCase need to be called as kebab-case in HTML (as HTML is case-insensitive)

  data() {
    return {
      operating_hours: ""
    }
  },

  created() {
    this.getOperatingHours()
  },

  methods: {
    getOperatingHours() {
      this.operating_hours = `${this.opening_hours} - ${this.closing_hours}`
    }
  }
}
</script>