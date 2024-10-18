<script setup>
import { ref, computed } from 'vue'
import backgrounds from '../data/backgrounds.json'
import Dynalink from './Dynalink.vue';

const props = defineProps({
  background:{
    Type:String,
    Default:""
  }
})

const innerText = computed(() => {
  var result = "Background: "
  if (props.background === "" || props.background === "?"){
    return result.concat("?")
  }
  return result.concat(props.background)
})

const domain = ref('https://2e.aonprd.com/')
const path = ref('Backgrounds.aspx')

function exists(x) {
  return x !== null && x !== undefined
}

function bgKey() {
  if (!exists(props.background)){
    return ""
  }
  var key = "".concat(props.background)
  if (props.background.length > 0){
    if (key[key.length - 1] === "?"){
      return key.slice(0, key.length - 1)
    }
  }
  return key
}
const backgroundParams = computed(() => {
  var result = null
  try{
    var key = bgKey()
    result = {"ID":`${backgrounds.backgrounds[key]['AoNID']}`}
  }
  catch (e){
    // console.log(e) // Mainly just logging safe typeerrors
    return null
  }
  return result
})
function renderLink() {
  var key = bgKey()
  var value = backgrounds.backgrounds[key]
  console.log(key)
  console.log(value)
  return value !== null && value !== undefined
  // return (backgroundParams["ID"] !== null && backgroundParams["ID"] !== undefined)
}

function setup(){
  return {renderLink}
}
</script>

<template>
  <Dynalink v-if="renderLink()"
    :inner-text="innerText"
    :domain="domain"
    :path="path"
    :params="backgroundParams"
    class="contents"
  />
  <p v-else class="contents">{{ innerText }}</p>
</template>

<style>
.contents {
  margin: 0;
  padding: 0;
}
</style>