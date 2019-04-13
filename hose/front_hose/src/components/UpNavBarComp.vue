<template>
  <b-navbar id="upnavbar">
    <b-navbar-brand href="#" class="ml-0">
      <img src="/static/favicon.ico" class="d-inline-block align-top" alt="logo">
    </b-navbar-brand>
    <b-navbar-brand>
      <h2>{{ loggedUsername }}</h2>
    </b-navbar-brand>
    <b-navbar-nav class="ml-auto">
      <b-button>
        <unicon name="sign-out-alt" fill="white"></unicon>
      </b-button>
    </b-navbar-nav>
  </b-navbar>
</template>

<script>
export default {
  name: 'UpNavBarComp',
  data: function () {
    return {
      loggedUsername: ''
    }
  },
  methods: {
    logOut: function () {
    }
  },
  mounted: function () {
    let returnLogin = true
    if ('authUser' in this.$store.state) {
      if (this.$store.state.isAuthenticated) {
        this.loggedUsername = this.$store.state.authUser.username
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
#upnavbar {
  background: var(--body-bg-dim);
}
</style>
