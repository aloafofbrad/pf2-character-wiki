<!-- This component displays information for characters. The main way to change what info is shown (and how) is to modify the components that are shown; rearrange/rewite/delete them; or create new ones entirely. -->
<script setup>
import Name from './Name.vue'
import Tag from '../Tag.vue'
import { ref, computed, inject } from 'vue'
const DESELECTED = inject('DESELECTED')
const CATEGORIES = inject('CATEGORIES')
const props = defineProps({
  category: { type:String, required: true },
})
const emit = defineEmits(['updateSelection'])

function updateSelection(id, category) {
  console.log(`Deselect updateSelection(${id}, ${category})`)
  emit('updateSelection', id, category)
}

function close() { updateSelection(DESELECTED, props.category) }
</script>

<template>
  <div class="deselect prevent-select" @click="close()">
    <p>❌</p>
  </div>
</template>

<style>
.deselect {
  position: absolute;
  left: calc(100% - 3em - 24px);
  z-index: 3;
  font-family: monospace;
  font-weight: bold;
  text-align: center;
  background-color: white;
  color: black;
  padding: 4px 4px 4px 4px;
  margin: 4px 4px 4px 4px;
  border-radius: 32px;
  filter:grayscale(1.0);
}
.deselect:hover, .deselect:hover > * {
  scale: calc(1.05);
}
.deselect, .deselect > * {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  text-align: center;
  height: 32px;
  width: 32px;
}

</style>