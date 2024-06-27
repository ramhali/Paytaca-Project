<template>
  <q-page class="flex flex-center">
    <div class="flex flex-center justify-center" >

      <q-card class="q-pa-md text-center" style="max-width: 600px">
        <h5 class="q-mt-xs">Account Details</h5>
        <q-form @submit="onSubmit" @reset="onReset" class="q-gutter-md">
          <h6 class="flex q-mb-none">Account Details</h6>
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
          />

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
  import axios from 'axios'
  import { useQuasar } from 'quasar'
  import { useRouter } from 'vue-router';

  const $q = useQuasar()
  const router = useRouter()

  const user = ref({
    username:null,
    businessName: null,
    contactNumber: null,
    password1: null,
    password2: null,
    address: null,
    street: null,
    city: null,
    country: null,
  })

  const onSubmit = async () => {
    try {
      console.log(user.value.businessName, user.value.contactNumber, user.value.password1);
      await axios.post('http://localhost:3000/users', user.value)
      $q.notify({
        type: 'positive',
        icon: 'cloud_done',
        message: 'User registered successfully!'
      })
      console.log(user.value.businessName, user.value.contactNumber, user.value.password1);
      onReset()
      router.push('/home')
    } catch (error) {
      $q.notify({
        type: 'negative',
        message: 'Failed to register user'
      })
      onReset()
    }
  }

  const onReset = () => {
    user.value=ref(null)
  }
</script>
