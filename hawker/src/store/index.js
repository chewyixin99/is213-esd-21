import { reactive } from 'vue'

const globalState = reactive({
  user_id: 2000,
  selected_items: []
})

const stateSetters = {
  updateUser_id(payload) {
    globalState.user_id = payload
  },

  addSelectedItem(payload) {
    globalState.selected_items.push(payload)
    // console.log(payload)
  },

  removeSelectedItem() {
    
  }
}

export {
  globalState,
  stateSetters
}