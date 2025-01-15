<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import participationStorageService from "@/services/ParticipationStorageService";
import QuizService from '../services/QuizService.js';
import QuestionDisplay from '../components/QuestionDisplay.vue';

// Références réactives pour la gestion de l'état
const currentQuestionPosition = ref(1); // Commencer avec la première question
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
  if (currentQuestion.value.answerIndex === selectedAnswerIndex) {
    score.value++;
  }

  if (currentQuestionPosition.value < totalNumberOfQuestions.value) {
    currentQuestionPosition.value++;
    loadQuestionByPosition(currentQuestionPosition.value);
  } else {
    participationStorageService.saveParticipationScore(score.value);
    endQuiz();
  }
}

// Fonction pour gérer la fin du quiz
function endQuiz() {
  router.push('/score');
}

// Initialisation au montage du composant
onMounted(async () => {
  totalNumberOfQuestions.value = await QuizService.getTotalQuestions();
  await loadQuestionByPosition(currentQuestionPosition.value);
});
</script>

<template>
  <div class="question-manager">
    <main class="main-content">
      <div class="question-container">
        <h2>Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestions }}</h2>
        <QuestionDisplay 
          v-if="currentQuestion" 
          :current-question="currentQuestion" 
          @click-on-answer="answerClickedHandler" />
      </div>
    </main>
    <footer class="footer">
      &copy; 2025 - Quiz Application
    </footer>
  </div>
</template>





<style scoped>
/* Respect du style sombre avec le vert précédent */
:root {
  --color-background: #181818;
  --color-card: #282828;
  --color-text: #f8f8f8;
  --color-accent: #32cd32; /* Vert lime utilisé précédemment */
  --color-muted: #888888;
}

/* Structure générale */
.question-manager {
  font-family: 'Inter', sans-serif;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: var(--color-background);
  color: var(--color-text);
}

/* Header */
.header {
  text-align: center;
  padding: 20px;
  background-color: var(--color-card);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
}

.header h1 {
  margin: 0;
  font-size: 2rem;
  color: var(--color-accent);
}

/* Contenu principal */
.main-content {
  flex-grow: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

/* Conteneur de la question */
.question-container {
  background-color: var(--color-card);
  border-radius: 10px;
  padding: 20px;
  width: 100%;
  max-width: 600px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  text-align: center;
}

.question-container h2 {
  font-size: 1.5rem;
  margin-bottom: 20px;
  color: var(--color-accent);
}

/* Footer */
.footer {
  text-align: center;
  padding: 10px;
  font-size: 0.9rem;
  color: var(--color-muted);
  background-color: var(--color-card);
}

/* Transitions */
.question-container,
.header {
  transition: background-color 0.3s, color 0.3s;
}
</style>
