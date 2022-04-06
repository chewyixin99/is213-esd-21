import { reactive } from 'vue'

const globalState = reactive({
  user_id: localStorage.getItem('user_id') || null,
  selected_items: []
})

const stateSetters = {
  resetState() {
    globalState.user_id = null
    globalState.selected_items = []
  },

  updateUser_id(payload) {
    globalState.user_id = payload
  },

  addSelectedItem(payload) {
    globalState.selected_items.push(payload)
  },

  removeSelectedItem(index) {
    globalState.selected_items.splice(index, 1)
  },

  clearSelectedItems() {
    globalState.selected_items = []
  }
}

export {
  globalState,
  stateSetters
}