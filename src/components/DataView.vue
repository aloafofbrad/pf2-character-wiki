<!-- This component displays the appropriate entry for the given category. -->
<script setup>
import CharacterEntry from './entries/CharacterEntry.vue'
import JournalEntry from './entries/JournalEntry.vue';
import { ref, reactive, computed, inject, watchEffect } from 'vue'
const DESELECTED = inject('DESELECTED')
const props = defineProps({
  characterData: { type: String, required: true },
  journalData: { type: String, required: true },
  settingData: { type: String, required: true },
  entry: { type:Object, required: true },
})
const selected = defineModel('selected', { type:Number, required: true })
const category = defineModel('category', { type:String, required: true })
const emit = defineEmits(['updateSelection'])

function showDataFromCategory(cat){
  // if (!noSelectionMade()){
  //   return cat === category.value
  // }
  // return false
  if (noSelectionMade()) { return false }
  return cat === category.value
}

/* Returns true if the selected entry is the deselected value */
function noSelectionMade() { return selected.value === DESELECTED }

const debug = computed(() => {
  var result = `DataView Stats: | selected.value: ${selected.value} | props.category: ${props.category} | showDataFromCategory(props.category): ${showDataFromCategory(props.category)}`
  return result
})

function updateSelection(id, category){
  console.log(`DataView updateSelection(${id}, ${category})`)
  emit('updateSelection', id, category)
}
</script>

<template>  
  <div class="dataView">
    <div>
      <h3>{{ debug }}</h3>
    </div>
    <!-- CharacterEntry
     To change data shown in the CharacterEntry, or the way that data is 
     shown, you'll need to modify the file for the CharacterEntry 
     component (see the top of this file for its location, in the 
     imports section). Don't change the v-show binding here, regardless 
     of which containers are shown.
     -->
    <div class="bio" v-if="showDataFromCategory(props.characterData)">
      <CharacterEntry
        :ID="props.entry.id"
        :info="props.entry.info"
        :category="category"
        @update-selection="updateSelection">
      </CharacterEntry>
    </div>
    <!-- end CharacterEntry -->
    <!-- JournalEntry -->
    <div class="bio" v-else-if="showDataFromCategory(props.journalData)">
      <JournalEntry
        :ID="props.entry.id"
        :info="props.entry.info"
        :category="category"
        @update-selection="updateSelection"
      ></JournalEntry>
    </div>
    <!-- end JournalEntry -->
    <!-- TODO: SETTINGS -->
  </div>
</template>

<style scoped>
.dataView {
  top: auto;
  z-index: 1;
  margin: 0;
  padding: 0;
  display: flex;
  flex-flow: column nowrap;
  justify-content: flex-start;
  align-items: center;
  flex-grow: 1;
}

/* \/ \/ \/ CSS for CharacterEntry, JournalEntry, SettingEntry \/ \/ */
/* Contains .split */
.bio {
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
  .split {
    justify-content: flex-start;
    align-items: flex-start;
    z-index: 1;
  }

  .leftColumn {
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
  .split {
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: center;
    align-items: flex-start;

    z-index: 1;
  }

  .leftColumn {
    width: 100%;
    .tagList {
      margin-left: 4px;
      margin-right: 4px;
    }
  }

  .leftColumn > .InfoBox > .tagList {
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

.bio, .split {
  display: flex;
  position: absolute;
  font-family: serif;
}

/* \/ \/ LEFT COLUMN \/ \/ */
.leftColumn {
  height: 100%;
  display: flex;
  flex-flow: column wrap;
  align-items: flex-start;
}

.leftColumn {
  .TitleBox {
    display: flex;
    flex-flow: column nowrap;
    justify-content: flex-start;
    align-items: center;

    * {
      margin-top: 0.05em;
    }
  }
  .TitleBox, .InfoBox {
    width: 100%;
  }
}

/* /\ /\ LEFT COLUMN /\ /\ */

/* \/ \/ RIGHT COLUMN \/ \/ */
.rightColumn {
  width: 100%;
  height: 100%;
  display: flex;
  flex-flow: column wrap;
  align-items: flex-start;
}

.basics {
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

.story {
  width: calc(100% - 2em);
  display: flex;
  flex-flow: row wrap;
  align-items: flex-start;
  justify-content: flex-start;
}

/* /\ /\ RIGHT COLUMN /\ /\ */
/* /\ /\ /\ CSS for CharacterEntry, JournalEntry, SettingEntry /\ /\ */
</style>