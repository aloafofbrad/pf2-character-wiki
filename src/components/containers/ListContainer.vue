<script setup>
import Tag from '../Tag.vue';
import { ref, computed } from 'vue'
const props = defineProps({
  entries: {
    Type: Array,
    default: []
  }
})

const emit = defineEmits(['updateSelection'])

function isAValidId(id) {
  return (id >= 0 && id <= (props.entries.length - 1))
}

</script>

<template>
  <div id="ListContainer">
    <Tag v-show="isAValidId(entry.id)" v-for="entry in props.entries" @click="$emit('updateSelection', entry.id)">
      {{ entry.info.name }}
    </Tag>
  </div>
</template>

<style scoped>

#ListContainer {
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
  }
}

</style>