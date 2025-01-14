const questions = [
  {
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
        resolve(questions[position - 1]); // Position commence à 1, donc on accède à l'index - 1
      }, 0);
    });
  },
  
  
  getTotalQuestions() {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve(questions.length);
      }, 0);
    });
  }
};
