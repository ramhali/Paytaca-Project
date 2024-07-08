import { defineStore } from 'pinia';

export const authStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: null,
    isLoggedIn: !!localStorage.getItem('token')
  }),
  actions: {
    login(token, user) {
      this.token = token;
      this.user = user;
      this.isLoggedIn = true;
      localStorage.setItem('token', token);
    },
    logout() {
      this.token = null;
      this.user = null;
      this.isLoggedIn = false;
      localStorage.removeItem('token');
    },
    setUser(user) {
      this.user = user;
    }
  }
});
