<!-- This component displays the appropriate entry for the given category. -->
<script setup>
import CharacterEntry from './entries/CharacterEntry.vue'
import { ref, reactive, computed, inject, watchEffect } from 'vue'
const DESELECTED = inject('DESELECTED')
const props = defineProps({
  characterData: { type: String, required: true },
  journalData: { type: String, required: true },
  settingData: { type: String, required: true },
  entry: { type:Object }
})
const selected = defineModel('selected', { type:Number, required: true })
const category = defineModel('category', { type:String, required: true })
const emit = defineEmits(['updateSelection'])

function showDataFromCategory(category){
  if (!noSelectionMade()){
    return props.category === category
  }
  return false
}

/* Returns true if the selected entry is the deselected value */
function noSelectionMade() { return selected.value === DESELECTED }

const debug = computed(() => {
  var result = `DataView Stats: | viewMode: ${props.viewMode} | selected.value: ${selected.value} | props.category: ${props.category}`
  return result
})

function updateSelection(id, category){
  console.log(`DataView updateSelection(${id}, ${category})`)
  emit('updateSelection', id, category)
}
</script>

<template>  
  <div class="dataView">
    <div>
      <h3>{{ debug }}</h3>
    </div>
    <!-- CharacterEntry
     To change data shown in the CharacterEntry, or the way that data is 
     shown, you'll need to modify the file for the CharacterEntry 
     component (see the top of this file for its location, in the 
     imports section). Don't change the v-show binding here, regardless 
     of which containers are shown.
     -->
    <div id="bio" v-show="showDataFromCategory(props.characterData)">
      <CharacterEntry
        :ID="selected"
        :info="props.entry.info"
        :category="category"
        @update-selection="updateSelection">
      </CharacterEntry>
    </div>
    <!-- end CharacterEntry -->
    <!-- TODO: JOURNAL -->
    <!-- TODO: SETTINGS -->
  </div>
</template>

<style scoped>
.dataView {
  top: auto;
  z-index: 1;
  margin: 0;
  padding: 0;
  display: flex;
  flex-flow: column nowrap;
  justify-content: flex-start;
  align-items: center;
  flex-grow: 1;
}
</style>