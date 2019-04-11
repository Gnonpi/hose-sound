<template>
  <div>
    User home page: {{ username }}
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'UserHomePage',
  data: function () {
    return {
      username: ''
    }
  },
  methods: {
    getUserInfo: function () {
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
      const userIdUrl = this.$store.state.endpoints.baseUrl + '/user/rest/hoser/' + this.$store.state.authUser.id
      axiosInstance.get(userIdUrl, {
      })
        .then(response => {
          this.username = response.data.username
        })
        .catch(error => {
          console.debug('Error')
          console.debug(error)
          console.debug(JSON.stringify(error, null, 2))
        })
    }
  },
  mounted: function () {
    let returnLogin = true
    if ('authUser' in this.$store.state) {
      console.debug(this.$store.state.authUser)
      if (this.$store.state.isAuthenticated) {
        this.getUserInfo()
        returnLogin = false
      } else {
        console.debug('user not auth')
      }
    } else {
      console.debug('authUser not in state')
    }
    if (returnLogin) {
      console.log('Going back to login')
      this.$router.push({name: 'HomePage'})
    }
  }
}
</script>

<style scoped>

</style>
