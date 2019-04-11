import Vue from 'vue'
import Router from 'vue-router'
import HomePage from '@/components/HomePage'
import LegalsPage from '@/components/LegalsPage'
import UserHomePage from '@/components/UserHomePage'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HomePage',
      component: HomePage
    }, {
      path: '/legals',
      name: 'LegalsPage',
      component: LegalsPage
    }, {
      path: '/u',
      name: 'UserHomePage',
      component: UserHomePage
    }
  ]
})
