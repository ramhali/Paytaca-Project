<template>
  <q-page padding>

    <h2>PayApi</h2>
    <div class="flex flex-center justify-center">
      <q-card style="width:500px;" class="q-pa-lg">
        <q-card-section class="flex flex-center">
          <vue-qrcode
            class="q-mb-sm"
            :value="code"
            :size=300
            level="H"
          />
        </q-card-section>
        <q-card-section class="flex flex-center">
          <label>{{ addressData }}</label>
        </q-card-section>
      </q-card>
    </div>
  </q-page>
</template>

<script setup>
import { api } from 'src/boot/axios';
import { onMounted, ref } from 'vue';

let addressData = ref(null)
let amountData = ref(null)

let code = ref(null)

const getResponse = async ()=>{
  const response = await api.get('/pay/redirected?amount=111.50&currency=PHP&amount_bch=0.005584773353368394690708740296&address=bitcoincash:qzu63ymznxeywuwwhwslxu9pq46vpwzd4vq4scsvp3')

  addressData.value = response.data.address
  amountData.value = response.data.amount_bch

  generateQrCode(addressData.value, amountData.value)
}

const generateQrCode = (addressData, amountData) => {
  code.value = addressData + '?amount=' + amountData
  console.log("Code used to generate QR", code.value);
}


onMounted (()=>{
  getResponse()
})





</script>
