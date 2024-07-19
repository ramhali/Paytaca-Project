<template>
  <q-page padding>
    <div v-if="!isPaid" class="q-pa-md column flex-center relative-center">
      <div class="column q-mb-md">
        <label>Scan the qr code below before the address expires</label>
      </div>

      <q-card class="my-card shadow-6">
        <q-card-section class="q-pb-sm flex flex-center">
          <transition appear leave-active-class="animated flipOutY slower">
            <vue-qrcode v-if="code !== null" class="q-mt-md" :value="code" :size="250" level="H" />
          </transition>
        </q-card-section>

        <q-card-section class="q-py-sm q-px-md row flex-center q-col-gutter-xs">
          <q-btn flat no-caps color="accent" icon="content_copy">
            <div class="ellipsis" style="width: 200px">{{ addressData }}</div>
          </q-btn>
        </q-card-section>

        <q-card-section class="q-pt-lg q-pb-xs">
          <div class="row items-center">
            <q-linear-progress size="5px" :value="time / 120" color="accent" class="q-mr-md" />
          </div>
        </q-card-section>

        <q-card-section>
          <div class="q-my-sm text-h6 flex flex-center text-weight-regular">{{ descData }}</div>
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
          <transition appear enter-active-class="animated flipInY slower">
            <q-img src="/src/assets/images/paid_logo.png" alt="PAID" height="250px" width="250px" />
          </transition>
        </q-card-section>

        <q-card-section>
          <div class="q-my-sm text-h6 flex flex-center text-weight-bolder" style="color: #39a848;">Paytaca</div>
          <div class="text-subtitle1 flex flex-center text-weight-regular" style="color: #39a848;">Your Money, Your
            Control</div>
        </q-card-section>
      </q-card>
    </div>
  </q-page>
</template>

<script setup>
import { api } from 'src/boot/axios';
import { computed, onMounted, onUnmounted, ref } from 'vue';
import { useURLStore } from 'src/stores/urlstore';
import axios from 'axios';

const urlstore = useURLStore();

let addressData = ref(null);
let amountData = ref(null);
let descData = ref(null);


const time = ref(120);
const timer = ref(null);
const pollTimer = ref(null);

let code = ref(null);
let isPaid = ref(false);

const getQueryParams = async () => {
  const url = new URL(window.location.href);
  const params = new URLSearchParams(url.search);
  const queryParams = Object.fromEntries(params);

  console.log(url.search);
  console.log(queryParams);

  const urldata = {
    token: queryParams.token,
    amount: queryParams.amount,
    currency: queryParams.currency,
    desc: queryParams.desc
  }

  try {
    const response = await axios.get('http://localhost:8000/pay', {
      params: {
        token: urldata.token,
        amount: urldata.amount,
        currency: urldata.currency,
        desc: urldata.desc,
      }
    });

    const fetchedURL = response.data.url;

    console.log("Fetched URL",fetchedURL);
    urlstore.storeURL(fetchedURL);

    console.log(fetchedURL);
    getResponse(fetchedURL)
  } catch (error) {
    console.error(error);
  }
}

const getResponse = async (urldata) => {
  const response = await api.get(`${urldata}`);
  addressData.value = response.data.address;
  amountData.value = response.data.amount_bch;
  descData.value = response.data.desc;
  isPaid.value = response.data.paid;

  console.log("Response Data:\n", response.data);

  const currDate = new Date(response.data.created_at);
  const expiryDate = new Date(currDate.getTime() + 2 * 60 * 1000);
  const now = new Date();
  const remainingTime = Math.max(0, Math.floor((expiryDate - now) / 1000));
  time.value = remainingTime;

  console.log("Current Date: ", currDate);
  console.log("Expiry Date: ", expiryDate);

  startTimer(expiryDate);
  generateQrCode(addressData.value, amountData.value);
};

const generateQrCode = (addressData, amountData) => {
  code.value = `${addressData}?amount=${amountData}`;
  console.log("Code used to generate QR", code.value);
};

const formattedTime = computed(() => {
  const minutes = Math.floor(time.value / 60);
  const seconds = time.value % 60;
  return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
});

const startTimer = (endDate) => {
  if (timer.value) return; // Prevent multiple intervals
  timer.value = setInterval(() => {
    const now = new Date();
    const remainingTime = Math.max(0, endDate - now);
    time.value = Math.floor(remainingTime / 1000);

    if (remainingTime <= 0) {
      clearInterval(timer.value);
      timer.value = null;
      urlstore.removeURL();
    }
  }, 1000);
};

const checkPaymentStatus = async () => {
  const response = await api.get(`${urlstore.getUrl}`);
  isPaid.value = response.data.paid;
  if (isPaid.value) {
    clearInterval(pollTimer.value);
    pollTimer.value = null;
  }
};

onMounted(() => {
  getQueryParams()
  pollTimer.value = setInterval(checkPaymentStatus, 5000); // Poll every 5 seconds
});

onUnmounted(() => {
  clearInterval(timer.value);
  clearInterval(pollTimer.value);
  urlstore.removeURL();
});
</script>

<style scoped>
.ellipsis {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
