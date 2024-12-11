<script setup>
import Tag from '../Tag.vue';
import { ref, computed } from 'vue'

/* Props
    value       The value to be rendered
    type        The type associated with the instance of this component
    
    showables   If props.value is in this, the component will be 
                rendered. Overrides hideables; if a value is in both 
                lists, the component will render.
    hideables   If props.value is in this, the component won't be 
                rendered. Overridden by showables.
    
    checkType   If true, isShowable() checks that props.type is in 
                showables and not in hideables. Overrides props.value,
                regardless of which lists props.value is in.
    renderTag   If true, renders this component within a Tag.
 */
const props = defineProps({
  value: { type:String, default: "" },
  type: { type:String, default: "Normal", required: false },
  showables: { type:Array, default: [], required: false },
  hideables: { type:Array, default: [], required: false },
  checkType: { type:Boolean, default: false, required: false },
  renderTag: { type:Boolean, default: false, required: false },
})

function isInList(value, target){ return target.includes(value) }

const isShowable = computed(() => {
  var result = true

  // If there's nothing to see, no point in rendering
  if (props.value === ""){ return false }
  if (props.checkType){
    if (isInList(props.type, props.hideables)){ result = false }
    if (isInList(props.type, props.showables)){ result = true }
  }
  else {
    if (isInList(props.value, props.hideables)){ result = false }
    if (isInList(props.value, props.showables)){ result = true }
  }

  return result
})

const renderTag = computed(() => {
  return props.renderTag && isShowable.value
})

const innerText = computed(() => {
  var result = `Status: `
  result = result.concat(`${props.value}`)
  return result
})
</script>

<template>
  <Tag v-if="renderTag"><p>{{ innerText }}</p></Tag>
  <p v-else-if="isShowable">{{ innerText }}</p>
</template>

<style>
</style>