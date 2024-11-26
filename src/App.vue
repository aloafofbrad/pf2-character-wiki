<script setup>
import MainView from './components/MainView.vue'
import Navbar from './components/Navbar.vue'
import { ref, reactive, computed } from 'vue'
import packageJson from "../package.json"

/* Constants
    source          URL to your repo. Safe to use the empty string or disable rendering. Rendered in NavBar.
    DESELECTED      numerical ID that shows components that the user hasn't selected a character, journal
                    entry, or setting. arbitrary, but should be negative.
    SORT_ALPHA      Arbitrary; represents sorting an array in alphabetical order
    SORT_CHRONO     Arbitrary; represents sorting an array in chronological order (by an entry's ID)
    SEARCH_BLEACH   Used to strip userRegex of illegal characters

    ART_VIEW            Arbitrary; used to determine whether the ArtContainer is shown
    LIST_VIEW           Arbitrary; used to determine whether the ListContainer is shown
    DEFAULT_VIEW        Determines the default view. Should either be ART_VIEW or LIST_VIEW
    MULTI_VIEW_ENABLED  When false, only allows one view (ArtContainer, ListContainer, etc) to render
*/
const source = `https://github.com/aloafofbrad/pf2-character-wiki`
const DESELECTED = -1
const SORT_ALPHA = "alphabetical"
const SORT_CHRONO = "chronological"
const SEARCH_BLEACH = "/[^a-zA-Z0-9 -\?]/g"

const ART_VIEW = 0
const LIST_VIEW = 1
const DEFAULT_VIEW = ART_VIEW
const MULTI_VIEW_ENABLED = true

/* Reactive data variables
    dataMap     This the reactive map for the app. This is the single
                most important variable in the app. Any data that you
                want users to be able to view should be added into
                dataMap.
                To add data to dataMap, first import it using an import
                statement.
                Next, add it to the map using addArrayToReactiveMap().
    selected    Stores the ID of the entry that the user is currently
                viewed
    history     Stores a list of IDs that the user has previously viewed
    index       ???? Stores the current index of the history ????
    userRegex   Stores a user's search string
    viewMode    Stores the currently displayed view
    
    sortParadigm    Current sort paradigm. Update this to change the
                    default sort paradigm.
    sortParadigms   Mapping of comparison functions used for SORT_ALPHA
                    & SORT_CHRONO, in sort()
*/
const dataMap = ref({})
const selected = ref(DESELECTED)
const history = ref([DESELECTED,])
const index = ref(0)
const userRegex = ref('')
const viewMode = ref(DEFAULT_VIEW)
const sortParadigm = ref(SORT_CHRONO)
const sortParadigms = reactive({
  [SORT_ALPHA]: compareNames,
  [SORT_CHRONO]: compareIDs
})
/* Note: I'm not 100% sure why SORT_ALPHA & SORT_CHRONO are in
[brackets] in the declaration of sortParadigms, but I think it's
to allow the keys to be set up in a way that matches the string
values of SORT_ALPHA & SORT_CHRONO */


// read the data from the files
import characters from './data/characters.json'
import journal from './data/journals.json'
import settings from './data/settings.json'

/* Adds data to a given reactive map
    args:
    data     the data to be added to the reactive map
    map      the reactive map
    keyName  the name to use for the key
  Overwrites map.value[keyName] if it already exists.
*/
function addArrayToReactiveMap(data, map, keyName){
  map.value[keyName] = []
  for (let i = 0; i < data.length; i++){
    map.value[keyName].push(data[i])
  }
}
addArrayToReactiveMap(characters.data, dataMap, "characters")
addArrayToReactiveMap(journal.data, dataMap, "journal")
addArrayToReactiveMap(settings.data, dataMap, "settings")

/* Prints a given reactive map in the console
   args:
   obj   the object to print
*/
function consoleLogReactiveMap(obj){
  for (const key in obj){
    console.log(`${key}:`)
    console.log(obj[key].value)
  }
}
consoleLogReactiveMap()

/* Helper function for sorts
    Returns true if arg is null or undefined
*/
function DNE(arg) {
  return arg === null || arg === undefined
}

/* Helper function for sorts
    Handles edge cases where a exists and b doesn't,
    vice versa, or neither exists
    
    returns -1 if a exists and b does not
    returns 1 if b exists and a does not
    returns 0 if a and b DNE, or if a and b exist
*/
function compareAgainstDNE(a, b) {
  if (!DNE(a) && DNE(b)) {
    return -1
  }
  if (DNE(a) && !DNE(b)) {
    return 1
  }
  return 0
}

