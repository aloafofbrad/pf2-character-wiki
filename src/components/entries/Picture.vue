<script setup>
import { computed, inject } from 'vue'
const exists = inject('exists')
const props = defineProps({
  src:{ Type:String, default:"", required:true },
  placeholder: { Type:String, default:"", required:false },
  alt:{ Type:String, default:"", required:false },
  renderOnPlaceholder: { Type:Boolean, default: true, required: false}
})

function isEmptyString(s){ return s === "" }

// Determines if props.src is "renderable"
const sourceIsRenderable = computed(() => {
  return exists(props.src) && !isEmptyString(props.src)
})

// Returns the URL to be bound in the img element
const source = computed(() => {
  if (sourceIsRenderable.value){
    return new URL(`/${props.src}`, import.meta.url)
  }
  return new URL(`/${props.placeholder}`, import.meta.url)
})

/* Checks if the component should be rendered at all. Returns true
if either src is a valid URL, or if the component is set to render
when a URL to a placeholder image is given in props.placeholder */
const isShowable = computed(() => {
  if (sourceIsRenderable.value){ return true }
  return props.renderOnPlaceholder
})
</script>

<template>
  <img v-if="isShowable" :src="source" :alt="props.alt"/>
</template>

<style>
</style>