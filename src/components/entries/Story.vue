<script setup>
import Author from './Author.vue';

const props = defineProps({
  contents: { type:Object, required: true }
})
</script>

<template>
  <div class="story">
    <p v-for="rawtext in props.contents.text">{{ rawtext }}</p>
    <!-- <MDRenderer v-for="rawtext in props.contents.text" :value="rawtext"></MDRenderer> -->
    <Author :name="props.contents.author.name"
      :id="props.contents.author.id"
      :date="props.contents.author.date"
      :addendum="props.contents.author.addendum"
    ></Author>
  </div>
</template>

<style scoped>
.story {
  display: flex;
  flex-flow: column wrap;
  justify-content: flex-start;
  align-items: flex-start;
  width: inherit;
  margin-top: 1.5em;

  p {
    margin-top: unset;
    margin-bottom: 0.25em;
    text-indent: 1.5em;
    text-align: justify;
  }
  
  p:first-of-type {
    text-indent: 0;
  }
}
</style>