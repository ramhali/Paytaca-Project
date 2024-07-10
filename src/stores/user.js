import { defineStore } from 'pinia';
import axios from 'axios';

export const useUserStore = defineStore('user', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user')) || null,
    xpubKey: localStorage.getItem('xpub_key') || null,
    walletHash: localStorage.getItem('wallet_hash') || null,
    storeName: localStorage.getItem('store_name') || null,
  }),
  actions: {
    async fetchUserData() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/');
        console.log(response.data);
        const data = response.data;
        this.user = { username: data.username };
        this.xpubKey = data.xpub_key;
        this.walletHash = data.wallet_hash;
        this.storeName = data.store_name;

        localStorage.setItem('user', JSON.stringify({ username: data.username }));
        localStorage.setItem('xpub_key', data.xpub_key);
        localStorage.setItem('wallet_hash', data.wallet_hash);
        localStorage.setItem('store_name', data.store_name);
      } catch (error) {
        console.error('Error fetching user data:', error);
      }
    },
  },
  getters: {
    getUser() {
      return this.user ? this.user.username : "User";
    },
    getXpubKey() {
      return this.xpubKey;
    },
    getWalletHash() {
      return this.walletHash;
    },
    getStoreName() {
      return this.storeName;
    }
  }
});
