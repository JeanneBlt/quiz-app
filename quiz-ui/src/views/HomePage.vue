<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

// Déclaration de la variable réactive qui stockera les scores
const registeredScores = ref([]);

// Fonction pour récupérer les meilleurs scores
const fetchTopScores = async () => {
  try {
    const response = await axios.get('http://localhost:5000/quiz-info'); // Remplace par ton URL API

    // Vérifie si l'API renvoie bien une liste de scores
    if (response.data.scores && Array.isArray(response.data.scores)) {
      // Trie les scores du plus haut au plus bas et garde les 5 meilleurs
      registeredScores.value = response.data.scores
        .sort((a, b) => b.score - a.score) // Tri décroissant
        .slice(0, 5); // Sélection des 5 meilleurs
    } else {
      console.error("Format de réponse inattendu :", response.data);
    }
  } catch (error) {
    console.error("Erreur lors de la récupération des scores:", error);
  }
};

// Charger les scores au montage du composant
onMounted(fetchTopScores);
</script>



<style scoped>
/* Conteneur principal */
.container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
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
  background-color: #2a2a2a; /* Fond sombre */
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

.score-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 1.5rem;
  margin: 0.5rem 0;
  padding: 0.5rem;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 5px;
}

.rank {
  font-weight: bold;
  color: #f1c40f; /* Or */
  min-width: 50px; /* Assure un bon alignement */
  text-align: center;
}

.player-name {
  flex-grow: 1;
  text-align: left;
  padding-left: 15px; /* Espace entre le rang et le nom */
}

.spacer {
  flex-grow: 1; /* Ajoute de l’espace entre le nom et le score */
}

.score {
  font-weight: bold;
  color: #ffffff;
  min-width: 80px; /* Fixe la largeur pour un meilleur alignement */
  text-align: right;
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
      <div v-else>
        <div v-for="(scoreEntry, index) in registeredScores" :key="index">
          <span class="rank">#{{ index + 1 }}</span> 
          {{ scoreEntry.playerName }} - <strong>{{ scoreEntry.score }}</strong>
        </div>
      </div>
    </div>

    <!-- Bouton démarrer le quiz -->
    <router-link to="/new-quiz" class="start-quiz">Démarrer le quiz !</router-link>
  </div>
</template>