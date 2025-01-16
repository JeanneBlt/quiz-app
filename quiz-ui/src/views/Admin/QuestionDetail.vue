<template>
  <div class="question-details-container">
    <h1 class="title">Détails de la question</h1>
    <div class="question-details-content">
      <!-- Titre de la question -->
      <h2 class="question-title">{{ question.title }}</h2>

      <!-- Texte de la question -->
      <p class="question-text"><strong>Question :</strong> {{ question.text }}</p>

      <!-- Image de la question -->
      <div v-if="question.image" class="image-container">
        <img :src="question.image" alt="Image de la question" class="question-image" />
      </div>

      <!-- Réponses possibles -->
      <div class="answers-container">
        <p><strong>Réponses possibles :</strong></p>
        <ul class="answers-list">
          <li v-for="(answer, index) in question.answers" :key="index" class="answer-item">
            <p>{{ answer.text }} <span v-if="index === question.answerIndex" class="correct-answer-tag">(Bonne réponse)</span></p>
          </li>
        </ul>
      </div>

      <!-- Boutons pour éditer ou supprimer -->
      <div class="button-group">
        <button @click="editQuestion" class="edit-button">Éditer</button>
        <button @click="deleteQuestion" class="delete-button">Supprimer</button>
      </div>
    </div>
  </div>
</template>

<script>
import QuizService from '../../services/QuizService';

export default {
  data() {
    return {
      question: {}
    };
  },
  created() {
    this.fetchQuestion();
  },
  methods: {
    fetchQuestion() {
      const position = this.$route.params.position;
      if (position) {
        QuizService.getQuestionByPosition(position).then((question) => {
          this.question = { ...question };
        });
      }
    },
    editQuestion() {
      this.$router.push({ name: 'EditQuestion', params: { position: this.$route.params.position } });
    },
    deleteQuestion() {
      const position = this.$route.params.position;
      QuizService.deleteQuestion(position).then(() => {
        this.$router.push({ name: 'QuestionList' }); // Retour à la liste des questions
      }).catch((error) => {
        alert(error); // Affichage d'un message d'erreur si la suppression échoue
      });
    }
  }
};
</script>

<style scoped>
/* Conteneur principal */
.question-details-container {
  font-family: 'Arial', sans-serif;
  background-color: #1e1e1e; /* Fond sombre */
  color: #ffffff;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100vh;
  box-sizing: border-box;
}

.title {
  font-size: 3rem;
  font-weight: bold;
  color: #43d17a; /* Couleur verte */
  margin-bottom: 2rem;
}

/* Contenu des détails de la question */
.question-details-content {
  width: 100%;
  max-width: 600px;
  background-color: #2a2a2a;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
}

/* Titre de la question */
.question-title {
  font-size: 2rem;
  margin-bottom: 1.5rem;
  color: #ffffff;
}

/* Texte de la question */
.question-text {
  font-size: 1.2rem;
  color: #cccccc;
  margin-bottom: 1rem;
}

/* Image de la question */
.image-container {
  margin-top: 1.5rem;
}

.question-image {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

/* Réponses possibles */
.answers-container {
  margin-top: 2rem;
}

.answers-list {
  list-style-type: none;
  padding: 0;
}

.answer-item {
  margin-bottom: 1rem;
  font-size: 1.2rem;
  color: #ffffff;
}

.correct-answer-tag {
  font-weight: bold;
  color: #43d17a; /* Couleur verte pour la bonne réponse */
}

/* Boutons */
.button-group {
  display: flex;
  justify-content: space-between;
  margin-top: 2rem;
}

.edit-button,
.delete-button {
  padding: 1rem 2rem;
  font-size: 1.2rem;
  font-weight: bold;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s ease-in-out;
}

.edit-button {
  background-color: #43d17a;
  border: none;
  color: #1e1e1e;
}

.edit-button:hover {
  background-color: #1e1e1e;
  color: #43d17a;
  border: 2px solid #43d17a;
}

.delete-button {
  background-color: #ff5c5c;
  border: none;
  color: #ffffff;
}

.delete-button:hover {
  background-color: #1e1e1e;
  color: #ff5c5c;
  border: 2px solid #ff5c5c;
}
</style>
