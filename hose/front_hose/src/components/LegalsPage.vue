<template>
  <div>
    Legal text:{{ this.legalText }}
  </div>
</template>

<script>
// eslint-disable-next-line
import axios from 'axios'

const urlBackend = 'http://127.0.0.1:8000'

export default {
  name: 'LegalsPage',
  data: function () {
    return {
      legalText: null
    }
  },
  methods: {
    getLegalText: function () {
      axios.get(urlBackend + '/legals/')
        .then(response => {
          this.legalText = response.data.data.legal_text
        })
        .catch(error => {
          console.error(error)
          console.error(JSON.stringify(error, null, 2))
        })
    }
  },
  mounted: function () {
    this.getLegalText()
  }
}
</script>

<style scoped>

</style>
