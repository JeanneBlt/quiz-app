import axios from 'axios';

const instance = axios.create({
  baseURL: `${import.meta.env.VITE_API_URL}`,
  json: true,
});

export default {
  async call(method, resource, data = null, token = null) {
    var headers = {
      "Content-Type": "application/json",
    };

    if (!token) {
      token = localStorage.getItem('authToken');
    }

    if (token) {
      headers.Authorization = `Bearer ${token}`;
      console.log("Token envoyé :", headers.Authorization); // Ajout du log
    }

    return instance({
      method,
      headers: headers,
      url: resource,
      data,
    })
    .then((response) => {
      return { status: response.status, data: response.data };
    })
    .catch((error) => {
      console.error("Erreur API :", error.response?.status, error.response?.data);
      throw error; 
    });
  },
  
  getQuizInfo() {
    return this.call("get", "quiz-info");
  },

  getQuestion(position) {
    return this.call("get", `questions?position=${position}`);
  },

  addQuestion(question, token) {
    return this.call("post", "questions", question, token);
  },

  updateQuestion(id, question, token) {
    return this.call("put", `questions/${id}`, question, token);
  },

  deleteQuestion(id, token) {
    return this.call("delete", `questions/${id}`, null, token);
  },

  // Nouvelle méthode pour soumettre les données utilisateur
  async submitPlayerData(playerName, answers) {
    const data = {
      playerName,
      answers,
    };

    return this.call("post", "participations", data)
      .then((response) => {
        if (response.status === 200) {
          console.log("Player data successfully submitted:", response.data);
          return response.data;
        } else {
          console.error("Failed to submit player data:", response);
          throw new Error("Failed to submit player data");
        }
      });
  },
};

