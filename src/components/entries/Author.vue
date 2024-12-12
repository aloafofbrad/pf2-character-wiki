<script setup>
import { computed, inject } from 'vue'
const exists = inject('exists')
const props = defineProps({
  name: { type:String, default:"" },
  id: { type:Number, default:"" },
  defaultNameValue: { type:String, default:"Ezuldor the Archivist" },
  emdash: { type:String, default: "―" },
  date: { type:String, default: "" },
  addendum: { type:String, default: "" },
  useDefaultName: { type:Boolean, default: true }
})

function isEmptyString(str){ return str === "" }
function stringExists(str){ return !isEmptyString(str) && exists(str) }

function chooseName() {
  if (props.useDefaultName && isEmptyString(props.name)){
    return props.defaultNameValue
  }
  return props.name
}

const innerText = computed(() => {
  var result = props.emdash
  result = result.concat(chooseName())

  if (stringExists(props.date)){
    result = result.concat(`, ${props.date}`)
    result = result.concat(". ")
  }

  if (stringExists(props.addendum)){
    result = result.concat(`, ${props.addendum}`)
  }
  result = result.concat(". ")

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