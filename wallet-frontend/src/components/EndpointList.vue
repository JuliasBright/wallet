<template>
  <div>
    <h1>API Endpoints</h1>
    <ul>
      <li v-for="endpoint in endpoints" :key="endpoint.endpoint">
        <div class="endpoint-block">
          <h2>{{ endpoint.endpoint }}</h2>
          <p>Methods: {{ endpoint.methods }}</p>
          <p>Path: {{ endpoint.path }}</p>
          <button class="try-it-button">Try it out on Postman</button>
        </div>
      </li>
    </ul>
  </div>
</template>

<style>
ul {
  list-style: none;
}

.endpoint-block {
  border: 1px solid #ddd;
  padding: 16px;
  margin: 16px 0;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
}

.endpoint-block h2 {
  font-size: 24px;
  margin-bottom: 8px;
}

.endpoint-block p {
  font-size: 16px;
  margin: 4px 0;
}

.try-it-button {
  background-color: #007bff;
  color: #fff;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.try-it-button:hover {
  background-color: #0056b3;
}
</style>


<script>
import axios from 'axios';

export default {
  data() {
    return {
      endpoints: [],
    };
  },
  methods: {
    fetchEndpoints() {
      axios
        .get('http://127.0.0.1:5000/')
        .then((response) => {
          console.log(response);
          this.endpoints = response.data.routes;
        })
        .catch((error) => {
          console.error('Error fetching endpoints:', error);
        });
    },
  },
  created() {
    this.fetchEndpoints();
  },
};
</script>
