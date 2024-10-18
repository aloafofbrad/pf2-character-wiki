<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
    history: {
        Type: Array,
        Default: []
    },
    index: {
        Type: Number,
        Default: -1
    },
    version: {
        Type: String,
        Default: ""
    },
    searchQuery: {
        Type:String,
        Default: ""
    }
})
const searchQuery = ref('');

function canGoBack() {
    return props.index !== -1 && props.index > 0
}

function canGoForward() {
    return props.index !== -1 && props.index < (props.history.length - 1)
}
</script>

<template>
  <div class="Navbar">
    <!-- Left-aligned elements -->
    <form id="NavbarSearch" class="NavButton prevent-select"
    >
        Search <input name="query" v-model.trim="searchQuery" placeholder="you know you want to... :3" autocomplete="off" @submit.prevent="onSubmit" @keyup="$emit('updateSearch', searchQuery)"/>
    </form>
    <div class="NavButton prevent-select"
        @click="$emit('sortAlphabetically')"
        >
        ■Sort 🅰
    </div>
    <div class="NavButton prevent-select"
        @click="$emit('sortChronologically')"
        >
        ■Sort ⌛
    </div>
    <div class="NavButton prevent-select"
        v-show="canGoBack()" @click="$emit('goBack')"
        >
        ⬅️
    </div>
    <div class="NavButton prevent-select"
        v-show="canGoForward()" @click="$emit('goForward')"
        >
        ➡️
    </div>
    <!-- Right-aligned elements -->
    <div class="NavButton prevent-select NavButtonRight">■Source Code</div>
    <div class="NavButton prevent-select NavButtonRight">Version {{ version }}</div>
    <!-- <div class="NavButton prevent-select NavButtonRight" v-if="props.searchQuery.length">■{{ props.searchQuery }}■</div> -->
  </div>
</template>

<style>

.Navbar, .NavButton, .NavButtonRight {
    font-family: monospace;
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

.Navbar, .Navbar > .NavButton, .Navbar > .NavItem, form, input {
    height: 24px;
    color: white;
    background-color: black;
    opacity: 0.75;
}

.Navbar > .NavButton, .form {
    padding-left: 8px;
    padding-right: 8px;
}

.input[type=text]:focus {
    border: 1px solid black;
}

.NavButton:hover {
    background-color: white;
    opacity: 1.0;
    color: black;
}

.Navbar:last-child {
    margin-left:auto;
}

input:hover {
    background-color: white;
    opacity: 1.0;
    color: black;
    border: 1px solid black;
}

input {
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

input::placeholder {
    color: #fff;
    opacity: 1;
}

#NavbarSearch {
    display: flex;
    flex-flow: row wrap;
    justify-content: flex-end;
}
</style>