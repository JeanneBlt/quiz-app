<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import participationStorageService from "@/services/ParticipationStorageService";

const username = ref('');
const router = useRouter();

function launchNewQuiz() {
  participationStorageService.clear();
  participationStorageService.savePlayerName(username.value);
  participationStorageService.saveParticipationScore(0);
  console.log("Launch new quiz with", username.value);
  router.push('/questions');
}
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
  height: 100vh;
  text-align: center;
}

/* Texte */
.container p {
  font-size: 1.8rem;
  color: #43d17a; /* Couleur verte */
  margin-bottom: 1rem;
}

/* Champ de saisie */
input[type="text"] {
  padding: 0.8rem;
  font-size: 1.2rem;
  width: 300px;
  border: 2px solid #43d17a;
  border-radius: 5px;
  background-color: #2a2a2a;
  color: #ffffff;
  margin-bottom: 1.5rem;
  outline: none;
  transition: all 0.3s ease-in-out;
}

input[type="text"]:focus {
  border-color: #ffffff;
  box-shadow: 0 0 10px #43d17a;
}

/* Bouton */
button {
  padding: 0.8rem 2rem;
  font-size: 1.5rem;
  font-weight: bold;
  color: #1e1e1e;
  background-color: #43d17a;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s ease-in-out;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
}

button:hover {
  background-color: #1e1e1e;
  color: #43d17a;
  border: 2px solid #43d17a;
  transform: scale(1.05);
}
</style>

<template>
  <div class="container">
    <p>Saisissez votre nom :</p>
    <input type="text" v-model="username" placeholder="Username" />
    <div>
      <button @click="launchNewQuiz">GO!</button>
    </div>
  </div>
</template>
