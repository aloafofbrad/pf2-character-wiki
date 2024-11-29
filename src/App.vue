<script setup>
import MainView from './components/MainView.vue'
import Navbar from './components/Navbar.vue'
import { ref, reactive, computed, watchEffect } from 'vue'
import { provide } from 'vue'
import packageJson from "../package.json"

/* Constants
    source          URL to your repo. Safe to use the empty string or disable rendering. Rendered in NavBar.
    SEARCH_BLEACH   Used to strip userRegex of illegal characters
    DESELECTED      numerical ID that shows components that the user hasn't selected a character, journal
                    entry, or setting. arbitrary, but should be negative.

    props in MainView
    SORT_ALPHA      Arbitrary; represents sorting an array in alphabetical order
    SORT_CHRONO     Arbitrary; represents sorting an array in chronological order (by an entry's ID)

    ART_VIEW            Arbitrary; used to determine whether the ArtContainer is shown
    INDEX_VIEW          Arbitrary; used to determine whether the IndexContainer is shown
    LIST_VIEW           Arbitrary; used to determine whether the ListContainer is shown
    DEFAULT_VIEW        Determines the default view. Should either be ART_VIEW or LIST_VIEW
    MULTI_VIEW_ENABLED  When false, only allows one view (ArtContainer, ListContainer, etc) to render
*/
const source = `https://github.com/aloafofbrad/pf2-character-wiki`
const SEARCH_BLEACH = "/[^a-zA-Z0-9 -\?]/g"
const DESELECTED = -1
provide('DESELECTED', DESELECTED)

// props in MainView
const SORT_ALPHA = "alphabetical"
const SORT_CHRONO = "chronological"
const ART_VIEW = 0
const INDEX_VIEW = 1
const LIST_VIEW = 2
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
const dataMap = reactive({}) // model in MainView
const selected = ref(DESELECTED) // model in MainView
const history = ref([DESELECTED,])
const index = ref(0)
const userRegex = ref('')
const viewMode = ref(DEFAULT_VIEW) // prop in MainView
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
  var temp = {
    [keyName]: data
  }
  Object.assign(dataMap, temp)
}
addArrayToReactiveMap(characters.data, dataMap, "characters")
addArrayToReactiveMap(journal.data, dataMap, "journal")
addArrayToReactiveMap(settings.data, dataMap, "settings")

/* Computed & reactive properties re: categories
    A "category" in this context represents the type of information to be
    arranged and presented to the user. Initially this was just the
    characters, but the scope of the project has been expanded to include
    other information, such as journal entries, and descriptions of
    settings.

  CATEGORIES        Computed. In short, every key for key in dataMap.
                    Used for error prevention (validating categories).
  DEFAULT_CATEGORY  Computed. The first key in dataMap. The first
                    category shown when the app loads.
  category          Ref. The currently viewed category. This is used to
                    set the selected entry from that category.
  Since these are all either computed or based on computed values,
  they're all set up automatically for you. You shouldn't need to change
  anything in the three declarations below.
*/

function CATEGORIES() {
  var result;
  watchEffect(() => { result = Object.keys(dataMap); })
  return result;
}
function DEFAULT_CATEGORY() {
  return CATEGORIES()[0];
}
const category = ref(DEFAULT_CATEGORY()) // prop in MainView
provide('CATEGORIES', CATEGORIES())
provide('DEFAULT_CATEGORY', DEFAULT_CATEGORY())
console.log(`categories: `, CATEGORIES())
console.log(`default category: `, DEFAULT_CATEGORY())
console.log(`category: `, category)

/* Prints a given reactive map in the console
   args:
   obj   the object to print
*/
function consoleLogReactiveMap(obj){
  console.log("logging reactive map:")
  console.log(obj)
  console.log("done")
}
consoleLogReactiveMap(dataMap)

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
function noSelectionMade() {
  return selected.value === DESELECTED
}

// container display helper -- move to MainView?
function toggleView() {
  if (MULTI_VIEW_ENABLED){
    if (viewMode.value === ART_VIEW){
      viewMode.value = LIST_VIEW
      sortAlphabetically()
    }
    else if (viewMode.value === INDEX_VIEW) {
      viewMode.value = ART_VIEW
      sortChronologically()
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
  return (id >= 0 && id <= (dataMap[category.value].length - 1))
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
  if (isAValidId(id) && id !== selected.value){ selected.value = id }
  else{ selected.value = DESELECTED }
}

function setSelectedCategory(category){
  if (isAValidKey(category)) { category.value = category }
}

function getSelectedCategory(){ return category.value }

// History management
function isAValidHistoricalIndex(value) {
  return (value >= 0 && value <= (history.value.length - 1))
}

function goSomewhere(where) {
  setIndex(where)
  const curr = history.value[index.value]
  setSelectedEntry(curr.id)
  setSelectedCategory(curr.category)
}
function goBack() { goSomewhere(index.value - 1) }
function goForward() { goSomewhere(index.value + 1) }

function setIndex(value) {
  if (!isAValidHistoricalIndex(value)){ return }
  index.value = value
}

function pushHistory(id, category) {
  history.value.push({ id:id, category:category })
  setIndex(index.value + 1)
}

/* Called when *Container components emit update-selection */
function updateSelection(id, category) {
  pushHistory(id, category)
  setSelectedEntry(id)
  setSelectedCategory(category)
  // console.log(`history.value: ${history.value}`)
}

// Search -- move to NavBar?
function updateSearch(query) { userRegex.value = cleanString(query) }

// Helper for search -- move to NavBar?
function cleanString(s){ return s.replace(SEARCH_BLEACH, "") }

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

// Filters / searches for specific entries
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
      :view="viewMode" :art_view="ART_VIEW" :list_view="LIST_VIEW"
      :multi_view_enabled="MULTI_VIEW_ENABLED"
      @go-back="goBack" @go-forward="goForward"
      @sort-alphabetically="sortAlphabetically" @sort-chronologically="sortChronologically"
      @toggle-view="toggleView"
      @update-search="updateSearch"
    />
  </header>
  
  <!-- correct usage should be v-model:dataMap="dataMap" -->
  <!-- For each type of view you're using, there must be a binding for
   it, which must take its constant value. If MULTI_VIEW_ENABLED is
   false, there still must be a binding for the one type of view that
   will be used.
  
   For each category of data you want to show, there must be a binding
   for it, which must take its index from CATEGORIES(), or a hard-coded
   value. 
   
   What order the view and category bindings are declared in should not
   matter.
   
   See also the props in MainView.vue. -->
  <MainView v-model:dataMap="dataMap"
    v-model:selected="selected"
    v-model:category="category"
    :view-mode="viewMode"
    :art_view="ART_VIEW"
    :index_view="INDEX_VIEW"
    :list_view="LIST_VIEW"
    :default_view="DEFAULT_VIEW"
    :multi_view_enabled="MULTI_VIEW_ENABLED"
    @update-selection="updateSelection"
    :characterData="CATEGORIES()[0]"
    :journalData="CATEGORIES()[1]"
    :settingData="CATEGORIES()[2]"
  />

  <!-- <DataView :dataMap="dataMap" v-model:selected="selected"
    v-model:category="category" :valid-categories="CATEGORIES()"
    :deselected="DESELECTED">
  </DataView> -->
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