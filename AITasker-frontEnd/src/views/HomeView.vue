<template>
    <div class="expert-profile-slider">
      <swiper
        :slides-per-view="slidesPerView"
        :space-between="20"
        :pagination="{ clickable: true }"
        :breakpoints="swiperBreakpoints"
      >
        <swiper-slide v-for="(expert, index) in experts" :key="index">
          <Card :expert="expert" />
        </swiper-slide>
      </swiper>
    </div>
  </template>
  
  <script>
  import { Swiper, SwiperSlide } from 'swiper/vue';
  import { Pagination } from 'swiper/modules';
  import 'swiper/css';
  import 'swiper/css/pagination';
  import Card from '../components/Card.vue';
  
  export default {
    components: {
      Swiper,
      SwiperSlide,
      Card
    },
    data() {
      return {
        experts: [
          { name: '夢鏡影像工作室', rating: 4.0, expertise: 'Expert 影片/廣告拍攝' },
          { name: '夢鏡影像工作室', rating: 4.0, expertise: 'Expert 影片/廣告拍攝' },
          { name: '夢鏡影像工作室', rating: 4.0, expertise: 'Expert 影片/廣告拍攝' },
          { name: '夢鏡影像工作室', rating: 4.0, expertise: 'Expert 影片/廣告拍攝' },
          { name: '夢鏡影像工作室', rating: 4.0, expertise: 'Expert 影片/廣告拍攝' },
          { name: '夢鏡影像工作室', rating: 4.0, expertise: 'Expert 影片/廣告拍攝' },
          // Add more expert data here...
        ],
        swiperBreakpoints: {
          
          
          320: {
            slidesPerView: 1.5,
            spaceBetween: 5,
          },
          375: {
            slidesPerView: 2,
            spaceBetween: 10,
          },
          768: {
            slidesPerView: 4.5,
            spaceBetween: 15,
          },
          1024: {
            slidesPerView: 5.5,
            spaceBetween: 20,
          },
        },
      };
    },
    setup() {
      return {
        modules: [Pagination],
      };
    },
  };
  </script>
  
  <style scoped>
  .expert-profile-slider {
    padding: 20px 0;
  }
  </style>