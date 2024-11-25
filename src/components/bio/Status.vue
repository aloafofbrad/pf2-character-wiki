<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  value: {
    type:String,
    default:""
  },
  type: {
    type:String,
    default:""
  },
  parentDisplay: {
    type:Boolean,
    default:true
  },
  defaultValue: {
    type:String,
    default:""
  }
})

const parentElementId = "status"

function updateParentDisplay(show) {
  var parent = document.getElementById(parentElementId)
  if (show){
    parent.style.setProperty("display", "unset")
  }
  else{
    parent.style.setProperty("display", "none")
  }
}

function showable() {
  var result = false
  if ((props.type === "Player" || props.type === "Normal") || (props.type !== "Generic" && props.type !== "Group") && props.value !== "?"){
    result = true
  }
  if (props.parentDisplay) {
    updateParentDisplay(result)
  }
  return result
}

const innerText = computed(() => {
  var result = "Status: "
  result = result.concat(`${props.value}`)
  return result
})
</script>

<template>
  <p v-show="showable()">{{ innerText }}</p>
</template>

<style>
#characterName {
  text-align: center;
  width: 100%;
  margin: 0;
  margin-left: 3em;
  margin-right: 3em;
  word-wrap: break-word;
}
</style>