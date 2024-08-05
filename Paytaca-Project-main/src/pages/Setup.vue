<template>
    <q-page padding>
      <div class="q-pa-md row relative-center">
        <q-card class="q-pa-md q-my-md my-card shadow-5">
          <div class="row">
            <q-card-section>
              <q-img src="https://cdn.quasar.dev/img/parallax2.jpg" style="width: 300px; height: auto;">
                <div class="absolute-bottom text-h6">
                  <q-btn color="accent">Pay with Paytaca</q-btn>
                </div>
              </q-img>
            </q-card-section>
    
            <q-card-section class="full-width">
              <q-input
                filled
                v-model="code"
                type="textarea"
                rows="10"
                readonly
                style="font-family: monospace;"
              />
            </q-card-section>
          </div>
        </q-card>
    
        <q-space/>
    
        <q-card class="q-pa-md q-my-md my-card shadow-5">
          <div class="row">
            <q-card-section>
              <q-img src="https://cdn.quasar.dev/img/parallax2.jpg" style="width: 300px; height: auto;">
                <div class="absolute-bottom text-h6">
                  <a href="#">Pay with Paytaca</a>
                </div>
              </q-img>
            </q-card-section>
    
            <q-card-section class="full-width">
              <q-input
                filled
                v-model="link"
                class="inline-wrap"
                type="textarea"
                rows="10"
                readonly
                style="font-family: monospace;"
              />
            </q-card-section>
          </div>
        </q-card>
      </div>
      <div class="q-pa-md">
        <q-card class="q-pa-md q-my-md my-card shadow-5">
          <q-card-section class="q-px-md">
            <label>Required Parameters</label>
          </q-card-section>
    
          <hr>
          <q-card-section class="q-px-md">
            <q-table
                flat bordered
                :rows="rows"
                :columns="columns"
                row-key="name"
                hide-bottom
            >
                <template v-slot:body-cell-name="props">
                    <q-td :props="props" class="fixed-width">
                    {{ props.row.name }}
                    </q-td>
                </template>
                <template v-slot:body-cell-desc="props">
                    <q-td :props="props" class="inline-wrap">
                    {{ props.row.desc }}
                    </q-td>
                </template>
                <template v-slot:body-cell-ex="props">
                    <q-td :props="props" class="fixed-widthex">
                    {{ props.row.ex }}
                    </q-td>
                </template>
            </q-table>
          </q-card-section>
        </q-card>   
    
        <q-card class="q-pa-md q-my-md my-card shadow-5">
          <q-card-section class="q-px-md">
            <label>Optional Parameters</label>
          </q-card-section>
          <hr>
          <q-card-section class="q-px-md">
            <q-table
                flat bordered
                :rows="additionalRows"
                :columns="additionalColumns"
                row-key="name"
                hide-bottom
            >
                <template v-slot:body-cell-name="props">
                    <q-td :props="props" class="fixed-width">
                    {{ props.row.name }}
                    </q-td>
                </template>
                <template v-slot:body-cell-desc="props">
                    <q-td :props="props" class="inline-wrap">
                    {{ props.row.desc }}
                    </q-td>
                </template>
                <template v-slot:body-cell-ex="props">
                    <q-td :props="props" class="fixed-widthex inline-wrap">
                    {{ props.row.ex }}
                    </q-td>
                </template>
            </q-table>
          </q-card-section>
        </q-card>
      </div>
    </q-page>
</template>
    
<script>
    export default {
        data() {
            return {
                code: `
<form action="http://localhost:9000/pay/" method="get">

    <input type="hidden" name="token" value="eXaMPLET0kEN0NLy">
    <input type="hidden" name="amount" value="120">
    <input type="hidden" name="currency" value="PHP">
    <button type="submit">Go to MyApp Pay</button>

</form>
        `,
                link: `
<a href="http://localhost:9000/pay/?token=eXaMPLET0kEN0NLy&amp;amount=120&amp;currency=PHP&amp;">

    Pay with BCH

</a>
        `,
                columns: [
                { name: 'name', required: true, label: 'Parameter', align: 'left', field: row => row.name, format: val => `${val}`, sortable: false },
                { name: 'desc', label: 'Description', align: 'left', field: 'desc', sortable: false },
                { name: 'ex', label: 'Example', align: 'left', field: 'ex', sortable: false }
                ],
                rows: [
                {
                  name: 'action',
                  desc: 'The payment gateway website, where the user will be redirected after opting to pay in BCH',
                  ex: 'http://localhost:9000/pay/' 
                },
                {
                    name: 'token',
                    desc: 'Your unique account token, which can be viewed in the account information tab after you connect your wallet',
                    ex: 'eXaMPLET0kEN0NLy' 
                },
                {
                    name: 'amount',
                    desc: 'Total price the customer is required to pay',
                    ex: '120'
                },
                {
                    name: 'currency',
                    desc: 'The currency in which the amount is based',
                    ex: 'PHP'
                },
                ],
                additionalColumns: [
                { name: 'name', required: true, label: 'Parameter', align: 'left', field: row => row.name, format: val => `${val}`, sortable: false },
                { name: 'desc', label: 'Description', align: 'left', field: 'desc', sortable: false },
                { name: 'ex', label: 'Example', align: 'left', field: 'ex', sortable: false }
                ],
                additionalRows: [
                {
                    name: 'order_id',
                    desc: "The unique identifier of the order or product. Once the transaction is completed, this identifier will be marked as paid and sent as a POST request",
                    ex: 'Order-12345' 
                },
                {
                    name: 'desc',
                    desc: 'A brief description that will be displayed to the customers, informing them of what they are about to pay for',
                    ex: 'Value Meal'
                },
                {
                    name: 'callback_url',
                    desc: 'The URL to which the POST request will be sent once the transaction is completed',
                    ex: 'http://localhost:9000/test'
                },
                {
                    name: 'return_url',
                    desc: 'The URL to which the customers will be redirected once the transaction is completed',
                    ex: 'http://localhost:9000/test/landing'
                },
                ]
            };
        }
    };
</script>
    
<style scoped>
.relative-center {
    display: flex;
    justify-content: center;
    align-items: center;
}
.fixed-width {
    width: 150px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
.fixed-widthex {
    width: 225px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
.inline-wrap {
    white-space: normal;
}
</style>
  