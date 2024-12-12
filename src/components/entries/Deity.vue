<script setup>
import { ref, computed, inject } from 'vue'
import Dynalink from '../Dynalink.vue'
import deities from '../../data/deities.json'
const exists = inject('exists')
const domain = ref('https://2e.aonprd.com/')
const path = ref('Deities.aspx')
const props = defineProps({
  deity: { type:String, default:"" },
  prefix: { type:String, default:"Deity: ", required:false }
})

function deityKey() {
  if (!exists(props.deity)){ return "" }
  var key = "".concat(props.deity)
  if (props.deity.length > 0){
    if (key[key.length - 1] === "?"){
      return key.slice(0, key.length - 1)
    }
  }
  return key
}

const innerText = computed(() => {
  return props.prefix.concat(`${props.deity}`)
})

const ancestryParams = computed(() => {
  var result = null
  try{
    var key = deityKey()
    // console.log(deities.deities[key]['AoNID'])
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