import $ from 'jquery';
import jwt_decode from 'jwt-decode';

const ModuleUser = {
    state: { // 存储数据
      id: "",
      username: "",
      photo: "",
      followerCount: 0,
      access: "",
      refresh: "",
      is_login: false,

    },
    getters: { // 存储一些需要计算的数据
    },
    mutations: { // 放置修改state的操作
        updateUser(state, user) {
          state.id = user;
          state.username = user.username;
          state.photo = user.photo;
          state.followerCount = user.followerCount;
          state.access = user.access;
          state.refresh = user.refresh;
          state.is_login = user.is_login;
        },
        updateAccess(state, access) {
          state.access = access;
        },
        logout(state) { // 登出则将数据清空
          state.id = "";
          state.username = "";
          state.photo = "";
          state.followerCount = 0;
          state.access = "";
          state.refresh = "";
          state.is_login = false;
        }
    },
    actions: { // 定义对state的各种操作
        login(context, data) { // context是api，data是数据
          $.ajax({
            url: "https://app165.acapp.acwing.com.cn/api/token/",
            type: "POST",
            data: {
              username: data.username,
              password: data.password,
              
            },
            success(resp) {
              const {access, refresh} = resp;
              const access_obj = jwt_decode(access);

              // 每隔五分钟获取一次令牌
              setInterval(() => {
                $.ajax({
                  url: "https://app165.acapp.acwing.com.cn/api/token/refresh/",
                  type: "POST",
                  data: {
                    refresh,
                  },
                  success(resp) {
                    context.commit('updateAccess', resp.access);
                  }
                })
              }, 4.5 * 60 * 1000);
              $.ajax({
                url: "https://app165.acapp.acwing.com.cn/myspace/getinfo/",
                type: "GET",
                data: {
                    user_id: access_obj.user_id
                },
                headers: {
                    'Authorization': "Bearer " + access,
                },
                success(resp) {
                    context.commit("updateUser", {
                      ...resp,
                      access: access,
                      refresh: refresh,
                      is_login: true,
                    });
                    data.success();
                },
              })
            },
            error() {
              data.error();
            }
          });
        },
    },
    modules: { // 对state进行分割，单独维护某个state数据
    },
};

export default ModuleUser;