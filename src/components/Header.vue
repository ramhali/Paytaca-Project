<template>
  <q-header elevated>
    <q-toolbar class="bg-primary q-py-sm" >
      <q-btn class="hover-button q-py-sm" flat to="/">
          <q-img src="/src/assets/images/paytaca_light.11fed42b.png" alt="Paytaca Logo" height="32px" width="160px"
            style="padding-left: 1vw;" />
        </q-btn>

    </q-toolbar>
  </q-header>

</template>

<script>

export default {
  name: 'Header',
  setup() {
    return {
    }
  },
}
</script>

<style scoped>
.hover-button:hover{
  background-color: rgb(231, 231, 230);
}
</style>
