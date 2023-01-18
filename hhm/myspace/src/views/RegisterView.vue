<template>
  <ContentBase>
    <div class="row justify-content-md-center">
      <div class="col-3"> <!-- 一共12列，占3列 -->
        <form @submit.prevent="register">
          <!-- 执行完我们定义的login函数之后，会执行默认事件，通常我们使用:prevent 来阻止 -->
          <!-- 组件间进行交流，一般是需要追溯到祖宗组件，然后更改数据，在找到对应组件来交流，过程太过于麻烦 -->
          <!-- 使用vuex来存储全局变量，vuex维护了一棵状态数，每个子组件和vuex状态树进行沟通就好 -->
          <!-- vuex创建的对象在store/index.js中 -->
          <div class="mb-3">
            <label for="username" class="form-label">用户名</label>
            <input v-model="username" type="text" class="form-control" id="username">
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">密码</label>
            <input v-model="password" type="password" class="form-control" id="password">
          </div>
          <div class="mb-3">
            <label for="password_confirm" class="form-label">确认密码</label>
            <input v-model="password_confirm" type="password" class="form-control" id="password_confirm">
          </div>
          <!-- 报错信息 -->
          <div class="error-message">{{ error_message }}</div>
          <button type="submit" class="btn btn-primary">注册</button>
        </form>
      </div>
    </div>
  </ContentBase>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from '@/components/HelloWorld.vue'
import ContentBase from '../components/ContentBase';
import { ref } from 'vue';
import { useStore } from 'vuex';
import router from '@/router/index';
import $ from 'jquery';


export default {
  name: 'RegisterView',
  components: {
    // HelloWorld
    ContentBase,
  },
  setup() {
    const store = useStore();
    let username = ref('');
    let password = ref('');
    let password_confirm = ref('');
    let error_message = ref('');

    console.log(store, router);

    const register = () => { 
      error_message = ""; // 每次登录先清空error_message
      $.ajax({
        url: "https://app165.acapp.acwing.com.cn/myspace/user/",
        type: "POST",
        data: {
          username: username.value,
          password: password.value,
          password_confirm: password_confirm.value,
        },
        success(resp) {
          console.log(resp); 
        }
      });
    }

    return {
      username: username,
      password: password,
      password_confirm: password_confirm,
      error_message,
      register,
    }
  }
}
</script>

<style scoped>
button {
  width: 100%;
}

.error-message {
  color: red;
  font-weight: bold;
}
</style>