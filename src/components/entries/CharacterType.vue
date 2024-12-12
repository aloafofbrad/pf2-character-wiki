<script setup>
import { computed } from 'vue'

const props = defineProps({
  type: { type:String, default:"" },
  customTooltip: { type:String, default:"" },
  tooltips: { type:Object, default:{} }
})

const innerText = computed(() => {
  if (props.type === "Normal"){ return "" }
  return `(${props.type})`
})

const tooltips = {
  "Normal":  "",
  "Player":  "This entry represents a player character. Info shown here is highly subject to change. If you are the owner of this character and you see a mistake, please let your GM know.",
  "Group":   "This entry represents a group of NPCs. Individuals may vary from info shown here.",
  "Generic": "This entry represents multiple NPCs. Individuals may vary from info shown here.",
  "Deity":   "This entry represents a deity. In-game lore may differ from standard lore.",
  "Dragon":  "This entry represents a dragon.",
}

const tooltip = computed(() => {
  var result = ""
  if (props.customTooltip !== ""){
    result = props.customTooltip
  }
  else {
    try {
      result = props.tooltips[props.type]
    } catch (error) {
      result = ""
    }
  }
  return result
})
</script>

<template>
  <h2 :title="tooltip">{{ innerText }}</h2>
</template>

<style>
.characterType {
  text-align: center;
  margin-top: 0.1em;
}
</style>