<script setup>
import { ref, onMounted } from 'vue';
import { RouterLink } from 'vue-router';
import participationStorageService from "@/services/ParticipationStorageService";
import scoreStorageService from '@/services/ScoreStorageService';

// Récupération des données du joueur et de son score
const player = participationStorageService.getPlayerName();
const score = participationStorageService.getParticipationScore();
const registeredScores = ref([]);
const classement = ref('');

// Effectuer l'enregistrement et la récupération des scores lors du montage du composant
onMounted(async () => {
  // Sauvegarde du score du joueur
  await scoreStorageService.saveScore(player, score);
  console.log("score rentré : " + score);

  // Récupération des meilleurs scores (top 5)
  registeredScores.value = scoreStorageService.getTopScores(5);

  // Récupération du classement du joueur
  classement.value = scoreStorageService.getPlayerRank(player);
});
</script>

<template>
  <div class="container">
    <h1 class="player-name">
      {{ player }}
    </h1>
    <div class="score-section">
      <p>Ton score : <span class="score">{{ score }}</span></p>
    </div>
    <div class="top-scores-section">
      <h2>Meilleurs scores :</h2>
      <ul>
        <li v-for="scoreEntry in registeredScores" :key="scoreEntry.date">
          <span class="score-player">{{ scoreEntry.playerName }}</span> - <span class="score-value">{{ scoreEntry.score }}</span>
        </li>
      </ul>
    </div>
    <div class="ranking-section">
      <p>Ton classement : <span class="ranking">{{ classement }}</span></p>
    </div>
    <nav class="navigation">
      <RouterLink to="/" class="nav-link">Retour à l'accueil</RouterLink>
    </nav>
  </div>
</template>

<style scoped>
/* Styles globaux */
body {
  font-family: 'Arial', sans-serif;
  background-color: #1e1e1e;
  color: #ffffff;
  margin: 0;
  padding: 0;
}

/* Conteneur principal */
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 2rem;
}

/* Nom du joueur */
.player-name {
  font-size: 2.5rem;
  font-weight: bold;
  color: #43d17a;
  margin-bottom: 1rem;
}

/* Section du score */
.score-section p {
  font-size: 1.8rem;
  margin: 1rem 0;
}

.score {
  font-weight: bold;
  color: #43d17a;
}

/* Section des meilleurs scores */
.top-scores-section {
  margin: 2rem 0;
}

.top-scores-section h2 {
  font-size: 1.8rem;
  color: #ffffff;
  margin-bottom: 1rem;
}

.top-scores-section ul {
  list-style: none;
  padding: 0;
}

.top-scores-section li {
  font-size: 1.2rem;
  margin: 0.5rem 0;
}

.score-player {
  color: #43d17a;
  font-weight: bold;
}

.score-value {
  color: #ffffff;
}

/* Section du classement */
.ranking-section p {
  font-size: 1.8rem;
  margin: 1rem 0;
}

.ranking {
  font-weight: bold;
  color: #43d17a;
}

/* Navigation */
.navigation {
  margin-top: 2rem;
}

.nav-link {
  font-size: 1.2rem;
  color: #43d17a;
  text-decoration: none;
  font-weight: bold;
  transition: color 0.3s ease;
}

.nav-link:hover {
  color: #ffffff;
}
</style>
