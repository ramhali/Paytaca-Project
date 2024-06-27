<template>
  <q-page padding>
    <div>
      <h3>Welcome</h3>
    </div>
    <div>
      <label>Enter xPub Key</label>
      <q-input filled v-model="xKey" label="Input" stack-label required
        :rules="[(val) => !!val || 'xPub field cannot be empty']" />
      <p>xPub Key: {{ xKey }}</p>
    </div>

    <div class="flex flex-center justify-center" >
      <q-card style="width: 600px;">
        <q-card-section class="flex flex-center">
          <canvas id="qr-code" style="border: 2px solid black;"></canvas>
        </q-card-section>
        <q-card-section class="flex flex-center">
          <q-btn color="accent" label="Generate QR Code" @click="generateQrCode" />
        </q-card-section>
      </q-card>
    </div>
  </q-page>
</template>

<script>
import QRious from "qrious";

export default {
  name: 'PageName',
  data() {
    return {
      xKey: 'xpub661MyMwAqRbcFtFbBrD6e1nTx1KxvjqT4axHp6VLMiV5n1w7uTk34Jc4Ah1vcdTnoDd14KyyjZ3wwP4x9iFiUAMfCW4CgHbBrd5n74w2kLr'
    }
  },
  methods: {
    generateQrCode: function () {
      console.log('generated code')
      if (this.xKey !== "" & this.xKey != "\n") {
        new QRious({
          level: "H",
          padding: 25,
          size: 300,
          element: document.getElementById("qr-code"),
          value: this.xKey
        })
      }
    },
  }
}
</script>
