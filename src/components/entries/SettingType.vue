<script setup>
import Picture from './Picture.vue';
import { computed } from 'vue'

const props = defineProps({
  type: { type:String, default:"" },
  customTooltip: { type:String, default:"" },
  prefix: { type:String, default:"Type: " },
  country: { type:String, default:"" },
  emblem: { type:String, default:"" },
  placeholder: { type:String, default:"" },
})

const tooltips = {
  "Abode":   "",
  "Capital": "",
  "Cave":    "",
  "Country": "",
  "Dungeon": "",
  "Region":  "",
  "Temple":  "",
  "Village": ""
}

const adjectives = {
  "Abode":   "in",
  "Capital": "of",
  "Cave":    "in",
  "City":    "in",
  "Country": "",
  "Dungeon": "in",
  "Mountain": "in",
  "Normal": "",
  "Region":  "in",
  "Pub":  "in",
  "Temple":  "in",
  "Village": "in"
}

function getAdjective(){
  var result = ""
  try { result = adjectives[props.type] }
  catch (error){ result = "" }
  return result
}

const innerText = computed(() => {
  var result = props.type
  var adjective = getAdjective()
  if (adjective !== ""){
    result = result.concat(" ")
    result = result.concat(adjective)
    result = result.concat(" ")
    result = result.concat(props.country)
  }
  else if (props.type === "Normal") {
    result = "Location in ".concat(props.country)
  }
  else if (props.type === "Country"){
    result = "Country"
  }
  return result
})

const tooltip = computed(() => {
  var result = ""
  if (props.customTooltip !== ""){
    result = props.customTooltip
  }
  else {
    try {
      result = tooltips[props.type]
    } catch (error) {
      result = ""
    }
  }
  return result
})
</script>

<template>
  <div class="settingType">
    <h2 :title="tooltip">{{ innerText }}</h2>
    <Picture class="emblem" :src="props.emblem" :placeholder="props.placeholder"></Picture>
  </div>
</template>

<style>
.settingType {
  display: flex;
  flex-flow: row wrap;
  justify-content: flex-start;
  align-items: flex-start;
  h2 {
    margin-right: 0.25em;
  }
  .emblem {
    width: 2em;
    height: 2em;
  }
}


</style>