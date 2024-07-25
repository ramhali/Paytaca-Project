// const routes = [
//   {
//     path: "",
//     component: () => import("layouts/MainLayout.vue"),
//     children: [
//       {
//         path: "",
//         component: () => import("src/pages/Home.vue"),
//       },
//       {
//         path: "/login",
//         component: () => import("src/pages/Login.vue"),
//       },
//       {
//         path: "/register",
//         component: () => import("src/pages/Register.vue"),
//       },
//     ],
//   },
//   {
//     path: "",
//     component: () => import("layouts/AccountLayout.vue"),
//     children: [
//       {
//         path: "/account",
//         component: () => import("src/pages/Account.vue"),
//         meta: { requiresAuth: true },
//       },
//       {
//         path: "/account/info",
//         component: () => import("src/pages/AccountInfo.vue"),
//         meta: { requiresAuth: true },
//       },
//       {
//         path: "/account/transactions",
//         component: () => import("src/pages/Transactions.vue"),
//         meta: { requiresAuth: true },
//       }
//       ,
//       {
//         path: "/account/setup",
//         component: () => import("src/pages/Setup.vue"),
//         meta: { requiresAuth: true },
//       }
//     ]
//   },
//   {
//     path: "",
//     component: () => import("layouts/PayLayout.vue"),
//     children: [
//       {
//         path: "/pay/payredirect",
//         component: () => import("src/pages/PayApi.vue"),
//         // meta: { requiresAuth: true },
//       },
//       {
//         path: "/pay/",
//         component: () => import("src/pages/Pay.vue"),
//         // meta: { requiresAuth: true },
//       }
//     ],
//   },

//   // Always leave this as last one,
//   // but you can also remove it
//   {
//     path: "/:catchAll(.*)*",
//     component: () => import("pages/ErrorNotFound.vue"),
//   },
// ];

// export default routes;

const routes = [
  {
    path: "",
    component: () => import("layouts/MainLayout.vue"),
    children: [
      {
        path: "",
        name: "home",
        component: () => import("src/pages/Home.vue"),
      },
      {
        path: "/login",
        name: "login",
        component: () => import("src/pages/Login.vue"),
      },
      {
        path: "/register",
        name: "register",
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
        name: "account",
        component: () => import("src/pages/Account.vue"),
        meta: { requiresAuth: true },
      },
      {
        path: "/account/info",
        name: "account-info",
        component: () => import("src/pages/AccountInfo.vue"),
        meta: { requiresAuth: true },
      },
      {
        path: "/account/transactions",
        name: "transactions",
        component: () => import("src/pages/Transactions.vue"),
        meta: { requiresAuth: true },
      },
      {
        path: "/account/setup",
        name: "setup",
        component: () => import("src/pages/Setup.vue"),
        meta: { requiresAuth: true },
      },
    ],
  },
  {
    path: "",
    component: () => import("layouts/PayLayout.vue"),
    children: [
      {
        path: "/pay/payredirect",
        name: "payredirect",
        component: () => import("src/pages/PayApi.vue"),
        // meta: { requiresAuth: true },
      },
      {
        path: "/pay/",
        name: "pay",
        component: () => import("src/pages/Pay.vue"),
        // meta: { requiresAuth: true },
      },
      {
        path: "/test/",
        name: "test",
        component: () => import("src/pages/Test.vue"),
      },
    ],
  },
  {
    path: "/:catchAll(.*)*",
    name: "notfound",
    component: () => import("pages/ErrorNotFound.vue"),
  },
];

export default routes;
