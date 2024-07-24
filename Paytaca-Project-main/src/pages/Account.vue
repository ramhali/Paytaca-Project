<template>
  <q-page class="q-pa-lg">
    <div class="text-h2 q-my-md">
      <label class="text-weight-regular">
        Dashboard
      </label>
    </div>
    <div class="q-my-lg row justify-evenly">
      <q-card flat>
        <q-card-section class="q-pt-md q-pb-sm text-weight-bold" style="width: 250px;">
          BTC VALUE
        </q-card-section>

        <q-card-section class="q-py-sm">
          P
        </q-card-section>

      </q-card>

      <q-card flat>
        <q-card-section class="q-pt-md q-pb-sm text-weight-bold" style="width: 250px;">
          TOTAL INCOME
        </q-card-section>

        <q-card-section class="q-py-md">
          BCH {{amount_total}}
        </q-card-section>
      </q-card>

      <q-card flat>
        <q-card-section class="q-pt-md q-pb-sm text-weight-bold" style="width: 250px;">
          TRANSACTIONS COMPLETED
        </q-card-section>

        <q-card-section class="q-py-md">
          {{transaction_count || 0}}
        </q-card-section>
      </q-card>
    </div>
    
    <!-- <div class="q-my-lg">
      <q-card style="background-color: transparent;">
        <q-card-section>
          <div class="text-h6">Recent Transactions</div>
        </q-card-section>

        <q-card-section>
          <q-table
            :rows="rows"
            :columns="columns"
            :hide-pagination="true"
            row-key="name"
            flat
            style="background-color: transparent;"
          />
        </q-card-section>
      </q-card>
    </div> -->
    <div class="q-my-lg q-pt-lg">
      <q-card flat style="background-color: transparent;">
        <q-card-section>
          <div class="text-h6">Recent Transactions</div>
        </q-card-section>

        <q-card-section class="q-px-lg">
          <q-table
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
    
  </q-page>
</template>

<script setup>
import { useAuthStore } from 'src/stores/auth';
import { api } from 'src/boot/axios';
import { onMounted, ref } from 'vue';
import { date } from 'quasar';

const authStore = useAuthStore();
const token = authStore.getToken();
const data = ref([]);

const formatDate = (val) => date.formatDate(val, 'MM/DD/YYYY HH:mm:ss');

const columns = [
  { name: 'tx_id', align: 'center', label: 'Transaction ID', field: 'tx_id', headerClasses: 'transparent header-text',
    classes: 'transparent',
    style: {
      fontSize: '1em'
    }
  },
  { name: 'amount_fiat', align: 'center', label: 'Amount Fiat', field: 'amount_fiat', sortable: true, headerClasses: 'transparent header-text',
    classes: 'transparent',
    style: {
      fontSize: '1.1em'
    }
  },
  { name: 'currency', align: 'center', label: 'Currency', field: 'currency', headerClasses: 'transparent header-text',
    classes: 'transparent',
    style: {
      fontSize: '1.1em'
    }
  },
  { name: 'amount_bch', align: 'center', label: 'Amount (BCH)', field: 'amount_bch', sortable: true, headerClasses: 'transparent header-text' ,
    classes: 'transparent',
    style: {
      fontSize: '1.1em'
    }
  },
  { name: 'recipient', align: 'center', label: 'Recipient', field: 'recipient', headerClasses: 'transparent header-text' ,
    classes: 'transparent',
    style: {
      fontSize: '1.1em'
    }
  },
  { name: 'date', align: 'center', label: 'Date', field: 'created_at', format: formatDate, headerClasses: 'transparent header-text' ,
    classes: 'transparent',
    style: {
      fontSize: '1.1em'
    }
    },
];

let amount_total;
let transaction_count;

const fetchTransactions = async () => {
  try {
    const response = await api.get('', {
      headers: {
        'Authorization': `Token ${token}`,
        'Content-Type': 'application/json',
      }
    });
    data.value = response.data.table;

    amount_total = response.data.amount_total;
    transaction_count = response.data.transaction_count;
    
    console.log("Data: ", data.value);
  } catch (error) {
    console.error("Error fetching transactions: ", error);
  }
};

onMounted(() => {
  fetchTransactions();
});
</script>

<style>
.ellipsis {
  max-width: 150px;
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
  /* text-align: center; */
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
</style>