<script setup>
import Age from './Age.vue'
import Ancestry from './Ancestry.vue'
import Background from './Background.vue'
import Class from './Class.vue'
import CharacterType from './CharacterType.vue'
import Deity from './Deity.vue'
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
  <div id="deselect" class="prevent-select tag" @click="$emit('deselectEntry')" @keyup.esc="$emit('deselectEntry')">X</div>
  <div id="split">
    <div id="leftColumn">
      <img id="pic" :src="imageUrl()" alt="img" @click="$emit('deselectEntry')"/>
      <h1 v-if="info.type !== 'Normal'" id="characterName">{{ info.name }} ({{ info.type }})</h1>
      <h1 v-else id="characterName">{{ info.name }}</h1>
      <div class="BasicInfoBox">
          <ul class="tagList">
            <li class="tag" v-if="info.type !== 'Normal'"><CharacterType :type="info.type" :customTooltip="''"/></li>
            <li class="tag" v-if="info.pronouns !== 'None'">Pronouns: {{ info.pronouns }}</li>
            <li class="tag"><Ancestry :ancestry="info.ancestry" :heritage="info.heritage"/></li>
            <li class="tag"><Background :background="info.background"/></li>
            <li class="tag"><Class :class="info.class" :level="info.level"/></li>
            <li class="tag" v-if="info.deity !== ''"><Deity :deity="info.deity"/></li>
            <Age class="visible-mobile" :age="info.age" :ancestry="info.ancestry"/>
            <li class="tag visible-mobile" v-if="(info.type === 'Player' || info.type === 'Normal') || ((info.type !== 'Generic' && info.type !== 'Group') && info.status !== '?')">Status: {{ info.status }}</li>
            <li class="tag visible-mobile" v-if="info.nationality">Nationality: {{ info.nationality }}</li>
            <li class="tag">ID: {{ info.id }}</li>
          </ul>
        </div>
    </div>
    <div id="rightColumn">
      <div id="basics">
        <Emblem :nationality="info.nationality"/>
        <div class="BasicInfoBox">
          <ul class="tagList">
            <Age class="visible-landscape" :age="info.age" :ancestry="info.ancestry"/>
            <li class="tag visible-landscape" v-if="(info.type === 'Player' || info.type === 'Normal') || ((info.type !== 'Generic' && info.type !== 'Group') && info.status !== '?')">Status: {{ info.status }}</li>
            <li class="tag visible-landscape" v-if="info.nationality">Nationality: {{ info.nationality }}</li>
          </ul>
        </div>
      </div>
      <div id="biography">
        <ul>
          <p v-for="bi in info.biography" :key="bi.id">{{ bi }}</p>
        </ul>
      </div>
    </div>
  </div>
  <div></div>
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

/* Contains #split */
#bio {
  flex-direction: column;
  flex-wrap: wrap;
  z-index: 2;
  top: 24px;
  width: 100vw;
  height: 100%;
  min-height: calc(100vh - 24px);
  background-color: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(16px);
  overflow-y: auto;
}

/* CONTAINS leftColumn, rightColumn */
@media only screen and (orientation: landscape){
  #split {
    justify-content: flex-start;
    z-index: 1;
  }

  .visible-landscape {
    display: inherit;
  }

  .visible-mobile {
    display: none;
  }
}

@media only screen and (orientation: portrait){
  #split {
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: center;
    align-items: flex-start;

    z-index: 1;
  }

  .tagList {
    display: flex;
    flex-direction: column;
    flex-wrap: nowrap;
    align-items: center;
  }

  .visible-landscape {
    display: none;
  }

  .visible-mobile {
    display: inherit;
  }
}

#bio, #split {
  display: flex;
  position: absolute;
  font-family: serif;
}

/* \/ \/ \/ \/ LEFT COLUMN \/ \/ \/ \/ */
#leftColumn {
  width: 352px;
  height: 100%;
  display: flex;
  flex-flow: column wrap;
  align-items: flex-start;
}

#pic {
  width: 256px;
  padding-left: 48px;
  padding-right: 48px;
}

#characterName {
  width: 100%;
  margin: 0;
  padding-left: 0.25em;
  word-wrap: break-word;
}

#leftColumn > .BasicInfoBox {
  width: 100%;
}

#leftColumn > .tagList, #leftColumn > .tagList > .tag {
  padding-left: 4px;
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
  display: flex;
  flex-flow: row wrap;
  align-items: flex-start;
  justify-content: flex-start;
}

/* /\ /\ /\ /\ RIGHT COLUMN /\ /\ /\ /\ */

#deselect {
  position: absolute;
  z-index: 3;
  height: 1.5em;
  font-family: monospace;
  font-weight: bold;
  text-align: center;
  background-color: white;
  color: black;
}

#deselect:hover {
  background-color: #b4dd1e;
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