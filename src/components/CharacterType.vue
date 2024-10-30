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

function exists(x) {
  return x !== null && x !== undefined
}

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

// const domain = ref('https://2e.aonprd.com/')
// const path = ref('Ancestries.aspx')

// const ancestryParams = computed(() => {
//   var result = null
//   try{
//     var key = anKey()
//     console.log(ancestries.ancestries[key]['AoNID'])
//     result = {"ID":`${ancestries.ancestries[key]['AoNID']}`}
//   }
//   catch (e){
//     // console.log(e) // Mainly just logging safe typeerrors
//     return null
//   }
//   return result
// })

// function renderLink() {
//   // var result = ancestries.ancestries[props.ancestry]
//   // return result !== null && result !== undefined
//   // return (ancestryParams["ID"] !== null && ancestryParams["ID"] !== undefined)

//   // var key = anKey()
//   // var value = ancestries.ancestries[key]
//   // console.log(key + ":" + value)
//   // return exists(value)
// }

function setup(){
}
</script>

<template>
  <!-- <Dynalink v-if="renderLink()"
    :inner-text="innerText"
    :domain="domain"
    :path="path"
    :params="ancestryParams"
    class="contents"
  />
  <p v-else class="contents">{{ innerText }}</p> -->
  <p class="contents" :title="tooltip">{{ innerText }}</p>
</template>

<style>
.contents {
  margin: 0;
  padding: 0;
}
</style>