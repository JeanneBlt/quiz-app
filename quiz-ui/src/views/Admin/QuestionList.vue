<template>
    <div class="question-list">
      <button @click="createQuestion">Créer une question</button>
      <ul>
        <li v-for="(question, index) in questions" :key="index">
          <router-link :to="{ name: 'QuestionDetail', params: { position: index + 1 } }">{{ question.text }}</router-link>
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
  