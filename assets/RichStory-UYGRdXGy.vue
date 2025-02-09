<script setup>
import Author from './Author.vue';
import Entrylink from './Entrylink.vue';
import { computed } from 'vue'
const props = defineProps({
  contents: { type:Object, required:true },
  category: { type:String, required:true },
})
const emit = defineEmits(['updateSelection'])
const entryLinkPattern = /!\[(.+?)\]\((\d+?),\s?(\w+?)\)/gd;
function linkSubstrings(text){
  var result = []
  const matches = [...text.matchAll(entryLinkPattern)];
  for (let i = 0; i < matches.length; i++){
    const index = matches[i].index
    var curr = { text: matches[i][1],
                   id: parseInt(matches[i][2]),
             category: matches[i][3],
                start: matches[i].index,
                index: matches[i].index,
           fullLength: matches[i][0].length,
               length: matches[i][1].length,
                  end: matches[i].index + matches[i][0].length }
    result.push(curr)
  }
  return result
}
function nonLinkSubstrings(text, links){
  var startIndex = 0;
  if (links.length === 0){
    return [{ text: text,
                id: null,
          category: null,
             start: startIndex,
             index: startIndex,
        fullLength: text.length,
            length: text.length,
               end: text.length - 1 }]
  }
  var result = []
  for (let i = 0; i < links.length; i++){
    var substring; var fullLength;
    var a = links[i]
    var start = 0 + startIndex
    var end = a.start
    substring = text.slice(start, end)
    fullLength = start - end + 1
    var curr = { text: " ".concat(substring),
                   id: null,
             category: null,
                start: start,
                index: start,
           fullLength: fullLength,
               length: substring.length,
                  end: end }
    result.push(curr)
    startIndex = a.end + 1
  }
  if (startIndex + 1 !== text.length){
    var start = 0 + startIndex
    var end = text.length
    var substring = text.slice(start, end)
    var curr = { text: " ".concat(substring),
                   id: null,
             category: null,
                start: start,
                index: start, 
           fullLength: start - end + 1, 
               length: substring.length,
                  end: end }
    result.push(curr)
  }
  return result
}
function compareIndices(a, b){
  if (a.index < b.index){ return -1 }
  if (a.index > b.index){ return 1 }
  return 0
}
// return all substrings belonging to this text, in order
function zipper(text){
  var result = []
  // Get all of the links and plaintext from text
  var links = linkSubstrings(text)
  var plains = nonLinkSubstrings(text, links)
  // Add all of the links and plaintext to the result
  result = result.concat(links).concat(plains)
  /* Sort the results, by the index of where their first character 
  appears in text */
  result = result.sort(compareIndices)
  return result
}

const zippers = computed(() => {
  var result = []
  for (let i = 0; i < props.contents.text.length; i++){
    result.push(zipper(props.contents.text[i]))
  }
  return result
})

function updateSelection(id, category, caller="MDRenderer") {
  emit('updateSelection', id, category, caller)
}
</script>

<template>
  <div class="story">
    <p v-for="text in zippers">
       <Entrylink v-for="span in text"
        :id="span.id" :category="span.category"
        :start="span.start" :end="span.end" :length="span.fullLength"
        :index="span.index" :tooltips="true" :underline="true"
        @updateSelection="updateSelection"
       >{{ span.text }}</Entrylink>
    </p>
    <!-- <p v-for="rawtext in props.contents.text">{{ rawtext }}</p> -->
    <Author :name="props.contents.author.name"
      :id="props.contents.author.id"
      :date="props.contents.author.date"
      :addendum="props.contents.author.addendum"
    ></Author>
  </div>
</template>

<style module>
Entrylink {
  text-decoration: underline;
  color: #b4dd1e;
  background-color: black;

  &:hover {
    color: black;
    background-color: #b4dd1e;
  }
}
</style>

<style scoped>
.story {
  display: flex;
  flex-flow: column wrap;
  justify-content: flex-start;
  align-items: flex-start;
  width: inherit;
  margin-top: 1.5em;

  p {
    margin-top: unset;
    margin-bottom: 0.25em;
    text-indent: 1.5em;
    text-align: justify;
  }
  
  p:first-of-type {
    text-indent: 0;
  }
}
</style>