<template>
  <div class="card" style="width: 30rem;">
    <div class="card-body">
      <label class="label-class">时间: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<progress :value="elapsed / duration"></progress></label>

      <div class="time-class">{{ (elapsed / 1000).toFixed(1) }}s</div>

      <div class="label-class">
        计时长度:  <input type="range" v-model="duration" min="1" max="30000">
        {{ (duration / 1000).toFixed(1) }}s
      </div>

      <button  type="button" class="btn btn-primary" @click="elapsed = 0">Reset</button>
    </div>
  </div>
</template>

<script>
import { ref, onUnmounted } from 'vue'
import 'bootstrap/dist/css/bootstrap.css'; // 引入bootstrap样式
import 'bootstrap/dist/js/bootstrap'; // 引入bootstrap脚本

export default {

  setup() {
    const duration = ref(15 * 1000)
    const elapsed = ref(0)

    let lastTime = performance.now()
    let handle
    const update = () => {
      const time = performance.now()
      elapsed.value += Math.min(time - lastTime, duration.value - elapsed.value)
      lastTime = time
      handle = requestAnimationFrame(update)
    }

    update()
    onUnmounted(() => {
      cancelAnimationFrame(handle)
    })

    return {
      duration,
      elapsed
    }
  }
}
</script>

<style>
.card {
  margin: 0 auto;
  width: 300px;
  height: 200px;
}
.button-class {
  margin-top: 20px;
  margin-left: 140px;
}
.label-class {
  margin-left: 70px;
}

.time-class {
  margin-left: 122px;
}
.btn-primary {
  margin-top:10px;
  margin-left: 160px;
}
</style>
