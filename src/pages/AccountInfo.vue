<template>
  <q-page padding class="flex flex-center justify-center">
    <div>
      <q-card style="width: 600px;">
        <q-card-section>
          <label>Enter xPub Key:</label>
          <q-input filled v-model="xKey" label="xPub" stack-label required
          :rules="[(val) => !!val || 'xPub field cannot be empty']"
          />
          <label>Enter Wallet Hash:</label>
          <q-input filled v-model="walletHash" label="Wallet Hash" stack-label required
          :rules="[(val) => !!val || 'Wallet Hash field cannot be empty']" />
        </q-card-section>

        <q-separator color="accent" inset />

        <q-card-section>
          <label>Username:</label>
            <q-input v-model="username" readonly filled/>
          <label>Storename:</label>
            <q-input v-model="storename" readonly filled/>
          <label>Password:</label>
            <q-input v-model="password" readonly filled/>
        </q-card-section>

      </q-card>
    </div>
  </q-page>

</template>

<script setup>
  import { ref } from 'vue';

  const xKey = ref('samplexpub')
  const walletHash = ref('samplewallethash')
  const username = ref(null)
  const storename = ref(null)
  const password = ref(null)

</script>
