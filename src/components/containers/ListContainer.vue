<script setup>
import Tag from '../Tag.vue';
import { ref, computed } from 'vue'
const props = defineProps({
  entries: { Type: Array, default: [] },
  category: { Type: String, required: true }
})

const emit = defineEmits(['updateSelection'])

function isAValidId(id) {
  return (id >= 0 && id <= (props.entries.length - 1))
}

function entryClick(id) {
  console.log("entry clicked, id: ", id)
  emit('updateSelection', id)
}

</script>

<template>
  <div class="listContainer">
    <Tag v-show="isAValidId(entry.id)" v-for="entry in props.entries" @click="entryClick(entry.id)">
      {{ entry.info.name }}
    </Tag>
  </div>
</template>

<style scoped>

.listContainer {
  max-width: 100vw;
  min-height: 100%;
  display: flex;
  flex-flow: column nowrap;
  align-items: flex-start;
  justify-content: center;
  scroll-behavior: smooth;
  overflow-y: auto;
  min-height: auto;

  .tag {
    margin-left: 8px;
    margin-right: 8px;
    overflow-x: hidden;
    color: black;
    background-color: white;
  }

  .tag:hover {
    background-color: #b4dd1e;
  }
}

</style>