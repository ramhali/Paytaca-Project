<template>
  <q-layout view="hHh Lpr fFf">

    <Header></Header>
    <q-page-container class="bg-secondary">
      <router-view />
    </q-page-container>

  </q-layout>
</template>

<script>
import { ref } from 'vue'
import Header from 'src/components/Header.vue';

export default {
  name: 'AccountLayout',
  components:{Header},

  setup () {

  }
}
</script>
