<template>
  <q-page class="flex flex-center justify-center">
    <q-form v-if="!loading" @submit="submitForm">
      <div>
        <q-card style="min-width: 400px;">
          <q-card-section>
            <label class="text-weight-bold">User Token</label>
            <q-input
              class="q-mx-md q-pb-none"
              v-model="urldata.token"
              borderless
              type="password"
              required
              :rules="[(val) => !!val || 'User Token cannot be empty']"
            />
          </q-card-section>
          <q-card-section>
            <label class="text-weight-bold">Amount</label>
            <q-input
              class="q-mx-md q-pb-none"
              v-model="urldata.amount"
              outlined
              required
              :rules="[(val) => !!val || 'Amount cannot be empty']"
            />
          </q-card-section>

          <!-- <q-badge color="accent">
            Model : {{ urldata.currency }}
          </q-badge> -->

          <q-card-section>
            <label class="text-weight-bold">Currency</label>

            <q-input
              class="q-mx-md q-pb-none"
              v-model="urldata.currency"
              outlined
              required
              :rules="[(val) => !!val || 'Amount cannot be empty']"
            />
          </q-card-section>

          <q-card-section>
            <label class="text-weight-bold">Description</label>
            <q-input
              class="q-mx-md q-pb-none"
              v-model="urldata.desc"
              outlined
              autogrow
            />
          </q-card-section>
        </q-card>
      </div>
    </q-form>
    <q-spinner v-else>Loading</q-spinner>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useQuasar } from 'quasar';
import { useURLStore } from 'src/stores/urlstore';
import { useRouter } from 'vue-router';

const $q = useQuasar();
const router = useRouter()
const urlstore = useURLStore();
const loading = true

const urldata = ref({
  token: '',
  amount: 0,
  currency: '',
  desc: '',
  orderID: '',
  callback: ''
});

const getQueryParams = async () => {
  const url = new URL(window.location.href);
  const params = new URLSearchParams(url.search);
  const queryParams = Object.fromEntries(params);

  console.log(url.search);
  console.log("Query Params",queryParams);

  urldata.value.token = queryParams.token;
  urldata.value.amount = queryParams.amount;
  urldata.value.currency = queryParams.currency;
  urldata.value.desc = queryParams.desc;
  urldata.value.orderID = queryParams.order_id;
  urldata.value.callback = queryParams.callback;

  console.log(urldata.value.orderID);
}

const fetchURL = async () => {
  try {
    const response = await axios.get('http://localhost:8000/pay/', {
      params: {
        token: urldata.value.token,
        amount: urldata.value.amount,
        currency: urldata.value.currency,
        desc: urldata.value.desc,
        order_id: urldata.value.orderID,
        callback: urldata.value.callback
      }
    });

    const fetchedURL = response.data.url;

    console.log("Fetched URL",fetchedURL);
    urlstore.storeURL(fetchedURL);
    router.replace('/pay/payredirect');

    // $q.notify({ type: 'positive', message: 'URL fetched successfully!' });
  } catch (error) {
    console.error(error);
    $q.notify({ type: 'negative', message: 'Failed to fetch URL!' });
  }
};

const submitForm = async (event) => {
  event.preventDefault();
  try {
    await fetchURL();
  } catch (error) {
    console.error(error);
    $q.notify({ type: 'negative', message: 'Payment failed!' });
  }
};

onMounted(()=>{
  getQueryParams()
  fetchURL()
})


</script>
