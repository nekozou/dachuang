<template>
  <div class="home">
    <!-- <img alt="Vue logo" src="../assets/logo.png"> -->
    <!-- <HelloWorld msg="Welcome to Your Vue.js App"/> -->

    <!-- 下面是首页卡片样式，由于太靠左，用container将其包起来，container是bootstrap定义好的class，可以让我们响应式调整中间内容区域大小 -->
    <div class="container">
      <div class="card">
        <!-- <img src="..." class="card-img-top" alt="..."> // 图片 -->
        <div class="card-body">
          <slot></slot> <!-- 将Content组件所有子元素全部渲染到slot里面 -->
        </div>
      </div>
    </div>

  </div>
</template>


<script>
export default {
    name: "ContentBase",
}
</script>


<style>
.container {
  margin-top: 20px;
}
</style>