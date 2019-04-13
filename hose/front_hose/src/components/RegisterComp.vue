<template>
  <div>
    <h3>Register</h3>
    <b-alert v-if="showAlert" show variant="danger">
      {{ alertMessage }}
    </b-alert>
    <b-form id="register-form">
      <b-form-group label="Email" label-for="in-email" id="in-email-group"
          description="We'll never share your email with anyone else.">
        <b-form-input
          id="in-email"
          v-model="registerEmail"
          type="email"
          placeholder="Email"
          required></b-form-input>
      </b-form-group>
      <b-form-group label="Username" label-for="in-username" id="in-username-group">
        <b-form-input
          id="in-username"
          v-model="registerUsername"
          type="text"
          placeholder="Username"
          required
          maxLength="100"
        ></b-form-input>
      </b-form-group>
      <b-form-group label="Password" label-for="in-password1" id="in-password1-group">
        <b-form-input
          id="in-password1"
          v-model="registerPassword1"
          type="password"
          placeholder="Password"
          required
          maxLength="150"
        ></b-form-input>
      </b-form-group>
      <b-form-group label="Repear password" label-for="in-password2" id="in-password2-group"
                    description="Just to be sure">
        <b-form-input
          id="in-password2"
          v-model="registerPassword2"
          type="password"
          placeholder="Password"
          required
          maxLength="150"
        ></b-form-input>
      </b-form-group>
      <b-button
          @click.prevent="register"
          variant="primary"
          type="submit">
          Register
        </b-button>
    </b-form>
  </div>
</template>

<script>
import axios from 'axios'
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'

export default {
  name: 'RegisterComp',
  data: function () {
    return {
      showAlert: false,
      alertMessage: '',
      registerEmail: '',
      registerUsername: '',
      registerPassword1: '',
      registerPassword2: ''
    }
  },
  methods: {
    checkPasswordsEqual: function () {
      if (this.registerPassword1 !== this.registerPassword2) {
        this.raiseAlert('The two password are not equal')
        return false
      } else {
        return true
      }
    },
    register: function () {
      if (this.checkPasswordsEqual()) {
        axios.post(this.$store.state.endpoints.signup, {
          email: this.registerEmail,
          username: this.registerUsername,
          password: this.registerPassword1
        })
          .then(response => {
            console.log(response.data)
          })
          .catch(error => {
            if (error.response) {
              if (error.response.status === 409) {
                this.raiseAlert(error.response.data.error)
              }
            } else {
              console.error(error)
            }
          })
      }
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
