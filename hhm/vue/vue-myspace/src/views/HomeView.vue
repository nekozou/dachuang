<template>
  <ContentBase>
    首页
  </ContentBase>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from '@/components/HelloWorld.vue'

import ContentBase from '../components/ContentBase'; // 引入Content组件

export default {
  name: 'HomeView',
  components: {
    // HelloWorld
    ContentBase,
  }
}
</script>

<style scoped>
.container {
  margin-top: 20px;
}
</style>
