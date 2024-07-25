<template>
  <q-page class="q-pa-lg">
    <div v-if="!loading">
      <div class="text-h2 q-my-md">
      <label class="text-weight-regular">
        Dashboard
      </label>
      </div>
      <div class="dashboard q-my-lg row justify-evenly">
        <q-card class="bch-value q-my-lg"  style="color: white;">
          <q-card-section class="q-pt-md q-pb-sm text-weight-bold"  style="width: 250px;">
            BCH VALUE
          </q-card-section>

          <q-card-section class=" " >
            {{ currentBCH }}
          </q-card-section>
        </q-card>

        <q-card class="total-income q-my-lg"  style="color: white;">
          <q-card-section class="q-pt-md q-pb-sm text-weight-bold" style="width: 250px; ">
            TOTAL INCOME
          </q-card-section>

          <q-card-section class="q-py-md ">
            BCH {{ amount_total }}
          </q-card-section>
        </q-card>

        <q-card class="transactions q-my-lg"  style="color: white;">
          <q-card-section class="q-pt-md q-pb-sm text-weight-bold" style="width: 250px;">
            TRANSACTIONS COMPLETED
          </q-card-section>

          <q-card-section class="q-py-md ">
            {{ transaction_count || 0 }}
          </q-card-section>
        </q-card>
      </div>

      <div class="dashboard-table q-my-lg q-pt-lg">
        <q-card flat style="background-color: transparent;">
          <q-card-section>
            <div class="text-h6">Recent Transactions</div>
          </q-card-section>

          <q-card-section class="q-px-lg">
            <div v-if="!data" style="font-size: 1.5em;">
              No Data...
            </div>

            <q-table
              v-else
              :rows="data"
              :columns="columns"
              :hide-pagination="true"
              flat
              row-key="id"
              separator="horizontal"
              draggable="false"
              class="medium-text"
              no-data-label="Connect wallet on account info tab to start selling"
              style="background-color: transparent"
            >
              <template v-slot:body-cell-tx_id="props">
                <q-td :props="props">
                  <div class="ellipsis">{{ props.row.tx_id }}</div>
                </q-td>
              </template>
              <template v-slot:body-cell-recipient="props">
                <q-td :props="props">
                  <div class="ellipsis">{{ props.row.recipient }}</div>
                </q-td>
              </template>
            </q-table>
          </q-card-section>
        </q-card>
      </div>
    </div>

    <div v-else class="flex flex-center justify-center">
      <q-spinner  size="lg" color="accent" > </q-spinner>
    </div>


  </q-page>
</template>

<script setup>
import { useAuthStore } from 'src/stores/auth';
import { api } from 'src/boot/axios';
import { onMounted, onUnmounted, ref } from 'vue';

/// -------------- VARIABLES ----------------- ///

const loading = ref(true);

const authStore = useAuthStore();
const token = authStore.getToken();
const pollTimer = ref(null);
const data = ref([]);

const amount_total = ref(null);
const transaction_count = ref(null);
const resData = ref(null)
const error = ref()
const currentBCH = ref(error.value || "Loading....");

const formatDate = (val) => {
  const dateObj = new Date(val);
  return dateObj.toLocaleString('en-US', {
    timeZone: 'GMT',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  });
};

const columns = [
  { name: 'tx_id', align: 'left', label: 'Transaction ID', field: 'tx_id', headerClasses: 'transparent header-text',
    classes: 'transparent',
    style: {
      fontSize: '1em'
    }
  },
  { name: 'order_id', align: 'center', label: 'Order ID', field: 'order_id', headerClasses: 'transparent header-text',
    classes: 'transparent',
    style: {
      fontSize: '1em'
    }
  },
  { name: 'amount_fiat', align: 'left', label: 'Amount Fiat', field: 'amount_fiat', sortable: true, headerClasses: 'transparent header-text',
    classes: 'transparent',
    style: {
      fontSize: '1em'
    }
  },
  { name: 'currency', align: 'left', label: 'Currency', field: 'currency', headerClasses: 'transparent header-text',
    classes: 'transparent',
    style: {
      fontSize: '1em'
    }
  },
  { name: 'amount_bch', align: 'left', label: 'Amount (BCH)', field: 'amount_bch', sortable: true, headerClasses: 'transparent header-text' ,
    classes: 'transparent',
    style: {
      fontSize: '1em'
    }
  },
  { name: 'recipient', align: 'left', label: 'Recipient', field: 'recipient', headerClasses: 'transparent header-text' ,
    classes: 'transparent',
    style: {
      fontSize: '1em'
    }
  },
  { name: 'date', align: 'left', label: 'Date', field: 'created_at', format: formatDate, headerClasses: 'transparent header-text' ,
    classes: 'transparent',
    style: {
      fontSize: '1em'
    }
    },
];

/// -------------- FUNCTIONS ----------------- ///

const fetchTransactions = async () => {
  try {
    const response = await api.get('', {
      headers: {
        'Authorization': `Token ${token}`,
        'Content-Type': 'application/json',
      }
    });
    // console.log("Response: ",response);
    data.value = response.data.table;

    amount_total.value = response.data.amount_total;
    transaction_count.value = response.data.transaction_count;

    loading.value = false;

    // console.log("Amount Total", amount_total.value, "\nTransaction Count:", transaction_count.value);
    // console.log("Data: ", data.value);
  } catch (error) {
    console.error("Error fetching transactions: ", error);
  }
};

const exchangeRates = async () => {
  try {
    const response = await api.get('https://api.coingecko.com/api/v3/simple/price', {
      headers: {
        'Content-Type': 'application/json',
      },
      params: {
        ids: 'bitcoin-cash',
        vs_currencies: "php"
      }
    });
    console.log("Exchange Rates: ", response.data);
    resData.value = response.data
    currentBCH.value = '₱ ' + resData.value['bitcoin-cash'].php
    console.log("Current BCH to PHP: ", currentBCH.value);

  } catch (error) {
    currentBCH.value = ("Too Many Requests")
    console.error("Error fetching exchange rates: ", error);
  }
}

const pollData = () => {
  fetchTransactions();
  exchangeRates();
};


/// --------------------- LIFECYCLES -------------------- ///

onMounted(() => {
  pollData();
  console.log("mounted");
  pollTimer.value = setInterval(pollData, 60000); // 60 seconds
});

onUnmounted(() => {
  console.log("unmounted");
  clearInterval(pollTimer.value);
});
</script>

<style>
.ellipsis {
  max-width: 250px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.large-text .q-table__row,
.large-text .q-table__title,
.large-text .header-text {
  font-size: 1.4em;
}

.table-container {
  width: 100%;
}

.table-title {
  font-size: 2em;
  font-weight: bold;
  margin-bottom: 1em;
}

.status {
  padding: 0.5em;
  border-radius: 4px;
  text-align: center;
  font-weight: bold;
  color: white;
}

.paid {
  background-color: #21BA45;
}

.pending {
  background-color: #F2C037;
}

.dashboard {
  /* font-size: 1 em; */
  font-family: Verdana, Geneva, Tahoma, sans-serif;
}
.transactions {
  background-image: url(/src/assets/images/transaction_total.png);
  background-size: cover;
}
.total-income {
  background-image: url(/src/assets/images/income_total.png);
  background-size: cover;
}
.bch-value {
  background-image: url(/src/assets/images/bch_logo.png);
  background-size: cover;
}
</style>
