// import { route } from 'quasar/wrappers'
// import { createRouter, createMemoryHistory, createWebHistory, createWebHashHistory } from 'vue-router'
// import routes from './routes'
// import { useAuthStore } from 'src/stores/auth';

// /*
//  * If not building with SSR mode, you can
//  * directly export the Router instantiation;
//  *
//  * The function below can be async too; either use
//  * async/await or return a Promise which resolves
//  * with the Router instance.
//  */

// export default route(function (/* { store, ssrContext } */) {
//   const createHistory = process.env.SERVER
//     ? createMemoryHistory
//     : (process.env.VUE_ROUTER_MODE === 'history' ? createWebHistory : createWebHashHistory)

//   const Router = createRouter({
//     scrollBehavior: () => ({ left: 0, top: 0 }),
//     routes,
//     history: createHistory(process.env.VUE_ROUTER_BASE),routes
//   })

//   Router.beforeEach((to, from, next) => {
//     const authStore = useAuthStore();
//     const isAuthenticated = authStore.isAuthenticated || !!localStorage.getItem('token');

//     if (to.name === 'home' && isAuthenticated) {
//       next({ name: 'account', replace: true });
//     } else if (to.name === 'account' && !isAuthenticated) {
//       next({ name: 'home', replace: true });
//     } else if (to.name === 'login' && isAuthenticated) {
//       next({ name: 'account', replace: true });
//     } else {
//       next();
//     }
//   });


//   return Router
// })

import { route } from 'quasar/wrappers'
import { createRouter, createMemoryHistory, createWebHistory, createWebHashHistory } from 'vue-router'
import routes from './routes'
import { useAuthStore } from 'src/stores/auth';

export default route(function (/* { store, ssrContext } */) {
  const createHistory = process.env.SERVER
    ? createMemoryHistory
    : (process.env.VUE_ROUTER_MODE === 'history' ? createWebHistory : createWebHashHistory)

  const Router = createRouter({
    scrollBehavior: () => ({ left: 0, top: 0 }),
    routes,
    history: createHistory(process.env.VUE_ROUTER_BASE)
  })

  Router.beforeEach((to, from, next) => {
    const authStore = useAuthStore();
    const isAuthenticated = authStore.isAuthenticated || !!localStorage.getItem('token');

    if (to.matched.some(record => record.meta.requiresAuth)) {
      if (!isAuthenticated) {
        next({ name: 'login', replace: true });
      } else {
        next();
      }
    } else if (to.name === 'login' && isAuthenticated) {
      next({ name: 'account', replace: true });
    } else if (to.name === 'home' && isAuthenticated) {
      next({ name: 'account', replace: true });
    } else {
      next();
    }
  })

  return Router
})

