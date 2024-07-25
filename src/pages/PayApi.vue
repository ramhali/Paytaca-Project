<template>
  <q-page padding>
    <div v-if="!isPaid && !isExpired" class="q-pa-md column flex-center relative-center">
      <div class="column q-mb-md">
        <label>Scan the QR code below before the address expires</label>
      </div>

      <q-card class="my-card shadow-6">
        <q-card-section class="q-pb-sm flex flex-center">
          <transition appear leave-active-class="animated flipOutY slower">
            <vue-qrcode v-if="code" class="q-mt-md" :value="code" :size="250" level="H" />
          </transition>
        </q-card-section>

        <q-card-section class="q-py-sm q-px-md row flex-center q-col-gutter-xs">
          <q-btn flat no-caps color="accent" icon="content_copy" @click="copyAddress">
            <div class="ellipsis" style="width: 200px">{{ addressData }}</div>
          </q-btn>
        </q-card-section>

        <q-card-section class="q-pt-lg q-pb-xs">
          <div class="row items-center">
            <q-linear-progress size="5px" :value="time / timeSeconds" color="accent" class="q-mr-md" />
          </div>
          <div class="row items-center">
            {{ formattedTime }}
          </div>
        </q-card-section>

        <q-card-section>
          <div class="q-my-sm text-h6 flex flex-center text-weight-regular">{{ descData }}</div>
          <div class="text-subtitle1 flex flex-center text-weight-bold">BCH {{ amountData }}</div>
        </q-card-section>
      </q-card>
    </div>

    <div v-else-if="isExpired" class="q-pa-md column flex-center relative-center">
      <div class="column q-mb-md">
        <label>QR code expired!</label>
      </div>

      <q-card class="my-card shadow-6">
        <q-card-section class="q-pb-sm flex flex-center">
          <transition appear enter-active-class="animated flipInY slower">
            <q-img src="/src/assets/images/expired.png" alt="EXPIRED" height="250px" width="250px" />
          </transition>
        </q-card-section>

        <q-card-section class="q-py-sm q-px-md row flex-center q-col-gutter-xs">
          <q-btn flat no-caps color="accent" icon="content_copy" @click="copyAddress">
            <div class="ellipsis" style="width: 200px">{{ addressData }}</div>
          </q-btn>
        </q-card-section>

        <q-card-section class="q-pt-lg q-pb-xs">
          <div class="row items-center">
            <q-linear-progress size="5px" :value="time / timeSeconds" color="accent" class="q-mr-md" />
          </div>
          <div class="row items-center">
            {{ formattedTime }}
          </div>
        </q-card-section>

        <q-card-section>
          <div class="q-my-sm text-h6 flex flex-center text-weight-regular">{{ descData }}</div>
          <div class="text-subtitle1 flex flex-center text-weight-bold">BCH {{ amountData }}</div>
        </q-card-section>

        <q-card-section class="flex flex-center">
          <q-btn label="Click to Update BCH value" @click="updateBCH" color="accent" text-color="primary" rounded />
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
          <div class="text-subtitle1 flex flex-center text-weight-regular" style="color: #39a848;">Your Money, Your Control</div>
        </q-card-section>
      </q-card>
      <div v-if="countdown > 0" class="q-my-sm text-h6 flex flex-center text-weight-regular">Redirecting in {{ countdown }} seconds...</div>
    </div>
  </q-page>
</template>


<script setup>
import { api } from 'src/boot/axios';
import { computed, onBeforeUnmount, onMounted, onUnmounted, ref, watch } from 'vue';
import { useURLStore } from 'src/stores/urlstore';
import { useQuasar } from 'quasar';

const urlstore = useURLStore();
const url = urlstore.getUrl;
const $q = useQuasar();

const initTime = 90000; // milliseconds
const timeSeconds = initTime / 1000;

const addressData = ref(null);
const amountData = ref(null);
const descData = ref(null);
const orderID = ref(null);
const callback = ref(null);
const returnURL = ref(null);

const time = ref(0);
const timer = ref(null);
const pollTimer = ref(null);

const code = ref(null);
const isPaid = ref(false);
const isExpired = ref(false);
const countdown = ref(0);

const getResponse = async () => {
  try {
    const response = await api.get(`${url}`);
    addressData.value = response.data.address;
    amountData.value = response.data.amount_bch;
    descData.value = response.data.desc;
    isPaid.value = response.data.paid;
    orderID.value = response.data.order_id;
    callback.value = response.data.callback_url;
    returnURL.value = response.data.return_url;

    const currDate = new Date(response.data.created_at);
    const expiryDate = new Date(currDate.getTime() + initTime); // 1.5 minutes expiry
    const now = new Date();
    const remainingTime = Math.max(0, Math.floor((expiryDate - now) / 1000));
    time.value = remainingTime;

    generateQrCode(addressData.value, amountData.value);
    startTimer(expiryDate);
  } catch (error) {
    console.error("Error fetching data:", error);
    stopTimers(); // Stop timers on error
    $q.notify({ type: 'negative', message: 'Failed to fetch data!' });
  }
};

const generateQrCode = (addressData, amountData) => {
  code.value = `${addressData}?amount=${amountData}`;
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
      isExpired.value = true;
    }
  }, 1000);
};

const checkPaymentStatus = async () => {
  if (isExpired.value) {
    stopTimers();
    return;
  }

  try {
    const response = await api.get(`${url}`);
    isPaid.value = response.data.paid;

    if (isPaid.value) {
      stopTimers();
    }
  } catch (error) {
    console.error("Error checking payment status:", error);
    stopTimers();
    $q.notify({ type: 'negative', message: 'Failed to check payment status!' });
  }
};

const updateBCH = async () => {
  try {
    isExpired.value = false;

    const response = await api.put('account/transactions/', { address: addressData.value });

    if (response.data && response.data.updated_bch !== undefined) {
      amountData.value = response.data.updated_bch;
      generateQrCode(addressData.value, amountData.value);

      const curTime = new Date();
      const newTime = new Date(curTime.getTime() + initTime);

      startTimer(newTime);
    } else {
      throw new Error("Unexpected response format");
    }
  } catch (error) {
    console.error("Error in updateBCH PUT request:", error);
    $q.notify({ type: 'negative', message: 'Failed to update BCH value!' });
  }
};

const copyAddress = () => {
  navigator.clipboard.writeText(addressData.value).then(() => {
    $q.notify({ type: 'positive', message: 'Address copied to clipboard!' });
  }).catch(() => {
    $q.notify({ type: 'negative', message: 'Failed to copy address!' });
  });
};

const stopTimers = () => {
  clearInterval(timer.value);
  clearInterval(pollTimer.value);
  timer.value = null;
  pollTimer.value = null;
};

watch(isPaid, (newVal) => {
  if (newVal && returnURL.value) {
    countdown.value = 3;
    const countdownInterval = setInterval(() => {
      countdown.value -= 1;
      if (countdown.value <= 0) {
        clearInterval(countdownInterval);
        window.location.href = returnURL.value;
      }
    }, 1000);
  } else return
});

onMounted(() => {
  getResponse();
  pollTimer.value = setInterval(checkPaymentStatus, 5000); // Poll every 5 seconds
});

onUnmounted(() => {
  stopTimers();
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
