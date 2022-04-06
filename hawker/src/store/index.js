import { reactive } from 'vue'

const globalState = reactive({
  user_id: localStorage.getItem("user_id"),
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