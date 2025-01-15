<script setup>
  import { ref, onMounted } from 'vue';
  import { useRouter } from 'vue-router';
  import participationStorageService from "@/services/ParticipationStorageService";
  import QuizService from '../services/QuizService.js'; // Assurez-vous que QuizService.js est bien importé
  import QuestionDisplay from '../components/QuestionDisplay.vue';

  // Références réactives pour la gestion de l'état
  const currentQuestionPosition = ref(1);  // Commencer avec la première question
  const totalNumberOfQuestions = ref(0);
  const currentQuestion = ref(null);
  const router = useRouter();
  const score = ref(0);

  // Fonction pour charger une question en fonction de sa position
  async function loadQuestionByPosition(position) {
    const question = await QuizService.getQuestionByPosition(position);
    currentQuestion.value = question;
  }

  // Fonction de gestion de la réponse lorsque l'utilisateur clique sur une réponse
  function answerClickedHandler(selectedAnswerIndex) {
    console.log("Réponse sélectionnée : " + selectedAnswerIndex);

    // Comparer directement currentQuestion.value.answerIndex avec selectedAnswerIndex
    if(currentQuestion.value.answerIndex === selectedAnswerIndex){
      score.value++;  // Utilisez .value pour accéder et modifier le score
      console.log("Score actuel : " + score.value);
    }

    // Passer à la question suivante
    if (currentQuestionPosition.value < totalNumberOfQuestions.value) {
      currentQuestionPosition.value++;
      loadQuestionByPosition(currentQuestionPosition.value);
    } else {
      participationStorageService.saveParticipationScore(score.value);
      endQuiz(); // Si c'est la dernière question, on termine le quiz
    }
}


  // Fonction pour gérer la fin du quiz
  function endQuiz() {
    console.log("Quiz terminé !");
    router.push('/score');
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

<style scoped>
  /* Vous pouvez ajouter vos styles ici */
</style>
