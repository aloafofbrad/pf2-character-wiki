<script setup>
import { ref, computed } from 'vue'
import Subtitle from './Subtitle.vue'

const props = defineProps({
  nationality: String
})
const countries = {
  "Aremia":"public/emblems/Aremian-Empire-Emblem.png",
  "Esmaa":"public/emblems/Esmaan-Diocese-Emblem.png",
  "Frambe":"public/emblems/Frambean-Empire-Emblem.png",
  "Kolis":"public/emblems/Protectorate-of-Kolis-Emblem.png",
  "Okdi":"public/emblems/Okdian-Kingdom-Emblem.png",
  "Straia":"public/emblems/Straian-Empire-Emblem.png",
  "Yeonguk":"public/emblems/Most-Serene-Republic-of-Yeonguk-Emblem.png",
  "Any":"public/emblems/Neutral.png",
  "Neutral":"public/emblems/Neutral.png",
  "Uknown":"public/emblems/Unknown.png",
  "null":"public/emblems/Unknown.png",
  "?":"public/emblems/Unknown.png",
  "":"public/emblems/Unknown.png"
}
const nationalities = {
  "Aremia":"Aremian",
  "Esmaa":"Esmaan",
  "Frambe":"Frambean",
  "Kolis":"Kolissian",
  "Okdi":"Okdian",
  "Straia":"Straian",
  "Yeonguk":"Yeongukish",
  "Any":"Any",
  "Neutral":"Neutral",
  "Uknown":"Uknown",
  "null":"Uknown",
  "?":"Uknown",
  "":"Uknown"
}
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
</style>