<template>
  <img v-if="currentQuestion.image" :src="currentQuestion.image" alt="Question Image"/>
  <p>{{ currentQuestion.title }}</p>
  <p>{{ currentQuestion.text }}</p>
  <ul>
    <li v-for="(answer, index) in currentQuestion.possibleAnswers" :key="index">
      <a @click="emit('click-on-answer', { answer, index })">{{ answer.text }}</a>
    </li>
  </ul>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
  currentQuestion: Object
});

const emit = defineEmits(['click-on-answer']);
</script>

<style>
img {
  max-width: 50%;
  height: auto;
}
</style>