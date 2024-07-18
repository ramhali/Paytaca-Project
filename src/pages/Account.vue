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
