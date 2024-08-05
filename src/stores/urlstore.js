import { defineStore } from 'pinia';

export const useURLStore = defineStore('urlstore', {
  state: () => ({
    url: null || localStorage.getItem('url')
  }),
  actions: {
    storeURL(url){
      this.url = url
      localStorage.setItem('url', this.url);
    },
    removeURL(url){
      this.url = null
      localStorage.removeItem('url')
    }
  },
  getters: {
    getUrl (){
      return this.url
    }
  }
});
