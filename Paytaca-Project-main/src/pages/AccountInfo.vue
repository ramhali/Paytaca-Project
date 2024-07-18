<template>
  <q-page padding class="flex flex-center justify-center">
    <div>
      <!-- <q-card style="width: 600px;"> -->
        <q-card style="min-width: 450px;">
        <div class="flex fkex-center justify-center">
          <h5 class="q-my-sm q-pa-sm ">Account</h5>
        </div>

        <q-separator color="accent" inset />

        <q-card-section class="q-pt-sm">
          <label>xPub Key</label>
          <q-input
            class="q-pa-md"
            v-model="account.xpub_key"
            readonly
            borderless
            required
            autogrow
            bg-color="secondary"
            :rules="[(val) => !!val || 'xPub field cannot be empty']"
          />
          <label>Wallet Hash </label>
          <q-input
            v-model="account.wallet_hash"
            class="q-pa-md"
            readonly
            borderless
            required
            autogrow
            bg-color="secondary"
            :rules="[(val) => !!val || 'Wallet Hash field cannot be empty']" />
        </q-card-section>

        <q-separator color="accent" inset />

        <q-card-section>
          <label>Username:</label>
            <q-input
              v-model="account.username"
              class="q-pa-md"
              readonly
              borderless
              bg-color="secondary"/>
          <label>Storename:</label>
            <q-input
              v-model="account.store_name"
              class="q-pa-md"
              readonly
              borderless
              bg-color="secondary"/>
        </q-card-section>

      </q-card>
    </div>
  </q-page>

</template>

<script setup>
import { onBeforeMount, onMounted , onUnmounted } from 'vue';
import { useAuthStore } from 'src/stores/auth';

const authStore = useAuthStore()
const { account } = authStore

const getData = async  () => {
  authStore.fetchAccountData()
}

onBeforeMount(()=>{
  console.log("before mounted")
})

onMounted (()=>{
  getData()
  console.log("mounted");
})



onUnmounted (()=>{
  getData()
  console.log("unmounted");
})


</script>
