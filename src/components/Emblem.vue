<script setup>
import { ref, computed } from 'vue'
import countries from '../data/countries.json'
import nationalities from '../data/nationalities.json'

const props = defineProps({
  nationality: String
})

function imageUrl() { return new URL(`/${countries[props.nationality]}`, import.meta.url).href; }
const hover = ref(false)
</script>

<template>
  <div class="Emblem prevent-select" :tooltip="nationalities[nationality]"
    @mouseenter="hover = true" @mouseleave="hover = false"
  >
    <img id="emblem" :src="imageUrl(nationality)" :title="nationalities[nationality]"/>
  </div>
</template>

<style>

.Emblem {
  --size: 80px;
  width: var(--size);
  margin: 0;
  padding: 0;
  /* border: 2px solid #f0f; */
}

.Emblem {
  display: flex;
  flex-flow: row wrap;
  justify-content: center;
  align-items: center;
}

#emblem {
  --size: 64px;
  width: var(--size);
  height: var(--size);
  margin: 0;
  padding: 0;
}

@media only screen and (orientation:portrait){
  #emblem {
    --size: 64px;
    position: absolute;
    z-index: 3;
    left: calc(10% - calc(var(--size) / 2));
    top: calc(var(--size) + 24px);
  }
}
</style>