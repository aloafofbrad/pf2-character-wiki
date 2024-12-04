<script setup>
import Tile from '../Tile.vue';
import { ref, computed } from 'vue'
const props = defineProps({
  entries: { Type: Array, default: [] },
  category: { Type: String, required: true },
  maxID: { type: Number, required: true },
  displayKey: { type: String, required: true },
})

const emit = defineEmits(['updateSelection'])

function isAValidId(id) {
  return (id >= 0 && id < props.maxID)
}

function entryClick(id) {
  emit('updateSelection', id, props.category, "ArtContainer")
}

</script>

<template>
  <div class="artContainer">
    <Tile
      v-show="isAValidId(entry.id)"
      v-for="entry in props.entries"
      :id="entry.id"
      :info="entry.info"
      :displayKey="props.displayKey"
      @click="entryClick(entry.id)">
    </Tile>
  </div>
</template>

<style scoped>

.artContainer {
  max-width: 100vw;
  min-height: 100%;
  display: flex;
  flex-flow: row wrap;
  align-items: flex-start;
  justify-content: center;
  align-content: flex-start;
  scroll-behavior: smooth;
  overflow-y: auto;
  min-height: auto;
  padding-bottom: 24px;

  .Tile {
    margin: 2px;
  }
}

</style>