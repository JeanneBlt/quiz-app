import QuizApiService from "./QuizApiService";
import axios from 'axios';
const API_BASE_URL = 'http://localhost:5000';

export default {
  async getAllQuestions(){
    const response = await QuizApiService.getAllQuestions();
    console.log(response.data);
  },

  async getTotalQuestions() {
    const response = await QuizApiService.getQuizInfo();
    if (response.status === 200) {
      return response.data.size;
    } else {
      throw new Error("Erreur lors de la récupération des informations du quiz.");
    }
  },

  async getQuestionByPosition(position) {
    const response = await axios.get(`${API_BASE_URL}/questions?position=${position}`);
    return response.data;
  },

  async addQuestion(newQuestion, token) {
    return await axios.post(
      `${API_BASE_URL}/questions`,
      {
        title: newQuestion.title,
        text: newQuestion.text,
        image: newQuestion.image,
        position: newQuestion.position || 1, // Default position if not provided
        possibleAnswers: newQuestion.answers,
      },
      {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      }
    );
  },

  async updateQuestion(id, updatedQuestion, token) {
    try {
        const response = await axios.put(
            `http://localhost:5000/questions/${id}`,
            {
                title: updatedQuestion.title,
                text: updatedQuestion.text,
                image: updatedQuestion.image || "",
                position: updatedQuestion.position || 1,
                possibleAnswers: updatedQuestion.answers,
            },
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                    "Content-Type": "application/json",
                },
            }
        );
        return response.data;
    } catch (error) {
        console.error("Erreur lors de la mise à jour de la question :", error.response?.data || error.message);
        throw error;
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
