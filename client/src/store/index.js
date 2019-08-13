import Vue from 'vue'
import Vuex from 'vuex'

import feathersVuex from 'feathers-vuex'
import feathersClient from '../plugins/feathers-client'

const { service, auth, FeathersVuex } = feathersVuex(feathersClient, { idField: 'Id' })
Vue.use(Vuex)


Vue.use(FeathersVuex)
/*
 * If not building with SSR mode, you can
 * directly export the Store instantiation
 */

export default function (/* { ssrContext } */) {
  const Store = new Vuex.Store({
    modules: {
      // example
    },
    plugins:[
      auth({ userService: 'user',entityIdField:'Id' }),
      service('photo',{modelName:'Photo',idField: 'Id'}),
  ] ,

    // enable strict mode (adds overhead!)
    // for dev mode only
    strict: process.env.DEV
  })

  return Store
}
