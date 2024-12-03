<script setup>
import Author from './Author.vue';

const props = defineProps({
  contents: { type:Array, default:[] }
})
</script>

<template>
  <div class="story">
    <p v-for="rawtext in props.contents.text">{{ rawtext }}</p>
    <Author :name="props.contents.author.name"
      :id="props.contents.author.id"
      :date="props.contents.author.date"
      :addendum="props.contents.author.addendum"
    ></Author>
  </div>
</template>

<style scoped>
.story {
  flex-flow: column wrap;
  justify-content: flex-start;
  align-items: flex-start;
  margin-top: 1.5em;

  p {
    margin-bottom: 0.25em;
  }
}
</style>