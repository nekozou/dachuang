<template>
    <div class="card">
        <div class="card-body">
            <div class="row">
                <div class="col-3 img-field">
                    <img class="img-fluid" :src="user.photo" alt="">
                    <!-- img-fluid是bootstrap定义的默认样式，让图片能够自适应 -->
                </div>
                <div class="col-9">
                    <div class="username">{{  user.username }}</div>
                    <div class="fans">{{  user.followerCount }}</div>
                    <button @click="follow" v-if="!user.is_followed" type="botton" class="btn btn-secondary btn-sm">关注</button>
                    <button @click="unfollow" v-if="user.is_followed" type="botton" class="btn btn-secondary btn-sm">取消关注</button>
                    <!-- v-on:click用于绑定函数，常简写为@click -->
                </div>
            </div>
        </div>
    </div>
</template>
<!-- import { computed } from 'vue'; -->
<script>
// import { computed } from '@vue/runtime-core'
export default {
    name: "UserProfileInfo",
    props: { // 使用user，即使用父节点的数据
        user: {
            type: Object,
            required: true,
        },
    },
    setup(props, context) {
        // let fullName = computed(() => props.user.lastName + ' ' + p rops.user.firstName);

        // 定义关注函数
        const follow = () => {
            context.emit('follow');
        };

        const unfollow = () => {
            context.emit('unfollow'); // 触发父组件的某事件
        };

        return {
            // fullName,
            follow, // 必须要将函数返回给父组件
            unfollow,
        }
    }
}
</script>


<style scoped>
img {
    border-radius: 50%;
}

.username {
    font-weight: bold;

}

.fans {
    font-size: 12px;
    color: gray;
}

button {
    padding: 2px 4px;
    font-size: 12px;
}

.img-field {
    display: flex;
    flex-direction: column;
    justify-content: center;
}
</style>

