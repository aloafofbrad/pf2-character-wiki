<script setup>
import Age from './Age.vue'
import Ancestry from './Ancestry.vue'
import Background from './Background.vue'
import Class from './Class.vue'
import Dynalink from './Dynalink.vue'
import Emblem from './Emblem.vue'
import Group from './Group.vue'
import { ref, computed } from 'vue'

const props = defineProps({
  info: Object
})
function imageUrl() { return new URL(`/${props.info.image}`, import.meta.url) }

function setup(){
  return {nationalities, imageUrl}
}
</script>

<template class="bio">
  <div id="leftColumn">
    <div id="deselect" class="prevent-select" @click="$emit('deselectEntry')" @keyup.esc="$emit('deselectEntry')">x close</div>
    <img id="pic" :src="imageUrl()" alt="img" @click="$emit('deselectEntry')"/>
    <h1 v-if="info.type !== 'Normal'" id="characterName">{{ info.name }} ({{ info.type }})</h1>
    <h1 v-else id="characterName">{{ info.name }}</h1>
    <div class="BasicInfoBox">
        <ul class="tagList">
          <li class="tag" v-if="info.type !== 'Normal'" tooltip="This entry represents a {{ info.type }}.">Type: {{ info.type }}</li>
          <li class="tag" v-if="info.pronouns !== 'None'">Pronouns: {{ info.pronouns }}</li>
          <li class="tag"><Ancestry :ancestry="info.ancestry" :heritage="info.heritage"/></li>
          <li class="tag"><Background :background="info.background"/></li>
          <li class="tag"><Class :class="info.class" :level="info.level"/></li>
          <li class="tag">ID: {{ info.id }}</li>
        </ul>
      </div>
  </div>
  <div id="rightColumn">
    <div id="basics">
      <Emblem :nationality="info.nationality"/>
      <div class="BasicInfoBox">
        <ul class="tagList">
          <Age :age="info.age" :ancestry="info.ancestry"/>
          <li class="tag" v-if="(info.type === 'Player' || info.type === 'Normal') || ((info.type !== 'Generic' && info.type !== 'Group') && info.status !== '?')">Status: {{ info.status }}</li>
          <li class="tag" v-if="info.nationality">Nationality: {{ info.nationality }}</li>
        </ul>
      </div>
    </div>
    <div id="biography">
      <ul>
        <p v-for="bi in info.biography" :key="bi.id">{{ bi }}</p>
      </ul>
    </div>
  </div>
</template>

<style>
/* \/ \/ \/ \/ DEBUG \/ \/ \/ \/ */
/* #basics {
  border: 2px dotted #f00;
}

#bio {
  border: 2px dotted #fff;
}

#biography {
  border: 2px dotted #00f;
}

#leftColumn, #rightColumn {
  border: 2px dotted #0f0;
}

#characterName {
  border: 2px dotted #ff0;
} */
/* /\ /\ /\ /\ DEBUG /\ /\ /\ /\ */

/* CONTAINS leftColumn, rightColumn */
#bio {
  display:flex;
  flex-direction: row;
  position: absolute;
  top: 24px;
  /* top: calc(24px + 128px); */
  /* width: calc(100vw - 16px); */
  width: 100vw;
  height: 100vh;
  bottom: 100%;
  padding-top:0;
  margin-top:0;
  align-items:flex-start;
  justify-content: flex-start;
  border-top: 2px dotted #000;
  font-family: serif;
  background-color: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(16px);
}

/* \/ \/ \/ \/ LEFT COLUMN \/ \/ \/ \/ */
#leftColumn {
  width: 256px;
  height: 100%;
  display: flex;
  flex-flow: column wrap;
  align-items: flex-start;
}

#pic {
  width: 100%;
  background-color: #696969;
}

#characterName {
  width: 120%;
  margin: 0;
  padding-left: 0.25em;
  padding-right: 0.25em;
  word-wrap: break-word;
  /* font-family: serif; */
}

#leftColumn > .BasicInfoBox {
  width: 100%;
}

#leftColumn > .tagList, #leftColumn > .tagList > .tag {
  position: absolute;
  left: 2px;
}
/* /\ /\ /\ /\ LEFT COLUMN /\ /\ /\ /\ */

/* \/ \/ \/ \/ RIGHT COLUMN \/ \/ \/ \/ */
#rightColumn {
  width: 100%;
  height: 100%;
  display: flex;
  flex-flow: column wrap;
  align-items: flex-start;
}

/* #rightColumn {
  font-family: Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
  font-family: serif;
} */

#basics {
  width: 100%;
  display: flex;
  flex-flow: row wrap;
  justify-content: flex-start;
}

.BasicInfoBox {
  padding-right: 2em;
  /* border: 1px dotted; */
}

.BasicInfoBox > ul {
  margin: 0;
  padding-left: 0;
  padding-right: 1.5em;
}

#biography {
  width: calc(100% - 2em);
  padding-top: 1em;
  padding-left: 1em;
  display: flex;
  flex-flow: row wrap;
  align-items: flex-start;
  justify-content: flex-start;
  /* border: 1px white dotted; */
}

/* #biography > ul {
} */
/* /\ /\ /\ /\ RIGHT COLUMN /\ /\ /\ /\ */

/* div, h1, li, p, #characterName {
  color: #bababa;
} */

#deselect {
  width: calc(256px - 16px);
  height: 1.5em;
  font-size: x-small;
  text-align: center;
  background-color: white;
  color: black;
}

#deselect:hover {
  background-color: black;
  color: white;
}

.tag:hover {
  scale: calc(1.05);
}

.tag > p {
  color: black;
}

.tag > a:hover {
  color: black;
}

</style>