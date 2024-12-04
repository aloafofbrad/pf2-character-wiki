<script setup>
import { computed } from 'vue'

const props = defineProps({
  name: { type:String, default:"" },
  id: { type:Number, default:"" },
  defaultNameValue: { type:String, default:"?" },
  emdash: { type:String, default: "―" },
  date: { type:String, default: "" },
  addendum: { type:String, default: "" }
})

function isEmptyString(str){ return str === "" }
function exists(x){ return x !== undefined && x !== null }
function stringExists(str){ return !isEmptyString(str) && exists(str) }

const innerText = computed(() => {
  if (isEmptyString(props.name)) { return "" }
  var result = props.emdash
  if (props.name === props.defaultNameValue || !exists(props.name)){
    result = result.concat(props.defaultNameValue)
  }
  else { result = result.concat(props.name) }

  if (stringExists(props.date)){
    result = result.concat(`, ${props.date}`)
  }

  result = result.concat(". ")
  if (stringExists(props.addendum)){
    result = result.concat(props.addendum)
  }

  return result
})

</script>

<template>
  <h5 class="entryAuthor">{{ innerText }}</h5>
</template>

<style>
.entryAuthor {
  margin-left: 2em;
  margin-top: 0;
  text-align: flex-start;
  font-style: italic;
  word-wrap: break-word;
}
</style>