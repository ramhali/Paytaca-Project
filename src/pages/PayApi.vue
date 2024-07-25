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
          <q-btn flat no-caps color="accent" icon="content_copy">
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
          <transition appear leave-active-class="animated flipOutY slower">
            <vue-qrcode v-if="code" class="q-mt-md" :value="code" :size="250" level="H" />
          </transition>
        </q-card-section>

        <q-card-section class="q-py-sm q-px-md row flex-center q-col-gutter-xs">
          <q-btn flat no-caps color="accent" icon="content_copy">
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
    </div>
  </q-page>
</template>

<script setup>
import { api } from 'src/boot/axios';
import { computed, onMounted, onUnmounted, ref } from 'vue';
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
const orderID = ref(null)
const callback = ref(null)

const time = ref(0);
const timer = ref(null);
const pollTimer = ref(null);

// const progress = ref(null);
const code = ref(null);
const isPaid = ref(false);
const isExpired = ref(false);

const getResponse = async () => {
  try {
    const response = await api.get(`${url}`);
    addressData.value = response.data.address;
    amountData.value = response.data.amount_bch;
    descData.value = response.data.desc;
    isPaid.value = response.data.paid;
    orderID.value = response.data.order_id;
    callback.value = response.data.callback;

    console.log("Response Data:\n", response.data);

    const currDate = new Date(response.data.created_at);
    const expiryDate = new Date(currDate.getTime() + initTime); // 1.5 minutes expiry
    const now = new Date();
    const remainingTime = Math.max(0, Math.floor((expiryDate - now) / 1000));
    time.value = remainingTime;

    console.log("Current Date: ", currDate);
    console.log("Expiry Date: ", expiryDate);

    generateQrCode(addressData.value, amountData.value);
    startTimer(expiryDate);


  } catch (error) {
    console.error("Error fetching data:", error);
  }
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

    console.log("Remaining Time: ", remainingTime);

    if (remainingTime <= 0) {
      clearInterval(timer.value);
      timer.value = null;
      isExpired.value = true;
      console.log("isExpired set to ", isExpired.value);
    }
  }, 1000);


};

const checkPaymentStatus = async () => {
  if (isExpired.value) {
    // Stop checking if expired
    if (pollTimer.value) {
      clearInterval(pollTimer.value);
      pollTimer.value = null;
    }
    return;
  }

  try {
    const response = await api.get(`${url}`);
    isPaid.value = response.data.paid;

    if (isPaid.value) {
      clearInterval(pollTimer.value);
      pollTimer.value = null;

      const response2 = await api.post(`${url}`);

      console.log("Paid Response",response2.data);
    }
  } catch (error) {
    $q.notify({ type: 'negative', message: 'Failed to check payment status!' });
    console.error("Error checking payment status:", error);
  }
};

const updateBCH = async () => {
  try {
    console.log("Address: ", addressData.value);
    isExpired.value = false;
    console.log("isExpired set to ", isExpired.value);

    const response = await api.put('account/transactions/', { address: addressData.value });
    console.log("updateBCH PUT request:", response.data);

    amountData.value = response.data.value

    generateQrCode(addressData.value,  amountData.value);

    const curTime = new Date();
    const newTime = new Date(curTime.getTime() + initTime);
    console.log("Current Time: ", curTime, "\nNew Time: ", newTime);

    startTimer(newTime);

  } catch (error) {
    console.error("Error in updateBCH PUT request:", error);
  }
};

onMounted(() => {
  getResponse();
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
