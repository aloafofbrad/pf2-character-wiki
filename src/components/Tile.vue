<script setup>
import Subtitle from './Subtitle.vue'
import { ref, computed } from 'vue'

const props = defineProps({
  id: { type: Number, required: true },
  info: { type: Object, required: true },
  displayKey: { type: String, required: true }
})

const imageUrl = computed(() => {
  return new URL(`/${props.info.image}`, import.meta.url).href
})

const displayValue = computed(() => {
  // console.log("Tile displayKey: ", props.displayKey)
  return props.info[props.displayKey]
})

const hover = ref(false)
</script>

<template>
  <div class="Tile snappy"
    :style="{ backgroundImage: 'url(' + imageUrl + ')' }"
    @mouseenter="hover = true" @mouseleave="hover = false"
  >
    <Subtitle v-show="hover"
        :name="displayValue"
        :type="info.type">
    </Subtitle>
  </div>
</template>

<style>
.Tile {
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  width: 128px;
  height: 128px;
  background-size:cover;
  background-color: #696969;
  transition-duration: 125ms;
}

.Tile:hover {
  box-shadow: 0px 0px 12px 8px black;
  scale: calc(1.1);
}
</style>