<script setup>
// Dynamic links. Each one constructs a URL dynamically from the props given
import { ref, computed } from 'vue'

const props = defineProps({
  innerText:{
    // Text to be rendered inside the a tag
    type: String,
    default: ""
  },
  domain:{
    // Usually 'https://2e.aonprd.com'
    type: String,
    default: ""
  },
  path:{
    // Usually something like 'Ancestries.aspx'
    type: String,
    default: ""
  },
  params:{
    // Constructs the URL's query string.
    // Key-value pairs to use as URL parameters the given page. For Ancestries.aspx, ID 20 redirects to ratfolk.
    // The resulting URL of this example would be https://2e.aonprd.com/Ancestries.aspx?ID=20
    type: Object,
    default: {}
  }
})

// Construct a URL dynamically from the props given
const url = computed (() => {
  var result = ""
  if (props.innerText !== undefined && props.domain !== undefined &&
      props.path !== undefined && props.params !== undefined && 
      props.innerText !== null && props.domain !== null &&
      props.path !== null && props.params !== null) {
    var result = props.domain + props.path
    if (props.params){
      result = result.concat("?")
      // Construct the query string by appending each key-value pair to the URL
      for (const [param, arg] of Object.entries(props.params)){
        result = result.concat(param)
        result = result.concat("=")
        result = result.concat(arg)
        result = result.concat("&")
      }
      // Slice off the last &
      result = result.slice(0, result.length - 1)
    }
  }
  return result
})
</script>

<template>
  <a :href="url" target="_blank">{{ innerText }}</a>
</template>

<style>
a {
  /* color: #aaccff; */
  color: darkblue;
}

a:visited {
  /* color: #ffccff; */
  color: darkorchid;
}

a:hover {
  background-color: darkblue;
  color: white;
}

a:visited:hover {
  background-color: darkorchid;
  color: white;
}

</style>