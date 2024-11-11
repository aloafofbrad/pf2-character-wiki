<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
    history: {
        // Type: Array,
        Default: [],
        Required: false
    },
    index: {
        // Type: Number,
        Default: -1
    },
    version: {
        Type: String,
        Default: ""
    },
    source: {
        Type: String,
        Default: ""
    },
    searchQuery: {
        Type:String,
        Default: ""
    }
})
const emit = defineEmits(['goBack', 'goForward'])

const searchQuery = ref('')
const debug = true

function historyExists() {
    var result = props.history !== null && props.history !== undefined
    if (debug) {
        if (!result) {
            console.log("Navbar didn't get history")
        }
        console.log(`history (navbar): ${props.history}`)
    }
    return result
}

function indexExists() {
    var result = props.index !== null && props.index !== undefined
    if (debug) {
        if (!result) {
            console.log("Navbar didn't get index")
        }
        console.log(`history index (navbar): ${props.index}`)
    }
    return result
}

function canGoBack() {
    var result = false
    if (!historyExists() || !indexExists()){
        return false
    }
    result = props.index > 0
    return result
}

function canGoForward() {
    var result = false
    if (!historyExists() || !indexExists()){
        return false
    }
    result = props.index < (props.history.length - 1)
    return result
}

function getHTMLElement(id){
    var element = document.getElementById(id)
    return element
}

function updateElementStyle(element, property, value){
    if (element !== null && element !== undefined){
        try{
            // element.style.setProperty("filter", "grayscale(1.0)")
            element.style.setProperty(property, value)
        }
        catch{}
    }
}

function updateHistoryButtons(){
    var back = getHTMLElement("backButton")
    var forward = getHTMLElement("forwardButton")
    let filterValue = "grayscale(100%)"
    let noFilter = "none"
    if (canGoBack()){
        updateElementStyle(back, "filter", noFilter)
    }
    else {
        updateElementStyle(back, "filter", filterValue)
    }
    if (canGoForward()){
        updateElementStyle(forward, "filter", noFilter)
    }
    else {
        updateElementStyle(forward, "filter", filterValue)
    }
}

function goBack(){
    if (canGoBack()){
        emit('goBack')
    }
}

function goForward(){
    if (canGoForward()){
        emit('goForward')
    }
}

function move(direction){
    if (direction === 'back'){
        goBack()
    }
    if (direction === 'forward'){
        goForward()
    }
    updateHistoryButtons()
}
</script>

<template>
  <div class="Navbar">
    <!-- Left-aligned elements -->
    <form id="NavbarSearch" class="NavButton prevent-select">
        Search <input name="query" v-model.trim="searchQuery" placeholder="you know you want to... :3" autocomplete="off" @submit.prevent="onSubmit" @keyup="$emit('updateSearch', searchQuery)"/>
    </form>
    <div class="NavButton prevent-select" @click="$emit('sortAlphabetically')">
        ■Sort 🅰
    </div>
    <div class="NavButton prevent-select" @click="$emit('sortChronologically')">
        ■Sort ⌛
    </div>
    <div class="NavButton prevent-select historyButton" id="backButton" @click="move('back')">
        ■Back ⏪
    </div>
    <div class="NavButton prevent-select historyButton" id="forwardButton" @click="move('forward')">
        ■Next ⏩
    </div>
    <!-- Right-aligned elements -->
    <div class="NavButton prevent-select NavButtonRight"><a :href="props.source">■Source Code</a></div>
    <div class="NavButton prevent-select NavButtonRight">Version {{ version }}</div>
    <!-- <div class="NavButton prevent-select NavButtonRight" v-if="props.searchQuery.length">■{{ props.searchQuery }}■</div> -->
  </div>
</template>

<style>

.Navbar, .NavButton, .NavButton > * {
    font-family: monospace;
}

.NavButton > a {
    text-decoration: none;
}

.Navbar {
    position: absolute;
    z-index: 2;
    top: 0;
    left: 0;
    min-width: 100vw;
    justify-content: space-between;
    padding: unset;
    backdrop-filter: blur(8px);
}

.Navbar:after {
  content: '';
  display: table;
  clear: both;
}

.Navbar > .NavButton {
    float:left;
}

.Navbar > .NavButtonRight {
    float:right;
}

.Navbar {
    min-height: 24px;
}

.Navbar > .NavButton, form, input, a {
    height: 24px;
}

.Navbar, .Navbar > .NavButton, .NavButton > form, .NavButton > input, .NavButton > a {
    color: white;
    background-color: black;
    opacity: 0.75;
}

.Navbar > .NavButton, .form {
    padding-left: 8px;
    padding-right: 8px;
}

.NavButton > .input[type=text]:focus {
    border: 1px solid black;
}

.NavButton:hover {
    background-color: white;
    opacity: 1.0;
    color: black;
}

.NavButton > *, .NavButton:hover > *, .NavButton:hover > *:visited {
    background-color: inherit;
    color: inherit;
}

.Navbar:last-child {
    margin-left:auto;
}

.NavButton > input:hover {
    background-color: white;
    opacity: 1.0;
    color: black;
    border: 1px solid black;
}

.NavButton > input {
    outline: none;
    color: #fff;
    margin-top: 2px;
    margin-left: 0.5em;
    height: 12px;
    font-size: smaller;
    font-family: monospace;
    background-color: #181818;
    border: 1px solid white;
    width: 16em;
}

.NavButton > input::placeholder {
    color: #fff;
    opacity: 1;
}

#NavbarSearch {
    display: flex;
    flex-flow: row wrap;
    justify-content: flex-end;
}

.historyButton {
    filter: grayscale(100%);
}
</style>