<script setup>
import Age from './Age.vue'
import Ancestry from './Ancestry.vue'
import Background from './Background.vue'
import Class from './Class.vue'
import CharacterType from './CharacterType.vue'
import Deity from './Deity.vue'
import Nationality from './Nationality.vue'
import Tag from './Tag.vue'
import { ref, computed } from 'vue'

const props = defineProps({
  ID: Object,
  info: Object
})

const emit = defineEmits(['deselect-entry', 'select-entry'])
function imageUrl() { return new URL(`/${props.info.image}`, import.meta.url) }

function setup(){
  return {nationalities, imageUrl}
}
</script>

<template class="bio">
  <div id="deselect" class="prevent-select snappy" @click="$emit('deselect-entry')" @keyup.esc="$emit('deselect-entry')">❌</div>
  <div id="split">
    <div id="leftColumn">
      <img id="pic" :src="imageUrl()" alt="img" @click="$emit('deselect-entry')"/>
      <h1 v-if="info.type !== 'Normal'" id="characterName">{{ info.name }} ({{ info.type }})</h1>
      <h1 v-else id="characterName">{{ info.name }}</h1>
      <div class="BasicInfoBox">
          <div class="tagList">
            <Tag v-if="info.type !== 'Normal'"><CharacterType :type="info.type" :customTooltip="''"/></Tag>
            <Tag v-if="info.pronouns !== 'None'">Pronouns: {{ info.pronouns }}</Tag>
            <Tag><Ancestry :ancestry="info.ancestry" :heritage="info.heritage"/></Tag>
            <Tag><Background :background="info.background"/></Tag>
            <Tag><Class :class="info.class" :level="info.level"/></Tag>
            <Tag v-if="info.deity !== ''"><Deity :deity="info.deity"/></Tag>
            <Tag><Age :age="info.age" :ancestry="info.ancestry"/></Tag>
            <Tag v-if="(info.type === 'Player' || info.type === 'Normal') || ((info.type !== 'Generic' && info.type !== 'Group') && info.status !== '?')">Status: {{ info.status }}</Tag>
            <Tag><Nationality class="tag" v-if="info.nationality" :nationality="info.nationality"/></Tag>
            <Tag>ID: {{ info.id }}</Tag>
          </div>
        </div>
    </div>
    <div id="rightColumn">
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

  #leftColumn > .BasicInfoBox > .tagList {
    flex-direction: row;
    flex-wrap: wrap;
    /* align-items: center; */
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
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-content: center;
  z-index: 3;
  font-family: monospace;
  font-weight: bold;
  text-align: center;
  background-color: white;
  color: black;
  padding: 4px 4px 4px 4px;
  margin: 4px 4px 4px 4px;
  border-radius: 16px;
  filter:grayscale(1.0);
}
#deselect:hover {
  scale: calc(1.05);
}
#deselect, #deselect > * {
  height: 1.5em;
  width: 1.5em;
}

</style>