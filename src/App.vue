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
    DESELECTED      numerical ID that shows components that the user 
                    hasn't selected a character, journal
                    entry, or setting. arbitrary, but should be negative.

    The following are props in MainView:
    SORT_ALPHA      Arbitrary; represents sorting an array in 
                    alphabetical order (by an entry's name or title)
    SORT_CHRONO     Arbitrary; represents sorting an array in
                    chronological order (by an entry's ID)

    ART_VIEW        Arbitrary; determines whether the
                    ArtContainer is shown
    INDEX_VIEW      Arbitrary; determines whether the 
                    IndexContainer is shown
    LIST_VIEW       Arbitrary; determines whether the 
                    ListContainer is shown
    VIEWS           Array of all views, in arbitrary order. Does not 
                    affect DEFAULT_VIEW. When changing the view, the
                    default behavior is to increment viewMode.value,
                    switching to the next view in VIEWS, and eventually
                    cycling back to the first view.

    MULTI_VIEW_ENABLED    When true, enables switching between 
                          containers (ArtContainer, IndexContainer,
                          ListContainer, etc). Does not mean more than
                          one will be shown at a time.
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
const VIEWS = [ART_VIEW, INDEX_VIEW, LIST_VIEW]
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

/* Adds data to dataMap
    args:
    data     the data to be added to the reactive map
    keyName  the name to use for the key
  Overwrites dataMap.value[keyName] if it already exists.
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
  category of data are added to dataMap using addArrayToReactiveMap
  above.
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
                [categories[0]]:"name"
                [categories[1]]:"title"
                etc
                The value should be a key in the entry's info object.
  validViews    Constant. Must be configured manually. Views that can 
                be shown for each category. Each value should be an 
                array, even if there's only one view for that category.
                If all views are valid for a given category, you can
                use the constant VIEWS here instead.

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
    validViews: [INDEX_VIEW, LIST_VIEW]
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
                            info to display. ArtContainer will always 
                            use the entry's image key to display images 
                            regardless of the displayKey.
  currentViews (computed)   Returns the array of validViews for 
                            the current category. */
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
function DNE(arg) { return arg === undefined || arg === null }
function exists(arg) { return arg !== undefined && arg !== null }
provide('exists', exists)

/* Helper function for sorts
    Handles edge cases where a exists and b doesn't,
    vice versa, or neither exists
    
    returns -1 if a exists and b does not
    returns 1 if b exists and a does not
    returns 0 if a and b DNE, or if a and b exist
*/
function compareAgainstDNE(a, b) {
  if (!DNE(a) && DNE(b)) { return -1 }
  if (DNE(a) && !DNE(b)) { return 1 }
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
  if (aValue < bValue) { return -1 }
  if (aValue > bValue) { return 1 }
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
function goToView(num) {
  viewMode.value = num
  // if (viewMode.value >= currentViews.length){ viewMode.value = 0 }
  var found = false
  for (let i = 0; i < currentViews.length && !found; i++){
    if (num === currentViews[i]) { found = true }
  }
  if (found){
    if (viewMode.value === ART_VIEW){ sortChronologically() }
    else { sortAlphabetically() }
    // updateSelection(DESELECTED, category.value, false)
  }
}

function goToDefaultView(cat) {
  // var default = currentDefaultView
  var view = defaultViews(cat)
  goToView(view)
}

// Helper for data; rewritten as isAValidId(key, id)
function isAValidId(id) {
  if (DNE(id)) { return false }
  return (id >= 0 && id <= (dataMap[category.value].length - 1))
}

/* Helper for dataMap
    Tests if a key exists in dataMap
    args:
    key   the key to test
*/
function isAValidKey(key){
  const categories = CATEGORIES()
  for (let i = 0; i < categories.length; i++){
    if (key === categories[i]){ return true }
  }
  return false
}

function setSelectedEntry(id) {
  selected.value = DESELECTED
  if (isAValidId(id) && id !== selected.value){ selected.value = id }
  else{ selected.value = DESELECTED }
  return true
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
  debug     .
 */
function updateSelection(id, cat, caller="App", push=true, debug=true) {
  if (debug){
    console.log('updateSelection(', id, ', \'', cat, '\', \'', caller, '\', ', push, ', ', debug, ')') 
  }
  const old = { "id":selected.value, "category":category.value }
  var updatedEntry = setSelectedEntry(id)
  var updatedCategory = setSelectedCategory(cat)
  if (!(updatedEntry && updatedCategory)){
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
    if (!DNE(curr)){
      const currID = curr.id
      const currCategory = curr.category
      var debugMessage = "still at:"
      if (push){ debugMessage = "now viewing:" }
      console.log(`${debugMessage} {${currID}, ${currCategory}}`)
    }
  }
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

function matchesRegex(s, regex){
  var result = false
  try { result = regex.test(s) }
  catch (e){
    console.log("Expected error in matchesRegex")
    console.log(e)
  }
  return result
}

// Filters / searches for specific entries
function filter(list, cat) {
  if (userRegex.value==="" || DNE(userRegex.value)){return list.slice()}
  var sortKey = getSortKey(cat)
  var regex = new RegExp(userRegex.value.toLowerCase())
  console.log(`regex\t\t${regex}`)
  console.log(`sortKey\t${sortKey}`)
  return list.filter(entry => matchesRegex(entry['info'][sortKey].toLowerCase(), regex))
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
    <Navbar :version="packageJson.version"
      v-model:category="category"
      :searchQuery="userRegex"
      :history="history" :index="index"
      :source="source"
      :view="viewMode"
      :art_view="ART_VIEW"
      :index_view="INDEX_VIEW"
      :list_view="LIST_VIEW"
      :validViews="currentViews"
      @go-back="goBack" @go-forward="goForward"
      @sort-alphabetically="sortAlphabetically" 
      @sort-chronologically="sortChronologically"
      @goToView="goToView"
      @goToDefaultView="goToDefaultView"
      @update-search="updateSearch"
      @update-selection="updateSelection"
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
  <main>
    <MainView v-model:dataMap="arranged"
      v-model:selected="selected"
      v-model:category="category"
      :maxID="maxID"
      :view-mode="viewMode"
      :art_view="ART_VIEW"
      :index_view="INDEX_VIEW"
      :list_view="LIST_VIEW"
      :default_view="DEFAULT_VIEW"
      :multi_view_enabled="MULTI_VIEW_ENABLED"
      :displayKey="displayKey"
      @update-selection="updateSelection"
      :characterData="categories[1]"
      :journalData="categories[0]"
      :settingData="categories[2]"
    />
  </main>

  <!-- <DataView :dataMap="dataMap" v-model:selected="selected"
    v-model:category="category" :valid-categories="CATEGORIES()"
    :deselected="DESELECTED">
  </DataView> -->
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