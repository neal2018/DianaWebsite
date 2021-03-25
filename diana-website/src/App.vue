<template>
  <div>
    <GitHubToken />
    <div class="form-wrapper">
      <form @submit.prevent="handleSubmit">
        <div class="content-input-wrapper">
          <textarea class="content-input" id="content" v-model="content" :placeholder="placeholder"></textarea>
        </div>
        <div class="button-wrapper">
          <button class="button" type="submit" :disabled="isDisable">查 重</button>
        </div>
      </form>
    </div>
    <TextWrapper v-if="isError" msg="网络错误，请重试" />
    <TextWrapper v-else-if="isTooLong" :msg="'太长了！目前只支持' + maxLength + '字以下'" />
    <TextWrapper v-else-if="isSendRequest && !isGetResponse" msg="查重中" />
    <ResultReport v-else-if="isSendRequest && isGetResponse" :answer="answer" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import GitHubToken from "./components/GitHubToken.vue"
import TextWrapper from "./components/TextWrapper.vue"
import ResultReport from "./components/ResultReport.vue"

interface Answer {
  words: string,
  url: string,
  rate: string
}

ref: content = ''
ref: answer = [] as Answer[]
ref: isSendRequest = false
ref: isGetResponse = false
ref: isError = false
ref: isTooLong = false

const placeholder = `这个冬天真冷，窗外的大雪飞扬，像是要吹灭街上的光。但是看着嘉然跳跳唱唱，处刑大家的小作文，再被写给晚晚的小作文处刑，我觉得有股热流在身体里流淌，紧绷的立毛肌都舒展开来了。

当初在嘉然出现时，有人警告说雪崩时没有一片雪花是无辜的。但我现在想如果是落到嘉然的怀里，再冷的雪也会融化的吧。

可是我没有落到她的怀里，而是落到她的手心了。

我对然然的表演傻笑，旁边脸被冻得发红的妹妹问我，还有哪个冬天比这个更冷吗？

我突然很害怕。我知道，没有嘉然的冬天才是最冷的。

更让人难过的是我没有妹妹，但这个冬天迟早会来。`

const maxLength = 600

ref: isDisable = computed(() => isSendRequest && !isGetResponse && !isError)
const handleSubmit = async (e: Event) => {
  e.preventDefault()
  isError = false
  isSendRequest = true
  isGetResponse = false
  isTooLong = false

  if (content === '') {
    content = placeholder
  }
  if (content.length > maxLength) {
    isTooLong = true
    isGetResponse = true
    return
  }
  try {
    let response = await fetch('https://118.25.75.14:8888/check', {
      method: 'POST',
      body: JSON.stringify({ "content": content })
    })

    if (response.status == 200) {
      answer = await response.json()
      isGetResponse = true
      console.log(answer)
    } else {
      isError = true
    }
  }
  catch (err) {
    isError = true
  }
}
</script>

<style>
body {
  background-image: url("./src/assets/diana_celebrate.jpg");
  margin: 0;
  font-family: "Microsoft YaHei", "Heiti SC", "黑体", "Arial", sans-serif;
}

.form-wrapper {
  padding: 100px 0px 0px 0px;
}

.button-wrapper {
  text-align: center;
}

.button {
  margin: 30px;
  background-color: #b95e63;
  border-radius: 10px;
  font-size: 30px;
  width: 160px;
  height: 60px;
  color: #fde4dd;
  box-shadow: inset 0 -0.6em 1em -0.35em rgba(0, 0, 0, 0.17),
    inset 0 0.6em 2em -0.3em rgba(247, 160, 160, 0.15),
    inset 0 0 0em 0.05em rgba(255, 255, 255, 0.12);
  text-align: center;
  cursor: pointer;
}

.button:disabled {
  background-color: #fff;
  cursor: not-allowed;
}

.content-input-wrapper {
  padding: 30px 0;
}

.content-input {
  display: block;
  font-size: 20px;
  width: 75%;
  height: 500px;
  margin: 0px auto;
  padding: 10px;
  letter-spacing: 1px;
  line-height: 1.5;
  border-radius: 5px;
  border: 1px solid #ccc;
  background-color: rgba(255, 255, 255, 0.9);
  box-shadow: 1px 1px 1px #999;
  outline: none;
  overflow: auto;
}
</style>