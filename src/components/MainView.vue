<script setup>
import ArtContainer from './containers/ArtContainer.vue'
import DataView from './DataView.vue'
import IndexContainer from './containers/IndexContainer.vue'
import ListContainer from './containers/ListContainer.vue'
import { ref, reactive, computed, inject, watchEffect } from 'vue'
const DESELECTED = inject('DESELECTED')
const CATEGORIES = inject('CATEGORIES')
const props = defineProps({
  sort_alpha: { type: String, default: "alphabetical" },
  sort_chrono: { type: String, default: "chronological" },
  art_view: { type: Number, default: 0, required: true },
  index_view: { type: Number, default: 1, required: true },
  list_view: { type: Number, default: 2, required: true },
  multi_view_enabled: { type: Boolean, default: false },
  viewMode: { type: Number, required: true },

  /* Add a prop for each category name here. Each one just needs to be a
  required string. See also the MainView element in the App.vue
  template. */
  characterData: { type: String, required: true },
  journalData: { type: String, required: true },
  settingData: { type: String, required: true },
})
const dataMap = defineModel('dataMap', { type:Object, required: true })
const selected = defineModel('selected', { type:Number, required: true })
const category = defineModel('category', { type:String, required: true })
const emit = defineEmits(['updateSelection'])

function noSelectionMade() {
  return selected.value === DESELECTED
}
function showArt(){
  return props.viewMode === props.art_view && noSelectionMade()
}
function showIndex(){
  return props.viewMode === props.index_view && noSelectionMade()
}
function showList(){
  return props.viewMode === props.list_view && noSelectionMade()
}

/* Helper for dataMap
    Tests if a key exists in dataMap
    args:
    key   the key to test
*/
function isAValidKey(key) {
  // const result = CATEGORIES().find((k) => k === key);
  // return result
  for (let i = 0; i < CATEGORIES.length; i++){
    var curr = CATEGORIES[i];
    // console.log(curr)
    if (key === curr){
      return true
    }
  }
  return false
}

function isAValidId(id, category) {
  return id === DESELECTED || (id >= 0 && id < dataMap.value[category].length);
}

function getSelectedEntry() {
  // var result = dataMap.value[props.category].at(selected.value + 1) // works; saved as comment for posterity/sanity
  var result = dataMap.value[props.category].at(selected.value + 1) // works
  return result
}

const arranged = computed(() => {
  if (isAValidKey(props.category)){
    console.log("props.category is valid")
    console.log(dataMap.value[props.category])
    return dataMap.value[props.category]
    // return dataMap.value[props.category].filter(entry => matchesRegex(entry['info']['name']).toLowerCase(), regex);
  }
})

const debug = computed(() => {
  var result = `MainView Stats: | viewMode: ${props.viewMode} | selected.value: ${selected.value} | noSelectionMade(): ${noSelectionMade()}`
  result = result.concat(` | showArt(): ${showArt()} | showIndex(): ${showIndex()} | showList(): ${showList()}`)
  return result
})

function updateSelection(id, category) {
  if (isAValidKey(category)){
    if (isAValidId(id, category)){
      console.log("updateSelection()", id, ", ", category)
      emit('updateSelection', id, category)
    }
  }
  // if id or category isn't valid, there's no need to update!
}
</script>

<template>  
  <div class="mainView">
    <!-- Containers
     To change the way the character art or names are shown, alter these lines. If you only want art to
     be shown, only remove the ListContainer element, and vice versa. The v-show bindings need to be kept
     for each element, even if one element is removed. To make changes to how these containers and their
     respective elements are shown, you need to modify the file(s) of whichever container(s) you plan to
     use. See the top of this file for file locations, in the imports section. -->
    <div>
      <h3>{{ debug }}</h3>
    </div>
    <ArtContainer v-show="showArt()" :entries="arranged" :category="category" @update-selection="updateSelection"></ArtContainer>
    <IndexContainer v-show="showIndex()" :entries="arranged" @update-selection="updateSelection"></IndexContainer>
    <ListContainer v-show="showList()" :entries="arranged" @update-selection="updateSelection"></ListContainer>
    <!-- end Containers -->
    <!-- DataView
      This component is in charge of displaying data.
      For each category of data you have (characters, etc), you need to
      write a binding for it and pass the  -->
    <DataView v-show="!noSelectionMade()"
      v-model:selected="selected" v-model:category="category"
      :entry="getSelectedEntry()"
      :characterData="props.characterData"
      :journalData="props.journalData"
      :settingData="props.settingData"
      @update-selection="updateSelection">
    </DataView>
  </div>
</template>

<style scoped>
.mainView {
  top: auto;
  z-index: 0;
  margin: 0;
  padding: 0;
  display: flex;
  flex-flow: column nowrap;
  justify-content: flex-start;
  align-items: center;
  flex-grow: 1;
}
</style>