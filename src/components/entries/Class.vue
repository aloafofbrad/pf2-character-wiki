<script setup>
import { ref, computed, inject } from 'vue'
import Dynalink from '../Dynalink.vue'
import classes from '../../data/classes.json'
const exists = inject('exists')
const props = defineProps({
  class: {
    type:String,
    default:""
  },
  level: {
    type:String,
    default:""
  }
})

function classKey() {
  if (!exists(props.class)){
    return ""
  }
  var key = "".concat(props.class)
  if (props.class.length > 0){
    if (key[key.length - 1] === "?"){
      return key.slice(0, key.length - 1)
    }
  }
  return key
}

const innerText = computed(() => {
  var result = "Class: "
  if (props.level === "" || props.level === "?"){
    return result.concat(`${props.class}`)
  }
  
  // Select a suffix based on the level provided.
  // Since the expected range of numbers is only 1-20,
  // (maybe sometimes 0), levels 1-3 are the only ones
  // that use suffixes other than "th".
  var levelSuffix = "th"
  if (props.level === "1") {      levelSuffix = "st" }
  else if (props.level === "2") { levelSuffix = "nd" }
  else if (props.level === "3") { levelSuffix = "rd" }

  return result.concat(`${props.level}${levelSuffix}-level ${props.class}`)
})

const domain = ref('https://2e.aonprd.com/')
const path = ref('Classes.aspx')

const classParams = computed(() => {
  var result = null
  try{
    var key = classKey()
    // console.log(classes.classes[key]['AoNID'])
    result = {"ID":`${classes.classes[key]['AoNID']}`}
  }
  catch (e){
    return null
  }
  return result
})

function renderLink() {
  var key = classKey()
  var value = classes.classes[key]
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
    :params="classParams"
    class="contents"
  />
  <p v-else class="contents">{{ innerText }}</p>
</template>

<style>
</style>