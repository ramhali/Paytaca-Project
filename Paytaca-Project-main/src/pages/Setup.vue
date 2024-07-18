<template>
    <q-page padding>
        <div class="q-pa-md row relative-center">
            <q-card class="q-pa-md my-card">
                <div class="row">
                    <q-card-section>
                        <q-img src="https://cdn.quasar.dev/img/parallax2.jpg" style="width: 300px; height: auto;">
                            <div class="absolute-bottom text-h6">
                            <q-btn color="accent">Button</q-btn>
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

            <q-card class="q-pa-md my-card">
                <div class="row">
                    <q-card-section>
                        <q-img src="https://cdn.quasar.dev/img/parallax2.jpg" style="width: 300px; height: auto;">
                            <div class="absolute-bottom text-h6">
                                <a href="#">Link</a>
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
    </q-page>
</template>

<script>

export default {
  data() {
    return {
      code: `
<form action="http://oursite/pay/" method="get">
  <input type="hidden" name="token" value="1">
  <input type="hidden" name="amount" value="111.50">
  <input type="hidden" name="currency" value="PHP">
  <input type="hidden" name="desc" value="My First Order">
  <button type="submit">Go to MyApp Pay</button>
</form>
      `,
      link: `
<a href="http://localhost:8000/pay?token=4tDFHEJsPxLcCtvn&amp;amount=100.0101&amp;currency=PHP&amp;desc=Your+Product">

Pay with BCH

</a>
    `
    };
  }
};
</script>