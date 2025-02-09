<!-- This component displays containers for different categories when no entry is selected. When an entry is selected, it displays that entry via DataView. -->
<script setup>
import ArtContainer from './containers/ArtContainer.vue'
import DataView from './DataView.vue'
import IndexContainer from './containers/IndexContainer.vue'
import ListContainer from './containers/ListContainer.vue'
import { ref, reactive, computed, inject, watchEffect } from 'vue'
const DESELECTED = inject('DESELECTED')
const CATEGORIES = inject('CATEGORIES')
const viewData = inject('viewData')
const getSortKey = inject('getSortKey')
const exists = inject('exists')
const props = defineProps({
  maxID: { type:Number, required:true },
  sort_alpha: { type:String, default:"alphabetical" },
  sort_chrono: { type:String, default:"chronological" },
  art_view: { type:Number, default:0, required:true },
  index_view: { type:Number, default:1, required:true },
  list_view: { type:Number, default:2, required:true },
  viewMode: { type:Number, required:true },
  displayKey: { type:String, required:true },

  /* Add a prop for each category name here, named "{category}Key". Each 
  one just needs to be a required string. See also the MainView element 
  in the App.vue template. Also, for each of these props, add a 
  corresponding prop to DataView.vue's props. These are used to determine 
  which component DataView renders. */
  characterKey: { type: String, required: true },
  journalKey: { type: String, required: true },
  settingKey: { type: String, required: true },
})
const dataMap = defineModel('dataMap', { type:Object, required: true })
const selected = defineModel('selected', { type:Number, required: true })
const category = defineModel('category', { type:String, required: true })
const emit = defineEmits(['updateSelection'])

function noSelectionMade() { return selected.value === DESELECTED }
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
  for (let i = 0; i < CATEGORIES.length; i++){
    var curr = CATEGORIES[i];
    if (key === curr){
      return true
    }
  }
  return false
}

function isAValidId(id, category) {
  return id === DESELECTED || (id >= 0 && id < props.maxID);
}

function getSelectedEntry() {
  // Iterate through the category's data
  for (let i = 0; i < dataMap.value[props.category].length; i++){
    var currID = dataMap.value[props.category].at(i).id
    // Return the data when the selected ID is found
    if (selected.value === currID){
      return dataMap.value[props.category].at(i)
    }
  }
  return undefined
}

const arranged = computed(() => {
  if (isAValidKey(props.category)){
    console.log("props.category is valid")
    console.log(dataMap.value[props.category])
    return dataMap.value[props.category]
  }
})


function getSeeAlsoEntry(seeAlso={
  "id":DESELECTED, "category":"."
}){
  /* Get the displayValue for the "seeAlso" entry
  This is the part of the code that gets the name of the "seeAlso" entry.
  So if seeAlso is supposed to represent an arbitrary character Alice
  with an ID n, the object that gets pushed to the result will look like:
  {id:n, category:"characters", displayValue:"Alice"} */
  var displayKey = ""
  var displayValue = ""
  if (!exists(seeAlso.id)){ seeAlso.id = DESELECTED }
  if (!exists(seeAlso.category)){ seeAlso.category = props.category }
  if (seeAlso.id !== DESELECTED){
    if (seeAlso.category === "."){
      seeAlso.category = props.category
    }
    displayKey = getSortKey(seeAlso.category)

    // Get the displayValue
    try{
      for (let i = 0; i < dataMap.value[seeAlso.category].length; i++){
        if (seeAlso.id === dataMap.value[seeAlso.category].at(i).id){
          displayValue = dataMap.value[seeAlso.category].at(i).info[displayKey]
        }
      }
    }
    catch(e){ displayValue = "" }
  }

  return {
    id: seeAlso.id,
    category: seeAlso.category,
    displayValue: displayValue
  }
}

// Self-documenting. No need for comments
const seeAlso = computed(() => {
  var result = [];
  // Check that the category exists
  if (isAValidKey(props.category)){
    const entry = getSelectedEntry()

    if (exists(entry.info.seeAlso)){
      /* Get each "see also" from the entry
      These are objects that look like {"id":-1, "category":"."}
      Any category with a value of "." is a wildcard, which should be
      used to represent the same category that the entry belongs to. */
      for (let i = 0; i < entry.info.seeAlso.length; i++){
        var curr = getSeeAlsoEntry(entry.info.seeAlso[i])
        result.push(curr)
      }
    }
  }
  return result
})

const debug = computed(() => {
  return
  // var result = `MainView Stats: | viewMode: ${props.viewMode} | selected.value: ${selected.value} | noSelectionMade(): ${noSelectionMade()}`
  // result = result.concat(` | showArt(): ${showArt()} | showIndex(): ${showIndex()} | showList(): ${showList()}`)
  // return result
})

function updateSelection(id, category, caller="MainView") {
  if (isAValidKey(category)){
    if (isAValidId(id, category)){
      emit('updateSelection', id, category, caller)
    }
  }
  // if id or category isn't valid, there's no need to update!
}

const title = computed(() => { return props.category[0].toUpperCase().concat(props.category.slice(1).toLowerCase()) })
</script>

<template>  
  <div class="mainView">
    <!-- Containers
     To change the way the character art or names are shown, alter these 
     lines. If you only want art to be shown, only remove the 
     ListContainer element, and vice versa. The v-if and v-else-if 
     bindings need to be kept for each element, even if one element is 
     removed. To make changes to how these containers and their 
     respective elements are shown, you need to modify the file(s) of 
     whichever container(s) you plan to use.
     See the top of this file for file locations, in the imports section. -->
    <h3 v-if="debug">{{ debug }}</h3>    
    <h1 v-if="noSelectionMade()">{{ title }}</h1>
    <ArtContainer v-if="showArt()" :entries="arranged" 
    :category="category" :maxID="maxID" 
    :displayKey="props.displayKey"
    @update-selection="updateSelection">
    </ArtContainer>
    <IndexContainer v-else-if="showIndex()" :entries="arranged"
    :category="category" :maxID="maxID" 
    :displayKey="props.displayKey"
    @update-selection="updateSelection">
    </IndexContainer>
    <ListContainer v-else-if="showList()" :entries="arranged"
    :category="category" :maxID="maxID"
    :displayKey="props.displayKey"
    @update-selection="updateSelection">
    </ListContainer>
    <!-- end Containers -->
    <!-- DataView
      This component is in charge of displaying data.
      For each category of data you have (characters, etc), you need to
      write a binding for it and pass the  -->
    <DataView v-if="!noSelectionMade()"
      v-model:selected="selected" v-model:category="category"
      :entry="getSelectedEntry()"
      :characterKey="props.characterKey"
      :journalKey="props.journalKey"
      :settingKey="props.settingKey"
      :maxID="props.maxID"
      :seeAlso="seeAlso"
      @update-selection="updateSelection">
    </DataView>
  </div>
</template>

<style scoped>
.mainView {
  /* top: auto; */
  z-index: 0;
  margin: 0;
  padding: 0;
  display: flex;
  flex-flow: column nowrap;
  justify-content: flex-start;
  align-items: center;
}
</style>