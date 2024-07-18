<template>
  <q-layout view="lHh Lpr lFf">
    <Header/>
      <q-page-container class="bg-secondary">
      <!-- <q-page-container class="background-image"> -->
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

<style>
.background-image {
  background-image: url('assets/images/Untitled design.png');
  background-size: cover;
  background-position: center;
  width: 100%;
  position: relative;
}
</style>