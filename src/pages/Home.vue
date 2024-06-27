<template>
  <q-page class="flex flex-center">
    <h2>Welcome</h2>
    <div>
      <q-btn class="q-mr-md" color="accent" label="Register" size="small" @click="$router.push('register')" />
      <q-btn color="accent" label="Login" size="small" @click="$router.push('login')" />
    </div>
  </q-page>

</template>

<script setup>
defineOptions({
  name: 'index'
});
</script>
