<template>
    <div class="card">
        <div class="card-body edit-field">
            <label for="edit-post" class="form-label">编辑帖子</label>
            <textarea v-model="content" class="form-control" id="exampleFormControlTextarea1" rows="3"></textarea>
            <!-- v-model的意思将textarea的内容和content绑定起来 -->
            <button @click="post_a_post" type="button" class="btn btn-primary btn-sm">发帖</button>
        </div>
    </div>
</template>


<script>
import { ref } from 'vue';

export default {
    name: "UserProfileWrite",
    setup(props, context) {
        let content = ref(''); // 只是一个变量，而不是对象，因此可以使用ref，reactive必须要是对象

        const post_a_post = () => {
            context.emit('post_a_post', content.value);
            content.value = "";
        }

        return {
            content: content, // 实际上由于key和value一致，写成content也行
            post_a_post,
        }
    }
}
</script>


<style scoped>
.edit-field {
    margin-top: 20px;
}

button {
    margin-top: 10px;
}
</style>