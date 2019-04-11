<template>
  <div id="app">
    <main>
      <form class="login form">
        <div class="field">
          <label for="id_username">Username</label>
          <input
            v-model="username"
            type="text"
            placeholder="Username"
            autofocus="autofocus"
            maxlength="150"
            id="id_username">
        </div>
        <div class="field">
          <label for="id_password">Password</label>
          <input
            v-model="password"
            type="password"
            placeholder="Password"
            id="id_password">
        </div>
        <button
          @click.prevent="authenticate"
          class="button primary"
          type="submit">
          Log In
        </button>
      </form>
    </main>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'HomePage',
  data: function () {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    authenticate: function () {
      const payload = {
        username: this.username,
        password: this.password
      }
      axios.post(this.$store.state.endpoints.obtainJWT, payload)
        .then(response => {
          this.$store.commit('updateToken', response.data.token)

          const base = {
            baseURL: this.$store.state.endpoints.baseUrl,
            headers: {
            // Set your Authorization to 'JWT', not Bearer!!!
              Authorization: `JWT ${this.$store.state.jwt}`,
              'Content-Type': 'application/json'
            },
            xhrFields: {
              withCredentials: true
            }
          }
          // Even though the authentication returned a user object that can be
          // decoded, we fetch it again. This way we aren't super dependant on
          // JWT and can plug in something else.
          const axiosInstance = axios.create(base)
          axiosInstance({
            url: '/user/cur',
            method: 'get',
            params: {}
          })
            .then(response => {
              this.$store.commit('setAuthUser',
                {authUser: response.data, isAuthenticated: true}
              )
              console.debug('Logged in')
              this.$router.push({name: 'UserHomePage'})
            })
        })
        .catch(error => {
          console.log(error)
          console.debug(error)
          console.dir(error)
        })
    }
  }
}
</script>

<style scoped>

</style>
