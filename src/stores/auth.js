import { defineStore } from 'pinia';
import axios from 'axios';
import { api } from 'src/boot/axios';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    isLoggedIn: !!localStorage.getItem('token'),
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
    },
    logout() {
      this.token = null;
      this.user = null;
      this.isLoggedIn = false;
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      delete axios.defaults.headers.common['Authorization'];
    },
    setUser(user) {
      this.user = user;
      localStorage.setItem('user', JSON.stringify(user));
    },
     async fetchAccountData() {
      try {
        const response = await api.get('', {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${this.token}`
          },
        })
        this.account = response.data;

        // console.log("Account: ",this.account)
        // console.log("Response: ",response)

      } catch (error) {
        console.error('Error fetching account:', error)
      }
    },
  },
  getters: {
    getUser() {
      return this.user || "User";
    }
  },

});
