<script setup>
// import { ref, computed } from 'vue'

const props = defineProps({
  name: String,
  type: String
})
// const imageUrl = new URL(`/${props.info.image}`, import.meta.url).href
</script>

<template>
  <div class="SubtitleBox prevent-select">
    <h1 v-if="type === 'Normal'">{{ name }}</h1>
    <h1 v-else>{{ name }} ({{ type }})</h1>
  </div>
</template>

<style>
.SubtitleBox {
    display: flex;
    position: fixed;
    top: 64px;
    width: 128px;
    min-height: 32px;
    max-height: auto;
    opacity: 0.8;
    background-color: black;
    color: white;

    font-size: 40%;
    word-wrap: break-word;
    text-align: center;
    justify-content: center;
    align-content: center;
    
    /* padding: 2px; */
    border-radius: 0px;
    top: 100%;
    left: 80px;
    margin-left: -80px;
    
    position: absolute;
    z-index: 1;

    border-bottom: var(--h) solid #0000;
    --h: 5px;
    --w: 10px;
    --p: 50%;
}
</style>