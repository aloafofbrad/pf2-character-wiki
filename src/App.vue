<script setup>
import MainView from './components/MainView.vue'
import Navbar from './components/Navbar.vue'
import { ref, reactive, computed } from 'vue'
import { provide } from 'vue'
import packageJson from "../package.json"

/* Constants
    source          URL to your repo. Safe to use the empty string or 
                    disable rendering. Rendered in NavBar.
    SEARCH_BLEACH   Used to strip userRegex of illegal characters
    DESELECTED      Numerical ID that shows components that the user 
                    hasn't selected a character, journal entry, or 
                    setting. Arbitrary, but should be negative.
    INFO_KEY        Key used to access info objects in entry data. Not  
                    recommended to change this

    The following are props in MainView:
    SORT_ALPHA    Arbitrary; represents sorting an array in alphabetical 
                  order (by an entry's name or title)
    SORT_CHRONO   Arbitrary; represents sorting an array in chronological 
                  order (by an entry's ID)

    ART_VIEW      Arbitrary; determines whether the ArtContainer is 
                  shown
    INDEX_VIEW    Arbitrary; determines whether the IndexContainer is 
                  shown
    LIST_VIEW     Arbitrary; determines whether the ListContainer is 
                  shown
    VIEWS         Array of all views, in arbitrary order. Does not affect
                  DEFAULT_VIEW. When changing the view, the default 
                  behavior is to increment viewMode.value, switching to 
                  the next view in VIEWS, and eventually cycling back to 
                  the first view.
*/
const source = `https://github.com/aloafofbrad/pf2-character-wiki`
const SEARCH_BLEACH = "/[^a-zA-Z0-9 -\?]/g"
const DESELECTED = -1
provide('DESELECTED', DESELECTED)
const INFO_KEY = 'info'

// props in MainView
const SORT_ALPHA = "alphabetical"
const SORT_CHRONO = "chronological"
const SORT_KEYS = [SORT_ALPHA, SORT_CHRONO]
const ART_VIEW = 0
const INDEX_VIEW = 1
const LIST_VIEW = 2
const VIEWS = [ART_VIEW, INDEX_VIEW, LIST_VIEW]

/* Reactive data variables
    dataMap     This the reactive map for the app. This is the single most
                important variable in the app. Any data that you want 
                users to be able to view should be added into dataMap.
                To add data to dataMap, first import it using an import
                statement.
                Next, add it to the map using addArrayToReactiveMap().
    selected    Stores the ID of the entry that the user is currently 
                viewed
    history     Stores a list of IDs that the user has previously viewed
    index       ???? Stores the current index of the history ????
    userRegex   Stores a user's search string
    
    sortKey     Current key used in sort() for compareDataByKey()
    sortKeys    All keys used for sorting
*/
const dataMap = reactive({}) // model in MainView
const selected = ref(DESELECTED) // model in MainView
const history = ref([DESELECTED,])
const index = ref(0)
const userRegex = ref('')
const sortKey = ref(SORT_CHRONO)
const sortKeys = reactive({
  [SORT_ALPHA]: "name",
  [SORT_CHRONO]: "id"
})
/* Note: I'm not 100% sure why SORT_ALPHA & SORT_CHRONO are in [brackets] 
in the declaration of sortKeys, but I think it's to allow the keys to be 
set up in a way that matches the string values of SORT_ALPHA & 
SORT_CHRONO */

// read the data from the files
import characters from './data/characters.json'
import journal from './data/journals.json'
import settings from './data/settings.json'

/* Adds data to dataMap. Overwrites dataMap.value[keyName] if it exists.
    args:
    data     the data to be added to the reactive map
    keyName  the name to use for the key
  The order these are added matters & determines the first view users see when opening the page. See viewData for more details.
*/
function addArrayToReactiveMap(data, keyName){
  var temp = { [keyName]: data }
  Object.assign(dataMap, temp)
}
addArrayToReactiveMap(journal.data, "journal")
addArrayToReactiveMap(characters.data, "characters")
addArrayToReactiveMap(settings.data, "settings")

