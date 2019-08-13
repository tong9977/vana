import Vue from 'vue'
import Vuetify from 'vuetify'
import theme from './theme'
import 'vuetify/dist/vuetify.min.css'
import '@mdi/font/css/materialdesignicons.css'

import VuetifyToast from 'vuetify-toast-snackbar'
Vue.use(VuetifyToast)

import VueSignaturePad from 'vue-signature-pad';
Vue.use(VueSignaturePad);

import Lightbox from 'vue-my-photos'
Vue.component('lightbox', Lightbox);

import VuetifyDialog from 'vuetify-dialog'
Vue.use(VuetifyDialog)

import vueNumeralFilterInstaller from 'vue-numeral-filter';
 
Vue.use(vueNumeralFilterInstaller);

Vue.use(Vuetify, {
  iconfont: 'mdi',
  theme
})
