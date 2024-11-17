<script setup>
import { ref, computed } from 'vue'
import countries from '../../data/countries.json'
import nationalities from '../../data/nationalities.json'

const props = defineProps({
  nationality: String
})

function exists(x) {
  return x !== null && x !== undefined
}

const country = computed(() => {
  try {
    return countries["countries"][props.nationality]
  }
  catch {}
  return countries["countries"][""]
})

const nationality = computed(() => {
  try {
    return nationalities["nationalities"][props.nationality]
  }
  catch {}
  return nationalities["nationalities"][""]
})

const innerText = computed(() => {
  var result = "Nationality: "
  return result.concat(`${nationality.value}`)
})

function imageUrl() {
  return new URL(`/${country.value}`, import.meta.url).href;
}
const hover = ref(false)

</script>

<template>
  <div class="Nationality">
    <p>{{ innerText }}</p>
    <img id="nationality" :src="imageUrl()" :title="nationalities[nationality]" @mouseenter="hover = true" @mouseleave="hover = false"/>
  </div>
</template>

<style>

.Nationality {
  display: flex;
  flex-flow: row nowrap;
  justify-content: flex-start;
  align-items: center;
}

.Nationality > * {
  color: black;
}

.Nationality > img {
  /* border-radius: 16px; */
  width: 1.25em;
  height: 1.25em;
  margin-left: 4px;
}
</style>