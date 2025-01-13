<script setup>
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';
  import participationStorageService from "@/services/ParticipationStorageService";

  const username = ref('');
  const router = useRouter();

  function launchNewQuiz() {
    participationStorageService.savePlayerName(username.value);
    console.log("Launch new quiz with", username.value);
    router.push('/questions');
  }
</script>

<template>
  <div class="container">
    <p>Saisissez votre nom :</p>
    <input type="text" v-model="username" placeholder="Username"/>
    <div>
    <button @click="launchNewQuiz">GO!</button>
    </div>
  </div>
</template>