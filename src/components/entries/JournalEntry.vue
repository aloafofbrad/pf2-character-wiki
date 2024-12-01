<!-- This component displays information for characters. The main way to change what info is shown (and how) is to modify the components that are shown; rearrange/rewite/delete them; or create new ones entirely. -->
<script setup>
// Components designed for multiple types of entries
import Deselect from './Deselect.vue'
import Name from './Name.vue'
import Nationality from './Nationality.vue'
import Tag from '../Tag.vue'

// Components specific to characters
import { inject } from 'vue'
const DESELECTED = inject('DESELECTED')
const CATEGORIES = inject('CATEGORIES')
const props = defineProps({
  ID: { type:Number, required: true, default: -1 },
  info: { type:Object, required: true },
  category: { type:String, required: true },
})
const emit = defineEmits(['updateSelection'])

function updateSelection(id, category) {
  console.log(`CharacterEntry updateSelection(${id}, ${category})`)
  emit('updateSelection', id, category)
}

function close() { updateSelection(DESELECTED, props.category) }
function goTo(id, category) { updateSelection(id, category) }
function debug() {
  console.log("JournalEntry with ID", props.ID)
}
debug()
</script>

<template>
  <Deselect :category="props.category" @updateSelection="close()"/>
  <div class="split">
    <!-- LeftColumn -->
    <div class="leftColumn">
      <div class="TitleBox">
        <Name :name="info.title" :type="info.type" @click="close()"/>
      </div>
      <!-- Rest of the info. -->
      <div class="InfoBox">
          <div class="tagList">
            <!-- The ID is mainly shown for debugging. It's safe to 
            remove. -->
            <Tag>ID: {{ info.id }}</Tag>
          </div>
        </div>
    </div>
    <!-- RightColumn -->
    <div class="rightColumn">
      <div class="story">
        <ul>
          <p v-for="bi in info.contents" :key="bi.id">{{ bi }}</p>
        </ul>
      </div>
    </div>
  </div>
  <div></div>
</template>

<style>
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

/* \/ \/ \/ \/ LEFT COLUMN \/ \/ \/ \/ */
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

/* /\ /\ /\ /\ LEFT COLUMN /\ /\ /\ /\ */

/* \/ \/ \/ \/ RIGHT COLUMN \/ \/ \/ \/ */
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

/* /\ /\ /\ /\ RIGHT COLUMN /\ /\ /\ /\ */

</style>