<template>
  <q-layout>
    <q-header  class="q-pa-sm flex shadow-4">
      <q-btn flat to="/pay/payredirect" class="hover-button q-py-sm">
          <q-img src="/src/assets/images/paytaca_light.11fed42b.png" alt="Paytaca Logo" height="32px" width="160px"
            style="padding-left: 1vw;" />
      </q-btn>
    </q-header>

    <q-page-container class="bg-secondary">

      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>

</script>