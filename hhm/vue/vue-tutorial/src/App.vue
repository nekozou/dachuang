<!-- App.vue文件 -->
<template>
<div id="app">
  <form >
    <input v-model="newTodo">
    <button>Add Todo</button>
  </form>
  <ul>
    <li v-for="todo in todos" :key="todo.id">
      {{ todo.text }}
      <button @click="removeTodo(todo)">X</button>
    </li>
  </ul>
</div>
</template>



<script>
import { ref } from 'vue';
export default {
  setup() {
    let id = 0; // 给每个对象一个id

    const newTodo = ref('');
    const todos = ref([
      {id: id++, text: "Learn HTML"},
      {id: id++, text: "Learn JavaScript"},
      {id: id++, text: "Learn Vue"},
    ]);

    const addTodo = () => {
      todos.value.push({id: id++, text: newTodo.value});
      newTodo.value = "";
    };

    const removeTodo = (todo) => {
      todos.value = todos.value.filter((t) => t !== todo);
    };
    return {
      id,
      todos,
      newTodo,
      addTodo,
      removeTodo,
    }
  }
}
</script>

<style>

</style>
