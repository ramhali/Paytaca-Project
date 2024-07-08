<template>
  <q-page class="flex flex-center justify-center ">
    <div class="flex justify-center">
      <q-card class="q-pa-md text-center bg-accent text-primary" style="width: 450px" color="accent">
        <h3>Paytaca BCH Gateway</h3>
        <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Officia odit corporis voluptate eos magni numquam. Provident assumenda dolore, autem maxime eveniet, cum culpa hic minima eum pariatur, ducimus fugit velit.</p>
      </q-card>
    <q-card class="q-pa-md text-center" style="width: 450px">
      <h5 class="q-mt-sm">Login</h5>
      <q-form @submit="onSubmit" @reset="onReset" class="q-gutter-md">
        <q-input
          filled
          v-model="user.username"
          label="Username"
          stack-label
          required
        />
        <q-input
          filled
          type="password"
          v-model="user.password"
          label="Password"
          stack-label
          required
        />
        <div>
          <q-btn class="full-width" label="Login" type="submit" color="accent"/>
        </div>
        <div class="form-bottom">
          <p>Don't have an account?
            <router-link to="register">
              <a>Click here to Register</a>
            </router-link>
          </p>
        </div>
      </q-form>
    </q-card>
  </div>
  </q-page>
</template>

<script setup>
  import { ref } from 'vue'
  import {api} from 'boot/axios'
  import { useQuasar } from 'quasar'
  import { useRouter } from 'vue-router';
  import { authStore } from 'src/stores/auth';

  const $q = useQuasar()
  const router = useRouter()
  const store = authStore()

  const user = ref({
    username: null,
    password: null
  })

  const formRef = ref(null)

  // const onSubmit = async () => {
  //   try {
  //     const response = await api.post('http://127.0.0.1:8000/login', user.value)
  //       .then((response) => {
  //         authStore.login(response.data.token, response.data.user)
  //         console.log(response)
  //         if(response.data.status !='errors'){

  //           $q.notify({
  //           type: 'positive',
  //           icon: 'cloud_done',
  //           message: 'User Login successfully!'
  //           })

  //           router.push('/account')
  //         } else{
  //           $q.notify({
  //           type: 'negative',
  //           icon: 'error',
  //           message: `${response.data.errors}`
  //           })
  //         }

  //       })
  //       .catch(
  //         (error) => {
  //           console.log(error, error.message)
  //           $q.notify({
  //           type: 'negative',
  //           icon: 'error',
  //           message: `${error.message}`
  //           })
  //         }
  //       )
  //       .finally(
  //         onReset()
  //       )
  //   }
  //   catch (error) {
  //   }
  // }

  const onSubmit = async () => {
  try {
    const response = await api.post('http://127.0.0.1:8000/login', user.value);
    console.log(response);
    if (response.data.status !== 'errors') {
      store.login(response.data.token, response.data.username);
      console.log(response.data.username)
      $q.notify({
        type: 'positive',
        icon: 'cloud_done',
        message: 'User logged in successfully!',
        timeout: 2000
      });
      router.push('/account');
    }
    else {
      $q.notify({
        type: 'negative',
        icon: 'error',
        message: `${response.data.errors}`,
        timeout: 2000
      });
    }
    } catch (error) {
      $q.notify({
        type: 'negative',
        icon: 'error',
        message: `${error.message}`,
        timeout: 2000
      });
    }
  };


  const onReset = () => {
    user.value=ref(null)
  }
</script>

