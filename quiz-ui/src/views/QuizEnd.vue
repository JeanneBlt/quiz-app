<template>
    <div class="quiz-end">
      <h1>Félicitations !</h1>
      <p>Vous avez terminé le quiz.</p>
      <p>Votre score est : {{ score }}</p>
      <button @click="restartQuiz">Recommencer le quiz</button>
    </div>
  </template>
  
  <script setup>
    import { ref } from 'vue';
    const score = ref(0); // Vous pouvez calculer le score dans votre gestionnaire de questions
  
    function restartQuiz() {
      // Revenir à la page d'accueil ou recharger le quiz
      window.location.href = '/';
    }
  </script>
  