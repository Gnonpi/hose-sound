<template>
  <main>
    <UpNavBarComp></UpNavBarComp>
      <div id="hose-info">
        Hose <b>{{ hoseInformation.hoseName }}</b>
        with
        <router-link :to="{
          name: 'UserHomePage',
          params: {
            username: hoseOtherUser.username,
            userId: hoseOtherUser.userId}
          }">{{ hoseOtherUser.username }}
        </router-link>
        <br>
        <i>Last updated: {{ hoseInformation.timeLastUpdated }}</i>
      </div>
    <div id="available-songs">
      <div v-for="(song, index) in songs" :key="index">
        <b-card>
          <b-row>
            <b-col md="3">
              <b-img src="/static/favicon.ico" fluid img-alt="album art"></b-img>
            </b-col>
            <b-col md="5">
              <b-row>
                {{ song.name }}
              </b-row>
              <b-row>
                <i>Listened {{ song.times_listened }} time{{ song.times_listened > 1 ? 's':'' }}</i>
              </b-row>
            </b-col>
            <b-col md="4">
              <div id="play-button">
                <b-button size="lg">
                  <unicon width="15%" height="15%" name="play-circle" fill="white"></unicon>
                </b-button>
              </div>
            </b-col>
          </b-row>
        </b-card>
      </div>
    </div>
  </main>
</template>

<script>
import axios from 'axios'
import moment from 'moment'

import UpNavBarComp from './UpNavBarComp.vue'

import shared from '../shared.js'

export default {
  name: 'HoseViewPage',
  components: {UpNavBarComp},
  data: function () {
    return {
      hoseInformation: {
        hoseId: '',
        hoseName: '',
        timeLastUpdated: ''
      },
      hoseOtherUser: '',
      songs: []
    }
  },
  methods: {
    getHoseData: function (hoseId) {
      const hoseIdUrl = this.$store.state.endpoints.restHose + hoseId
      const currentUserId = this.$store.state.authUser.id
      // Get hose
      axios.get(hoseIdUrl, {
        headers: {
          Authorization: `JWT ${this.$store.state.jwt}`
        }
      })
        .then(response => {
          this.hoseInformation.hoseId = response.data.id
          this.hoseInformation.hoseName = response.data.hose_name
          let stringLastUpdate = response.data.time_last_update
          let momentDate = moment(stringLastUpdate)
          this.hoseInformation.timeLastUpdated = momentDate.format('MMMM Do YYYY, h:mm:ss a')
          this.hoseOtherUser = {
            userId: response.data.first_end,
            username: response.data.first_end_username
          }
          if (this.hoseOtherUser === currentUserId) {
            this.hoseOtherUser = {
              userId: response.data.second_end,
              username: response.data.second_end_username
            }
          }
        })
        .catch(error => {
          console.error(error)
        })
        .then(() => {
          this.getSongs()
        })
    },
    getSongs: function () {
      const hoseContentsUrl = this.$store.state.endpoints.restSongs
      axios.post(hoseContentsUrl, {
        'other_user_id': this.hoseOtherUser.userId,
        'hose_id': this.hoseInformation.hoseId
      }, {
        headers: {
          Authorization: `JWT ${this.$store.state.jwt}`
        }
      })
        .then(response => {
          this.songs = response.data
        })
        .catch(error => {
          console.error(error)
        })
    }
  },
  mounted: function () {
    const returnLogin = shared.verifyIsLogged(this)
    if (returnLogin === false) {
      this.loggedUsername = this.$store.state.authUser.username
      let hoseId = this.$route.params.hoseid
      if (typeof hoseId === 'undefined') {
        const currentUser = this.$store.state.authUser
        this.$router.replace({
          name: 'UserHomePage',
          params: {username: currentUser.username, userId: currentUser.id}
        })
      }
      this.getHoseData(hoseId)
    }
  },
  beforeRouteUpdate (to, from, next) {
    // react to route changes...
    // don't forget to call next()
    const returnLogin = shared.verifyIsLogged(this)
    let hoseId = to.params.hoseid
    if (returnLogin === false) {
      console.log('--> beforeRouteUpdate: get hose data')
      this.getHoseData(hoseId)
    }
    next()
  }
}
</script>

<style scoped>

</style>
