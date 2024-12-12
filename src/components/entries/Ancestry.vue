<script setup>
import { ref, computed, inject } from 'vue'
import Dynalink from '../Dynalink.vue'
import ancestries from '../../data/ancestries.json'
const exists = inject('exists')
const domain = ref('https://2e.aonprd.com/')
const path = ref('Ancestries.aspx')
const props = defineProps({
  ancestry: { type:String, default:"" },
  heritage: { type:String, default:"" },
  invalidHeritages: { type:Array, default:["", "?"], required:false }
})

function anKey() {
  if (!exists(props.ancestry)){ return "" }
  var key = "".concat(props.ancestry)
  if (props.ancestry.length > 0){
    if (key[key.length - 1] === "?"){
      return key.slice(0, key.length - 1)
    }
  }
  return key
}

function heritageIsValid(){
  return !props.invalidHeritages.includes(props.heritage)
}

const innerText = computed(() => {
  var result = "Ancestry: "
  if (heritageIsValid()){
    return result.concat(`${props.ancestry} (${props.heritage})`)
  }
  return result.concat(`${props.ancestry}`)
})

const ancestryParams = computed(() => {
  var result = null
  try{
    var key = anKey()
    result = {"ID":`${ancestries.ancestries[key]['AoNID']}`}
  }
  catch (e){
    // console.log(e) // Mainly just logging safe typeerrors
    return null
  }
  return result
})

function renderLink() {
  var key = anKey()
  var value = ancestries.ancestries[key]
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