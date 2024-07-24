<template>
  <q-header elevated>
    <q-toolbar class="bg-primary q-py-sm q-px-md" >
      <q-btn class="hover-button q-py-sm" flat to="/">
          <q-img src="/src/assets/images/paytaca_dark.cb10ef9d.png" alt="Paytaca Logo" height="32px" width="160px" />
      </q-btn>

      <q-space></q-space>
      
      <q-btn
        class="q-mr-md"
        color="accent"
        label="Login"
        size="small"
        text-color="primary"
        @click="$router.push('login')"
      />

      <q-btn 
        no-wrap 
        class="justify-left text-capitalize" 
        outline rounded color="accent" 
        icon-right="start" 
        label="Sign Up"
        @click="$router.push('register')"
       />
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