/* Helper function for sorts
    returns -1 if a is less than b
    returns 1 if a is greater than b
    returns 0 if a and b are equal
*/
function compareDataByKey(a, b, key) {
  if (DNE(a['info'][key]) || DNE(b['info'][key])) {
    return compareAgainstDNE(a, b)
  }
  var aValue = a['info'][key]
  var bValue = b['info'][key]
  if (aValue < bValue) {
    return -1
  }
  if (aValue > bValue) {
    return 1
  }
  return 0
}

/* Helper function for sorts
*/
function compareNames(a, b) {
  return compareDataByKey(a, b, 'name')
}

/* Helper function for sorts
*/
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

// Selection helpers
function deselectEntry() {
  setSelectedEntry(DESELECTED)
}

function noSelectionMade() {
  return selected.value === DESELECTED
}

// container display helper -- move to MainView?
function showArtContainer() {
  return noSelectionMade() && viewMode.value === ART_VIEW
}

// container display helper -- move to MainView?
function showListContainer() {
  return noSelectionMade() && viewMode.value === LIST_VIEW
}

// container display helper -- move to MainView?
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

// Helper for data; rewritten as isAValidId(key, id)
function isAValidId(id) {
  return (id >= 0 && id <= (entries.value.length - 1))
}
/* Helper for dataMap
    Tests if an ID is valid based on the given key for dataMap
    args:
    key   the key to test
    id    the id to test
*/
function isAValidId(key, id){
  try {
    var target = dataMap.value[key]
    if (target !== null && target !== undefined){
      return (id >= 0 && id <= (dataMap.value[key].length - 1))
    }
  }
  catch {
    return false
  }
}
/* Helper for dataMap
    Tests if a key exists in dataMap
    args:
    key   the key to test
*/
function isAValidKey(key){
  for (k in dataMap.value){
    if (key === k){
      return true
    }
  }
  return false
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
  for (let i = 0; i < entries.value.length; i++){
    if (selected.value === entries.value[i].id){
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
  if (!isAValidHistoricalIndex(value)){
    return
  }
  index.value = value
}

function pushHistory(curr) {
  history.value.push(curr)
  setIndex(index.value + 1)
}

/* Removes instances of DESELECTED from the history so that
    when goBack() and goForward() are called, DESELECTED is only
    shown at the beginning and end of the history. As such,
    the for loop ignores indices 0 and (n-1)
  
    Calling this function in updateSelection() and HandleBioClose() 
    because those will probably be called much less often than 
    goBack() and goForward()
*/
function cleanHistory() {
  var oldLength = history.value.length
  var newHistory = [DESELECTED,]
  for (let i = 1;i < oldLength;i++){
    var curr = history.value[i]
    if (curr !== DESELECTED){
      newHistory.push(curr)
    }
    // Fairly sure this is a bug; commented out for now
    // else if (i !== 0 && curr === DESELECTED){
    //   setIndex(index.value - 1)
    // }
  }
  // newHistory.push(history.value[oldLength - 1])
  history.value = newHistory
}

/* Called when *Container components emit update-selection */
function updateSelection(id) {
  /* Not actually sure why this is here; is it an edge case I forgot?
  I think this case should be removed entirely to be consistent with
  the bug fix in the else if clause in cleanHistory()
  
  TODO: test that this edge case ever actually happens*/
  if (id === selected.value){
    pushHistory(DESELECTED)
    console.log("That edge case ever actually happened")
  }
  // This *should* be the default case that gets called 99% of the time
  else{
    pushHistory(id)
  }
  setSelectedEntry(id)
  cleanHistory()
  console.log(`history.value: ${history.value}`)
}

/* Called when Bio component emits deselect-entry */
function handleBioClose(){
  deselectEntry()
  cleanHistory()
  console.log(`history.value: ${history.value}`)
}

// Search -- move to NavBar?
function updateSearch(query) {
  userRegex.value = cleanString(query)
}

// Helper for search -- move to NavBar?
function cleanString(s){
  return s.replace(SEARCH_BLEACH, "")
}

// Sort -- move this & helpers to MainView?
function sort(list) {
  var paradigm = sortParadigms[sortParadigm.value]
  if (paradigm === null || paradigm === undefined){
    return list.slice()
  }
  return list.slice().sort((a, b) => paradigm(a, b))
}

// Helper for search -- move to NavBar?
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

// Move to MainView?
function filter(list){
  if (userRegex.value === "" || userRegex.value === null || userRegex === undefined){
    return list.slice()
  }
  var regex = new RegExp(userRegex.value.toLowerCase())
  console.log("regex\t" + regex)
  return list.filter(entry => matchesRegex(entry['info']['name'].toLowerCase(), regex))
}

// Could likely move this to MainView?
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
  
  <MainView></MainView>
</template>

<style scoped>

body, main {
  overflow-y: hidden;
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