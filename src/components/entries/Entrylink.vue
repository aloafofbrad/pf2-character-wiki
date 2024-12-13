<script setup>
import { ref, computed, inject } from 'vue'
const exists = inject("exists")
/* Props
  id
  category
  active_css
  inactive_css
 */
const props = defineProps({
  id: { type:Number, default:null, required:false },
  category: { type:String, default:null, required:false },
  start: { type:Number, default:null, required:false },
  index: { type:Number, default:null, required:false },
  end: { type:Number, default:null, required:false },
  length: { type:Number, default:null, required:false },
  active_css:  { type:String, default:"activeEL", required:false },
  inactive_css: { type:String, default:"inactiveEL", required:false },
  tooltips: { type:Boolean, default:false, required:false },
  debug: { type:Boolean, default:false, required:false }
})
const emit = defineEmits(['updateSelection'])
const hover = ref(false)
const VALID = computed(() => {
  return exists(props.id) && exists(props.category)
})
function updateSelection(id, category, caller="EntryLink") {
  emit('updateSelection', id, category, caller)
}
function open(){ updateSelection(props.id, props.category) }
function tryOpen(){ if (VALID.value) { open() } }
const CSSclass = computed(() => {
  var result = "entrylink "
  if (VALID.value){ return result.concat(props.active_css) }
  if (props.debug){ result = result.concat("debugEL ")}
  return result.concat(props.inactive_css)
})
function title(){
  if (!props.tooltips || !VALID.value) { return ''}
  if (props.debug){
    return `characters: ${props.start}-${props.end} (${props.index}), link: (${props.id}, ${props.category})`
  }
  return `(${props.id}, ${props.category})`
}
</script>

<template>
  <span :class="CSSclass" @click="tryOpen" @mouseenter="hover=true" @mouseleave="hover=false" :title="title()"><slot></slot></span>
</template>

<style>
.inactiveEL {
  color: inherit;
  background-color: inherit;

  &:hover {
    color: inherit;
    background-color: inherit;
  }
}

.debugEL {
  &:nth-child(even){
    color: black;
    background-color: #babaff;
  }

  &:nth-child(odd){
    color: black;
    background-color: #ffbaba;
  }
}

.activeEL {
  color: #b4dd1e;
  background-color: inherit;
  text-decoration: underline;

  &:hover {
    color: black;
    background-color: #b4dd1e;
  }
}
</style>