<template>
  <q-page padding class="flex flex-center justify-center">
    <div >
      <q-card style="width:500px;" class="q-pa-lg">
        <q-card-section class="flex flex-center">
          <q-btn color="accent" label="Generate QR Code" @click="generateQrCode"/>
        </q-card-section>
        <q-card-section class="flex flex-center">

          <vue-qrcode
            class="q-mb-sm"
            :value="xpub_key"
            :size=300
            level="H"
          />
        </q-card-section>

      </q-card>
    </div>

  </q-page>
</template>

<!-- <script>
import { useRouter } from 'vue-router';

export default {
  name: 'PageName',
  data() {
    return {
      xKey: " ",
      walletHash: 'xpub661MyMwAqRbcFtFbBrD6e1nTx1KxvjqT4axHp6VLMiV5n1w7uTk34Jc4Ah1vcdTnoDd14KyyjZ3wwP4x9iFiUAMfCW4CgHbBrd5n74w2kLr',
      num : null,
      temp: null,
      router: useRouter()
    }
  },
  methods: {
    generateQrCode: function () {
      this.xKey = this.generateRandomString(120)
      console.log("xKey: ",this.xKey);

    },
    generateRandomString: function (length){
      const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
      let result = '';
      const charactersLength = characters.length;
      for (let i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
      }
      return result;
    }
  }
}
</script> -->
<script setup>
import { ref } from "vue";
import { useRouter } from 'vue-router';


  const router = useRouter()
  const xpub_key = ref('');
  const index = ref(0);
  const address = ref('');

function generateQrCode(){

}

</script>
