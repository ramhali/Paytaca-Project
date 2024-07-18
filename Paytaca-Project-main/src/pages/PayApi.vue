<template>
  <q-page padding>
    <div v-if="is_not_paid" class="q-pa-md column flex-center relative-center">
      <div class="column q-mb-md">
        <label>Scan the qr code below before the address expires</label>
      </div>
      <!-- 

      <q-card style="width:500px;" class="q-pa-xs q-mt-sm column shadow-7">
        <q-card-section class="q-pb-xs flex flex-center">
          <label class="text-bold">{{ descData }}</label>
        </q-card-section>

        <q-card-section class="flex flex-center">
          <vue-qrcode
            class="q-mb-sm"
            :value="code"
            :size=250
            level="H"
          />
        </q-card-section>

        <q-card-section class="q-px-md row flex-center q-col-gutter-xs">
          <q-btn round color="accent" icon="content_copy" />
          <label><strong>{{ addressData }}</strong></label>
        </q-card-section> -->
      
      <q-card class="my-card shadow-6">
        
          <q-card-section class="q-pb-sm flex flex-center">
            <transition
              appear
              leave-active-class="animated flipOutY slower"
            >
            <vue-qrcode
              class="q-mt-md"
              :value="code"
              :size=250
              level="H"
            />
          </transition>
          </q-card-section>
        

        <q-card-section class="q-py-sm q-px-md row flex-center q-col-gutter-xs">
            <q-btn flat no-caps color="accent" icon="content_copy">
              <div class="ellipsis" style="width: 200px">
                {{ addressData }}
              </div>
            </q-btn>
        </q-card-section>

        <q-card-section class="q-pt-lg q-pb-xs">
          <div class="row items-center">
            <q-linear-progress size="5px" :value="time/120" color="accent" class="q-mr-md" />
          </div>
        </q-card-section>

        <q-card-section>
          <div class="q-my-sm text-h6 flex flex-center text-weight-regular"> {{ descData }}</div>
          <div class="text-subtitle1 flex flex-center text-weight-bold">BCH {{ amountData }}</div>
        </q-card-section>
      </q-card>
    </div>

    <div v-else class="q-pa-md column flex-center relative-center">
      <div class="column q-mb-md">
        <label>Transaction Done!</label>
      </div>

      <q-card class="my-card shadow-6">
        <q-card-section class="q-pa-none">
          <transition
              appear
              enter-active-class="animated flipInY slower"
            >
            <q-img src="/src/assets/images/paid_logo.png" alt="PAID" height="250px" width="250px"/>
          </transition>
        </q-card-section>

        <q-card-section>
          <div class="q-my-sm text-h6 flex flex-center text-weight-bolder" style="color: #39a848;"> Paytaca </div>
          <div class="text-subtitle1 flex flex-center text-weight-regular" style="color: #39a848;"> Your Money, Your Control </div>
        </q-card-section>
      </q-card>
    </div>
  </q-page>
</template>

<script setup>
import { api } from 'src/boot/axios';
import { onMounted, ref, computed } from 'vue';

let addressData = ref(null)
let amountData = ref(null)
let descData = ref(null)

let code = ref(null)

const time = ref(120);
const timer = ref(null);

let is_not_paid = false

const getResponse = async ()=>{
  const response = await api.get('http://localhost:8000/pay/redirected?amount=111.50&currency=PHP&desc=My%20First%20Order&amount_bch=0.005661047928513403736799350122&address=bitcoincash:qrwzzj6w3uq2ztp2h2gqergkvjf660h9wyg5exj6w9')

  addressData.value = response.data.address
  amountData.value = response.data.amount_bch
  descData.value = response.data.desc

  generateQrCode(addressData.value, amountData.value)

  console.log("Code used to generate QR", response.data);
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
