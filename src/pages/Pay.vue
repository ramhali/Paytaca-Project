<template>
  <q-page class="flex flex-center justify-center">
    <q-form  @submit="submitForm">
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
            <q-select
              class="q-mx-md q-pb-none"
              v-model="urldata.currency"
              :options="options"
              option-label="currency"
              option-value="currency"
              outlined
              required
              :rules="[(val) => !!val || 'Currency cannot be empty']"
            >
            <template v-slot:option="scope">
              <q-item v-bind="scope.itemProps">
                <q-item-section>
                  <q-item-label>{{ scope.opt.currency }}</q-item-label>
                  <q-item-label caption>{{ scope.opt.name }}</q-item-label>
                </q-item-section>
              </q-item>
            </template>
            </q-select>
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
          <q-card-section>
            <div class="flex flex-center">
              <q-btn  label="Pay" type="submit" color="accent"
                text-color="primary" no-caps />
            </div>
          </q-card-section>
        </q-card>
      </div>
    </q-form>
  </q-page>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import { useQuasar } from 'quasar';
import { useURLStore } from 'src/stores/urlstore';
import { useRouter } from 'vue-router';
import optionsData from 'src/assets/countries-info.json'

const $q = useQuasar();
const router = useRouter()
const urlstore = useURLStore();
const options = optionsData

const urldata = ref({
  token: '4tDFHEJsPxLcCtvn',
  amount: 0,
  currency: options[167],
  desc: ''
});

const fetchURL = async () => {
  try {
    const response = await axios.get('http://localhost:8000/pay/', {
      params: {
        token: urldata.value.token,
        amount: urldata.value.amount,
        currency: urldata.value.currency['currency'],
        desc: urldata.value.desc,
      }
    });

    const fetchedURL = response.data.url;
    urlstore.storeURL(fetchedURL);
    router.push('/pay/payredirect');

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


// onMounted(()=>{
//   console.log(options);
// })


</script>
