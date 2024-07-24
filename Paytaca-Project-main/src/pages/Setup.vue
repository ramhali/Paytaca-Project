<template>
    <q-page padding>
        <div class="q-pa-md row relative-center">
            <q-card class="q-pa-md my-card shadow-5">
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

            <q-card class="q-pa-md my-card shadow-5">
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
                    <!-- <q-table
                    title="Treats"
                    :rows="rows"
                    :columns="columns"
                    row-key="name"
                    /> -->
                </q-card-section>
            </q-card>   

            <q-card class="q-pa-md q-my-md my-card shadow-5">
                <q-card-section class="q-px-md">
                    <label>Additional Parameters</label>
                </q-card-section>
                <hr>
            </q-card>
        </div>
    </q-page>
</template>

<script>

export default {
  data() {
    return {
      code: `
<form action="http://localhost:9000/pay/payredirect" target="_blank" method="get">
    <input type="hidden" name="token" value="3A6k4t99g0rLPaG2">
    <input type="hidden" name="amount" value="0.50">
    <input type="hidden" name="currency" value="PHP">
    <input type="hidden" name="desc" value="My First Order">
    <button type="submit">Go to MyApp Pay</button>
</form>
      `,
      link: `
<a href="http://localhost:9000/pay/payredirect?token=3A6k4t99g0rLPaG2&amp;amount=0.50&amp;currency=PHP&amp;desc=My+Product">

Pay with BCH

</a>
    `
    };
  }
};


</script>