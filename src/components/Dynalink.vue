<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  innerText:{
    type: String,
    default: ""
  },
  domain:{
    type: String,
    default: ""
  },
  path:{
    type: String,
    default: ""
  },
  params:{
    type: Object,
    default: {}
  }
})

const url = computed (() => {
  var result = ""
  if (props.innerText !== undefined && props.domain !== undefined &&
      props.path !== undefined && props.params !== undefined && 
      props.innerText !== null && props.domain !== null &&
      props.path !== null && props.params !== null) {
    var result = props.domain + props.path
    if (props.params){
      result = result.concat("?")
      for (const [param, arg] of Object.entries(props.params)){
        result = result.concat(param)
        result = result.concat("=")
        result = result.concat(arg)
        result = result.concat("&")
      }
      result = result.slice(0, result.length - 1)
    }
  }
  return result
})
</script>

<template>
  <a :href="url">{{ innerText }}</a>
</template>

<style>
a {
  color: #aaccff;
}

a:visited {
  color: #ffccff;
}
</style>