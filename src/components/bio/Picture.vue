<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  src:{
    Type: String,
    Default: "public/silhouette.jpg"
  }
})
// function imageUrl() { return new URL(`/${props.info.image}`, import.meta.url) }

const source = computed(() => {
  return new URL(`/${props.src}`, import.meta.url)
})
</script>

<template>
  <img id="pic" :src="source" alt="img"/>
</template>

<style>
#pic {
  width: 256px;
  margin-left: 48px;
  margin-right: 48px;
  border-radius: 4px;
}
</style>