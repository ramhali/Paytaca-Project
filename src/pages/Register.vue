<template>
  <q-page class="flex flex-center">
    <div class="flex justify-center">
      <q-card class="q-pa-md text-center bg-accent text-primary" style="width: 450px" color="accent">
        <h3>Paytaca BCH Gateway</h3>
        <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Officia odit corporis voluptate eos magni numquam. Provident assumenda dolore, autem maxime eveniet, cum culpa hic minima eum pariatur, ducimus fugit velit.</p>
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

  const $q = useQuasar()
  const router = useRouter()

  const user = ref({
    username:null,
    store_name: null,
    password1: null,
    password2: null,
    // address: null,
    // street: null,
    // city: null,
    // country: null,
    // contactNumber: null,
  })

  const onSubmit = async () => {
      const response = await api.post('http://127.0.0.1:8000/register', user.value)
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
            router.push('/')
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

  const onReset = () => {
    user.value=ref(null)
  }
</script>
