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
</style>