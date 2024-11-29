<!-- This component displays information for characters. The main way to change what info is shown (and how) is to modify the components that are shown; rearrange/rewite/delete them; or create new ones entirely. -->
<script setup>
import Age from './Age.vue'
import Ancestry from './Ancestry.vue'
import Background from './Background.vue'
import Class from './Class.vue'
import CharacterType from './CharacterType.vue'
import Deity from './Deity.vue'
import Name from './Name.vue'
import Nationality from './Nationality.vue'
import Picture from './Picture.vue'
import Status from './Status.vue'
import Tag from '../Tag.vue'
import { ref, computed, inject } from 'vue'
const DESELECTED = inject('DESELECTED')
const CATEGORIES = inject('CATEGORIES')
const props = defineProps({
  ID: { type:Number, required: true, default: -1 },
  info: { type:Object, required: true },
  category: { type:String, required: true }
})
const emit = defineEmits(['updateSelection'])

function updateSelection(id, category) {
  emit('updateSelection', id, category)
}

function close() { updateSelection(DESELECTED, props.category) }
function goTo(id, category) { updateSelection(id, category) }
</script>

<template class="bio" @keyup.esc="close()">
  <div id="deselect" class="prevent-select" @click="close()"><p>❌</p></div>
  <div id="split">
    <!-- LeftColumn
     This is intended to be the character's picture, name, and so on and 
     so forth. -->
    <div id="leftColumn">
      <div class="CharacterBox">
        <!-- Remove the following line to remove the image: -->
        <Picture :src="info.image" @click="close()"/>
        <Name :name="info.name" :type="info.type" @click="close()"/>
        <CharacterType :type="info.type" :customTooltip="''"/>
      </div>
      <!-- Rest of the character info. -->
      <div class="InfoBox">
          <div class="tagList">
            <Tag v-if="info.pronouns !== '?'">Pronouns: {{ info.pronouns }}</Tag>
            <Tag><Ancestry :ancestry="info.ancestry" :heritage="info.heritage"/></Tag>
            <Tag><Background :background="info.background"/></Tag>
            <Tag><Class :class="info.class" :level="info.level"/></Tag>
            <Tag v-if="info.deity !== ''"><Deity :deity="info.deity"/></Tag>
            <Tag><Age :age="info.age" :ancestry="info.ancestry"/></Tag>
            <Tag v-if="(info.type === 'Player' || info.type === 'Normal') || ((info.type !== 'Generic' && info.type !== 'Group') && info.status !== '?')">Status: {{ info.status }}</Tag>
            <!-- <Tag id="status"><Status :value="info.status", :defaultValue="''"></Status></Tag> -->
            <Tag><Nationality class="tag" v-if="info.nationality" :nationality="info.nationality"/></Tag>
            <!-- The ID is mainly shown for debugging. It's safe to 
            remove. -->
            <Tag>ID: {{ info.id }}</Tag>
          </div>
        </div>
    </div>
    <!-- RightColumn -->
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
    align-items: flex-start;
    z-index: 1;
  }

  #leftColumn {
    width: 352px;
    border-width: 0 2px 0 0; 
    border-color: rgba(186, 186, 186, 0.5);
    border-style: solid;
    border-radius: 16px;

    .tagList {
      margin-left: 4px;

      .tag {
        margin-left: inherit;

        * {
          margin-left: unset;
        }
      }
    }
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

  #leftColumn {
    width: 100%;
    .tagList {
      margin-left: 4px;
      margin-right: 4px;
    }
  }

  #leftColumn > .InfoBox > .tagList {
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
  height: 100%;
  display: flex;
  flex-flow: column wrap;
  align-items: flex-start;
}

#leftColumn {
  .CharacterBox {
    display: flex;
    flex-flow: column nowrap;
    justify-content: flex-start;
    align-items: center;

    * {
      margin-top: 0.05em;
    }
  }
  .CharacterBox, .InfoBox {
    width: 100%;
  }
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

.InfoBox {
  padding-right: 2em;
  /* border: 1px dotted; */
}

.InfoBox > ul {
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
  font-family: monospace;
  font-weight: bold;
  text-align: center;
  background-color: white;
  color: black;
  padding: 4px 4px 4px 4px;
  margin: 4px 4px 4px 4px;
  border-radius: 32px;
  filter:grayscale(1.0);
}
#deselect:hover, #deselect:hover > * {
  scale: calc(1.05);
}
#deselect, #deselect > * {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  text-align: center;
  height: 32px;
  width: 32px;
}

</style>