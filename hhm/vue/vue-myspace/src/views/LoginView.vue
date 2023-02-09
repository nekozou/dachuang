<template>
  <ContentBase>
    <div class="row justify-content-md-center">
      <div class="col-3"> <!-- 一共12列，占3列 -->
        <form @submit.prevent="login">
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
          <!-- 报错信息 -->
          <div class="error-message">{{ error_message }}</div>
          <button type="submit" class="btn btn-primary">登录</button>
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


export default {
  name: 'LoginView',
  components: {
    // HelloWorld
    ContentBase,
  },
  setup() {
    const store = useStore();
    let username = ref('');
    let password = ref('');
    let error_message = ref('');

    const login = () => { // 登录按钮函数
      error_message = ""; // 每次登录先清空error_message
      store.dispatch("login", {
        username: username.value,
        password: password.value,

        success() {
          // 成功则实现跳转
          router.push({name: 'userlist'});
        },
        error() {
          error_message.value = "用户名或密码错误";
        },
      })
    }

    return {
      username: username,
      password: password,
      error_message,
      login,
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