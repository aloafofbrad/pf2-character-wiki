<!-- This component displays the appropriate entry for the given category. -->
<script setup>
import CharacterEntry from './entries/CharacterEntry.vue'
import JournalEntry from './entries/JournalEntry.vue';
import SettingEntry from './entries/SettingEntry.vue';
import { computed, inject } from 'vue'
const DESELECTED = inject('DESELECTED')
const props = defineProps({
  characterKey: { type: String, required: true },
  journalKey: { type: String, required: true },
  settingKey: { type: String, required: true },
  entry: { type:Object, required: true },
  maxID: { type:Number, required: true },
  seeAlso: { type:Array, default: [], required: false}
})
const selected = defineModel('selected', { type:Number, required: true })
const category = defineModel('category', { type:String, required: true })
const emit = defineEmits(['updateSelection'])

/* Returns true if the selected entry is the deselected value */
function noSelectionMade() { return selected.value === DESELECTED }

function isCurrentCategory(cat){
  return !noSelectionMade() && cat === category.value
}

const debug = computed(() => {
  return
  var result = `DataView Stats: | selected.value: ${selected.value} | props.category: ${props.category} | isCurrentCategory(props.category): ${isCurrentCategory(props.category)}`
  return result
})

function updateSelection(id, category, caller="DataView"){
  emit('updateSelection', id, category, caller)
}
</script>

<template>  
  <div class="dataView">
    <div>
      <h3 v-if="debug">{{ debug }}</h3>
    </div>
    <!-- CharacterEntry
     To change data shown in the CharacterEntry, or the way that data is 
     shown, you'll need to modify the file for the CharacterEntry 
     component (see the top of this file for its location, in the 
     imports section). Don't change the v-show binding here, regardless 
     of which containers are shown.
     -->
    <div class="entry" v-if="isCurrentCategory(props.characterKey)">
      <CharacterEntry
        :ID="props.entry.id"
        :info="props.entry.info"
        :category="category"
        :maxID="props.maxID"
        :seeAlso="props.seeAlso"
        @update-selection="updateSelection">
      </CharacterEntry>
    </div>
    <!-- end CharacterEntry -->
    <!-- JournalEntry -->
    <div class="entry" v-else-if="isCurrentCategory(props.journalKey)">
      <JournalEntry
        :ID="props.entry.id"
        :info="props.entry.info"
        :category="category"
        :maxID="props.maxID"
        :seeAlso="props.seeAlso"
        @update-selection="updateSelection"
      ></JournalEntry>
    </div>
    <!-- end JournalEntry -->
    <!-- SettingEntry -->
    <div class="entry" v-else-if="isCurrentCategory(props.settingKey)">
      <SettingEntry
        :ID="props.entry.id"
        :info="props.entry.info"
        :category="category"
        :maxID="props.maxID"
        :seeAlso="props.seeAlso"
        @update-selection="updateSelection"
      ></SettingEntry>
    </div>
    <!-- end SettingEntry -->
  </div>
</template>

<style>
/* \/ \/ \/ CSS for CharacterEntry, JournalEntry, SettingEntry \/ \/ */
/* Contains .split */
.entry, .split {
  display: flex;
  position: absolute;
  font-family: serif;
}

.entry {
  flex-direction: column;
  flex-wrap: wrap;
  z-index: 2;
  width: 100vw;
  height: 100%;
  min-height: calc(100vh - 24px);
  background-color: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(16px);
}

/* CONTAINS leftColumn, rightColumn */
@media only screen and (orientation: landscape){
  .split {
    justify-content: flex-start;
    align-items: flex-start;
  }

  .leftColumn {
    width: 352px;
    border-width: 0 2px 0 0;

    .tagList {
      margin-left: 0.25em;

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
  }

  .leftColumn {
    width: 100%;
    border-width: 0 0 2px 0;
    padding-bottom: 1em;
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

/* \/ \/ LEFT COLUMN \/ \/ */
.leftColumn {
  height: 100%;
  display: flex;
  flex-flow: column wrap;
  align-items: flex-start;
  border-color: rgba(186, 186, 186, 0.5);
  border-style: solid;
  border-top-right-radius: 16px;
  border-bottom-right-radius: 16px;
}

.leftColumn {
  .mainPic {
    width: 256px;
    margin-left: 48px;
    margin-right: 48px;
    border-radius: 4px;
    background-color: #bababa;
  }

  .TitleBox {
    display: flex;
    flex-flow: column nowrap;
    justify-content: flex-start;
    align-items: center;
    width: 100%;

    * {
      margin-top: 0.05em;
    }
  }

  .InfoBox {
    padding-right: 2em;
    width: 100%;
    display: flex;
    flex-flow: column nowrap;
    justify-content: flex-start;
    align-items: center;
    text-align: center;
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
  margin-left: 2em;
  margin-right: 2em;
  margin-bottom: 4em;
}

.stories {
  display: flex;
  flex-flow: column nowrap;
  justify-content: flex-start;
  align-items: center;
  width: inherit;
}

/* /\ /\ RIGHT COLUMN /\ /\ */
/* /\ /\ /\ CSS for CharacterEntry, JournalEntry, SettingEntry /\ /\ */
</style>

<style scoped>
/* \/ \/ \/ \/ CSS for DataView \/ \/ \/ \/ */
.dataView {
  z-index: 1;
  margin: 0;
  padding: 0;
  display: flex;
  flex-flow: column nowrap;
  justify-content: flex-start;
  align-items: center;
  background-color: #f0f;
}
</style>