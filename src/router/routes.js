const routes = [
  {
    path: "",
    component: () => import("layouts/MainLayout.vue"),
    children: [
      {
        path: "",
        component: () => import("src/pages/Home.vue"),
      },
      {
        path: "/login",
        component: () => import("src/pages/Login.vue"),
      },
      {
        path: "/register",
        component: () => import("src/pages/Register.vue"),
      },
    ],
  },
  {
    path: "",
    component: () => import("layouts/AccountLayout.vue"),
    children: [
      {
        path: "/account",
        component: () => import("src/pages/Account.vue"),
        meta: { requiresAuth: true },
      },
      {
        path: "/account/info",
        component: () => import("src/pages/AccountInfo.vue"),
        meta: { requiresAuth: true },
      },
      {
        path: "/account/transactions",
        component: () => import("src/pages/Transactions.vue"),
        meta: { requiresAuth: true },
      },
      {
        path: "/account/payredirect",
        component: () => import("src/pages/PayApi.vue"),
        // meta: { requiresAuth: true },
      }
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: "/:catchAll(.*)*",
    component: () => import("pages/ErrorNotFound.vue"),
  },
];

export default routes;
