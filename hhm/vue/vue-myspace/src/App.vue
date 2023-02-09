<template>
  <!-- <nav> // 原有导航栏
    <router-link to="/">Home</router-link> |
    <router-link to="/about">About</router-link>
  </nav> -->

<NavBar />

  <router-view/> <!-- 内容区域根据不同网址做一个分页展示 -->
</template>

<script>
import 'bootstrap/dist/css/bootstrap.css'; // 引入bootstrap样式
import 'bootstrap/dist/js/bootstrap'; // 引入bootstrap脚本

import NavBar from './components/NavBar'; // 由于每个页面都有导航栏，因此将导航栏组件导入到根组件

export default {
  name: "App",
  components: {
    NavBar,
  }
}

</script>


<style>

</style>
