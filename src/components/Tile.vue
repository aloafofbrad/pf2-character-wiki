<script setup>
import Subtitle from './Subtitle.vue'
import { ref, computed } from 'vue'

const props = defineProps({
  id: Number,
  info: Object
})

const imageUrl = computed(() => {
  return new URL(`/${props.info.image}`, import.meta.url).href
})
const hover = ref(false)
</script>

<template>
  <div class="Tile snappy"
    :style="{ backgroundImage: 'url(' + imageUrl + ')' }"
    @mouseenter="hover = true" @mouseleave="hover = false"
  >
    <Subtitle v-show="hover"
        :name="info.name"
        :type="info.type">
    </Subtitle>
  </div>
</template>

<style>
.Tile {
  display:block;
  width: 128px;
  height: 128px;
  /* background-image: v-bind(imageUrl); */
  background-size:cover;
  /* border: 2px solid #f0f; */
  background-color: #696969;
  transition-duration: 125ms;
}

.Tile > p {
  visibility: hidden;
}

.Tile:hover {
  box-shadow: 0px 0px 12px 8px black;
  scale:calc(1.1);
}
</style>