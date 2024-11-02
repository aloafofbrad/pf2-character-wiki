<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  type: {
    type:String,
    default:""
  },
  customTooltip: {
    type:String,
    default:""
  }
})

const innerText = computed(() => {
  var result = "Type: "
  if (props.type !== ""){
    result = result.concat(`${props.type}`)
  }
  return result
})

const tooltip = computed(() => {
  var result = ""
  if (props.customTooltip !== ""){
    result = props.customTooltip
  }
  else if (props.type !== "Normal") {
    if (props.type === "Player") { result = "This entry represents a player character. Info shown here is highly subject to change. If you are the owner of this character and you see a mistake, please let your GM know." }
    else if (props.type === "Group") { result = "This entry represents a group of NPCs. Individuals may vary from info shown here." }
    else if (props.type === "Generic") { result = "This entry represents multiple NPCs. Individuals may vary from info shown here." }
    else if (props.type === "Deity") { result = "This entry represents a deity. In-game lore may differ from standard lore."}
    else if (props.type === "Dragon") { result = "This entry represents a dragon."}
    else { result = "This entry is unique." }
  }
  return result
})
</script>

<template>
  <p :title="tooltip">{{ innerText }}</p>
</template>

<style>
</style>