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

const urlBackend = 'http://127.0.0.1:8000'

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
      axios.post(urlBackend + '/auth/api-token-auth/', payload)
        .then(response => {
          let jwtToken = response.data.token
          const base = {
            baseUrl: urlBackend,
            headers: {
              Authorization: `JWT ${jwtToken}`,
              'Content-Type': 'application/json'
            },
            xhrFields: {
              withCredentials: true
            }
          }
          const axiosInstance = axios.create(base)
          axiosInstance({
            url: '/user/',
            method: 'get',
            params: {}
          })
            .then((response) => {
              let authUser = response.data
              console.log(`authUser: ${authUser}`)
            })
        })
        .catch(error => {
          console.log(error)
          console.debug(error)
        })
    }
  }
}
</script>

<style scoped>

</style>
