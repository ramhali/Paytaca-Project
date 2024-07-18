<template>
  <q-page padding class="flex flex-center justify-center">
    <!-- Display form only when not loading -->
    <q-form v-if="!loading" @submit="updateWalletInfo">
      <div>
        <q-card style="min-width: 500px;">
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
              :type="is_connected ? 'text' : 'password'"
              :rules="[(val) => !!val || 'User Token cannot be empty']"

            />
          </q-card-section>

          <q-separator color="accent" inset />

          <div class="q-px-sm">
            <h6 class="q-my-xs q-pt-sm flex flex-center">Wallet Details</h6>
          </div>

          <q-card-section class="q-pt-sm">
            <label class="text-weight-bold">xPub Key</label>
            <label :style="{ fontWeight: 'bold', color: is_connected ? 'green' : 'red' }">
              {{ is_connected ? '(Connected)' : '(Not Connected)' }}
            </label>
            <div class="flex flex-center">
              <q-input
              class="q-px-md q-mt-sm"
              style="min-width:  450px;"
              v-model="xpub_key"
              :readonly="is_connected && readonlyXpub"
              draggable="false"
              borderless
              required
              autogrow
              :bg-color="readonlyXpub ? 'primary' : 'secondary'"
              :rules="[(val) => !!val || 'xPub Key cannot be empty']"
            />
            <q-icon
              v-if="is_connected"
              :name="readonlyXpub ? 'edit' : 'send'"
              class="cursor-pointer"
              size="20px"
              @click="toggleReadonly('xpub')"
            >
            <q-tooltip>{{readonlyXpub ? 'Edit Xpub Key': 'Confirm Changes'}}</q-tooltip>
            </q-icon>
            </div>

            <label class="text-weight-bold">Wallet Hash</label>
            <label :style="{ fontWeight: 'bold', color: is_connected ? 'green' : 'red' }">
              {{ is_connected ? '(Connected)' : '(Not Connected)' }}
            </label>
            <div class="flex flex-center">
              <q-input
              class="q-px-md q-mt-sm"
              style="min-width:  450px;"
              v-model="wallet_hash"
              :readonly="is_connected && readonlyWalletHash"
              draggable="false"
              borderless
              required
              autogrow
              :bg-color="readonlyWalletHash ? 'primary' : 'secondary'"
              :rules="[(val) => !!val || 'Wallet Hash cannot be empty']"
            />
            <q-icon
              v-if="is_connected"
              :name="readonlyWalletHash ? 'edit' : 'send'"
              class="cursor-pointer"
              size="20px"
              @click="toggleReadonly('walletHash')"
            >
              <q-tooltip>{{readonlyWalletHash ? 'Edit Wallet Hash': 'Confirm Changes'}}</q-tooltip>
            </q-icon>
            </div>

            <q-separator v-if="!is_connected" color="accent" />

            <div class="flex flex-center">
              <q-btn
                v-if="!is_connected"
                class="q-mt-md"
                label="Enter Wallet Details"
                type="submit"
                color="accent"
                text-color="primary"
                no-caps
              />

            </div>
          </q-card-section>
        </q-card>
      </div>
    </q-form>
    <!-- Spinner to indicate loading -->
    <q-spinner v-else size="lg" color="accent">Loading</q-spinner>
  </q-page>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useAuthStore } from 'src/stores/auth';
import { api } from 'src/boot/axios';
import { useQuasar } from 'quasar';

const authStore = useAuthStore();
const token = authStore.getToken();
const $q = useQuasar()

const xpub_key = ref(null);
const wallet_hash = ref(null);
const user_token = ref(null);
const is_connected = ref(false);
const loading = ref(true);
const readonlyXpub = ref(true);
const readonlyWalletHash = ref(true);

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
    console.error('Error fetching account data:', error);
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

    await api.post('account/wallet-info/', data, {
      headers: {
        'Authorization': `Token ${token}`,
        'Content-Type': 'application/json'
      }
    });
    $q.notify({
      type: 'positive',
      icon: 'cloud_done',
      message: 'Wallet Connected!',
      timeout: 2000
    });

    window.location.reload();
  } catch (error) {
    console.error('Error updating wallet info:', error.response ? error.response.data : error.message);
  }
};


const toggleReadonly = async (field) => {
  if (field === 'xpub') {
    if (!readonlyXpub.value) {
      await updateField('xpub_key', xpub_key.value);
    }
    readonlyXpub.value = !readonlyXpub.value;
  } else if (field === 'walletHash') {
    if (!readonlyWalletHash.value) {
      await updateField('wallet_hash', wallet_hash.value);
    }
    readonlyWalletHash.value = !readonlyWalletHash.value;
  }
};

const updateField = async (field, value) => {
  try {
    const data = {
      xpub_key: xpub_key.value,
      wallet_hash: wallet_hash.value
    };
    const response = await api.put('account/wallet-info/', data, {
      headers: {
        'Authorization': `Token ${token}`,
        'Content-Type': 'application/json'
      }
    });
    console.log(response);
    $q.notify({
      type: 'positive',
      icon: 'cloud_done',
      message: 'Wallet Updated!',
      timeout: 2000
    });
  } catch (error) {
    console.error( error.response ? error.response.data : error.message);
  }
};

onMounted(() => {
  fetchAccountData();

});
</script>
