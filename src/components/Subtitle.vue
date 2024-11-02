<script setup>

const props = defineProps({
  name: String,
  type: String
})
</script>

<template>
  <div id="subtitleBox" class="SubtitleBox prevent-select">
    <h1 v-if="type === 'Normal'">{{ name }}</h1>
    <h1 v-else>{{ name }} ({{ type }})</h1>
  </div>
</template>

<style>
.SubtitleBox {
    display: flex;
    flex-direction: column;
    height: auto;
    width: inherit;
    max-height: 128px;
    opacity: 0.8;
    background-color: black;
    color: white;

    text-align: center;
    justify-content: flex-end;
}

.SubtitleBox > * {
  font-size: small;
  word-wrap: break-word;
  padding-left: 4px;
  padding-right: 4px;
  margin-top: 0px;
  margin-bottom: 2px;
}
</style>