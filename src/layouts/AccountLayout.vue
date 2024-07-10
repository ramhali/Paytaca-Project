<template>
  <q-layout view="hHh lpR lFf" >
    <q-header elevated class="q-pa-sm flex">
      <q-btn dense flat round icon="menu" @click="toggleLeftDrawer" color="accent" />
      <q-btn flat to="/account" class="hover-button q-py-sm">
          <q-img src="/src/assets/images/paytaca_light.11fed42b.png" alt="Paytaca Logo" height="32px" width="160px"
            style="padding-left: 1vw;" />
      </q-btn>
      <q-space/>
      <!-- <div style="padding: 0" class="flex flex-center justify-center">
        <label  style="color: #1e293b; padding: 0;">Welcome, {{username}}!</label>
      </div> -->
      <q-space/>
      <q-btn
          label="Logout"
          @click = logoutUser()
          color="accent"
          class="q-p-md"
        />
    </q-header>

    <q-drawer v-model="leftDrawerOpen" side="left" overlay elevated>
      <q-scroll-area class="fit">
          <q-list>

            <q-separator/>
            <q-item>
              <q-item-section>Welcome, {{username}}!</q-item-section>
            </q-item>
            <q-separator/>
            <router-link to="/account" class="q-item-link">
              <q-item clickable  v-ripple >
              <q-item-section avatar>
              <q-icon name="home" />
              </q-item-section>
              <q-item-section>Home</q-item-section>
              </q-item>
            </router-link>
            <router-link to="/account/info" class="q-item-link">
              <q-item clickable  v-ripple >
              <q-item-section avatar>
              <q-icon name="person" />
              </q-item-section>
              <q-item-section>Account info</q-item-section>
              </q-item>
            </router-link>
            <router-link to="/account/transactions" class="q-item-link">
              <q-item clickable  v-ripple >
              <q-item-section avatar>
              <q-icon name="view_list" />
              </q-item-section>
              <q-item-section>Transactions</q-item-section>
              </q-item>
            </router-link>
              <q-separator/>
            <q-item clickable  v-ripple @click="logoutUser">
              <q-item-section avatar>
              <q-icon name="logout" />
              </q-item-section>
              <q-item-section>Logout</q-item-section>
              </q-item>
          </q-list>
        </q-scroll-area>
    </q-drawer>


    <q-page-container class="bg-secondary">

      <router-view />
    </q-page-container>

  </q-layout>
</template>

<script setup>
import { ref } from 'vue';
import { api } from 'src/boot/axios';
import { useRouter } from 'vue-router';
import { useQuasar } from 'quasar'
import { useAuthStore } from 'src/stores/auth';

const leftDrawerOpen = ref(false)
const $q = useQuasar()
const router = useRouter()
const authStore = useAuthStore();
const username = authStore.getUser

function toggleLeftDrawer(){
  leftDrawerOpen.value = !leftDrawerOpen.value
}

 function logoutUser() {
  try {
    api.get('http://127.0.0.1:8000/logout');
    authStore.logout();

    $q.notify({
      type: 'positive',
      icon: 'check',
      message: `Logged out Successfully`,
      timeout: 2000
    });

    router.push('/');
  } catch (error) {
    console.error('Logout error:', error);
    $q.notify({
      type: 'negative',
      icon: 'error',
      message: `${error.message}`,
      timeout: 2000
    });
  }
}

</script>

<style scoped>
.hover-button:hover{
  background-color: rgb(231, 231, 230);
}
.q-item-link {
  text-decoration: none;
  color: inherit;
}
</style>
