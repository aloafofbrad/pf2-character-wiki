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
  },
  defaultNameValue: {
    type:String,
    default:""
  }
})

const innerText = computed(() => {
  var result = ""
  if (props.name === props.defaultNameValue || props.name === undefined || props.name === null){
    result = "?"
  }
  else {
    result = result.concat(`${props.name}`)
  }
  if (props.type !== "Normal"){
    result = result.concat(`\n(${props.type})`)
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
  /* margin: 0;
  margin-left: 3em;
  margin-right: 3em; */
  word-wrap: break-word;
}
</style>