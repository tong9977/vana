import Vue from 'vue'
import VuetifyDialog from 'vuetify-dialog'

Vue.use(VuetifyDialog, {
    prompt: {
        actions: {
            false: 'No',
            true: {
              text: 'OK',
              color: 'primary',
              outline: false,
            }
          },
          icon: false, // to disable icon just put false
          width: 500
    }
  })