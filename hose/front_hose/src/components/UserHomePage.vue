<template>
  <div>
    User home page: {{ username }}
  </div>
</template>

<script>
import axios from 'axios'

const urlBackend = 'http://localhost:8000'

export default {
  name: 'UserHomePage',
  data: function () {
    return {
      username: ''
    }
  },
  methods: {
    getUserInfo: function () {
      axios.get(urlBackend + '/user/browse-hosers/', {
      })
        .then(response => {
          console.log(response.data)
        })
        .catch(error => {
          console.debug('Error')
          console.debug(error)
          console.debug(JSON.stringify(error, null, 2))
        })
    }
  }
}
</script>

<style scoped>

</style>
