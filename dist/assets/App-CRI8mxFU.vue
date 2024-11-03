<script setup>
import Bio from './components/Bio.vue'
import Tile from './components/Tile.vue'
import Navbar from './components/Navbar.vue'
import { ref, reactive, computed } from 'vue'
import packageJson from "../package.json"

import data from './data/characters.json'

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
const history = ref([-1,])
const index = ref(0)
const userRegex = ref('')
const SEARCH_BLEACH = "/[^a-zA-Z0-9 -\?]/g"

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
  var old = 0 + index.value
  if (!isAValidHistoricalIndex(value)){
    return
  }
  index.value = value
  // console.log(`history index, prev: ${old}`)
  // console.log(`history index, curr: ${index.value}`)
}

function pushHistory(curr) {
  history.value.push(curr)
  setIndex(index.value + 1)
  // console.log(`history: ${history.value}`)
}

function handleTileClick(id) {
  if (id === selected.value){
    pushHistory(DESELECTED)
  }
  else{
    pushHistory(id)
  }
  setSelectedEntry(id)
  console.log(history.value)
}

function handleBioClose(){
  // pushHistory(DESELECTED)
  deselectEntry()
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
    <Navbar :searchQuery="userRegex" :history="history" :index="index" :version="packageJson.version"
      @go-back="goBack" @go-forward="goForward" @sort-alphabetically="sortAlphabetically"
      @sort-chronologically="sortChronologically" @update-search="updateSearch"
    />
  </header>
  
  <main>
    <div id="ArtContainer" v-show="noSelectionMade()">
      <Tile
        v-show="isAValidId(entry.id)"
        v-for="entry in arranged"
        :key="entry.id"
        :info="entry.info"
        @click="handleTileClick(entry.id)">
      </Tile>
    </div>
    <div id="bio" v-show="!noSelectionMade()">
      <Bio
        :ID="selected.value"
        :info="getSelectedEntry().info"
        @deselect-entry="handleBioClose()"
        @select-entry="handleTileClick(entry.id)">
      </Bio>
    </div>
  </main>
</template>

<style scoped>
header {
  line-height: 1.5;
}

main {
  margin: 0;
  padding: 0;
  display: contents;
}

#ArtContainer {
  max-width: 100vw;
  max-height: calc(100vh - 24px);
  top: 24px;
  display: flex;
  flex-flow: row wrap;
  align-items: flex-start;
  justify-content: flex-start;
  align-content: flex-start;
  scroll-behavior: auto;
}

#ArtContainer > .Tile {
  margin: 2px;
}

</style>