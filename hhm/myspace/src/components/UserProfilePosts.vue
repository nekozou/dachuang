<template>
    <div class="card">
        <div class="card-body">
            <!-- v-for就是循环，对于posts中的每一个post，我都构造一个div，每个子单元都需要用:key绑定一个key属性，保证其唯一 -->
            <div v-for="post in posts.posts" :key="post.id"> <!-- posts对象有count和posts两个值 -->
                <div class="card single-post">
                    <div class="card-body">
                        {{ post.content }}
                    </div>
                </div>
            </div>
            
        </div>
    </div>

</template> 

<script>
export default {
    name: "UserProfilePosts",
    props: {
        posts: {
            type: Object, // 类型
            required: true, // 表示必须传过来
            
        },
    },
}
</script>


<style scoped>
.single-post {
    margin-top: 10px;
}
</style>