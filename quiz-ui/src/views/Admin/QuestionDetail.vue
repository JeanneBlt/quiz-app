<template>
  <div class="question-details">
    <h1>Détails de la question</h1>
    <div>
      <h2>{{ question.title }}</h2> <!-- Affichage du titre -->
      <p><strong>Question :</strong> {{ question.text }}</p> <!-- Affichage du texte (ancien intitulé) -->
      <img v-if="question.image" :src="question.image" alt="Image de la question" class="question-image" />
      
      <div>
        <p><strong>Réponses possibles :</strong></p>
        <ul>
          <li v-for="(answer, index) in question.answers" :key="index">
            <p>{{ answer.text }} <span v-if="answer.isCorrect">(Bonne réponse)</span></p>
          </li>
        </ul>
      </div>

      <div>
        <button @click="editQuestion">Éditer</button>
        <button @click="deleteQuestion">Supprimer</button>
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
      QuizService.updateQuestion(position, null).then(() => {
        this.$router.push({ name: 'QuestionManager' }); // Retour à la liste des questions
      });
    }
  }
};
</script>

<style scoped>
.question-image {
  max-width: 100%;
  height: auto;
  margin-top: 20px;
}
</style>
