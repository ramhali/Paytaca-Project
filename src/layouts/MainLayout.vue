<template>
  <q-layout view="lHh Lpr lFf">
    <Header/>
    <q-page-container class="bg-secondary">
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import Header from 'src/components/Header.vue';

defineOptions({
  name: 'MainLayout'
})


</script>
