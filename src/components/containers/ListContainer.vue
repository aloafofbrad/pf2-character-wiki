<script setup>
import Tag from '../Tag.vue';
import { ref, computed } from 'vue'
const props = defineProps({
  entries: { Type: Array, default: [] },
  category: { Type: String, required: true },
  maxID: { type: Number, required: true },
  displayKey: { type: String, required: true },
})
const emit = defineEmits(['updateSelection'])

function isAValidId(id) {
  // return (id >= 0 && id <= (props.entries.length - 1))
  console.log(`id (${id}) < props.maxID (${props.maxID})`)
  return (id >= 0 && id < props.maxID)
}

function entryClick(id) {
  emit('updateSelection', id, props.category, "ListContainer")
}

function display(entry) { return entry.info[props.displayKey] }

</script>

<template>
  <div class="listContainer">
    <Tag v-show="isAValidId(entry.id)" v-for="entry in props.entries" @click="entryClick(entry.id)">
      {{ display(entry) }}
    </Tag>
  </div>
</template>

<style scoped>

.listContainer {
  max-width: 100vw;
  width: 120%;
  min-height: 100%;
  display: flex;
  flex-flow: column nowrap;
  align-items: flex-start;
  justify-content: center;
  scroll-behavior: smooth;
  overflow-y: auto;
  min-height: auto;

  .tag {
    margin-left: 12px;
    margin-right: 12px;
    overflow-x: hidden;
    color: black;
    background-color: white;
  }

  .tag:hover {
    background-color: #b4dd1e;
  }
}

</style>