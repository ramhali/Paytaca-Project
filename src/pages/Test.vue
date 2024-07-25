<template>
  <h1>HELLO USER</h1>
  <div>{{ data }}</div>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import { api } from 'boot/axios'
import { useQuasar } from 'quasar'
import { useRouter } from 'vue-router'

const $q = useQuasar()
const router = useRouter()
const data = ref(null)

const onSubmit = async () => {
  try {
    const response = await api.get('http://localhost:8000/test/')
    data.value = response.data
    console.log(data.value)
  } catch (error) {
    console.error('Error fetching account data:', error)
  }
}

let intervalId

onMounted(() => {
  onSubmit()  // Call the function initially
  intervalId = setInterval(onSubmit, 5000)  // Poll every 5 seconds
})

onUnmounted(() => {
  clearInterval(intervalId)  // Clear interval when component is unmounted
})
</script>
