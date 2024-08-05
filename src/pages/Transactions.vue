<template>
  <q-page class="flex flex-center">

    <q-card v-if="!loading" class=" q-ma-xl q-pa-md">
      <div class="q-pa-md flex justify-center">
        <div class="table-container">
          <div class="table-title">

            Transactions
          </div>

          <div v-if="data.status === 'Empty Transaction'" style="font-size: 1.5em; width: 600px;">
            No Transactions...
          </div>

          <q-table
            v-else
            :rows="data"
            :columns="columns"
            row-key="id"
            separator="horizontal"
            draggable="false"
            class="large-text"
            style="border: 2px solid #eff6ff;"
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
            <template v-slot:body-cell-status="props">
              <q-td :props="props">
                <div :class="['status', props.row.paid ? 'paid' : 'pending']">
                  {{ props.row.paid ? 'Paid' : 'Pending' }}
                </div>
              </q-td>
            </template>
          </q-table>

          </div>
      </div>
    </q-card>

    <q-spinner v-else size="lg" color="accent"> </q-spinner>
  </q-page>
</template>

<script setup>
import { useAuthStore } from 'src/stores/auth';
import { api } from 'src/boot/axios';
import { onMounted, ref } from 'vue';


const loading = ref(true);

const authStore = useAuthStore();
const token = authStore.getToken();
const data = ref([]);


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
  { name: 'tx_id', align: 'center', label: 'Transaction ID', field: 'tx_id',
    style: {
      fontSize: '1em'
    }
  },
  { name: 'order_id', align: 'center', label: 'Order ID', field: 'order_id',
    style: {
      fontSize: '1em'
    }
  },
  { name: 'amount_fiat', align: 'center', label: 'Amount Fiat', field: 'amount_fiat', sortable: true,
    style: {
      fontSize: '1em'
    }
  },
  { name: 'currency', align: 'center', label: 'Currency', field: 'currency',
    style: {
      fontSize: '1em'
    }
  },
  { name: 'amount_bch', align: 'center', label: 'Amount (BCH)', field: 'amount_bch', sortable: true,
    style: {
      fontSize: '1em'
    }
  },
  { name: 'recipient', align: 'center', label: 'Recipient', field: 'recipient',
    style: {
      fontSize: '1em'
    }
  },
  { name: 'date', align: 'center', label: 'Date', field: 'created_at', format: formatDate,
    style: {
      fontSize: '1em'
    }
  },
  { name: 'status', align: 'center', label: 'Status', field: 'paid',
    style: {
      fontSize: '1em'
    }
  },
];


const fetchTransactions = async () => {
  try {
    const response = await api.get('account/transactions/', {
      headers: {
        'Authorization': `Token ${token}`,
        'Content-Type': 'application/json',
      }
    });
    loading.value = false;
    data.value = response.data;
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
