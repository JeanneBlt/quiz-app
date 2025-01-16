<template>
  <div class="question-list-container">
    <!-- Titre de la page -->
    <h1 class="title">Gestion des Questions</h1>

    <!-- Bouton de création de question -->
    <button class="create-button" @click="createQuestion">Créer une question</button>

    <!-- Liste des questions -->
    <ul class="question-list">
      <li v-for="(question, index) in questions" :key="index" class="question-item">
        <router-link :to="{ name: 'QuestionDetail', params: { position: index + 1 } }" class="question-link">
          <span class="question-index">Question {{ index + 1 }}:</span> {{ question.text }}
        </router-link>
      </li>
    </ul>
  </div>
</template>

<script>
import QuizService from '../../services/QuizService';

export default {
  data() {
    return {
      questions: [] 
    };
  },
  created() {
    this.fetchQuestions();
  },
  methods: {
    fetchQuestions() {
      const totalQuestions = 5;
      for (let i = 1; i <= totalQuestions; i++) {
        QuizService.getQuestionByPosition(i).then((question) => {
          this.questions.push(question);
        });
      }
    },
    createQuestion() {
      this.$router.push({ name: 'EditQuestion', params: { position: 0 } }); // Créer une nouvelle question
    }
  }
};
</script>

<style scoped>
/* Conteneur principal */
.question-list-container {
  font-family: 'Arial', sans-serif;
  background-color: #1e1e1e; /* Fond sombre */
  color: #ffffff; /* Texte blanc */
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
  box-sizing: border-box;
}

/* Titre principal */
.title {
  font-size: 3rem;
  font-weight: bold;
  color: #43d17a; /* Couleur verte */
  margin-bottom: 2rem;
}

/* Bouton créer une question */
.create-button {
  padding: 1rem 2rem;
  font-size: 1.25rem;
  font-weight: bold;
  background-color: #43d17a;
  color: #1e1e1e;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s ease-in-out;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
}

.create-button:hover {
  background-color: #1e1e1e;
  color: #43d17a;
  border: 2px solid #43d17a;
  transform: scale(1.05);
}

/* Liste des questions */
.question-list {
  width: 100%;
  max-width: 800px;
  list-style: none;
  margin: 2rem 0;
  padding: 0;
}

.question-item {
  background-color: #2a2a2a;
  padding: 1rem 1.5rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
  transition: transform 0.2s ease-in-out;
}

.question-item:hover {
  transform: scale(1.02);
}

/* Lien vers les détails de la question */
.question-link {
  text-decoration: none;
  color: #43d17a;
  font-size: 1.25rem;
  display: flex;
  align-items: center;
}

.question-link:hover {
  text-decoration: underline;
}

/* Index de la question */
.question-index {
  font-weight: bold;
  color: #ffffff;
  margin-right: 0.5rem;
}
</style>
