import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../views/HomePage.vue';
import QuestionManager from '../views/QuestionManager.vue';
import Score from '../views/Score.vue';
import Admin from '../views/Admin.vue'

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
      component: () => import('../views/NewQuizPage.vue'), // Page d'accueil ou d'entrée du quiz
    },
    {
      path: "/questions",
      name: "QuestionManager",  // Gestion des questions du quiz
      component: QuestionManager,
    },
    {
      path: "/score",
      name: "Score",  // Gestion des questions du quiz
      component: Score,
    },
    {
      path: "/admin",
      name: "Admin",  // Gestion des questions du quiz
      component: Admin,
    },
  ],
})

export default router