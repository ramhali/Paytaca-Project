import { defineStore } from 'pinia';
import axios from 'axios';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    isLoggedIn: false,
    user: JSON.parse(localStorage.getItem('user')) || null,
    account: {
      username: '',
      token: '',
      xpub_key: '',
      wallet_hash: '',
      store_name: '',
    },
  }),
  actions: {
    login(token, user) {
      this.token = token;
      this.user = user;
      this.isLoggedIn = true;
      console.log(token);
      localStorage.setItem('token', this.token);
      localStorage.setItem('user', JSON.stringify(user));
      axios.defaults.headers.common['Authorization'] = `Token ${this.token}`;
      axios.defaults.headers.common['Content-Type'] = 'application/json';
      console.log("Logged In")
    },
    logout() {
      this.token = null;
      this.user = null;
      this.isLoggedIn = false;
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      delete axios.defaults.headers.common['Authorization'];
      console.log("Logged Out")
    },
    setUser(user) {
      this.user = user;
      localStorage.setItem('user', JSON.stringify(user));
    },
    getToken() {
      return this.token
    }
  },
  getters: {
    getUser() {
      return this.user || "User";
    },
  },

});
