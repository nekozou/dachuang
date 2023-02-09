import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import UserListView from '../views/UserListView'
import UserProfileView from '../views/UserProfileView'
import LoginView from '../views/LoginView'
import RegisterView from '../views/RegisterView'
import NotFoundView from '../views/NotFoundView'


const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  // {
  //   path: '/about',
  //   name: 'about',
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  // }
  {
    path: '/userlist/',
    name: 'userlist',
    component: UserListView
  },
  {
    path: '/userprofile/:userId/', // userId是参数
    name: 'userprofile',
    component: UserProfileView
  },
  {
    path: '/login/',
    name: 'login',
    component: LoginView
  },  
  {
    path: '/register/',
    name: 'register',
    component: RegisterView
  },  
  {
    path: '/404/',
    name: '404',
    component: NotFoundView
  },
  // 正则表达式
  {
    path: '/:catchAll(.*)', // 匹配到任意字符串，类似else情况
    redirect: '/404/'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
