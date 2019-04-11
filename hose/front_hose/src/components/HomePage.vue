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

const urlBackend = 'http://localhost:8000'

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
          console.log(jwtToken)
          this.$router.push('/u')
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
