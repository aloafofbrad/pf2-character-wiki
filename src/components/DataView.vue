<script setup>
import Bio from './bio/Bio.vue'
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

/* Helper for dataMap
    Tests if a key exists in dataMap
    args:
    key   the key to test
*/
function isAValidKey(key){
  for (let i = 0; i < props.validCategories.length; i++){
    var curr = props.validCategories[i];
    console.log(curr)
    if (key === curr){
      return true
    }
  }
  return false
}

/* Returns the selected entry. This is expected to be an integer equal to
or larger than 0, but at most equal to the number of entries in the array */
// function getSelectedEntry() {
//   // console.log("getSelectedEntry()")
//   // console.log("dataMap.value: ", dataMap.value)
//   // console.log("props.category: ", props.category)
//   console.log("selected.value: ", selected.value)

//   // var result = dataMap.value[props.category].at(selected.value) // saved as comment for posterity/sanity
//   var result = dataMap.value[props.category].at(selected.value) // works
//   // console.log("result: ", result)
//   return result
// }

/* Returns true if the selected entry is the deselected value */
function noSelectionMade() { return selected.value === DESELECTED }

const debug = computed(() => {
  var result = `DataView Stats: | viewMode: ${props.viewMode} | selected.value: ${selected.value} | props.category: ${props.category}`
  return result
})

function updateSelection(id, category){
  emit('updateSelection', id, category)
}
</script>

<template>  
  <div class="dataView">
    <div>
      <h3>{{ debug }}</h3>
    </div>
    <!-- Bio
     To change data shown in the Bio, or the way that data is shown,
     you'll need to modify the file for the Bio component (see the top of
     this file for its location, in the imports section). Don't change
     the v-show binding here, regardless of which containers are shown.
     -->
    <div id="bio" v-show="showDataFromCategory(props.characterData)">
      <Bio
        :ID="selected"
        :info="props.entry.info"
        :category="category"
        @update-selection="updateSelection">
      </Bio>
    </div>
    <!-- end Bio -->
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