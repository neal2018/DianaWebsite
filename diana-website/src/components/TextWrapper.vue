<template>
    <div class="text-wrapper">
        <p>{{ msg }}</p>
    </div>
</template>
    
<script setup lang="ts">
import { defineProps } from "vue";
defineProps({
    msg: String,
});
</script>
    
<style scoped>
.text-wrapper {
    font-size: 25px;
    font-weight: bold;
    text-align: center;
    background-color: rgba(185, 154, 134, 0.6);
    color: rgba(45, 45, 45, 0.9);
    border: 1px solid #ccc;
    border-radius: 10px;
    height: 100px;
    width: 50%;
    margin: 20px auto;
    padding: 10px;
}
</style>
    