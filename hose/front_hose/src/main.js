// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import Vuex from 'vuex'
import App from './App'
import router from './router'

import VueAxios from 'vue-axios'
import axios from 'axios'

// eslint-disable-next-line
import jwt_decode from 'jwt-decode'

import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import Unicon from 'vue-unicons'
// https://antonreshetov.github.io/vue-unicons/
import { uniSignOutAlt, uniSlidersV } from 'vue-unicons/src/icons'

Unicon.add([uniSignOutAlt, uniSlidersV])
Vue.use(Unicon)

Vue.use(Vuex)
Vue.use(VueAxios, axios)

Vue.use(BootstrapVue)

axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'

Vue.config.productionTip = false

const urlBackend = 'http://localhost:8000'
const store = new Vuex.Store({
  state: {
    jwt: localStorage.getItem('t'),
    endpoints: {
      baseUrl: urlBackend,
      obtainJWT: urlBackend + '/auth/api-token-auth/',
      refreshJWT: urlBackend + '/auth/auth/api-token-refresh/',
      restHoser: urlBackend + '/user/rest/hoser/',
      signup: urlBackend + '/signup/'
    }
  },
  mutations: {
    setAuthUser (state, {authUser, isAuthenticated}) {
      Vue.set(state, 'authUser', authUser)
      Vue.set(state, 'isAuthenticated', isAuthenticated)
    },
    logoutUser (state) {
      localStorage.removeItem('t')
      state.jwt = null
      Vue.delete(state, 'authUser')
      Vue.delete(state, 'isAuthenticated')
    },
    updateToken (state, newToken) {
      localStorage.setItem('t', newToken)
      state.jwt = newToken
    },
    removeToken (state) {
      localStorage.removeItem('t')
      state.jwt = null
    }
  },
  actions: {
    obtainToken (username, password) {
      const payload = {
        username: username,
        password: password
      }
      axios.post(this.state.endpoints.obtainJWT, payload)
        .then(response => {
          this.commit('updateToken', response.data.token)
        })
        .catch(error => {
          console.log(error)
        })
    },
    refreshToken () {
      const payload = {
        token: this.state.jwt
      }

      axios.post(this.state.endpoints.refreshJWT, payload)
        .then(response => {
          this.commit('updateToken', response.data.token)
        })
        .catch(error => {
          console.log(error)
        })
    },
    inspectToken () {
      const token = this.state.jwt
      if (token) {
        const decoded = jwt_decode(token)
        const exp = decoded.exp
        const origIat = decoded.orig_iat

        if (exp - (Date.now() / 1000) < 1800 && (Date.now() / 1000) - origIat < 628200) {
          this.dispatch('refreshToken')
        } else if (exp - (Date.now() / 1000) < 1800) {
          // DO NOTHING, DO NOT REFRESH
        } else {
          // PROMPT USER TO RE-LOGIN, THIS ELSE CLAUSE COVERS THE CONDITION WHERE A TOKEN IS EXPIRED AS WELL
          router.push({name: 'HomePage'})
        }
      }
    }
  }
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
