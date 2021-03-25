<template>
  <div class="result-report">
    <p>平均匹配率为 {{ avgRate }}</p>
    <p v-if="avgRate <= 0.55">重复率比较低，再接再厉！</p>
    <p v-else>重复率有点高，要加油噢！</p>
  </div>
  <table class="result-table">
    <thead>
      <tr>
        <th>文字</th>
        <th>匹配率</th>
        <th>相似链接</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="temp in answer">
        <td class="td-words">{{ temp.words }}</td>
        <td
          class="td-rate"
          :style="'color:' + (parseFloat(temp.rate) > 0.7 ? 'red' : 'black') + ';'"
        >{{ temp.rate }}</td>
        <td v-if="temp.url !== 'No Pair'" class="td-link">
          <a :href="temp.url" target="_blank">链接地址</a>
        </td>
        <td v-else class="td-link">无相似链接</td>
      </tr>
    </tbody>
  </table>
</template>
    
<script setup lang="ts">
import { defineProps, computed } from "vue";
interface Answer {
  words: string,
  url: string,
  rate: string
}
const props = defineProps<{
  answer: Answer[]
}>();
ref: avgRate = computed(() => {
  if (props.answer.length == 0) {
    return 0;
  }
  const totalWeightedRate = props.answer.reduce(function(sum: number, object: Answer) {
    return sum + parseFloat(object.rate) * object.words.length;
  }, 0);
  const totalLength = props.answer.reduce(function(sum: number, object: Answer) {
    return sum + object.words.length;
  }, 0);
  return (totalWeightedRate / totalLength).toFixed(3);
})
</script>
    
<style scoped>
.result-report,
.result-table {
  background-color: rgba(255, 255, 255, 0.8);
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.4);
  color: rgba(45, 45, 45, 0.9);
  margin: 50px auto 100px auto;
  border: 1px solid #ccc;
  width: 75%;
}

.result-report {
  width: 75%;
  font-size: 20px;
  text-align: center;
}

.result-table {
  font-size: 18px;
  border-collapse: collapse;
}

.result-table th {
  font-size: 22px;
  padding: 10px;
}

.td-words {
  width: 50%;
  border-top: 1px solid rgb(14, 13, 13);
  padding: 10px;
}

.td-rate,
.td-link {
  width: 10%;
  text-align: center;
  border-top: 1px solid rgb(14, 13, 13);
  padding: 10px;
}

.td-link {
  width: 15%;
}
</style>
    