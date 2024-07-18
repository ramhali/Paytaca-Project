<template>
<q-page class="flex flex-center">
  <div class="q-pa-md flex justify-center">
    <q-table
      title="Transactions"
      :rows="data"
      :columns="columns"
      row-key="index"
      separator="cell"
      draggable="false"
      class="shadow-11"
    />
  </div>
</q-page>>
</template>

<script setup>
import { useAuthStore } from 'src/stores/auth';
import { api } from 'src/boot/axios';
import { onMounted } from 'vue';
import { ref } from 'vue';

const authStore = useAuthStore();
const token = authStore.getToken();
const data = ref([])

const columns = [
  {
    name: 'id',
    label: 'ID',
    field: 'id'
  },

  { name: 'tx_id', align: 'center', label: 'Transaction ID', field: 'tx_id' },
  { name: 'amount_fiat', align: 'center', label: 'Amount Fiat', field: 'amount_fiat', sortable:true},
  { name: 'currency', align: 'center', label: 'Currency', field: 'currency'},
  { name: 'amount_bch', align: 'center', label: 'Amount (BCH)', field: 'amount_bch', sortable:true},
  { name: 'recipient', align: 'center', label: 'Recipient', field: 'recipient'},
  { name: 'date', align: 'center', label: 'Date', field: 'created_at'},
  { name: 'status', align: 'center', label: 'Status', field: 'paid'},
]

const fetchTransactions = async () => {
  const response = await api.get('account/transactions/', {
    headers: {
      'Authorization': `Token ${token}`,
      'Content-Type': 'application/json',
    }
  });
  data.value = response.data
  console.log("Data: ", data.value);
}


onMounted(()=>{
  // console.log("\nToken:",urldata.value.token,"\nAmount:",urldata.value.amount, "\nCurrency:",urldata.value.currency, "\nDescription:",urldata.value.desc,);
  fetchTransactions()
})
</script>

<style>
.col-name {
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
