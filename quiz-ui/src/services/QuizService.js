import QuizApiService from "./QuizApiService";

export default {
  async getAllQuestions(){
    const response = await QuizApiService.getAllQuestions();
    console.log(response.data);
  },

  async getQuestionByPosition(position) {
    const response = await QuizApiService.getQuestion(position);
    if (response.status === 200) {
      return response.data;
    } else {
      throw new Error("Erreur lors de la récupération de la question.");
    }
  },

  async getTotalQuestions() {
    const response = await QuizApiService.getQuizInfo();
    if (response.status === 200) {
      return response.data.size;
    } else {
      throw new Error("Erreur lors de la récupération des informations du quiz.");
    }
  },

  async addQuestion(newQuestion, token) {
    const response = await QuizApiService.addQuestion(newQuestion, token);
    if (response.status === 201) {
      return response.data;
    } else {
      throw new Error("Erreur lors de l'ajout de la question.");
    }
  },

  async updateQuestion(id, updatedQuestion, token) {
    const response = await QuizApiService.updateQuestion(id, updatedQuestion, token);
    if (response.status === 200) {
      return response.data;
    } else {
      throw new Error("Erreur lors de la mise à jour de la question.");
    }
  },

  async deleteQuestion(id, token) {
    const response = await QuizApiService.deleteQuestion(id, token);
    if (response.status === 204) {
      return true;
    } else {
      throw new Error("Erreur lors de la suppression de la question.");
    }
  },
};
