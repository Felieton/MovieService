import Vue from 'vue'
import VueRouter from 'vue-router'
import routes from "./routes";
import store from "@/store";
import {GROUPS_ACCESS} from "@/store/group_types";

Vue.use(VueRouter)

const router = new VueRouter({
  scrollBehavior() {
    return { x: 0, y: 0 };
  },
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

/*
 * Routes auth control
 * meta: {
 *   authRequired: true/false,
 *   authGroupRequired: group_name
 * }
 */
router.beforeEach( (to, from, next) => {
  if (to.matched.some(record => record.meta.authRequired)) {
    if (!store.getters.isAuthenticated) {
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
    }
    else {
      const requiredGroup = to.matched.reduce( (prev, current) => {
        return (
            GROUPS_ACCESS[prev.meta.authGroupRequired] >= GROUPS_ACCESS[current.meta.authGroupRequired]
        ) ? prev : current
      }).meta.authGroupRequired

      // it does not ensure that every misconfiguration will be reported!
      if (!(requiredGroup in GROUPS_ACCESS)) {
        next(new Error(
            'Routes meta data misconfiguration. ' +
            `Argument authGroupRequired "${requiredGroup}" is invalid`
        ))
      }
      else if (requiredGroup && !store.getters.loggedUserHasGroup(requiredGroup)) {
        next(new Error('Access denied'))
      }
      else next()
    }
  }
  else {
    next()
  }
})

export default router
