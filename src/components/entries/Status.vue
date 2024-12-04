<script setup>
import Tag from '../Tag.vue';
import { ref, computed } from 'vue'

/* Props
    value             The value to be rendered
    type              The type associated with the instance of this
                      component
    showableValues    If props.value is in this, the component will be 
                      rendered. Overrides hideableValues.
    hideableValues    If props.value is in this, the component won't be
                      rendered. Overridden by showableValues.
    checkType         If true, showable() checks that props.type is in
                      showableValues and not in hideableValues.
    renderTag         If true, renders this component within a Tag.
 */
const props = defineProps({
  value: { type:String, default: "" },
  type: { type:String, default: "Normal", required: false },
  showableValues: { type:Array, required: false, default: ["Player", 
  "Normal", "Dead", "In Party"
  ] },
  hideableValues: { type:Array, required: false, default: ["Generic"] },
  checkType: { type:Boolean, default: false, required: false },
  renderTag: { type:Boolean, default: false, required: false },
})

function isIn(value, target){
  for (let i = 0; i < target.length; i++){
    if (value === target.at(i)){ return true }
  }
  return false
}

function isInShowables(value){ return isIn(value, props.showableValues) }
function isInHideables(value){ return isIn(value, props.hideableValues) }

function showable(){
  var result = true
  if (isInHideables(props.value)){ result = false }
  if (isInShowables(props.value)){ result = true }
  if (props.checkType){
    if (isInHideables(props.type)){ result = false }
    if (isInShowables(props.type)){ result = true }
  }
  return result
}

function renderTag(){
  return props.renderTag && showable()
}

const innerText = computed(() => {
  var result = `Status: `
  result = result.concat(`${props.value}`)
  return result
})
</script>

<template>
  <Tag v-if="renderTag()"><p>{{ innerText }}</p></Tag>
  <p v-else-if="showable()">{{ innerText }}</p>
</template>

<style>
</style>