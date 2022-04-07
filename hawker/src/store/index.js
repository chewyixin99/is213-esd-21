import { reactive } from 'vue'

const globalState = reactive({
  user_id: localStorage.getItem('user_id') || null,
  selected_items: [],
  avail_balance: null,
  total_balance: null,
})

const stateSetters = {
  resetState() {
    globalState.user_id = null
    globalState.selected_items = []
    globalState.avail_balance = null
    globalState.total_balance = null
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
  },

  update_availBalance(payload) {
    globalState.avail_balance = payload
  },

  update_totalBalance(payload) {
    globalState.total_balance = payload
  }
}

export {
  globalState,
  stateSetters
}