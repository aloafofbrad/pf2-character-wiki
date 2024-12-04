<script setup>
import { ref, computed } from 'vue'
import Dynalink from '../Dynalink.vue';
import backgrounds from '../../data/backgrounds.json'

const props = defineProps({
  background:{ Type:String, Default:"" }
})

const addendum = computed (() => {
  var result = ""
  var key = bgKey()
  var rarity = "Common"
  try{
    rarity = backgrounds.backgrounds[key]["rarity"]
    if (rarity !== "Common") {
      result = `${rarity}!`
    }
  }
  catch (e){
    rarity = "Common"
  }
  return result
})

const innerText = computed(() => {
  var result = "Background: "
  if (props.background === "" || props.background === "?"){
    return result.concat("?")
  }
  if (addendum.value !== "" && addendum.value !== "?") {
    return result.concat(`${props.background} (${addendum.value})`)
  }
  return result.concat(`${props.background}`)
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
  return exists(value)
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
  />
  <p v-else>{{ innerText }}</p>
</template>

<style>
</style>