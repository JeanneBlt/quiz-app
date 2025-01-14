export default {
      clear() {
        // Supprime toutes les données stockées dans localStorage
        window.localStorage.removeItem("playerName");
        window.localStorage.removeItem("participationScore");
      },
    
      savePlayerName(playerName) {
        // Sauvegarde le nom du joueur dans localStorage
        window.localStorage.setItem("playerName", playerName);
      },
    
      getPlayerName() {
        // Récupère le nom du joueur depuis localStorage
        return window.localStorage.getItem("playerName");
      },
    
      saveParticipationScore(participationScore) {
        // Sauvegarde le score de participation dans localStorage
        window.localStorage.setItem("participationScore", participationScore);
      },
    
      getParticipationScore() {
        // Récupère le score de participation depuis localStorage
        return window.localStorage.getItem("participationScore");
      }
    };