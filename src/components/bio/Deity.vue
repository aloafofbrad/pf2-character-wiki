<script setup>
import { ref, computed } from 'vue'
import Dynalink from '../Dynalink.vue'
import deities from '../../data/deities.json'

const props = defineProps({
  deity: {
    type:String,
    default:""
  }
})

function exists(x) {
  return x !== null && x !== undefined
}

function deityKey() {
  if (!exists(props.deity)){
    return ""
  }
  var key = "".concat(props.deity)
  if (props.deity.length > 0){
    if (key[key.length - 1] === "?"){
      return key.slice(0, key.length - 1)
    }
  }
  return key
}

const innerText = computed(() => {
  var result = "Deity: "
  return result.concat(`${props.deity}`)
})

const domain = ref('https://2e.aonprd.com/')
const path = ref('Deities.aspx')

const ancestryParams = computed(() => {
  var result = null
  try{
    var key = deityKey()
    console.log(deities.deities[key]['AoNID'])
    result = {"ID":`${deities.deities[key]['AoNID']}`}
  }
  catch (e){
    return null
  }
  return result
})

function renderLink() {
  var key = deityKey()
  var value = deities.deities[key]
  return exists(value)
}

function setup(){
  return {key, renderLink}
}
</script>

<template>
  <Dynalink v-if="renderLink()"
    :inner-text="innerText"
    :domain="domain"
    :path="path"
    :params="ancestryParams"
  />
  <p v-else>{{ innerText }}</p>
</template>

<style>
</style>