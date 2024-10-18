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
    <img id="pic" :src="imageUrl()" alt="img"/>
    <h1 v-if="info.type !== 'Normal'" id="characterName">{{ info.name }} ({{ info.type }})</h1>
    <h1 v-else id="characterName">{{ info.name }}</h1>
    <div class="BasicInfoBox">
        <ul>
          <li v-if="info.pronouns !== 'None'">Pronouns: {{ info.pronouns }}</li>
          <li><Ancestry :ancestry="info.ancestry" :heritage="info.heritage"/></li>
          <!-- <li>Background: {{ info.background }}</li> -->
          <li><Background :background="info.background"/></li>
          <li v-if="info.level !== '?' && info.level !== ''">Class: {{ info.level }}-level {{ info.class }}</li>
          <li v-else>Class: {{ info.class }}</li>
          <li>ID: {{ info.id }}</li>
        </ul>
      </div>
  </div>
  <div id="rightColumn">
    <div id="basics">
      <Emblem :nationality="info.nationality"/>
      <div class="BasicInfoBox">
        <ul>
          <Age :age="info.age" :ancestry="info.ancestry"/>
          <li v-if="(info.type === 'Player' || info.type === 'Normal') || ((info.type !== 'Generic' && info.type !== 'Group') && info.status !== '?')">Status: {{ info.status }}</li>
          <li v-if="info.nationality">Nationality: {{ info.nationality }}</li>
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

#characterName, li, p, .Bio > div, Age, Ancestry, Background, Emblem {
  color:black;
}

/* CONTAINS leftColumn, rightColumn */
#bio {
  display:flex;
  flex-direction: row;
  /* top: 24px; */
  top: calc(24px + 128px);
  width: calc(100vw - 16px);
  height: 100vh;
  bottom: 100%;
  padding-top:0;
  margin-top:0;
  align-items:flex-start;
  justify-content: flex-start;
  border-top: 2px dotted #000;
  font-family: serif;
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
  width: 256px;
  background-color: #696969;
}

#characterName {
  max-width: 256px;
  margin: 0;
  padding-left: 0.25em;
  padding-right: 0.25em;
  word-wrap: break-word;
  /* font-family: serif; */
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
  /* padding-right: 4px; */
  border: 1px solid;
}

.BasicInfoBox > ul {
  margin: 0;
  padding-left: 1.5em;
  padding-right: 1.5em;
}

#biography {
  width: 100%;
  display: flex;
  flex-flow: row wrap;
  align-items: flex-start;
  justify-content: flex-start;
}

/* #biography > ul {
} */
/* /\ /\ /\ /\ RIGHT COLUMN /\ /\ /\ /\ */
</style>