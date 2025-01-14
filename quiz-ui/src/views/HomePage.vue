<script setup>
import { ref, onMounted } from 'vue';
import quizApiService from "@/services/QuizApiService";
import scoreStorageService from '@/services/ScoreStorageService';

const registeredScores = ref([]);

onMounted(async () => {
		console.log("Home page mounted");
    registeredScores.value = scoreStorageService.getTopScores(5);
});
</script>

<style>
</style>

<template>
  <h1>Quiz Game</h1>

  <div>
    Meilleurs scores: 
    <div v-for="scoreEntry in registeredScores" v-bind:key="scoreEntry.date">
      {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
    </div>
  </div>

  <router-link to="/new-quiz">Démarrer le quiz !</router-link>
</template>