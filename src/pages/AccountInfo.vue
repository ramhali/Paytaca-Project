<template>
  <q-page padding class="flex flex-center justify-center">
    <q-form v-if="!loading" @submit="updateWalletInfo">
      <div>
        <q-card style="min-width: 450px;">
          <div class="flex flex-center justify-center">
            <h5 class="q-my-xs q-pt-sm">Account</h5>
          </div>

          <q-card-section class="q-py-sm">
            <label class="text-weight-bold">User Token</label>
            <q-input
              class="q-mx-md q-pb-none"
              v-model="user_token"
              readonly
              borderless
              required
              :rules="[(val) => !!val || 'xPub field cannot be empty']"
            />
          </q-card-section>

          <q-separator color="accent" inset />

          <div class="q-px-sm">
            <h6 class="q-my-xs q-pt-sm flex flex-center">Wallet Details</h6>
          </div>

          <q-card-section class="q-pt-sm">
            <label class="text-weight-bold">xPub Key</label>
            <label v-if="!is_connected" style="font-weight: bold; color: red">(Not Connected)</label>
            <label v-else style="font-weight: bold; color: green">(Connected)</label>

            <q-input
              v-if="is_connected"
              class="q-px-md q-mt-sm"
              v-model="xpub_key"
              readonly
              draggable="false"
              borderless
              required
              autogrow
              bg-color="secondary"
            />
            <q-input
              v-else
              class="q-px-md q-mt-sm"
              v-model="xpub_key"
              borderless
              required
              autogrow
              bg-color="secondary"
              :rules="[(val) => !!val || 'Wallet Hash field cannot be empty']"
            />

            <label class="text-weight-bold">Wallet Hash</label>
            <label v-if="!is_connected" style="font-weight: bold; color: red">(Not Connected)</label>
            <label v-else style="font-weight: bold; color: green">(Connected)</label>

            <q-input
              v-if="is_connected"
              class="q-px-md q-mt-sm"
              v-model="wallet_hash"
              readonly
              draggable="false"
              borderless
              required
              autogrow
              bg-color="secondary"
            />
            <q-input
              v-else
              class="q-px-md q-mt-sm"
              v-model="wallet_hash"
              borderless
              required
              autogrow
              bg-color="secondary"
              :rules="[(val) => !!val || 'Wallet Hash field cannot be empty']"
            />

            <q-separator v-if="!is_connected" color="accent" />

            <div class="flex flex-center">
              <q-btn
                v-if="!is_connected"
                class="q-mt-md"
                label="Enter wallet details"
                type="submit"
                color="accent"
                text-color="primary"
              />
            </div>
          </q-card-section>
        </q-card>
      </div>
    </q-form>
    <q-spinner v-else size="lg" color="accent"></q-spinner> <!-- Spinner to indicate loading -->
  </q-page>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useAuthStore } from 'src/stores/auth';
import { api } from 'src/boot/axios';

const authStore = useAuthStore();
const token = authStore.getToken();

let xpub_key = ref(null);
let wallet_hash = ref(null);
let user_token = ref(null);
let is_connected = ref(false);
let loading = ref(true);

const fetchAccountData = async () => {
  try {
    const response = await api.get('', {
      headers: {
        'Authorization': `Token ${token}`,
        'Content-Type': 'application/json',
      }
    });

    xpub_key.value = response.data.xpub_key;
    wallet_hash.value = response.data.wallet_hash;
    user_token.value = response.data.token;

    const walletGet = await api.get('/account/wallet-info', {
      headers: {
        'Authorization': `Token ${token}`,
        'Content-Type': 'application/json',
      }
    });

    if (walletGet.status === 'Empty') {
      is_connected.value = false;
    } else if (walletGet.data && walletGet.data.length > 0) {
      is_connected.value = walletGet.data[0].is_connected;
    } else {
      is_connected.value = false;
    }
  } catch (error) {
    console.log(error);
  } finally {
    loading.value = false;
  }
};

const updateWalletInfo = async () => {
  try {
    const data = {
      xpub_key: xpub_key.value,
      wallet_hash: wallet_hash.value
    };

    const walletPost = await api.post('account/wallet-info/', data, {
      headers: {
        'Authorization': `Token ${token}`,
        'Content-Type': 'application/json'
      }
    });
    window.location.reload();
    console.log(walletPost.data);
  } catch (error) {
    console.error('Error updating wallet info:', error.response ? error.response.data : error.message);
  }
};

onMounted(() => {
  fetchAccountData();
});
</script>
