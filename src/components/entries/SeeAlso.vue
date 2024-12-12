<script setup>
import Tag from '../Tag.vue';
import { computed, inject } from 'vue'
const DESELECTED = inject('DESELECTED')
const exists = inject('exists')
const props = defineProps({
  contents: { type:Array, default:[] },
  titleString: { type:String, default: "See also:", required: false },
  unrenderable: { type:Object, required: false, default: {
    "id":-1,
    "category":".",
    "displayValue":""
  }}
})
const emit = defineEmits(['updateSelection'])

function isRenderable(entry){
  if (!exists(entry.id)){ return false }
  if (!exists(entry.category)){ return false }
  if (!exists(entry.displayValue)){ return false }
  if (entry.id === DESELECTED){ return false }
  if (entry.displayValue === ""){ return false }
  return true
}

function compareDisplayValues(a, b){
  if (a.displayValue > b.displayValue){ return 1 }
  if (a.displayValue < b.displayValue){ return -1 }
  return 0
}

const arranged = computed(() => {
  var result = [];
  for (let i = 0; i < props.contents.length; i++){
    var curr = props.contents[i]
    console.log(curr)
    if (isRenderable(curr)){ result.push(curr) }
  }
  // console.log("See Also (below):")
  // console.log(result)
  return result.sort(compareDisplayValues)
})

function updateSelection(id, category, caller="SeeAlso"){
  emit('updateSelection', id, category, caller)
}
function goTo(id, category){ updateSelection(id, category) }
</script>

<template>
  <div class="seeAlso">
    <h3 v-if="arranged.length > 0">{{ props.titleString }}</h3>
    <Tag v-for="obj in arranged" @click="goTo(obj.id, obj.category)">
      <p>{{ obj.displayValue }}</p>
    </Tag>
  </div>
</template>

<style scoped>
.seeAlso {
  display: flex;
  flex-flow: row wrap;
  justify-content: flex-start;
  align-items: center;
  margin-top: 1.5em;
  padding-top: 0;
  padding-bottom: 0;

  h3 {
    margin-right: 0.5em;
    margin-bottom: 0;
    margin-top: 0;
  }

  .tag {
    /* border-radius: unset; */
    background-color: white;
    color: black;

    &:hover {
      background-color: #b4dd1e;
    }

    p, p:hover {
      background-color: inherit;
      color: inherit;
    }

    /* &:first-of-type {
      border-top-left-radius: 16px;
      border-bottom-left-radius: 16px;
    }

    &:last-of-type {
      border-top-right-radius: 16px;
      border-bottom-right-radius: 16px;
    } */
  }
}
</style>