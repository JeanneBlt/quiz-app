<template>
  <div class="question-manager">
    <h1>Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestions }}</h1>
    
    <!-- Vérifiez si currentQuestion est non nul avant de passer à QuestionDisplay -->
    <QuestionDisplay 
      v-if="currentQuestion" 
      :current-question="currentQuestion" 
      @click-on-answer="answerClickedHandler" />
  </div>
</template>

<script setup>
  import { ref, onMounted } from 'vue';
  import QuizService from '../services/QuizService.js'; // Assurez-vous que QuizService.js est bien importé
  import QuestionDisplay from '../components/QuestionDisplay.vue';

  // Références réactives pour la gestion de l'état
  const currentQuestionPosition = ref(1);  // Commencer avec la première question
  const totalNumberOfQuestions = ref(0);
  const currentQuestion = ref(null);

  // Fonction pour charger une question en fonction de sa position
  async function loadQuestionByPosition(position) {
    const question = await QuizService.getQuestionByPosition(position);
    currentQuestion.value = question;
  }

  // Fonction de gestion de la réponse lorsque l'utilisateur clique sur une réponse
  function answerClickedHandler(selectedAnswerIndex) {
    console.log("Réponse sélectionnée : " + selectedAnswerIndex);

    // Passer à la question suivante
    if (currentQuestionPosition.value < totalNumberOfQuestions.value) {
      currentQuestionPosition.value++;
      loadQuestionByPosition(currentQuestionPosition.value);
    } else {
      endQuiz(); // Si c'est la dernière question, on termine le quiz
    }
  }

  // Fonction pour gérer la fin du quiz
  function endQuiz() {
    console.log("Quiz terminé !");
    // Ici vous pouvez rediriger l'utilisateur vers une page de résultats, ou afficher une notification de fin
  }

  // Initialisation au montage du composant
  onMounted(async () => {
    // Récupérer le nombre total de questions
    totalNumberOfQuestions.value = await QuizService.getTotalQuestions();
    
    // Charger la première question
    await loadQuestionByPosition(currentQuestionPosition.value);
  });
</script>

<style>
  /* Vous pouvez ajouter vos styles ici */
</style>
