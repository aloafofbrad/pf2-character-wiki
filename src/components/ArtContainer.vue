<script setup>
import Tile from './Tile.vue';
import { ref, computed } from 'vue'
const props = defineProps({
  entries: {
    Type: Array,
    default: []
  }
})

const emit = defineEmits(['handleTileClick'])

function isAValidId(id) {
  return (id >= 0 && id <= (props.entries.length - 1))
}

</script>

<template>
  <div id="ArtContainer">
    <Tile
      v-show="isAValidId(entry.id)"
      v-for="entry in props.entries"
      :key="entry.id"
      :info="entry.info"
      @click="$emit('handleTileClick', entry.id)">
    </Tile>
  </div>
</template>

<style scoped>

#ArtContainer {
  max-width: 100vw;
  min-height: 100%;
  display: flex;
  flex-flow: row wrap;
  align-content: center;
  scroll-behavior: smooth;
  overflow-y: auto;
  min-height: auto;
  padding-bottom: 24px;

  .Tile {
    margin: 2px;
  }
}

@media only screen and (orientation: landscape){
  #ArtContainer {
    justify-content: center;
  }
}

@media only screen and (orientation: portrait){
  #ArtContainer {
    justify-content: center;
  }
}

</style>