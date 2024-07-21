<template>
  <div class="flex justify-between px-8">
    <div>
        <!-- <label for="search-dropdown" class="mb-2 text-sm font-medium text-gray-900 sr-only dark:text-white">Your Email</label> -->
        <button id="dropdown-button" @click="toggleDropdown" class="flex-shrink-0 z-10 inline-flex items-center py-2.5 px-4 text-sm font-medium text-center text-gray-900 bg-gray-100 border border-gray-300 rounded-s-lg hover:bg-gray-200 focus:ring-4 focus:outline-none focus:ring-gray-100 dark:bg-gray-700 dark:hover:bg-gray-600 dark:focus:ring-gray-700 dark:text-white dark:border-gray-600" type="button">
          {{ selectedCategory }}
          <svg class="w-2.5 h-2.5 ms-2.5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 10 6">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 4 4 4-4"/>
          </svg>
        </button>
        <div v-if="dropdownVisible" id="dropdown" class="absolute z-10 bg-white divide-y divide-gray-100 rounded-lg shadow w-44 dark:bg-gray-700">
          <ul class="py-2 text-sm text-gray-700 dark:text-gray-200" aria-labelledby="dropdown-button">
            <li v-for="category in categories" :key="category">
              <button type="button" @click="selectCategory(category)" class="inline-flex w-full px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">{{ category }}</button>
            </li>
          </ul>
        </div>
      </div>
      <form class="flex h-10" @submit.prevent="submitSearch">

          <div class="relative w-full flex">
            <input type="search" v-model="searchQuery" id="search-dropdown" class="relative m-0 block flex-auto rounded border border-solid border-neutral-200 bg-transparent bg-clip-padding px-3 py-[0.25rem] text-base font-normal leading-[1.6] text-surface outline-none transition duration-200 ease-in-out placeholder:text-neutral-500 focus:z-[3] focus:border-primary focus:shadow-inset focus:outline-none motion-reduce:transition-none dark:border-white/10 dark:text-white dark:placeholder:text-neutral-200 dark:autofill:shadow-autofill dark:focus:border-primary" required />
            <button type="submit">
              <svg class="w-4 h-4" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">
                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z"/>
              </svg>
              <span class="sr-only">Search</span>
            </button>
            
          </div>
        
      </form>
  </div>
   
    
  </template>
  
  <script>
  export default {
    name: 'ChatSub',
    data() {

      return {
        dropdownVisible: false,
        selectedCategory: 'You Role',
        searchQuery: '',
        categories: ['Seller', 'Buyer']
      };
    },
    methods: {
      toggleDropdown() {
        this.dropdownVisible = !this.dropdownVisible;
      },
      selectCategory(category) {
        this.selectedCategory = category;
        this.dropdownVisible = false;
      },
      submitSearch() {
        // Handle the search submission here
        console.log(`Searching for "${this.searchQuery}" in category "${this.selectedCategory}"`);
      }
    }
  };
  </script>
  
  <style scoped>
  /* Add any scoped styles here */
  </style>
  