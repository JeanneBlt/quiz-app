import QuizApiService from "./QuizApiService";

export default {
  clear() {
    // Supprime toutes les données stockées dans localStorage
    window.localStorage.removeItem("playerName");
    window.localStorage.removeItem("participationScore");
    window.localStorage.removeItem("userAnswers");
  },

  savePlayerName(playerName) {
    window.localStorage.setItem("playerName", playerName);
  },

  getPlayerName() {
    return window.localStorage.getItem("playerName");
  },

  saveParticipationScore(participationScore) {
    window.localStorage.setItem("participationScore", participationScore);
  },

  getParticipationScore() {
    const score = window.localStorage.getItem("participationScore");
    return score ? Number(score) : 0;
  },

  saveUserAnswers(userAnswers) {
    window.localStorage.setItem("userAnswers", JSON.stringify(userAnswers));
  },

  getUserAnswers() {
    const answers = window.localStorage.getItem("userAnswers");
    return answers ? JSON.parse(answers) : [];
  },

  addUserAnswer(answerIndex) {
    const currentAnswers = this.getUserAnswers();
    currentAnswers.push(answerIndex+1);
    this.saveUserAnswers(currentAnswers);
  },

  async sendPlayerData() {
    const playerName = this.getPlayerName();
    const userAnswers = this.getUserAnswers();
  
    console.log("Player name:", playerName);
    console.log("User answers:", userAnswers);
  
    if (!playerName || userAnswers.length === 0) {
      throw new Error("Player name or answers are missing!");
    }
  
    try {
      const response = await QuizApiService.submitPlayerData(playerName, userAnswers);
      console.log("Player data successfully sent:", response);
    } catch (error) {
      console.error("Error sending player data:", error);
    }
  }
  
};
