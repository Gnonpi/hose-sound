// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import Vuex from 'vuex'
import VueAxios from 'vue-axios'
import App from './App'
import router from './router'
import axios from 'axios'

Vue.use(Vuex)
Vue.use(VueAxios, axios)

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
      refreshJWT: urlBackend + '/auth//auth/api-token-refresh/'
    }
  },
  mutations: {
    setAuthUser (state, {
      authUser,
      isAuthenticated
    }) {
      Vue.set(state, 'authUser', authUser)
      Vue.set(state, 'isAuthenticated', isAuthenticated)
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
