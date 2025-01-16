<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const password = ref('');
const loginError = ref(false);

const login = () => {
  if (password.value === 'adminpassword') {
    router.push('/admin/questions'); // Redirige vers la page admin si connexion réussie
  } else {
    loginError.value = true;
  }
};
</script>

<template>
  <div class="container">
    <!-- Titre principal -->
    <h1 class="title">Admin Login</h1>

    <!-- Formulaire de connexion -->
    <div class="login-form">
      <h2>Connectez-vous</h2>
      <form @submit.prevent="login">
        <div class="form-group">
          <label for="password">Mot de passe:</label>
          <input
            type="password"
            id="password"
            v-model="password"
            placeholder="Entrez votre mot de passe"
            required
          />
        </div>

        <!-- Erreur si mot de passe incorrect -->
        <div v-if="loginError" class="error-message">
          Mot de passe incorrect.
        </div>

        <button type="submit" class="login-button">Se connecter</button>
      </form>
    </div>
  </div>
</template>

<style scoped>
/* Styles généraux */
body {
  font-family: 'Arial', sans-serif;
  background-color: #1e1e1e; /* Fond sombre */
  color: #ffffff; /* Texte blanc */
  margin: 0;
  padding: 0;
}

/* Conteneur principal */
.container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh; /* Hauteur de la fenêtre */
  text-align: center;
}

/* Titre principal */
.title {
  font-size: 4rem;
  font-weight: bold;
  color: #43d17a; /* Couleur verte */
  margin-bottom: 2rem;
}

/* Formulaire de connexion */
.login-form {
  background-color: #2a2a2a; /* Fond sombre */
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
  width: 90%;
  max-width: 400px;
}

.login-form h2 {
  font-size: 2rem;
  margin-bottom: 1.5rem;
  color: #ffffff;
}

/* Champs du formulaire */
.form-group {
  margin-bottom: 1.5rem;
  text-align: left;
}

label {
  display: block;
  font-size: 1rem;
  margin-bottom: 0.5rem;
}

input {
  width: 100%;
  padding: 0.75rem;
  font-size: 1rem;
  border: 1px solid #555555;
  border-radius: 5px;
  background-color: #1e1e1e;
  color: #ffffff;
  outline: none;
  transition: border-color 0.3s;
}

input:focus {
  border-color: #43d17a;
}

/* Bouton de connexion */
.login-button {
  padding: 0.75rem 2rem;
  font-size: 1.25rem;
  font-weight: bold;
  background-color: #43d17a;
  color: #1e1e1e;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s ease-in-out;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
  width: 100%;
}

.login-button:hover {
  background-color: #1e1e1e;
  color: #43d17a;
  border: 2px solid #43d17a;
  transform: scale(1.05);
}

/* Message d'erreur */
.error-message {
  color: #ff4d4d;
  font-size: 0.9rem;
  margin-top: -1rem;
  margin-bottom: 1rem;
  text-align: left;
}
</style>
