<template>
<!-- 引入bootstrap导航栏样式 -->
<nav class="navbar navbar-expand-lg bg-body-tertiary">
  <div class="container">
    <router-link class="navbar-brand" :to="{name: 'home'}">Myspace</router-link>
    <!-- 意思是将这个页面调到home对应的路由页面里面 -->
    <!-- router-link 本质上也是a标签，只不过里面有特殊属性，vue中给某个标签绑定属性用': + 名称' -->
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarText" aria-controls="navbarText" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarText">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <li class="nav-item">
          <router-link class="nav-link active" :to="{name: 'home'}">首页</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" :to="{name: 'userlist'}">好友列表</router-link>
        </li>
      </ul>
      <ul class="navbar-nav" v-if="!$store.state.user.is_login">
        <li class="nav-item">
          <router-link class="nav-link active" :to="{name: 'login'}">登录</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" :to="{name: 'register'}">注册</router-link>
        </li>
      </ul>
      <ul class="navbar-nav" v-if="$store.state.user.is_login">
        <li class="nav-item">
          <router-link class="nav-link active" :to="{name: 'userprofile', params: {userId: $store.state.user.id}}">{{ $store.state.user.username }}</router-link>
        </li>
        <li class="nav-item">
          <a class="nav-link" style="cursor: pointer" @click="logout">退出</a>
        </li>
      </ul>
      
    </div>
  </div>
</nav>

</template>


<script>

import { useStore } from 'vuex';

// 将这个组件导出
export default {
    name: "NavBar",
    setup() {
      const store = useStore();
      const logout = () => {
        store.commit('logout');
      };

      return {
        logout,
      }
    }
}
</script>



<style scoped> /* scoped保证组件间css选择器不会相互影响 */


</style>