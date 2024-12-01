<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  name: { type:String, default:"" },
  type: { type:String, default:"Normal" },
  defaultNameValue: { type:String, default:"?" }
})

const entryName = computed(() => {
  var result = ""
  if (props.name === props.defaultNameValue || props.name === undefined || props.name === null){ result = "?" }
  else { result = props.name }
  return result
})

</script>

<template>
  <h1 class="entryName">{{ entryName }}</h1>
  <!-- <h2 id="characterType">{{ charType }}</h2> -->
</template>

<style>
.entryName {
  text-align: center;
  width: 100%;
  margin: 0;
  /* margin-left: 3em;
  margin-right: 3em; */
  word-wrap: break-word;
}
/* #characterType {
  text-align: center;
  margin-top: 0.1em;
} */
</style>