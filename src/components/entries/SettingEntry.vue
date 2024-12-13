<!-- This component displays information for characters. The main way to change what info is shown (and how) is to modify the components that are shown; rearrange/rewite/delete them; or create new ones entirely. -->
<script setup>
// Components designed for multiple types of entries
import Deity from './Deity.vue'
import EntryChanger from './EntryChanger.vue'
import Name from './Name.vue'
import Picture from './Picture.vue'
import RichStory from './RichStory.vue'
import SeeAlso from './SeeAlso.vue'
import Status from './Status.vue'
import Tag from '../Tag.vue'

// Components specific to settings
import SettingType from './SettingType.vue'
import { inject } from 'vue'
const DESELECTED = inject('DESELECTED')
const CATEGORIES = inject('CATEGORIES')
const showables = []
const hideables = []
const PLACEHOLDER = 'public/emblems/Unknown.png'
const props = defineProps({
  ID: { type:Number, required: true, default: -1 },
  info: { type:Object, required: true },
  category: { type:String, required: true },
  maxID: { type:Number, required: true },
  seeAlso: { type:Array, default: [], required: false}
})
const emit = defineEmits(['updateSelection'])

function close() { updateSelection(DESELECTED, props.category) }
function goTo(id, category, caller="JournalEntry"){
  updateSelection(id, category, caller)
}
function updateSelection(id, category, caller="JournalEntry") {
  emit('updateSelection', id, category, caller)
}
</script>

<template>
  <div>
    <div class="split">
      <!-- LeftColumn -->
      <div class="leftColumn">
        <EntryChanger :id="info.id" :category="props.category"
        :maxID="props.maxID" @updateSelection="goTo"></EntryChanger>
        <div class="TitleBox">
          <!-- TODO: Change CSS class to emblem, whatever that means -->
          <Name :name="info.name" :type="info.type" @click="close()"/>
          <SettingType :type="info.type" :emblem="info.emblem" :country="info.country" :placeholder="PLACEHOLDER"></SettingType>
        </div>
        <!-- Rest of the info. -->
        <div class="InfoBox">
          <Picture class="map" :src="info.image" :placeholder="PLACEHOLDER" :renderOnPlaceholder="false"></Picture>
          <div class="tagList">
            <Status :value="info.status" :type="info.type"
            :checkType="true" :renderTag="true"
            :showables="showables" :hideables="hideables"
            ></Status>
            <Tag v-if="info.plane !== ''"><p>Plane: {{ info.plane }}</p></Tag>
            <!-- TODO: update Deity component for multiple deities -->
            <div class="deities" v-if="info.deities.length > 0">
              <h5>Deities:</h5>
              <Tag v-for="deity in info.deities"><Deity :deity="deity" :prefix="''"/></Tag>
            </div>
            <Tag v-if="info.population !== ''"><p>Population: {{ info.population }}</p></Tag>
          </div>
        </div>
      </div>
      <!-- RightColumn -->
      <div class="rightColumn">
        <div class="stories">
          <RichStory class="story" v-for="story in props.info.contents" 
            :contents="story" :category="props.category" @updateSelection="updateSelection">
          </RichStory>
          <!-- <Story class="story" v-for="story in props.info.contents" 
          :contents="story">
          </Story> -->
        </div>
        <SeeAlso :contents="props.seeAlso" @updateSelection="updateSelection"/>
      </div>
    </div>
  </div>
</template>

<style scoped>
.entryName {
  border-color: rgba(186, 186, 186, 0.5);
  border-style: solid;
  border-width: 0 0 2px 0;
  border-radius: 16px;
}

.map {
  width: 256px;
  height: 256px;
}

.deities {
  display: flex;
  flex-flow: row wrap;
  justify-content: flex-start;
  align-items: center;

  h5 {
    margin: 0;
    margin-right: 0.25em;
  }
}
</style>