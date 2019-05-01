import Vue from 'vue'
import Router from 'vue-router'
import HomePage from '@/components/HomePage'
import LegalsPage from '@/components/LegalsPage'
import UserHomePage from '@/components/UserHomePage'
import HoseViewPage from '@/components/HoseViewPage'

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
      path: '/u/:username',
      name: 'UserHomePage',
      component: UserHomePage
    }, {
      path: '/h/:hoseid',
      name: 'HoseViewPage',
      component: HoseViewPage
    }
  ]
})
