<template>
    <div id="login-comp">
      <h3>Login</h3>
      <b-alert v-if="showAlert" show variant="danger">
        {{ alertMessage }}
      </b-alert>
      <b-form id="login-form">
        <b-form-group label="Username" label-for="in-username" id="in-username-group">
          <b-form-input
            id="in-username"
            v-model="username"
            type="text"
            placeholder="Username"
            autofocus="autofocus"
            required
            maxlength="150"></b-form-input>
        </b-form-group>
        <b-form-group label="Password" label-for="in-pwsd" id="in-pwsd-group">
          <b-form-input
            id="in-pwsd"
            v-model="password"
            type="password"
            placeholder="Password"
          ></b-form-input>
        </b-form-group>
        <b-button
          @click.prevent="authenticate"
          id="b-login"
          variant="primary"
          type="submit">
          Log In
        </b-button>
      </b-form>
    </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'LoginComp',
  data: function () {
    return {
      username: '',
      password: '',
      showAlert: false,
      alertMessage: ''
    }
  },
  methods: {
    authenticate: function () {
      const payload = {
        username: this.username,
        password: this.password
      }
      // const headers = {
      //   withCredentials: true
      // }
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
              this.$router.push({
                name: 'UserHomePage',
                params: {
                  username: response.data.username,
                  userId: response.data.id
                }
              })
            })
        })
        .catch(error => {
          console.log(error)
          console.debug(error)
          console.dir(error)
          if (error.response) {
            if (error.response.status === 400) {
              let message = 'Invalid username or password'
              this.raiseAlert(message)
              this.password = ''
            }
          }
        })
    },
    raiseAlert: function (message) {
      this.showAlert = true
      this.alertMessage = message
    }
  }
}
</script>

<style scoped>

</style>
