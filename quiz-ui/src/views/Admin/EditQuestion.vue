<template>
  <div class="edit-question-container">
    <h1 class="title">{{ isEditing ? 'Éditer' : 'Créer' }} une question</h1>

    <form @submit.prevent="saveQuestion" class="form-container">
      <!-- Titre de la question -->
      <div class="input-group">
        <label for="questionTitle">Titre de la question :</label>
        <input 
          type="text" 
          id="questionTitle" 
          v-model="question.title" 
          placeholder="Titre de la question" 
          required 
        />
      </div>

      <!-- Texte de la question -->
      <div class="input-group">
        <label for="questionText">Texte de la question :</label>
        <input 
          type="text" 
          id="questionText" 
          v-model="question.text" 
          placeholder="Texte de la question" 
          required 
        />
      </div>

      <!-- Image -->
      <div class="input-group">
        <label for="image">Image :</label>
        <input type="file" id="image" @change="handleFileUpload" />
        <img v-if="imagePreview" :src="imagePreview" alt="Aperçu de l'image" class="image-preview" />
      </div>

      <!-- Réponses -->
      <div v-for="(answer, index) in question.answers" :key="index" class="answer-container">
        <div class="input-group">
          <label :for="'answer' + index">Réponse {{ index + 1 }} :</label>
          <input 
            type="text" 
            v-model="answer.text" 
            :id="'answer' + index" 
            placeholder="Texte de la réponse" 
            required
          />
        </div>
        <div class="checkbox-group">
          <input 
            type="checkbox" 
            v-model="answer.isCorrect" 
            :id="'correctAnswer' + index"
            @change="onAnswerCorrectChange(index)" 
          />
          <label :for="'correctAnswer' + index">Réponse correcte</label>
        </div>
      </div>

      <!-- Boutons de sauvegarde ou d'annulation -->
      <div class="button-group">
        <button type="submit" class="submit-button">Sauvegarder</button>
        <button type="button" @click="cancelEdit" class="cancel-button">Annuler</button>
      </div>
    </form>
  </div>
</template>

<script>
import QuizService from '../../services/QuizService';

export default {
  data() {
    return {
      question: {
        title: '',
        text: '',
        image: null,
        answers: [
          { text: '', isCorrect: false },
          { text: '', isCorrect: false },
          { text: '', isCorrect: false },
          { text: '', isCorrect: false },
        ],
      },
      imagePreview: null,
      isEditing: false,
    };
  },
  created() {
    const position = this.$route.params.position;

    if (position && !isNaN(position)) {
      this.isEditing = true;
      this.fetchQuestion(position);
    } else {
      this.initializeNewQuestion();
    }
  },
  methods: {
    async fetchQuestion(position) {
      try {
        const question = await QuizService.getQuestionByPosition(position);
        this.question = { ...question };
        this.imagePreview = question.image;
      } catch (error) {
        console.error('Erreur lors de la récupération de la question :', error);
        this.initializeNewQuestion();
      }
    },
    initializeNewQuestion() {
      this.question = {
        title: '',
        text: '',
        image: null,
        answers: [
          { text: '', isCorrect: false },
          { text: '', isCorrect: false },
          { text: '', isCorrect: false },
          { text: '', isCorrect: false },
        ],
      };
      this.imagePreview = null;
      this.isEditing = false;
    },
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = () => {
          this.imagePreview = reader.result;
          this.question.image = reader.result;
        };
        reader.readAsDataURL(file);
      }
    },
    onAnswerCorrectChange(index) {
      this.question.answers.forEach((answer, i) => {
        if (i !== index) {
          answer.isCorrect = false;
        }
      });
    },
    async saveQuestion() {
    try {
        const token = localStorage.getItem('authToken');
        if (!token) {
            alert("Authentification requise pour cette action !");
            return;
        }

        const position = parseInt(this.$route.params.position);
        console.log("Position récupérée :", position);

        if (this.isEditing) {
            console.log("Mise à jour de la question :", this.question);
            await QuizService.updateQuestion(position, this.question, token);
        } else {
            console.log("Création d'une nouvelle question :", this.question);
            await QuizService.addQuestion(this.question, token);
        }

        this.$router.push({ name: 'QuestionList' });
    } catch (error) {
        console.error('Erreur lors de la sauvegarde de la question :', error);
    }
}

  },
};
</script>

<style scoped>
/* Garde le style existant */
</style>


<style scoped>
/* Styles généraux */
.edit-question-container {
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

/* Formulaire */
.form-container {
  width: 100%;
  max-width: 600px;
  background-color: #2a2a2a;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
}

.input-group {
  margin-bottom: 1.5rem;
}

.input-group label {
  font-size: 1.2rem;
  color: #ffffff;
  margin-bottom: 0.5rem;
  display: block;
}

.input-group input {
  width: 100%;
  padding: 1rem;
  font-size: 1rem;
  border-radius: 5px;
  border: 1px solid #43d17a;
  background-color: #3b3b3b;
  color: #ffffff;
}

.input-group input:focus {
  outline: none;
  border-color: #1e1e1e;
}

/* Preview image */
.image-preview {
  max-width: 100px;
  max-height: 100px;
  margin-top: 1rem;
}

/* Réponses */
.answer-container {
  margin-bottom: 1.5rem;
}

.checkbox-group {
  display: flex;
  align-items: center;
  margin-top: 0.5rem;
}

.checkbox-group input {
  margin-right: 0.5rem;
}

.checkbox-group label {
  font-size: 1rem;
  color: #ffffff;
}

/* Boutons */
.button-group {
  display: flex;
  justify-content: space-between;
  margin-top: 1.5rem;
}

.submit-button,
.cancel-button {
  padding: 1rem 2rem;
  font-size: 1.2rem;
  font-weight: bold;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s ease-in-out;
}

.submit-button {
  background-color: #43d17a;
  border: none;
  color: #1e1e1e;
}

.submit-button:hover {
  background-color: #1e1e1e;
  color: #43d17a;
  border: 2px solid #43d17a;
}

.cancel-button {
  background-color: #ff5c5c;
  border: none;
  color: #ffffff;
}

.cancel-button:hover {
  background-color: #1e1e1e;
  color: #ff5c5c;
  border: 2px solid #ff5c5c;
}
</style>
