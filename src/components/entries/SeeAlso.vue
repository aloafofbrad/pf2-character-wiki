<script setup>
import Tag from '../Tag.vue';
import { computed, inject } from 'vue'
const DESELECTED = inject('DESELECTED')
const props = defineProps({
  contents: { type:Array, default:[] },
  unrenderable: { type:Object, required: false, default: {
    "id":-1,
    "category":".",
    "displayValue":""
  }}
})
const emit = defineEmits(['updateSelection'])

function exists(x) { return x !== undefined && x !== null }
function isRenderable(entry){
  if (!exists(entry.id)){ return false }
  if (!exists(entry.category)){ return false }
  if (!exists(entry.displayValue)){ return false }
  if (entry.id === DESELECTED){ return false }
  if (entry.displayValue === ""){ return false }
  return true
}

const arranged = computed(() => {
  var result = [];
  for (let i = 0; i < props.contents.length; i++){
    var curr = props.contents[i]
    console.log(curr)
    if (isRenderable(curr)){ result.push(curr) }
  }
  console.log("See Also (below):")
  console.log(result)
  return result
})

function updateSelection(id, category, caller="SeeAlso"){
  emit('updateSelection', id, category, caller)
}
function goTo(id, category){ updateSelection(id, category) }
</script>

<template>
  <div class="seeAlso">
    <Tag v-for="obj in arranged" @click="goTo(obj.id, obj.category)">
      <p>{{ obj.displayValue }}</p>
    </Tag>
  </div>
</template>

<style scoped>
.seeAlso {
  flex-flow: column wrap;
  justify-content: flex-start;
  align-items: flex-start;
  margin-top: 1.5em;

  p {
    margin-top: unset;
    margin-bottom: 0.25em;
    text-indent: 1.5em;
  }
  
  p:first-of-type {
    text-indent: 0;
  }
}
</style>