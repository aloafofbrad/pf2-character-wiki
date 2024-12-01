<script setup>
import Tag from '../Tag.vue';
import { ref, computed, onMounted } from 'vue'
const props = defineProps({
  entries: { Type: Array, default: [] },
  category: { Type: String, required: true },
  maxID: { type: Number, required: true },
  displayKey: { type: String, required: true },
})
const emit = defineEmits(['updateSelection'])
const arranged = defineModel({ type: Object, default: {}, required: false })

function isAValidId(id) {
  // return (id >= 0 && id <= (props.entries.length - 1))
  console.log(`id (${id}) < props.maxID (${props.maxID})`)
  return (id >= 0 && id < props.maxID)
}

function entryClick(id) {
  console.log("entry clicked, id: ", id)
  emit('updateSelection', id, props.category)
}

function display(entry) { return entry.info[props.displayKey] }

const letters = ["A","B","C","D","E","F","G",
                 "H","I","J","K","L","M","N",
                 "O","P","Q","R","S","T","U",
                 "V","W","X","Y","Z","?","0",
                 "1","2","3","4","5","6","7",
                 "8","9"];

function arrange() {
  var result = {};
  for (let i = 0; i < letters.length; i++){
    var curr = letters.at(i)
    try{
      result[curr] = props.entries.filter(entry => entry.info[props.displayKey].startsWith(curr))
      console.log(result[curr])
    }
    catch (e) {}
    if (result[curr] === undefined) { result[curr] = [] }
  }
  arranged.value = result
}

const showableLetters = computed(() => {
  var result = []
  const keys = Object.keys(arranged.value)
  for (let i = 0; i < keys.length; i++){
    if (arranged.value[keys[i]].length > 0) { result.push(keys[i]) }
  }
  return result
})

onMounted(() => {
  arrange()
})
</script>

<template>
  <div class="indexContainer">
    <div class="section" v-for="letter in showableLetters">
      <h3>{{ letter }}</h3>
      <div class="indexSectionEntries">
        <Tag  v-for="entry in arranged[letter]" v-show="isAValidId(entry.id)"
          @click="entryClick(entry.id)">
          {{ display(entry) }}
        </Tag>
      </div>
    </div>
  </div>
</template>

<style scoped>

@media only screen and (orientation:landscape){
  .indexContainer {
    height: 90vh;
    align-self: flex-start;
    margin-left: 5em;

    .section {
      width: 110%;
    }
  }
}

@media only screen and (orientation:portrait){
  .indexContainer {
    height: 100%;
    align-self: center;
    margin-left: 0;
    margin-bottom: 2em;

    .section {
      width: 100%;
    }
  }
}

.indexContainer {
  /* border: 1px solid #f0f; */
  display: flex;
  flex-flow: column wrap;
  align-items: flex-start;
  justify-content: flex-start;
  scroll-behavior: smooth;
  min-height: auto;
  column-gap: 2.5em;

  .section {
    /* border: 1px solid #0f0; */
    display: flex;
    flex-flow: column nowrap;
    align-items: flex-start;
    justify-content: center;

    h1 {
      margin-bottom: 0.25em;
    }

    .indexSectionEntries {
      border-top: 1px solid;
      width: inherit;
      padding-top: 0.5em;
      padding-bottom: 0.5em;
    }

  }

  .tag {
    margin-left: 8px;
    margin-right: 8px;
    overflow-x: hidden;
    color: black;
    background-color: white;
  }

  .tag:hover {
    background-color: #b4dd1e;
  }
}

</style>