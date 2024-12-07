<script setup>
// Dynamic links. Each one constructs a URL dynamically from the props given
import { ref, computed, inject } from 'vue'
const exists = inject('exists')

/* Props
  innerText   Text to be rendered inside the a tag
  domain      Usually 'https://2e.aonprd.com'
  path        Usually something like Ancestries.aspx
  params      Used to construct the URL's query string. Key:value pairs
              to use as URL parameters for the given page. For
              Ancestries.aspx, ID 20 redirects to ratfolk. The resulting
              URL would be https://2e.aonprd.com/Ancestries.aspx?ID=20
 */
const props = defineProps({
  innerText:{ type: String, default: "" },
  domain:{ type: String, default: "" },
  path:{ type: String, default: "" },
  params:{ type: Object, default: {} }
})

function allPropsExist(){
  return exists(props.innerText) && exists(props.domain) &&
         exists(props.path) && exists(props.params)
}
// Construct a URL dynamically from the props given
const url = computed (() => {
  var result = ""
  if (allPropsExist()) {
    var result = props.domain + props.path
    if (props.params){
      result = result.concat("?")
      /* Construct the query string by appending each key-value pair to 
      the URL */
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
  <a :href="url" target="_blank" class="dynalink">{{ innerText }}</a>
</template>

<style>
.dynalink {
  /* color: #aaccff; */
  color: darkblue;

  &:visited {
    /* color: #ffccff; */
    color: darkorchid;
  }

  &:hover {
    background-color: inherit;
    color: white;
  }

  &:visited:hover {
    background-color: inherit;
    color: white;
  }
}

</style>