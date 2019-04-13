<template>
  <div id="global-home">
    <div>
      <a href="/">
        <img type="image/png" id="img-banner" src="/static/banner.png" alt="banner">
      </a>
      <nav class="nav nav-pills nav-fill">
        <a class="nav-link" href="/signup">
          <button type="button" class="btn btn-secondary">
            Share music now
          </button>
        </a>
        <a class="nav-link" href="/">
          <button type="button" class="btn btn-secondary">
            About Hose
          </button>
        </a>
        <router-link to="/legals/">
          <button type="button" class="btn btn-secondary">
            Legal Stuff
          </button>
        </router-link>
      </nav>
    </div>

    <main>
      <LoginComp></LoginComp>
      <hr>
      <RegisterComp></RegisterComp>
    </main>
  </div>
</template>

<script>
import RegisterComp from './RegisterComp.vue'
import LoginComp from './LoginComp.vue'

export default {
  name: 'HomePage',
  components: {LoginComp, RegisterComp},
  data: function () {
    return {
    }
  },
  methods: {
    doStuff: function () {
      console.log('lol')
    }
  }
}
</script>

<style scoped>

</style>
