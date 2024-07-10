<template>
<q-page class="flex flex-center">
  <div class="q-pa-md flex justify-center">
    <q-table
      title="Transactions"
      :rows="rows"
      :columns="columns"
      row-key="index"
      separator="cell"
      draggable="false"
    />
  </div>
</q-page>>
</template>

<script setup>
const columns = [
  {
    name: 'index',
    label: '#',
    field: 'index'
  },
  {
    name: 'name',
    required: true,
    label: 'Name',
    align: 'left',
    field: row => row.name,
    format: val => `${val}`,
    sortable: true
  },
  // { name: 'calories', align: 'center', label: 'Calories', field: 'calories', sortable: true },
  // { name: 'fat', label: 'Fat (g)', field: 'fat', sortable: true },
  // { name: 'carbs', label: 'Carbs (g)', field: 'carbs' },
  // { name: 'protein', label: 'Protein (g)', field: 'protein' },
  // { name: 'sodium', label: 'Sodium (mg)', field: 'sodium' },
  // { name: 'calcium', label: 'Calcium (%)', field: 'calcium', sortable: true, sort: (a, b) => parseInt(a, 10) - parseInt(b, 10) },
  // { name: 'iron', label: 'Iron (%)', field: 'iron', sortable: true, sort: (a, b) => parseInt(a, 10) - parseInt(b, 10) }

  { name: 'txid', align: 'center', label: 'Transaction ID', field: 'txid' },
  { name: 'amount_fiat', align: 'center', label: 'Amount Fiat', field: 'amount_fiat', sortable:true},
  { name: 'amount_bch', align: 'center', label: 'Amount (BCH)', field: 'amount_bch', sortable:true},
  { name: 'recipient', align: 'center', label: 'Recipient', field: 'recipient'},
  { name: 'date', align: 'center', label: 'Date', field: 'date'},
  { name: 'status', align: 'center', label: 'Status', field: 'status'},
]

const rows = [
  {
    name: 'name1',
    txid: 'txid1',
    amount_fiat: 20.00,
    amount_bch: 0.0005,
    recipient: 'recipient1',
    date:'10/30/20',
    status:'Paid'
  },
  {
    name: 'name2',
    txid: 'txid2',
    amount_fiat: 40.00,
    amount_bch: 0.0010,
    recipient: 'recipient2',
    date: '10/30/20',
    status: 'Pending'
  },
  {
    name: 'name3',
    txid: 'txid3',
    amount_fiat: 400.00,
    amount_bch: 0.0100,
    recipient: 'recipient2',
    date: '10/30/20',
    status: 'Pending'
  },
  {
    name: 'name4',
    txid: 'txid4',
    amount_fiat: 200.00,
    amount_bch: 0.0050,
    recipient: 'recipient2',
    date: '10/30/20',
    status: 'Pending'
  },
  {
    name: 'name1',
    txid: 'txid1',
    amount_fiat: 20.00,
    amount_bch: 0.0005,
    recipient: 'recipient1',
    date:'10/30/20',
    status:'Paid'
  },
  {
    name: 'name2',
    txid: 'txid2',
    amount_fiat: 40.00,
    amount_bch: 0.0010,
    recipient: 'recipient2',
    date: '10/30/20',
    status: 'Pending'
  },
  {
    name: 'name3',
    txid: 'txid3',
    amount_fiat: 400.00,
    amount_bch: 0.0100,
    recipient: 'recipient2',
    date: '10/30/20',
    status: 'Pending'
  },
  {
    name: 'name4',
    txid: 'txid4',
    amount_fiat: 200.00,
    amount_bch: 0.0050,
    recipient: 'recipient2',
    date: '10/30/20',
    status: 'Pending'
  }
]

rows.forEach((row, index) => {
  row.index = index + 1
})
</script>

<style>

</style>