/* Computed & reactive properties re: categories
  A "category" in this context represents the type of information to be 
  arranged and presented to the user. Initially this was just the 
  characters, but the scope of the project has been expanded to include 
  other information, such as journal entries, and descriptions of 
  settings.

  CATEGORIES        Function. In short, every key for key in dataMap. 
                    Used for error prevention (validating categories).
  DEFAULT_CATEGORY  Constant. The first key in dataMap. The first 
                    category shown when the app loads.
  category          Ref. The currently viewed category. This is used to 
                    set the selected entry from that category.
  Since CATEGORIES and DEFAULT_CATEGORY are functions, they're both set 
  up automatically for you. You shouldn't need to change anything in the 
  three declarations below. The default category is always the first 
  category of data are added to dataMap using addArrayToReactiveMap above.
*/

function CATEGORIES() { return Object.keys(dataMap) }
const categories = CATEGORIES()
const DEFAULT_CATEGORY = categories[0]
const category = ref(DEFAULT_CATEGORY) // prop in MainView
provide('CATEGORIES', categories)
provide('DEFAULT_CATEGORY', DEFAULT_CATEGORY)
console.log(`categories: `, categories)
console.log(`default category: `, DEFAULT_CATEGORY)
console.log(`category: `, category)

/* viewData     Constant. Must be configured manually. Maps each category 
                to a displayKey and an array of validViews.
  displayKey    Map each category to the key you want displayed in 
                whatever container(s) you're using. Each key:value pair 
                here should look like one of the following:
                [categories[0]]:"name", [categories[1]]:"title", etc
                The value should be a key in the entry's info object.
  validViews    Constant. Must be configured manually. Views that can be 
                shown for each category. Each value should be an array, 
                even if there's only one view for that category. If all 
                views are valid for a given category, you can use the 
                constant VIEWS here instead.

  DEFAULT_VIEW    Automatic. Determines the default view. Initial value 
                  is the default category's default view.
  viewMode        Automatic, reactive. Stores the currently displayed 
                  view. Initial value is DEFAULT_VIEW.
*/
const viewData = {
  [categories[0]]:{ // JOURNALS
    displayKey: "title",
    validViews: [LIST_VIEW, INDEX_VIEW]
  },
  [categories[1]]:{ // CHARACTERS
    displayKey: "name",
    validViews: VIEWS
  },
  [categories[2]]:{ // settings
    displayKey: "name",
    validViews: [LIST_VIEW, INDEX_VIEW]
  },
}
var keys = Object.keys(viewData)
for (let i = 0; i < keys.length; i++){
  viewData[keys[i]].defaultView = viewData[keys[i]].validViews[0]
}
provide('viewData', viewData)
const DEFAULT_VIEW = viewData[DEFAULT_CATEGORY].defaultView
const viewMode = ref(DEFAULT_VIEW)

/* displayKey (computed)    Used by containers to determine which entry 
                            info to display. ArtContainer will always use 
                            the entry's image key to display images 
                            regardless of the displayKey.
  currentViews (computed)   Returns the array of validViews for the 
                            current category. */
const displayKey = computed(() => {
  var result = viewData[category.value].displayKey
  console.log("displayKey: ", result)
  return result
})

const currentViews = computed(() => {
  var result = viewData[category.value].validViews
  console.log("currentViews: ", result)
  return result
})

const currentDefaultView = computed(() => {
  var result = viewData[category.value].defaultView
  console.log("defaultView: ", result)
  return result
})

function defaultViews(cat) { return viewData[cat].defaultView }
function getSortKey(cat){ return viewData[cat].displayKey }
provide('getSortKey', getSortKey)

function consoleLogReactiveMap(obj){
  console.log("logging reactive map:")
  console.log(obj)
  console.log("done")
}
consoleLogReactiveMap(dataMap)

function DNE(arg) { return arg === undefined || arg === null }
function exists(arg) { return arg !== undefined && arg !== null }
provide('exists', exists)

/* Helper function for sorts
    Handles edge cases where a exists and b doesn't, vice versa, or neither exists */
