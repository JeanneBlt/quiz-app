<template>
  <div class="edit-question">
    <h1>{{ isEditing ? 'Éditer' : 'Créer' }} la question</h1>
    
    <form @submit.prevent="saveQuestion">
      <label for="questionTitle">Titre de la question:</label>
      <input 
        type="text" 
        id="questionTitle" 
        v-model="question.title" 
        placeholder="Titre de la question" 
        required 
      />
      
      <label for="questionText">Texte de la question:</label>
      <input 
        type="text" 
        id="questionText" 
        v-model="question.text" 
        placeholder="Texte de la question" 
        required 
      />
      
      <label for="image">Image:</label>
      <input type="file" id="image" @change="handleFileUpload" />
      <img v-if="imagePreview" :src="imagePreview" alt="Aperçu de l'image" class="image-preview" />
      
      <div v-for="(answer, index) in question.answers" :key="index" class="answer-container">
        <label :for="'answer' + index">Réponse {{ index + 1 }}:</label>
        <input 
          type="text" 
          v-model="answer.text" 
          :id="'answer' + index" 
          placeholder="Texte de la réponse" 
          required 
        />
        <input 
          type="checkbox" 
          v-model="answer.isCorrect" 
          :id="'correctAnswer' + index"
          @change="onAnswerCorrectChange(index)" 
        /> 
        <label for="'correctAnswer' + index">Réponse correcte</label>
      </div>
      
      <button type="submit">Sauvegarder</button>
      <button type="button" @click="cancelEdit">Annuler</button>
    </form>
  </div>
</template>

<script>
import QuizService from '../../services/QuizService';

export default {
  data() {
    return {
      question: {
        title: '', // Titre de la question
        text: '',  // Texte de la question (ancien "intitulé")
        image: null,
        answers: [
          { text: '', isCorrect: false },
          { text: '', isCorrect: false },
          { text: '', isCorrect: false },
          { text: '', isCorrect: false }
        ]
      },
      imagePreview: null,
      isEditing: false
    };
  },
  created() {
    const position = this.$route.params.position;
    if (position) {
      this.isEditing = true;
      this.fetchQuestion(position);
    }
  },
  methods: {
    fetchQuestion(position) {
      QuizService.getQuestionByPosition(position).then((question) => {
        this.question = { ...question };
        this.imagePreview = question.image;
      });
    },
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = () => {
          this.imagePreview = reader.result;
        };
        reader.readAsDataURL(file);
      }
    },
    onAnswerCorrectChange(index) {
      this.question.answers.forEach((answer, i) => {
        if (i !== index) {
          answer.isCorrect = false; // Désélectionner les autres réponses
        }
      });
    },
    saveQuestion() {
      const position = parseInt(this.$route.params.position);
      if (this.isEditing) {
        QuizService.updateQuestion(position, this.question).then(() => {
          this.$router.push({ name: 'QuestionManager' });
        });
      } else {
        QuizService.addQuestion(this.question).then(() => {
          this.$router.push({ name: 'QuestionManager' });
        });
      }
    },
    cancelEdit() {
      this.$router.push({ name: 'QuestionList' });
    }
  }
};
</script>

<style scoped>
.image-preview {
  max-width: 100px;
  max-height: 100px;
  margin-top: 10px;
}
.answer-container {
  margin-bottom: 10px;
}
</style>

  