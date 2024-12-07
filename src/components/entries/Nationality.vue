<script setup>
import { ref, computed, inject } from 'vue'
import countries from '../../data/countries.json'
import nationalities from '../../data/nationalities.json'
const exists = inject('exists')
const props = defineProps({
  nationality: { Type: String, Default: "?" },
  showCountryName: { Type: Boolean, Default: false }
})

const country = computed(() => {
  if (!exists(props.nationality)){
    return countries["countries"]["?"]
  }
  return countries["countries"][props.nationality]
})

const nationality = computed(() => {
  if (!exists(props.nationality)){
    return nationalities["nationalities"]["?"]
  }
  return nationalities["nationalities"][props.nationality]
})

const innerText = computed(() => {
  if (props.showCountryName){
    return country.value
  }
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