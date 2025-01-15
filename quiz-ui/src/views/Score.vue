<script setup>
import { ref, onMounted } from 'vue';
import { RouterLink, RouterView } from 'vue-router'
import participationStorageService from "@/services/ParticipationStorageService";
import scoreStorageService from '@/services/ScoreStorageService';

// Récupération des données du joueur et de son score
const player = participationStorageService.getPlayerName();
const score = participationStorageService.getParticipationScore();
const registeredScores = ref([]);
const classement = ref('');

// Effectuer l'enregistrement et la récupération des scores lors du montage du composant
onMounted(async () => {
    // Sauvegarde du score du joueur
    await scoreStorageService.saveScore(player, score);
    console.log("score rentré : " + score);

    // Récupération des meilleurs scores (top 5)
    registeredScores.value = scoreStorageService.getTopScores(5);

    // Récupération du classement du joueur
    classement.value = scoreStorageService.getPlayerRank(player);
});
</script>

<template>
    <h1>
        {{ player }}
    </h1>
    <div>
        Ton score : {{ score }}
    </div>
    <div>
        Meilleurs scores: 
        <div v-for="scoreEntry in registeredScores" v-bind:key="scoreEntry.date">
            {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
        </div>
    </div>
    <div>
        Ton classement : {{ classement }}
    </div>
    <nav>
        <RouterLink to="/">Recommencer</RouterLink>
    </nav>
</template>

<style scoped>
</style>
