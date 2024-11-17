<script setup>
import { ref, computed } from 'vue'
import Dynalink from './Dynalink.vue'
import ancestries from '../data/ancestries.json'

const props = defineProps({
  contents: {
    Type:String,
    Default: "This entry is about a group of characters."
  }
})

function setup(){
  return {}
}
</script>

<template>
  <p class="group">{{ contents }}</p>
</template>

<style>
.group {
  /* padding: 0;
  margin: 0; */
  padding-top: 0;
}
</style>