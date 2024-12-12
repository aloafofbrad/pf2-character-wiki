<script setup>
import { computed, onMounted } from 'vue'

const props = defineProps({
  value: { type:String, required: true }
})

const conversionTable = {
  // italic
  "italic":{
    "head":"\\s\\*",
    "headReplace": " <em>",
    "tail":"\\*\\s",
    "tailReplace": "</em> ",
    "capture":"\\s\\*(.*)\\*\\s"
  },
  // bold
  "\\s\\*\\*": " <strong>",
  "\\*\\*\\s": "</strong> ",
  // bold & italic
  "\\s\\*\\*\\*": " <em><strong>",
  "\\*\\*\\*\\s": "</strong></em>",
  // blockquote
  "$>*\\s": "",
}

function matchesRegex(s, regex){
  var result = false
  try { result = regex.test(s) }
  catch (e){
    console.log("Expected error in matchesRegex")
    console.log(e)
  }
  return result
}

// // test if s is a match for a trailing MD tag
// function matchesTail(s, tail){
//   var regex = new RegExp(tail)
//   return matchesRegex(s, regex)
// }

function mdToHTML(){}

const innerHTML = computed(() => {
  var result = ""
  return result
})

onMounted(() => {
  var element = document.getElementById("MDRenderer")
  if (element !== undefined && element !== null){
    element.innerHTML = innerHTML.value
  }
})
</script>

<template>
  <div id="MDRenderer"></div>
</template>

<style scoped>
.story {
  flex-flow: column wrap;
  justify-content: flex-start;
  align-items: flex-start;
  margin-top: 1.5em;

  p {
    margin-bottom: 0.25em;
  }
}
</style>