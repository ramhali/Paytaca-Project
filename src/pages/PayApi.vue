<template>
  <q-page padding>
    <div class="flex flex-center justify-center">
      <q-card style="width:500px;" class="q-pa-lg">
        <q-card-section class="flex flex-center">
          <vue-qrcode
            v-if="code!==null"
            class="q-mb-sm"
            :value="code"
            :size=300
            level="H"
          />
        </q-card-section>
        <q-card-section class="flex flex-center">
          <!-- <label>{{ addressData }}</label> -->
           <q-btn class="text-body1" flat icon="content_copy" color="accent" no-caps>
            <div class="ellipsis" style="width: 200px;">
              {{ addressData }}
            </div>
           </q-btn>
        </q-card-section>

        <q-card-section>
          <div class="flex ">
            <q-linear-progress size="5px" :value="time/120" color="accent" />
            <p>{{ formattedTime }}</p>
          </div>
        </q-card-section>
      </q-card>
    </div>
  </q-page>
</template>

<script setup>
import { api } from 'src/boot/axios';
import { computed, onMounted, ref } from 'vue';

let addressData = ref(null)
let amountData = ref(null)

const time = ref(120);
const timer = ref(null);

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
  startTimer()
}

const formattedTime = computed(() => {
  const minutes = Math.floor(time.value / 60);
  const seconds = time.value % 60;
  return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
});

const startTimer = () => {
  if (timer.value) return; // Prevent multiple intervals
  timer.value = setInterval(() => {
    if (time.value <= 0) {
      clearInterval(timer.value);
      timer.value = null;
    } else {
      time.value--;
    }
  }, 1000);
};

onMounted (()=>{
  getResponse()
})





</script>
