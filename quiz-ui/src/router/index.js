import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import QuestionManager from '../views/QuestionManager.vue'
import QuizEnd from '../views/QuizEnd.vue'

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
      path: "/quiz-end",
      name: "QuizEnd",  // Page de fin du quiz
      component: QuizEnd,
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue'), // Si vous avez une page "about"
    },
  ],
})

export default router