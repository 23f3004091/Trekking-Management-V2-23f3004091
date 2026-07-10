<script setup>
import apiClient from '../axiosApi.js'
import { onMounted, ref } from 'vue'

const resData = ref('Loading...')

const fetchData = async () => {
  try {
    const response = await apiClient.get("/")
    resData.value = response.data
    return response
  } catch (err) {
    console.error("Error fetching data:", err)
    resData.value = "Failed to load"
  }
}


onMounted(() => {
  fetchData()
})
// const get = await response
</script>

<template>
  <h1>{{ resData }}</h1>
</template>
