<template>
  <q-page class="flex flex-center">
    <div class="flex justify-center">
      <q-card class="q-pa-md text-justify bg-accent text-primary" style="width: 450px" color="accent">
        <h3 class="text-center">Paytaca BCH Gateway</h3>
         <p>
          As the preferred choice for BCH enthusiasts globally, Paytaca is poised to lead the charge in introducing billions to the utility of BCH over traditional currencies, both fiat and crypto. With its unwavering commitment to accessibility, security, and innovation, Paytaca stands as the quintessential tool for navigating the evolving landscape of peer-to-peer digital transactions.
         </p>
         <p>
          Empower your transactions.
         </p>
         <p>
          <strong>Start accepting BCH today!</strong>
         </p>
      </q-card>

      <q-card class="q-pa-md text-center" style="width: 450px">
        <h5 class="q-mt-xs">Registration Form</h5>
        <q-form @submit="onSubmit" @reset="onReset" class="q-gutter-md">
          <h6 class="flex q-mb-none">Account Details</h6>
          <q-input
            filled
            v-model="user.store_name"
            label="Business Name"
            stack-label
            required
          />
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
            v-model="user.password1"
            label="Password"
            stack-label
            required
            hint="Must contain at least 8 characters"
          />
          <q-input
            filled
            type="password"
            v-model="user.password2"
            label="Confirm Password"
            stack-label
            required
            hint="Re-type your password"
          />

<!--
          <h6 class="flex q-mb-none">Business Details</h6>
          <q-input
            filled
            v-model="user.businessName"
            label="Business Name"
            stack-label
            required
          />
          <q-input
            filled
            v-model="user.contactNumber"
            label="Primary Contact Number"
            stack-label
            required
          />
          <q-input
            filled
            v-model="user.address"
            label="Address"
            stack-label
            required
          />
          <q-input
            filled
            v-model="user.street"
            label="Street"
            stack-label
            required
          />
          <q-input
            filled
            v-model="user.city"
            label="City/Municipality"
            stack-label
            required
          />
          <q-input
            filled
            v-model="user.country"
            label="Country"
            stack-label
            required
          /> -->

          <div>
            <q-btn class="full-width" label="Create Account" type="submit" color="accent"/>
          </div>
          <div class="form-bottom">
            <p>Already have an account?
              <router-link to="login">
                <a>Click here to Login</a>
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
  import { useAuthStore } from 'src/stores/auth';

  const $q = useQuasar()
  const router = useRouter()
  const authStore = useAuthStore()

  const user = ref({
    username:null,
    store_name: null,
    password1: null,
    password2: null,
  })
  const loginData = ref({
    username:null,
    password: null,
  })

  const onSubmit = async () => {
      const response = await api.post('register/', user.value)
        .then(
          (response) => {
          console.log(response)
          if(response.data.status !='errors'){
            $q.notify({
            type: 'positive',
            icon: 'cloud_done',
            message: 'User Registered Successfully!',
            timeout: 2000
            })
            // router.replace('/')
            loginData.value.username = user.value.username
            loginData.value.password = user.value.password1
            console.log("Login Data:", loginData.value);
            Login()
          }
          else{
            for (let index in response.data.errors.username){
              $q.notify({
              type: 'negative',
              icon: 'error',
              multiLine: true,
              message: `${response.data.errors.username[index]}`,
              timeout: 2000
              })
            }

            for (let index in response.data.errors.password2){
              $q.notify({
              type: 'negative',
              icon: 'error',
              multiLine: true,
              message: `${response.data.errors.password2[index]}`,
              timeout: 2000
              })
            }
          }

        })
        .catch(
          (error) => {
            console.log(error, error.message)
            $q.notify({
            type: 'negative',
            icon: 'error',
            message: `${error.message}`,
            timeout: 1000
            })
          }
        )
  }
  const Login = async () => {
  try {
    const csrfToken = window.csrfToken;
    const response = await api.post('login/', loginData.value, {
      headers: {
        'X-CSRFToken': csrfToken
      },
      withCredentials: true
    });
    console.log("Login Response: ",response.data);

    if (response.data.status !== 'errors') {
      authStore.login(response.data.token, response.data.username);
      $q.notify({
        type: 'positive',
        icon: 'cloud_done',
        message: 'User logged in successfully!',
        timeout: 2000
      });
      router.replace('/account');
    } else {
      $q.notify({
        type: 'negative',
        icon: 'error',
        message: `${response.data.errors}`,
        timeout: 2000
      });
      console.log(response.data);
    }
  } catch (error) {
    if (error.response && error.response.status === 401) {
      $q.notify({
        type: 'negative',
        icon: 'error',
        message: 'Incorrect Username or Password',
        timeout: 2000
      });
    }
    console.error(error);
  }
};

  const onReset = () => {
    user.value=ref(null)
  }
</script>

<style scoped>
p {
  font-size: 1.2em;
}
</style>
