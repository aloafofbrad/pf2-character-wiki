<script setup>

import { ref, computed } from 'vue'

/* Props
  id
  category
 */
const props = defineProps({
  id: { type:Number, required: true },
  category: { type:String, required: true }
})
const emit = defineEmits(['updateSelection'])
const hover = ref(false)
function updateSelection(id, category, caller="EntryLink") {
  emit('updateSelection', id, category, caller)
}
function open(){ updateSelection(props.id, props.category) }
</script>

<template>
  <div class="entrylink" @click="open()" @mouseenter="hover=true" @mouseleave="hover=false">
    <p>
      <slot></slot>
    </p>
  </div>
</template>

<style>
.entrylink {
  color: inherit;
  background-color: inherit;

  &:hover {
    color: inherit;
    background-color: inherit;
  }
}
</style>