<template>
    <div class="card" style="min-width: 10rem;">
      <div class="position-relative">
        <img src="../assets/龍年賀卡.png" class="card-img-top" alt="Night city view">
        <!-- <button class="btn btn-light rounded-circle position-absolute top-50 start-50 translate-middle">
          <i class="bi bi-play-fill"></i>
        </button> -->
        <span class="position-absolute top-0 start-0 bg-warning text-dark p-1 m-2">T</span>
        <div class="position-absolute bottom-0 start-0 m-2">
          <img src="../../public/logo.png" class="rounded-circle" alt="Logo" width="40" height="40">
        </div>
      </div>
      <div class="card-body">
      <h5 class="card-title">{{ expert.name }}</h5>
      <div class="d-flex align-items-center mb-2">
        <div class="text-warning me-2">
          <i v-for="n in 5" :key="n" :class="['bi', n <= expert.rating ? 'bi-star-fill' : 'bi-star']"></i>
        </div>
        <span>{{ expert.rating.toFixed(1) }}</span>
      </div>
      <p class="card-text">{{ expert.expertise }}</p>
      <div class="d-flex justify-content-between">
        <button class="btn btn-outline-secondary">Profile</button>
        <button class="btn btn-warning">Ask</button>
      </div>
    </div>
    </div>
  </template>
  
  <script>
  import 'bootstrap-icons/font/bootstrap-icons.css'
  import 'bootstrap/dist/css/bootstrap.css'
  import 'bootstrap'
  import { defineComponent } from 'vue';
  export default defineComponent({
  name: 'Card',
  props: {
    expert: {
      type: Object,
      required: true
    }
  }
})
  </script>
  
  <style scoped>
  /* You can add any additional custom styles here */
  </style>