import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../views/HomePage.vue';
import NewQuizPage from '../views/NewQuizPage.vue';
import QuestionManager from '../views/QuestionManager.vue';
import Score from '../views/Score.vue';

// Admin views
import Admin from '../views/Admin/Admin.vue'; // Page d'accueil admin (connexion)
import QuestionList from '../views/Admin/QuestionList.vue'; // Liste des questions
import QuestionDetail from '../views/Admin/QuestionDetail.vue'; // Détail d'une question
import EditQuestion from '../views/Admin/EditQuestion.vue'; // Édition d'une question

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "HomePage",
      component: HomePage,
    },
    {
      path: "/new-quiz",
      name: "NewQuiz",
      component: NewQuizPage, // Page d'accueil ou d'entrée du quiz
    },
    {
      path: "/questions",
      name: "QuestionManager",  // Gestion des questions du quiz
      component: QuestionManager,
    },
    {
      path: "/score",
      name: "Score",
      component: Score,
    },
    {
      path: "/admin",
      name: "Admin",
      component: Admin,  // Page de login admin
    },
    {
      path: "/admin/questions",
      name: "QuestionList",
      component: QuestionList, // Liste des questions
    },
    {
      path: "/admin/question/:position",
      name: "QuestionDetail",
      component: QuestionDetail, // Détail d'une question
      props: true, // Passer la position comme paramètre
    },
    {
      path: "/admin/edit-question/:position",
      name: "EditQuestion",
      component: EditQuestion, // Page d'édition d'une question
      props: true, // Passer la position comme paramètre
    }
  ],
});

export default router;
