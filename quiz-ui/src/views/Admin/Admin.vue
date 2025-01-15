<template>
  <div class="admin">
    <h1>Connexion Administrateur</h1>
    <input type="password" v-model="password" placeholder="Mot de passe" />
    <button @click="login">Connexion</button>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </div>
</template>

<script>
import { useRouter } from 'vue-router';

export default {
  data() {
    return {
      password: '',
      errorMessage: ''
    };
  },
  methods: {
    login() {
      const correctPassword = 'adminPassword'; // Remplacer par un mécanisme d'authentification réel
      if (this.password === correctPassword) {
        this.$router.push({ name: 'QuestionList' }); // Rediriger vers la liste des questions
      } else {
        this.errorMessage = 'Mauvais mot de passe';
      }
    }
  }
};
</script>
