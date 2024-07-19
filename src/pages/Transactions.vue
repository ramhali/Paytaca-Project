<template>
  <q-page class="flex flex-center">
    <q-card class="shadow-5 q-ma-xl q-pa-md">
      <div class="q-pa-md flex justify-center">
        <div class="table-container">
          <div class="table-title">

            Transactions
          </div>
          <q-table
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
  { name: 'tx_id', align: 'center', label: 'Transaction ID', field: 'tx_id', headerClasses: 'bg-grey-1 header-text',
    classes: 'bg-grey-1',
    style: {
      fontSize: '1.2em'
    }
  },
  { name: 'amount_fiat', align: 'center', label: 'Amount Fiat', field: 'amount_fiat', sortable: true, headerClasses: 'bg-grey-1 header-text',
    classes: 'bg-grey-1',
    style: {
      fontSize: '1.2em'
    }
  },
  { name: 'currency', align: 'center', label: 'Currency', field: 'currency', headerClasses: 'bg-grey-1 header-text',
    classes: 'bg-grey-1',
    style: {
      fontSize: '1.2em'
    }
  },
  { name: 'amount_bch', align: 'center', label: 'Amount (BCH)', field: 'amount_bch', sortable: true, headerClasses: 'bg-grey-1 header-text' ,
    classes: 'bg-grey-1',
    style: {
      fontSize: '1.2em'
    }
  },
  { name: 'recipient', align: 'center', label: 'Recipient', field: 'recipient', headerClasses: 'bg-grey-1 header-text' ,
    classes: 'bg-grey-1',
    style: {
      fontSize: '1.2em'
    }
  },
  { name: 'date', align: 'center', label: 'Date', field: 'created_at', format: formatDate, headerClasses: 'bg-grey-1 header-text' ,
    classes: 'bg-grey-1',
    style: {
      fontSize: '1.2em'
    }
  },
  { name: 'status', align: 'center', label: 'Status', field: 'paid', headerClasses: 'bg-grey-1 header-text' ,
    classes: 'bg-grey-1',
    style: {
      fontSize: '1.2em'
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
