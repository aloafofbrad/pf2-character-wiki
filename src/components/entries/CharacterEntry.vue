<!-- This component displays information for characters. The main way to change what info is shown (and how) is to modify the components that are shown; rearrange/rewite/delete them; or create new ones entirely. -->
<script setup>
// Components designed for multiple types of entries
import EntryChanger from './EntryChanger.vue'
import Name from './Name.vue'
import Nationality from './Nationality.vue'
import RichStory from './RichStory.vue'
import SeeAlso from './SeeAlso.vue'
import Status from './Status.vue'
import Tag from '../Tag.vue'

// Components specific to characters
import Age from './Age.vue'
import Ancestry from './Ancestry.vue'
import Background from './Background.vue'
import Class from './Class.vue'
import CharacterType from './CharacterType.vue'
import Deity from './Deity.vue'
import Picture from './Picture.vue'
import { inject } from 'vue'
const DESELECTED = inject('DESELECTED')
const showables = ['Player', 'Normal', 'Dead', 'In Party']
const hideables = ['Generic', 'Mythological']
const PLACEHOLDER = 'public/silhouette.jpg'
const props = defineProps({
  ID: { type:Number, required: true, default: -1 },
  info: { type:Object, required: true },
  category: { type:String, required: true },
  maxID: { type:Number, required: true },
  debug: { type:Boolean, required: false, default: false },
  seeAlso: { type:Array, default: [], required: false}
})
const emit = defineEmits(['updateSelection'])

function updateSelection(id, category, caller="CharacterEntry") {
  emit('updateSelection', id, category, caller)
}

function close() { updateSelection(DESELECTED, props.category) }
function goTo(id, category, caller="CharacterEntry"){
  updateSelection(id, category, caller)
}
function debug() {
  console.log(`CharacterEntry with ID`, props.ID, `(below)`)
  console.log(props.info)
}
if (props.debug){ debug() }
</script>

<template>
  <div>
    <div class="split">
      <!-- LeftColumn
      This is intended to be the character's picture, name, and so on and 
      so forth. -->
      <div class="leftColumn">
        <EntryChanger :id="props.ID" :maxID="props.maxID"
          :category="props.category" @updateSelection="goTo"
        ></EntryChanger>
        <div class="TitleBox">
          <!-- Remove the following line to remove the image: -->
          <Picture class="mainPic" :src="info.image" :placeholder="PLACEHOLDER" @click="close()"/>
          <Name :name="info.name" :type="info.type" @click="close()"/>
          <CharacterType :type="info.type" :customTooltip="''"/>
        </div>
        <!-- Rest of the info. -->
        <div class="InfoBox">
          <div class="tagList">
            <Tag v-if="info.pronouns !== '?'">Pronouns: {{ info.pronouns }}</Tag>
            <Status :value="info.status" :type="info.type"
              :checkType="true" :renderTag="true"
              :showables="showables" :hideables="hideables"
            ></Status>
            <Tag><Ancestry :ancestry="info.ancestry" :heritage="info.heritage"/></Tag>
            <Tag><Background :background="info.background"/></Tag>
            <Tag><Class :class="info.class" :level="info.level"/></Tag>
            <Tag v-if="info.deity !== ''"><Deity :deity="info.deity"/></Tag>
            <Tag><Age :age="info.age" :ancestry="info.ancestry"/></Tag>
            <Tag><Nationality class="tag" v-if="info.nationality" :nationality="info.nationality"/></Tag>
          </div>
        </div>
      </div>
      <!-- RightColumn -->
      <div class="rightColumn">
        <div class="stories">
          <RichStory class="story" v-for="story in props.info.contents" 
            :contents="story" :category="props.category" @updateSelection="updateSelection">
          </RichStory>
          <!-- <Story v-for="story in props.info.contents"   
            :contents="story">
          </Story> -->
        </div>
        <SeeAlso :contents="props.seeAlso" @updateSelection="updateSelection"/>
      </div>
    </div>
    <div></div>
  </div>
</template>

<style>
</style>