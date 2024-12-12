<!-- This component displays information for characters. The main way to change what info is shown (and how) is to modify the components that are shown; rearrange/rewite/delete them; or create new ones entirely. -->
<script setup>
// Components designed for multiple types of entries
import EntryChanger from './EntryChanger.vue'
import Name from './Name.vue'
import Nationality from './Nationality.vue'
import SeeAlso from './SeeAlso.vue'
import Status from './Status.vue'
import Story from './Story.vue'
import Tag from '../Tag.vue'

// Components specific to journals
import { inject } from 'vue'
const DESELECTED = inject('DESELECTED')
const CATEGORIES = inject('CATEGORIES')
const showables = ['Ongoing', 'Ended']
const hideables = ['Mythological']
const props = defineProps({
  ID: { type:Number, required: true, default: -1 },
  info: { type:Object, required: true },
  category: { type:String, required: true },
  maxID: { type:Number, required: true },
  seeAlso: { type:Array, default: [], required: false}
})
const emit = defineEmits(['updateSelection'])

function updateSelection(id, category, caller="JournalEntry") {
  emit('updateSelection', id, category, caller)
}

function close() { updateSelection(DESELECTED, props.category) }
function goTo(id, category, caller="JournalEntry"){
  updateSelection(id, category, caller)
}
function debug() {
  console.log("JournalEntry with ID", props.ID)
}
debug()
</script>

<template>
  <div>
    <div class="split">
      <!-- LeftColumn -->
      <div class="leftColumn">
        <EntryChanger :id="info.id" :category="props.category"
        :maxID="props.maxID" @updateSelection="goTo"></EntryChanger>
        <div class="TitleBox">
          <Name :name="info.title" :type="info.type" @click="close()"/>
        </div>
        <!-- Rest of the info. -->
        <div class="InfoBox">
            <div class="tagList">
              <Status :value="info.status" :type="info.type"
                :checkType="true" :renderTag="true"
                :showables="showables"
                :hideables="hideables"
              ></Status>
            </div>
          </div>
      </div>
      <!-- RightColumn -->
      <div class="rightColumn">
        <div class="stories">
          <Story class="story" v-for="story in props.info.contents" 
            :contents="story">
          </Story>
        </div>
        <SeeAlso :contents="props.seeAlso" @updateSelection="updateSelection"/>
      </div>
    </div>
    <div></div>
  </div>
</template>

<style>
</style>