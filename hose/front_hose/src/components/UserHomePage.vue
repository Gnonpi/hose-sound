<template>
  <main>
    <UpNavBarComp></UpNavBarComp>
    <h1>User: {{ username }}</h1>
    <div id="displayed-hoses">
      <div v-for="(hose, index) in accessibleHoses" :key="index">
        <b-card :id="'hose-card-' + index">
          <h6 slot="header" class="mb-0">
            Hose
            <router-link :to="{
              name: 'HoseViewPage',
              params: {
                hoseid: hose.id}
               }">{{ hose.hose_name }}
            </router-link>
          </h6>
          <b-card-text>
            <b-row>
              <b-col md="4">
                <router-link to="/h">
                  <b-img thumbnail type="image/png" id="'img-hose-' + hose.id" src="/static/favicon.ico"></b-img>
                </router-link>
              </b-col>
              <b-col md="5">
                With
                <router-link :to="{
                  name: 'UserHomePage',
                  params: {
                    username: hose.username,
                    userId: hose.userId}
                   }">
                  <h5><b>{{ hose.username }}</b></h5>
                </router-link>
              </b-col>
              <b-col md="1">
                Contains {{ hose.number_of_songs }} song{{ hose.number_of_songs > 1 ? 's':'' }}
              </b-col>
            </b-row>
          </b-card-text>
          <em slot="footer">Last update {{ hose.time_last_update }}</em>
        </b-card>
        <hr>
      </div>
    </div>
  </main>
</template>

<script>
import shared from '../shared.js'
import UpNavBarComp from './UpNavBarComp.vue'
import axios from 'axios'

export default {
  name: 'UserHomePage',
  components: {UpNavBarComp},
  data: function () {
    return {
      loggedUsername: '',
      username: '',
      accessibleHoses: []
    }
  },
  methods: {
    getUserInfo: function (userId) {
      const base = {
        baseURL: this.$store.state.endpoints.baseUrl,
        headers: {
          Authorization: `JWT ${this.$store.state.jwt}`,
          'Content-Type': 'application/json'
        },
        xhrFields: {
          withCredentials: true
        }
      }
      const axiosInstance = axios.create(base)
      const userIdUrl = this.$store.state.endpoints.restHoser + userId
      axiosInstance.get(userIdUrl, {})
        .then(response => {
          this.username = response.data.username
          response.data.accessible_hoses.forEach(hose => {
            this.accessibleHoses.push(this.formatHose(hose))
          })
        })
        .catch(error => {
          console.debug('Error')
          console.debug(error)
          console.debug(JSON.stringify(error, null, 2))
        })
    },
    formatHose: function (hose) {
      let otherUser = {userId: hose.second_end, username: hose.second_end_username}
      if (this.username === hose.second_end_username) {
        otherUser = {userId: hose.first_end, username: hose.first_end_username}
      }
      delete hose.first_end
      delete hose.first_end_username
      delete hose.second_end
      delete hose.second_end_username
      hose = Object.assign(hose, otherUser)
      return hose
    }
  },
  mounted: function () {
    const returnLogin = shared.verifyIsLogged(this)
    if (returnLogin === false) {
      this.loggedUsername = this.$store.state.authUser.username
      let userId = this.$route.params.userId
      if (typeof userId === 'undefined') {
        userId = this.$store.state.authUser.id
      }
      this.getUserInfo(userId)
    }
  },
  beforeRouteUpdate (to, from, next) {
    // react to route changes...
    // don't forget to call next()
    this.username = ''
    this.accessibleHoses = []
    const returnLogin = shared.verifyIsLogged(this)
    if (returnLogin === false) {
      let userId = to.params.userId
      this.getUserInfo(userId)
    }
    next()
  }
}
</script>

<style scoped>

</style>
