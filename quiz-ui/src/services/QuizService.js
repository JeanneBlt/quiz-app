const questions = [
  {
    title: 'Géographie',
    text: 'Quelle est la capitale de la France ?',
    image: "question_images/question1.jpg",
    answers: [
      { text: 'Paris' },
      { text: 'Londres' },
      { text: 'Berlin' },
      { text: 'Madrid' }
    ],
    answerIndex: 0
  },
  {
    title: 'Océans',
    text: 'Quel est le plus grand océan du monde ?',
    image: "question_images/question2.jpg",
    answers: [
      { text: 'Océan Atlantique' },
      { text: 'Océan Pacifique' },
      { text: 'Océan Indien' },
      { text: 'Océan Arctique' }
    ],
    answerIndex: 1
  },
  {
    title: 'Déserts',
    text: 'Quel est le plus grand désert du monde ?',
    image: "question_images/question3.jpg",
    answers: [
      { text: 'Sahara' },
      { text: 'Désert de Gobi' },
      { text: 'Désert de Kalahari' },
      { text: 'Désert d’Atacama' }
    ],
    answerIndex: 0
  },
  {
    title: 'Littérature',
    text: 'Qui a écrit "Les Misérables" ?',
    image: "question_images/question4.jpg",
    answers: [
      { text: 'Émile Zola' },
      { text: 'Albert Camus' },
      { text: 'Marcel Proust' },
      { text: 'Victor Hugo' }
    ],
    answerIndex: 3
  },
  {
    title: 'Chimie',
    text: 'Quel est le symbole chimique de l\'or ?',
    image: "question_images/question5.jpg",
    answers: [
      { text: 'Au' },
      { text: 'Ag' },
      { text: 'O' },
      { text: 'Hg' }
    ],
    answerIndex: 0
  }
];

export default {
  getQuestionByPosition(position) {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve(questions[position - 1]);
      }, 0);
    });
  },

  getTotalQuestions() {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve(questions.length);
      }, 0);
    });
  },

  updateQuestion(position, updatedQuestion) {
    return new Promise((resolve, reject) => {
      if (position > 0 && position <= questions.length) {
        questions[position - 1] = updatedQuestion; 
        resolve();
      } else {
        reject("Question non trouvée");
      }
    });
  },

  addQuestion(newQuestion) {
    return new Promise((resolve) => {
      questions.push(newQuestion);
      resolve();
    });
  }
};
