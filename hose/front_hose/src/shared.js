export default {
  verifyIsLogged: function (component) {
    let returnLogin = true
    if ('authUser' in component.$store.state) {
      if (component.$store.state.isAuthenticated) {
        returnLogin = false
      } else {
        console.debug('User not auth')
      }
    } else {
      console.debug('authUser not in state')
    }
    if (returnLogin) {
      console.log('Going back to login')
      component.$router.push({name: 'HomePage'})
    }
    return returnLogin
  },
  formatDate: function (date) {
    let options = {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    }
    return date.toLocaleString('en-UK', options)
  }
}