function compareAgainstDNE(a, b) {
  if (!DNE(a) && DNE(b)) { return -1 }
  if (DNE(a) && !DNE(b)) { return 1 }
  return 0
}

/* Helper function for sorts */
function compareDataByKey(a, b, key) {
  if (DNE(a[INFO_KEY][key]) || DNE(b[INFO_KEY][key])) {
    return compareAgainstDNE(a[INFO_KEY][key], b[INFO_KEY][key])
  }
  var aValue = a[INFO_KEY][key]
  var bValue = b[INFO_KEY][key]
  if (aValue < bValue) { return -1 }
  if (aValue > bValue) { return 1 }
  return 0
}

// Sorts
function sortKeyIsValid(key){ return SORT_KEYS.includes(key) }
function setSortKey(key){if (sortKeyIsValid(key)){ sortKey.value = key }}

// Selection helpers
function noSelectionMade() {
  return selected.value === DESELECTED
}

// container display helper
function goToView(num) {
  viewMode.value = num
  if (currentViews.value.includes(num)){
    if (viewMode.value === INDEX_VIEW){ setSortKey(SORT_ALPHA) }
    else { setSortKey(SORT_CHRONO) }
  }
}

function goToDefaultView(cat) {
  var view = defaultViews(cat)
  goToView(view)
}

function isAValidId(id) {
  if (DNE(id)) { return false }
  if (id === DESELECTED) { return true }
  return (id >= 0 && id <= (dataMap[category.value].length - 1))
}

function isAValidKey(key){ return CATEGORIES().includes(key) }

function setSelectedEntry(id) {
  selected.value = DESELECTED
  if (isAValidId(id)){
    selected.value = id
    return true
  }
  return false
}

function setSelectedCategory(newCategory){
  if (isAValidKey(newCategory)) {
    category.value = newCategory
    return true
  }
  return false
}

// History management
function isAValidHistoricalIndex(value) {
  return (value >= 0 && value <= (history.value.length - 1))
}

/* Update the history without pushing to it. Not meant to be called 
directly; call goBack()/goForward() instead. Even though
updateSelection() has a push argument that can be set to false to disable 
pushing to the history, this is the preferred way to change the history 
since goSomewhere() is the preferred way to change the history without 
pushing to it, since updateSelection() requires the user to know what ID 
and category to go to. goSomewhere() figures that out for the user. */
function goSomewhere(where) {
  setIndex(where)
  const curr = history.value[index.value]
  setSelectedEntry(curr.id)
  setSelectedCategory(curr.category)
}
function goBack() { goSomewhere(index.value - 1) }
function goForward() { goSomewhere(index.value + 1) }
function goBackToStart() { goSomewhere(0) }
function goForwardToEnd() { goSomewhere(history.value.length - 1) }

function setIndex(value) {
  if (!isAValidHistoricalIndex(value)){ return }
  index.value = value
}

function pushHistory(id, category) {
  history.value.push({ id:id, category:category })
  if (history.value.length === 101){
    history.value = history.value.slice(-99)
  }
  else{ setIndex(index.value + 1) }
}

/* Called when *Container components emit update-selection
  id        ID of the entry to switch to
  cat       ID of the category to switch to. Note that this might not be
            different from the current category.
  caller    The component that originally called this
  push      If true, pushes id and cat to history.value
  debug     If true, runs console.logs
 */
function updateSelection(id, cat, caller="App", push=true, debug=true) {
  if (debug){
    console.log('updateSelection(', id, ', \'', cat, '\', \'', caller, '\', ', push, ', ', debug, ')') 
  }
  const old = { "id":selected.value, "category":category.value }
  var updatedEntry = setSelectedEntry(id)
  var updatedCategory = setSelectedCategory(cat)
  if (!updatedEntry && !updatedCategory){
    push = false
    if (debug){
      console.log("updatedEntry: ", updatedEntry, "\tupdatedCategory: ", updatedCategory)
    }
  }
  if (cat !== category.value){
    goToView(currentDefaultView)
  }
  if (push) {
    pushHistory(id, cat)
  }
  else {
    selected.value = old.id
    category.value = old.category
  }
  if (debug){
    const curr = history.value[index.value]
    if (exists(curr)){
      const currID = curr.id
      const currCategory = curr.category
      var debugMessage = "still at:"
      if (push){ debugMessage = "now viewing:" }
      console.log(`${debugMessage} {${currID}, ${currCategory}}`)
    }
  }
}

