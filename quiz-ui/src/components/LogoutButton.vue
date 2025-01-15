<template>
    <button @click="logout" class="logout-btn">Déconnexion</button>
  </template>
  
  <script>
  export default {
    methods: {
      logout() {
        // Ici, tu pourrais supprimer un token d'authentification, réinitialiser l'état, etc.
        this.$router.push({ name: 'Admin' }); // Redirige vers la page de login
      }
    }
  }
  </script>
  
  <style scoped>
  .logout-btn {
    padding: 10px 20px;
    background-color: #f44336;
    color: white;
    border: none;
    cursor: pointer;
    font-size: 16px;
  }
  
  .logout-btn:hover {
    background-color: #d32f2f;
  }
  </style>
  