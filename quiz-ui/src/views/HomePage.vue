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

<style scoped>
/* Styles généraux */
body {
  font-family: 'Arial', sans-serif;
  background-color: #1e1e1e; /* Fond sombre */
  color: #ffffff; /* Texte blanc */
  margin: 0;
  padding: 0;
}

/* Conteneur principal */
.container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh; /* Hauteur de la fenêtre */
  text-align: center;
}

/* Titre principal */
.title {
  font-size: 4rem;
  font-weight: bold;
  color: #43d17a; /* Couleur verte */
  margin-bottom: 2rem;
}

/* Section des scores */
.scores {
  background-color: #2a2a2a; /* Fond sombre pour la section */
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
  width: 80%;
  max-width: 600px;
  margin-bottom: 2rem;
}

.scores h2 {
  font-size: 2rem;
  margin-bottom: 1rem;
  color: #ffffff;
}

.scores div {
  font-size: 1.5rem;
  margin: 0.5rem 0;
  color: #cccccc;
}

/* Bouton démarrer le quiz */
.start-quiz {
  padding: 0.75rem 2rem;
  font-size: 1.5rem;
  font-weight: bold;
  background-color: #43d17a;
  color: #1e1e1e;
  text-decoration: none;
  border-radius: 5px;
  transition: all 0.3s ease-in-out;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
}

.start-quiz:hover {
  background-color: #1e1e1e;
  color: #43d17a;
  border: 2px solid #43d17a;
  transform: scale(1.05);
}
</style>

<template>
  <div class="container">
    <!-- Titre principal -->
    <h1 class="title">Quiz Game</h1>

    <!-- Section des scores -->
    <div class="scores">
      <h2>Meilleurs scores</h2>
      <div v-if="registeredScores.length === 0">Aucun score enregistré pour le moment.</div>
      <div v-for="scoreEntry in registeredScores" v-bind:key="scoreEntry.date">
        {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
      </div>
    </div>

    <!-- Bouton démarrer le quiz -->
    <router-link to="/new-quiz" class="start-quiz">Démarrer le quiz !</router-link>
  </div>
</template>
