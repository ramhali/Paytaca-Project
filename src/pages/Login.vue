<template>
  <q-page class="flex flex-center justify-center ">
    <div>
    <q-card class="q-pa-md text-center" style="max-width: 400px">
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
          <q-btn label="Login" type="submit" color="accent" class="full-width"/>
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
  import axios from 'axios'
  import { useQuasar } from 'quasar'
  import { useRouter } from 'vue-router';

  const $q = useQuasar()
  const router = useRouter()

  const user = ref({
    username: null,
    password: null
  })

  const formRef = ref(null)

  const onSubmit = async () => {
    // try {
    //   console.log("User input: ",user.value);
    //   const response = await axios.get(`http://localhost:3000/users`, {
    //     params: {
    //       businessName: user.value.username,
    //       password: user.value.password
    //     }
    //   })

    //   console.log("Response: ",JSON.stringify(response.data));
    //   // if (response.data.length > 0) {
    //   //   $q.notify({
    //   //     type: 'positive',
    //   //     message: 'Login successful!'
    //   //   })
    //   //   router.push('/home')
    //   //   resetForm()
    //   // }
    //   // else {
    //   //   $q.notify({
    //   //     type: 'negative',
    //   //     message: 'Invalid Input'
    //   //   })
    //   // }
    //   router.push('/account')

    // } catch (error) {

    //     $q.notify({
    //       type: 'negative',
    //       message: 'Failed to Login'
    //     })
    //     onReset()
    // }

    try {
      const response = await axios.post('http://127.0.0.1:8000/login/')
        
    } catch (error) {

    }
  }

  const onReset = () => {
    user.value=ref(null)
  }
</script>

