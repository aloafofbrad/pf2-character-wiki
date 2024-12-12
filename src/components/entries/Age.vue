<script setup>
import { ref, computed, inject } from 'vue'
import ancestries from '../../data/ancestries.json'
const exists = inject('exists')
const props = defineProps({
  age: {
    type: Object,
    default: {
        "age":"",
        "exact":false,
    }
  },
  ancestry: {
    type: String,
    default: ""
  },
  calculateHumanYears:{
    type:Boolean,
    default:false
  }
})

function anKey() {
  if (!exists(props.ancestry)){
    return ""
  }
  var key = "".concat(props.ancestry)
  if (props.ancestry.length > 0){
    if (key[key.length - 1] === "?"){
      return key.slice(0, key.length - 1)
    }
  }
  return key
}

const doCalculation = ref(false) // separate from props to allow overriding in case of missing Ancestry data

const lifespan = computed(() => {
    var result = 73
    try {
        result = ancestries.ancestries[props.ancestry].lifespan
        doCalculation.value = true
    }
    catch (e){
        console.log(e)
        result = -2
        doCalculation.value = false
    }
    return result
})
const age = computed(() => {
    var result = "Age: "
    if (props.age === undefined && (props.ancestry === undefined || props.ancestry === '')){
        return result.concat("?")
    }
    if (props.age.age === ""){
        return result.concat("?")
    }
    if (props.age.exact){
        result = result.concat(`${props.age.age}`)
    }
    else{
        result = result.concat(`About ${props.age.age}`)
    }
    if ((doCalculation.value || props.calculateHumanYears) && props.ancestry !== undefined && props.ancestry !== "Human"){
        // Don't worry, this works, trust me
        var growthFactor = Math.abs(1 / props.ancestry.lifespan)
        var humanYears = props.age.age * growthFactor * 73
        result = result.concat(` (${humanYears} H.Y.)`)
    }
    return result
})

function showHumanYears() {
    if (doCalculation){
        return exists(props.ancestry) && props.ancestry !== 'Human'
    }
    return false
}

</script>

<template>
    <p v-if="showHumanYears()" tooltip="Human Years">{{ age }}</p>
    <p v-else>{{ age }}</p>
</template>

<style>
</style>