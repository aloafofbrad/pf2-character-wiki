<script setup>
import ArtContainer from './components/ArtContainer.vue'
import Bio from './components/Bio.vue'
import ListContainer from './components/ListContainer.vue'
import Navbar from './components/Navbar.vue'
import { ref, reactive, computed } from 'vue'
import packageJson from "../package.json"

import data from './data/characters.json'

const source = `https://github.com/aloafofbrad/pf2-character-wiki`

var entries = ref([])

for (let i = 0; i < data.data.length; i++){
  entries.value.push(data.data[i])
}

console.log("entries:")
console.log(entries.value)

const DESELECTED = -1
const SORT_DEFAULT = "default"
const SORT_ALPHA = "alphabetical"
const SORT_CHRONO = "chronological"
const SORT_ALPHA_DESC = "alphabetical_desc"
const SORT_CHRONO_DESC = "chronological_desc"

const selected = ref(DESELECTED)
const history = ref([DESELECTED,])
const index = ref(0)
const userRegex = ref('')
const SEARCH_BLEACH = "/[^a-zA-Z0-9 -\?]/g"

const ART_VIEW = 0
const LIST_VIEW = 1
const DEFAULT_VIEW = ART_VIEW
const MULTI_VIEW_ENABLED = true
const viewMode = ref(DEFAULT_VIEW)

// Comparisons & helpers
function DNE(arg) {
  return arg === null || arg === undefined
}

function compareAgainstDNE(a, b) {
  // console.log("CompareAgainstDNE: " + a + ", " + b)
  if (!DNE(a) && DNE(b)) {
    return -1
  }
  if (DNE(a) && !DNE(b)) {
    return 1
  }
  return 0
}

function compareDataByKey(a, b, key) {
  if (DNE(a['info'][key]) || DNE(b['info'][key])) {
    return compareAgainstDNE(a, b)
  }
  // console.log(a['info'][key] + " < " + b['info'][key] + "?")
  if (a['info'][key] < b['info'][key]) {
    return -1
  }
  if (a['info'][key] > b['info'][key]) {
    return 1
  }
  return 0
}

function compareNames(a, b) {
  return compareDataByKey(a, b, 'name')
}

function compareIDs(a, b){
  return compareDataByKey(a, b, 'id')
}

// Sorts
function sortAlphabetically() {
  sortParadigm.value = SORT_ALPHA
}

function sortChronologically() {
  sortParadigm.value = SORT_CHRONO
}

function deselectEntry() {
  setSelectedEntry(DESELECTED)
}

function noSelectionMade() {
  return selected.value === DESELECTED
}

function showArtContainer() {
  return noSelectionMade() && viewMode.value === ART_VIEW
}

function showListContainer() {
  return noSelectionMade() && viewMode.value === LIST_VIEW
}

function toggleView() {
  if (MULTI_VIEW_ENABLED){
    if (viewMode.value === ART_VIEW){
      viewMode.value = LIST_VIEW
      sortAlphabetically()
    }
    else if (viewMode.value === LIST_VIEW) {
      viewMode.value = ART_VIEW
      sortChronologically()
    }
  }
  updateSelection(DESELECTED)
}

function isAValidId(id) {
  // console.log("validating id\t" + id + "\tagainst\t" + (entries.value.length - 1))
  return (id >= 0 && id <= (entries.value.length - 1))
}

function setSelectedEntry(id) {
  if (isAValidId(id) && id !== selected.value){
    selected.value = id
  }
  else{
    selected.value = DESELECTED
  }
  console.log(`NOW VIEWING ENTRY: ${id}`)
}

function getSelectedEntry() {
  if (noSelectionMade()) {
    return entries.value[0]
  }
  // console.log("checking " + 0 + " thru " + entries.length + "...")
  for (let i = 0; i < entries.value.length; i++){
    if (selected.value === entries.value[i].id){
      // console.log("found " + entries[i].info['name'])
      return entries.value[i]
    }
  }
  return entries.value[0]
}

// History management
function isAValidHistoricalIndex(value) {
  return (value >= 0 && value <= (history.value.length - 1))
}

function goBack() {
  setIndex(index.value - 1)
  setSelectedEntry(history.value[index.value])
}

function goForward() {
  setIndex(index.value + 1)
  setSelectedEntry(history.value[index.value])
}

