<template>
  
    <form class="max-w-lg mx-auto " @submit.prevent="submitSearch">
      <div class="flex items-center">
        <!-- Go Back Button -->
        <button @click="goBack" type="button" class="flex-shrink-0 z-10 inline-flex items-center py-2.5 px-4 text-sm font-medium text-center text-gray-900 bg-gray-100 border border-gray-300 rounded-s-lg hover:bg-gray-200 focus:ring-4 focus:outline-none focus:ring-gray-100 dark:bg-gray-700 dark:hover:bg-gray-600 dark:focus:ring-gray-700 dark:text-white dark:border-gray-600">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M3.825 9L9.425 14.6L8 16L0 8L8 0L9.425 1.4L3.825 7H16V9H3.825Z" fill="#1C1B1F"/>
            </svg>
        </button>
        <!-- Search Input -->
        <div class="relative w-full flex ml-4">
          <input type="search" v-model="searchQuery" id="search-dropdown" class="relative m-0 block flex-auto rounded border border-solid border-neutral-200 bg-transparent bg-clip-padding px-3 py-[0.25rem] text-base font-normal leading-[1.6] text-surface outline-none transition duration-200 ease-in-out placeholder:text-neutral-500 focus:z-[3] focus:border-primary focus:shadow-inset focus:outline-none motion-reduce:transition-none dark:border-white/10 dark:text-white dark:placeholder:text-neutral-200 dark:autofill:shadow-autofill dark:focus:border-primary" required />
          <button type="submit">
            <svg class="w-4 h-4" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">
              <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z"/>
            </svg>
            <span class="sr-only">Search</span>
          </button>
        </div>
      </div>
    </form>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';
  
  // Define reactive variables
  const searchQuery = ref('');
  
  // Access Vue Router
  const router = useRouter();
  
  // Method to handle the go back action
  const goBack = () => {
    router.go(-1); // Navigates back one step in history
  };
  
  // Method to handle search submission
  const submitSearch = () => {
    console.log(`Searching for "${searchQuery.value}"`);
  };
  </script>
  
  <style scoped>
  /* Add any scoped styles here */
  </style>
  