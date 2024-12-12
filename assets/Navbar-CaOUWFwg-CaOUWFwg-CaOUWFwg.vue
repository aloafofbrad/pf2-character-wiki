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
    },
    view: {
        Type: Number
    },
    art_view: {
        Type: Number
    },
    list_view: {
        Type: Number
    },
    multi_view_enabled: {
        Type: Boolean
    }
})
const emit = defineEmits(['goBack', 'goForward', 'toggleView'])

const searchQuery = ref('')
const debug = true

const viewToggleText = computed(() => {
    var artText = "View List"
    var listText = "View Art"
    if (props.view === props.art_view){
        return artText
    }
    else if (props.view === props.list_view){
        return listText
    }
    return artText
})

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

function toggleView() {
    emit('toggleView')
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
    <div class="NavButton prevent-select" v-if="props.multi_view_enabled" @click="toggleView()">■{{ viewToggleText }}</div>
    <!-- Right-aligned elements -->
    <div class="NavButton prevent-select NavButtonRight"><a :href="props.source">■Source Code</a></div>
    <div class="NavButton prevent-select NavButtonRight">Version {{ version }}</div>
    <!-- <div class="NavButton prevent-select NavButtonRight" v-if="props.searchQuery.length">■{{ props.searchQuery }}■</div> -->
  </div>
</template>

<style>

.Navbar {
    min-height: 24px;
    overflow-y: hidden;
    font-family: monospace;
    overflow-y: hidden;
    width: 100%;
    justify-content: space-between;
    padding: unset;
    backdrop-filter: blur(8px);

    a {
        text-decoration: none;
    }

    .NavButton {
        display: flex;
        flex-flow: column nowrap;
        justify-content: center;
        align-items: center;
        float: left;
        font-family: inherit;

        * {
            display: inherit;
            flex-flow: inherit;
            justify-content: inherit;
            align-items: inherit;
            font-family: inherit;
        }

        &:hover {
            background-color: white;
            opacity: 1.0;
            color: black;
        }

        input {
            font-size: smaller;
            font-family: monospace;
            border: 1px solid white;
            margin-left: 0.5em;
            height: 12px;
            width: 16em;
            outline: none;

            &:hover {
                background-color: white;
                opacity: 1.0;
                color: black;
                border: 1px solid black;
            }

            &[type=text]:focus {
                border: 1px solid black;
            }

            &::placeholder {
                color: #fff;
                opacity: 1;
            }
        }
    }

    .NavButton, form {
        padding-left: 8px;
        padding-right: 8px;
    }

    .NavButton, form, input, a {
        height: 24px;
    }

    .NavButtonRight {
        float: right;
    }

    &:last-child {
        margin-left:auto;
    }
}

.Navbar {
    color: white;
    background-color: black;
    opacity: 0.75;

    .NavButton {
        color: inherit;
        background-color: inherit;
        opacity: inherit;

        * {
            color: inherit;
            background-color: inherit;
            opacity: inherit;
        }
    }
}

#NavbarSearch {
    display: flex;
    flex-flow: row nowrap;
    justify-content: center;
    align-items: center;
}

.historyButton {
    filter: grayscale(100%);
}
</style>