function setIndex(value) {
  // var old = 0 + index.value
  // console.log(`history index, prev: ${old}`)
  if (!isAValidHistoricalIndex(value)){
    return
  }
  index.value = value
  // console.log(`history index, curr: ${index.value}`)
}

function pushHistory(curr) {
  history.value.push(curr)
  setIndex(index.value + 1)
  // console.log(`history: ${history.value}`)
}

function cleanHistory() {
  /* Removes instances of DESELECTED from the history so that
  when goBack() and goForward() are called, DESELECTED is only
  shown at the beginning and end of the history. As such,
  the for loop ignores indices 0 and (n-1)
  
  Calling this function in updateSelection() and HandleBioClose() 
  because those will probably be called much less often than 
  goBack() and goForward() */
  var oldLength = history.value.length
  var newHistory = [DESELECTED,]
  for (let i = 1;i < oldLength - 1;i++){
    var curr = history.value[i]
    if (curr !== DESELECTED){
      newHistory.push(curr)
    }
    else if (i !== 0 && curr === DESELECTED){
      setIndex(index.value - 1)
    }
  }
  newHistory.push(history.value[oldLength - 1])
  history.value = newHistory
}

function updateSelection(id) {
  if (id === selected.value){
    pushHistory(DESELECTED)
  }
  else{
    pushHistory(id)
  }
  setSelectedEntry(id)
  cleanHistory()
  console.log(`history.value: ${history.value}`)
}

function handleBioClose(){
  // pushHistory(DESELECTED)
  deselectEntry()
  cleanHistory()
  console.log(`history.value: ${history.value}`)
}

// Search
function updateSearch(query) {
  userRegex.value = cleanString(query)
}

function cleanString(s){
  return s.replace(SEARCH_BLEACH, "")
}

const sortParadigm = ref(SORT_CHRONO)
const sortParadigms = reactive({
  [SORT_ALPHA]: compareNames,
  [SORT_CHRONO]: compareIDs
})

function sort(list) {
  var paradigm = sortParadigms[sortParadigm.value]
  if (paradigm === null || paradigm === undefined){
    return list.slice()
  }
  return list.slice().sort((a, b) => paradigm(a, b))
}

function matchesRegex(s, regex){
  try {
    var result = regex.test(s)
    return result
  }
  catch (e){
    console.log("Expected error in matchesRegex")
    console.log(e)
  }
  return false

}

function filter(list){
  if (userRegex.value === "" || userRegex.value === null || userRegex === undefined){
    return list.slice()
  }
  var regex = new RegExp(userRegex.value.toLowerCase())
  console.log("regex\t" + regex)
  return list.filter(entry => matchesRegex(entry['info']['name'].toLowerCase(), regex))
}

const arranged = computed(() => {
  var sorted = sort(entries.value)
  var filtered = filter(sorted)
  console.log(filtered.slice())
  return filtered.slice()
})
</script>

<template>
  <header>
    <Navbar :searchQuery="userRegex" :version="packageJson.version"
      :history="history" :index="index" :source="source"
      :view="viewMode" :art_view="ART_VIEW" :list_view="LIST_VIEW" :multi_view_enabled="MULTI_VIEW_ENABLED"
      @go-back="goBack" @go-forward="goForward"
      @sort-alphabetically="sortAlphabetically" @sort-chronologically="sortChronologically"
      @toggle-view="toggleView"
      @update-search="updateSearch"
    />
  </header>
  
  <main>
    <ArtContainer v-show="showArtContainer()" :entries="arranged" @update-selection="updateSelection"/>
    <ListContainer v-show="showListContainer()" :entries="arranged" @update-selection="updateSelection"/>
    <div id="bio" v-show="!noSelectionMade()">
      <Bio
        :ID="selected.value"
        :info="getSelectedEntry().info"
        @deselect-entry="handleBioClose()"
        @select-entry="updateSelection(entry.id)">
      </Bio>
    </div>
  </main>
</template>

<style scoped>

body, main {
  overflow-y: hidden;
}

template {
  display: flex;
  flex-flow: column nowrap;
  justify-content: flex-start;
}

header {
  position: sticky;
  z-index: 2;
  top: 0vh;
  left: 0;
  overflow-y: hidden;
  width: 100%;
}

main {
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

#listContainer > ul > .Tag {
  background-color: white;
  color: black;
}

</style>