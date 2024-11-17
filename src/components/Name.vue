<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  name: {
    type:String,
    default:""
  },
  type: {
    type:String,
    default:"Normal"
  }
})

const innerText = computed(() => {
  var result = ""
  if (props.name === "" || props.name === undefined || props.name === null){
    result = "?"
  }
  else {
    result = result.concat(`${props.name}`)
  }
  if (props.type !== "Normal"){
    result = result.concat(` (${props.type})`)
  }
  return result
})
</script>

<template>
  <h1 id="characterName">{{ innerText }}</h1>
</template>

<style>
#characterName {
  text-align: center;
  width: 100%;
  margin: 0;
  padding-left: 0.25em;
  word-wrap: break-word;
}
</style>