
import feathers from '@feathersjs/feathers'
import socketio from '@feathersjs/socketio-client'
import auth from '@feathersjs/authentication-client'
import io from 'socket.io-client'
import Vue from 'vue'
import { FeathersVuexFind, FeathersVuexGet } from 'feathers-vuex'



//const url = process.env.VUE_APP_SERVER_API
const url = "http://localhost:3030/"
console.log(url)
const socket = io(url, {transports: ['websocket']})

Vue.component('feathers-vuex-find', FeathersVuexFind)
Vue.component('feathers-vuex-get', FeathersVuexGet) 

const feathersClient = feathers()
  .configure(socketio(socket))
  .configure(auth({ storage: window.localStorage }))


export default feathersClient