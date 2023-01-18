<!-- 这个组件是页面最顶层的组件，因此一般将数据存到这里
 -->
<template>
  <ContentBase>
    <div class="row">
      <!-- 相当于将一个页面分为22分，class是bootstrap默认class，表示第几列 -->
      <div class="col-3">
        <UserProfileInfo @follow="follow" @unfollow="unfollow" :user="user" />
        <!-- :是v-bind的缩写，将这个组件绑定一个属性 -->
        <!-- 子组件向父组件传递信息，需要先绑定事件，通过触发父组件绑定事件来修改数据 -->

        <UserProfileWrite @post_a_post="post_a_post"/>
      </div>
      <div class="col-9">
        <UserProfilePosts :posts="posts" />
        <!-- posts为reactive类型变量，当posts更新时，会被重新渲染 -->
      </div>
        
    </div>
  </ContentBase>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from '@/components/HelloWorld.vue'
import ContentBase from '../components/ContentBase';
import UserProfileInfo from '../components/UserProfileInfo';
import UserProfilePosts from '../components/UserProfilePosts';
import UserProfileWrite from '../components/UserProfileWrite';
import { reactive } from 'vue';
import { useRoute } from 'vue-router';
import $ from 'jquery'; 
import { useStore } from 'vuex';

export default { // 导出组件
  name: 'UserProfileView',
  components: {
    // HelloWorld
    ContentBase,
    UserProfileInfo,
    UserProfilePosts,
    UserProfileWrite,
  },
  setup: () => { // 初始化变量，函数
    const store = useStore();
    const route = useRoute();
    const userId = route.params.userId;


     const user = reactive ({});

     const posts = reactive({});

     $.ajax({
      url: "https://app165.acapp.acwing.com.cn/myspace/getinfo/",
      type: "GET",
      data: {
        user_id: userId,

      },
      headers: {
        'Authorization' : "Bearer " + store.state.user.access,
      },
      success(resp) {
        user.id = resp.id;
        user.username = resp.username;
        user.photo = resp.photo;
        user.followerCount = resp.followerCount;
        user.is_followed = resp.is_followed;
      },

     });

     $.ajax({
      url: "https://app165.acapp.acwing.com.cn/myspace/post/",
      type: "GET",
      data: {
        user_id: userId,

      },
      headers: {
        'Authorization': "Bearer " + store.state.user.access,
      },
      success(resp) {
        posts.posts=resp;
      }
     });

     const follow = () => { // follow事件
        if (user.is_followed) return ;
        user.is_followed = true;
        user.followerCount ++;
     };

     const unfollow = () => {
        if (!user.is_followed) return ;
        user.is_followed = false;
        user.followerCount --;
     };

     const post_a_post = (content) => {
        posts.count ++;
        posts.posts.unshift({
          id: posts.count,
          userId: 1,
          content: content,
        })
     }


     return {
      user: user,
      follow,
      unfollow,
      posts, // 想用什么数据就将什么数据返回，返回了才能在前面的html中调用
      post_a_post,
     }
  }
}
</script>

<style scoped>

</style>