<template>
    <div>
      <h1>API Endpoints</h1>
      <ul>
        <li v-for="endpoint in endpoints" :key="endpoint.endpoint">
          <h2>{{ endpoint.endpoint }}</h2>
          <p>Methods: {{ endpoint.methods }}</p>
          <p>Path: {{ endpoint.path }}</p>
          <p>Example:</p>
          <pre>{{ endpoint.example }}</pre>
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  /* eslint-disable */
  import axios from 'axios'; // Import Axios
  
  export default {
    data() {
      return {
        endpoints: [],
      };
    },
    created() {
      // Make an Axios GET request to your Flask app to fetch the list of endpoints and examples
      axios.get('http://127.0.0.1:5000').then(response => {
        this.endpoints = response.data.routes;
        console.log(response);
      }).catch(error => {
        console.error('Error fetching endpoints:', error);
      });
    },
  };
  </script>
  