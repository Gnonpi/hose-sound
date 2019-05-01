<template>
  <b-navbar id="upnavbar">
    <b-navbar-brand :href="'/u/' + loggedUsername" class="ml-0">
      <img src="/static/favicon.ico" class="d-inline-block align-top" alt="logo">
    </b-navbar-brand>
    <b-navbar-brand>
      <h2>
        <router-link
          id="link-back-user"
          :to="{
            name: 'UserHomePage',
            params: {
              username: loggedUsername,
              userId: loggedUserId}
        }">
          {{ loggedUsername }}
        </router-link>
      </h2>
    </b-navbar-brand>
    <b-navbar-nav class="ml-auto">
      <b-button>
        <unicon name="sliders-v" fill="white"></unicon>
      </b-button>
      &nbsp;
      <b-button @click="logOut">
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
      loggedUsername: '',
      loggedUserId: ''
    }
  },
  methods: {
    logOut: function () {
      console.log('Logging out')
      this.$store.commit('logoutUser')
      this.$router.push({name: 'HomePage'})
    }
  },
  mounted: function () {
    let returnLogin = true
    if ('authUser' in this.$store.state) {
      if (this.$store.state.isAuthenticated) {
        this.loggedUsername = this.$store.state.authUser.username
        this.loggedUserId = this.$store.state.authUser.userId
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
