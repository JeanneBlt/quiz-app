export default {
    saveScore(playerName, score) {
      const scores = this.getScores(); // Récupère les scores existants.
      
      // Vérifie si un score existe déjà pour ce joueur
      const existingScoreIndex = scores.findIndex(score => score.playerName === playerName);
      
      if (existingScoreIndex !== -1) {
        // Si le joueur existe, on remplace le score seulement si le nouveau score est supérieur
        if (scores[existingScoreIndex].score < score) {
          scores[existingScoreIndex].score = score; // Remplace le score
        }
      } else {
        // Si le joueur n'existe pas, on ajoute le nouveau score
        const newScore = { playerName, score };
        scores.push(newScore);
      }
  
      // Trie les scores par ordre décroissant (meilleur score en premier)
      scores.sort((a, b) => b.score - a.score);
  
      // Sauvegarde la liste mise à jour dans localStorage
      window.localStorage.setItem('scores', JSON.stringify(scores));
    },
  
    /**
     * Récupère la liste des scores stockés dans localStorage.
     * @returns {Array} Liste des scores.
     */
    getScores() {
      const scores = window.localStorage.getItem('scores');
      return scores ? JSON.parse(scores) : []; // Si aucun score n'est trouvé, retourne un tableau vide.
    },
  
    /**
     * Supprime tous les scores stockés dans localStorage.
     */
    clearScores() {
      window.localStorage.removeItem('scores');
    },
  
    /**
     * Récupère un score spécifique pour un joueur depuis localStorage.
     * @param {string} playerName - Le nom du joueur dont le score est recherché.
     * @returns {number|null} Le score du joueur ou null s'il n'est pas trouvé.
     */
    getScoreForPlayer(playerName) {
      const scores = this.getScores();
      const playerScore = scores.find(score => score.playerName === playerName);
      return playerScore ? playerScore.score : null; // Retourne null si le joueur n'est pas trouvé.
    },
  
    /**
     * Récupère les meilleurs scores stockés dans localStorage (top N scores).
     * @param {number} n - Le nombre de meilleurs scores à récupérer.
     * @returns {Array} Liste des meilleurs scores (maximum de N scores).
     */
    getTopScores(n) {
      const scores = this.getScores();
      return scores.slice(0, n); // Retourne les N premiers scores (meilleurs).
    },
  
    /**
     * Récupère la position d'un joueur dans le classement (ex: 2/10) avec gestion des égalités.
     * @param {string} playerName - Le nom du joueur dont la position est recherchée.
     * @returns {string|null} La position du joueur dans le classement (ex: "2/10") ou null s'il n'est pas trouvé.
     */
    getPlayerRank(playerName) {
        const scores = this.getScores(); // Récupère les scores triés par score décroissant
    
        if (scores.length === 0) return null;
    
        let rank = 1;  // Rang initial, tous les joueurs commencent au rang 1
        let previousScore = null;
        let positionCount = 0;  // Compteur pour les joueurs ayant le même score
    
        // On parcourt la liste triée des scores
        for (let i = 0; i < scores.length; i++) {
            const scoreEntry = scores[i];
    
            // Si le score actuel est égal au précédent, on ne change pas le rang
            if (scoreEntry.score === previousScore) {
                positionCount++;  // On incrémente le compteur de joueurs avec le même score
            } else {
                // Si le score change, on met à jour le rang en fonction du nombre de joueurs précédents
                rank += positionCount;
                positionCount = 1;  // Réinitialisation du compteur de joueurs pour le nouveau score
            }
    
            // Mémorisation du score actuel
            previousScore = scoreEntry.score;
    
            // Si c'est le joueur que nous recherchons, on retourne son rang
            if (scoreEntry.playerName === playerName) {
                const totalPlayers = scores.length;  // Nombre total de joueurs
                return `${rank}/${totalPlayers}`;    // Format du classement : "1/5", "2/5", etc.
            }
        }
    
        return null;  // Si le joueur n'est pas trouvé, retourner null
    }
    
};