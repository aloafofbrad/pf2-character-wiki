<script setup>

import Entrylink from './Entrylink.vue';
import Tag from '../Tag.vue';
import { ref, computed, inject } from 'vue'
const DESELECTED = inject('DESELECTED')
const CATEGORIES = inject('CATEGORIES')

const props = defineProps({
  id: { type:Number, required: true },
  category: { type:String, required: true },
  maxID: { type:Number, required: true },
  debug: { type:Boolean, default: true, required: false }
})
const emit = defineEmits(['updateSelection'])
// TODO: fix the off-by-one error that means I have to use props.maxID - 2
function prevID(){return props.id === 0 ? props.maxID - 2 : props.id - 1;}
function nextID(){return props.id === props.maxID - 2 ? 0 : props.id + 1;}
function updateSelection(id, category, caller="EntryChanger") {
  if (props.debug){
    console.log(`Entrychanger: curr: ${props.id}, next: ${id}, maxID: ${props.maxID}`)
  }
  emit('updateSelection', id, category, caller)
}
function goTo(id, category, caller="EntryChanger"){
  updateSelection(id, category, caller)
}
function close() { updateSelection(DESELECTED, props.category) }
</script>

<template>
  <div class="entryChanger">
    <Tag class="prevent-select"><Entrylink :id="DESELECTED" :category="props.category" @updateSelection="close">■Exit</Entrylink></Tag>
    <Tag class="prevent-select"><Entrylink :id="prevID()" :category="props.category" @updateSelection="goTo">■Prev</Entrylink></Tag>
    <Tag class="prevent-select"><Entrylink :id="nextID()" :category="props.category" @updateSelection="goTo">■Next</Entrylink></Tag>
    <Tag>Curr: {{ props.id }}</Tag>
  </div>
</template>

<style>
.entryChanger {
    display: flex;
    flex-flow: row nowrap;
    width: 100%;
    justify-content: center;
    align-items: center;
    font-size: medium;
    font-family: monospace;

    .tag {
      color: white;
      background-color: rgba(0,0,0,0);
      border-radius: 0;
      transition-duration: 0ms;
      font-size: inherit;
      font-family: inherit;

      * {
        color: inherit;
        font-size: inherit;
        font-family: inherit;
      }

      &:hover {
        color: black;
        background-color: white;
        scale: calc(1);
        transition-duration: 0ms;
      }

      &:hover::selection {
        color: white;
        background-color: black;
      }

      &::selection {
        color: white;
        background-color: rgba(0,0,0,0);
      }
    }
  }
</style>