// Search
function updateSearch(query) { userRegex.value = cleanString(query) }
function cleanString(s){ return s.replace(SEARCH_BLEACH, "") }

function sort(list) {
  var key = sortKeys[sortKey.value]
  if (!exists(key)){ return list.slice() }
  return list.slice().sort((a, b) => compareDataByKey(a, b, key))
}

function matchesRegex(s, regex){
  var result = false
  try { result = regex.test(s) }
  catch (e){
    console.log("Error in matchesRegex")
    console.log(e)
  }
  return result
}
provide('matchesRegex', matchesRegex)

// Filters / searches for specific entries
function filter(list, cat) {
  if (userRegex.value==="" || DNE(userRegex.value)){return list.slice()}
  var sortKey = getSortKey(cat)
  var regex = new RegExp(userRegex.value.toLowerCase())
  console.log(`regex\t\t${regex}`)
  console.log(`sortKey\t${sortKey}`)
  return list.filter(entry => matchesRegex(entry[INFO_KEY][sortKey].toLowerCase(), regex))
}

function sortAndFilter(category) {
  var filtered = filter(dataMap[category], category)
  var sorted = sort(filtered)
  console.log(sorted.slice())
  return sorted.slice()
}

const arranged = computed(() => {
  const categories = CATEGORIES()
  var result = {}
  for (let i = 0; i < categories.length; i++){
    result[categories[i]] = sortAndFilter(categories[i])
  }
  return result
})

const maxID = computed(() => {
  var result = dataMap[category.value].length
  console.log("maxID: ", result)
  return result
})

</script>

<template>
  <header>
    <Navbar :version="packageJson.version" :source="source"
      v-model:category="category"
      :searchQuery="userRegex"
      :history="history" :index="index"
      :view="viewMode" :validViews="currentViews"
      :art_view="ART_VIEW" :index_view="INDEX_VIEW" :list_view="LIST_VIEW"
      @go-back="goBack" @go-forward="goForward"
      @sort-alphabetically="setSortKey(SORT_ALPHA)" 
      @sort-chronologically="setSortKey(SORT_CHRONO)"
      @goToView="goToView" @goToDefaultView="goToDefaultView"
      @update-search="updateSearch" @update-selection="updateSelection"
    />
  </header>
  
  <!-- For each type of container used in MainView, there must be a 
   binding for it, which must take its constant value. For each category 
   of data you want to show, there must be a binding for it, which must 
   take its index from CATEGORIES(), or a hard-coded value. What order 
   the view and category bindings are declared in should not matter.
   See also the props in MainView.vue. -->
  <main>
    <MainView v-model:dataMap="arranged" v-model:selected="selected"
      v-model:category="category" :maxID="maxID"
      :view-mode="viewMode" :default_view="DEFAULT_VIEW" :displayKey="displayKey"
      :art_view="ART_VIEW" :index_view="INDEX_VIEW" :list_view="LIST_VIEW"
      @update-selection="updateSelection"
      :characterKey="categories[1]"
      :journalKey="categories[0]"
      :settingKey="categories[2]"
    />
  </main>
</template>

<style scoped>

header {
  position: sticky;
  z-index: 2;
  top: 0;
  left: 0;
  margin-bottom: 0;
  padding-bottom: 0;
  overflow-y: hidden;
  width: 100%;
}

main {
  position: sticky;
  min-height: 100vh;
  top: 0;
  left: 0;
  z-index: 0;
  margin: 0;
  padding: 0;
  display: flex;
  flex-flow: column nowrap;
  justify-content: flex-start;
  align-items: center;
}

</style>